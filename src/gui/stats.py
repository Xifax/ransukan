# -*- coding=utf-8 -*-
"""
Kanji selection statistics UI dialog.
"""

# external #
from PyQt4.QtCore import Qt, QThread, pyqtSignal
from PyQt4.QtGui import QWidget, QGridLayout, QPushButton, \
                        QLabel, QProgressBar, QSpinBox
#import numpy as np

# own #
from graphWidget import MplWidget
from db.kanji import Kanji
from gui.params import PLOT_WIDTH

class StatsUI(QWidget):
    def __init__(self, al, parent=None):
        super(StatsUI, self).__init__(parent)

        self.create_ui_components()
        self.compose_ui()
        self.init_composition()
        self.init_components()
        self.init_actions()

        self.al = al

    def create_ui_components(self):
        self.layout = QGridLayout()

        self.statPlot = MplWidget()
        (self.refreshPlot, self.runTest, self.clearStats,
        self.switchFreqDom, self.statInfo, self.testNumber,
        self.targetMaxPicked, self.beginTest, self.testProgress) = \
        (QPushButton('&Refresh'), QPushButton('&Test'), QPushButton('&Clear'),
        QPushButton('&Switch'), QLabel(''), QSpinBox(), QSpinBox(), QPushButton('Go!'),
        QProgressBar())

    def compose_ui(self):
        self.layout.addWidget(self.statPlot, 0, 0, 1, 4)
        self.layout.addWidget(self.refreshPlot, 1, 0)
        self.layout.addWidget(self.runTest, 1, 1)
        self.layout.addWidget(self.clearStats, 1, 2)
        self.layout.addWidget(self.switchFreqDom, 1, 3)
        self.layout.addWidget(self.statInfo, 2, 0, 1, 4)
        self.layout.addWidget(self.testNumber, 3, 0)
        self.layout.addWidget(self.targetMaxPicked, 3, 1)
        self.layout.addWidget(self.beginTest, 3, 2, 1, 2)
        self.layout.addWidget(self.testProgress, 4, 0, 1, 4)

        self.setLayout(self.layout)

    def init_composition(self):
        self.setWindowTitle('Stats')
        self.setWindowFlags(Qt.Tool)

    def init_components(self):
        self.refreshPlot.setToolTip('Update plot based on db stats')
        self.runTest.setToolTip('Run automated selection/distribution batch-tests')
        self.clearStats.setToolTip('Reset currently accumulated distribution stats')
        self.switchFreqDom.setToolTip('Switch plot between displaying \
n_picked(frequency) or n_picked(dominance)')

        self.statPlot.setMinimumWidth(PLOT_WIDTH)

        self.testNumber.hide()
        self.targetMaxPicked.hide()
        self.beginTest.hide()
        self.testProgress.hide()

        self.testNumber.setRange(10, 100000)
        self.testNumber.setToolTip('Number of tests to perform')
        self.targetMaxPicked.setRange(1, 1000)
        self.targetMaxPicked.setToolTip('Target average times picked: if > 1, \
will prefer this param over total number of tests')

    def init_actions(self):
        self.refreshPlot.clicked.connect(self.refresh_plot)
        self.clearStats.clicked.connect(self.reset_stats)
        self.runTest.clicked.connect(self.batch_test)
        self.switchFreqDom.clicked.connect(self.switch_freq_dom)

        self.beginTest.clicked.connect(self.begin_test)

    ##### actions #####

    def refresh_plot(self):
        #todo: how about 2d/3d contour, eh?
        self.statPlot.kanjiStats(Kanji.freq_stats())
        self.update_stat_info()

    def batch_test(self):
        if self.beginTest.isVisible():
            self.testNumber.hide()
            self.targetMaxPicked.hide()
            self.beginTest.hide()
            if self.testProgress.value() == 0:
                self.testProgress.hide()
        else:
            self.testNumber.show()
            self.targetMaxPicked.show()
            self.beginTest.show()
            if self.testProgress.value() != 0:
                self.testProgress.show()

    def reset_stats(self):
        Kanji.reset_stats()
        self.refresh_plot()

    def switch_freq_dom(self):
        pass

    def showEvent(self, event):
        self.refresh_plot()
        self.show()

    def update_stat_info(self):
        try:
            count, (picked, freqs), picked_count = \
                Kanji.query.count(), Kanji.freq_stats(), Kanji.picked_count()
            self.statInfo.setText("Kanji in DB: <b>%d</b> | Max picked: <b>%d</b> | \
Max frequency: <b>%d</b> | Picked at least once: <b>%d</b>" %
                    (count, max(picked), max(freqs), picked_count))
            self.update()
        except ValueError:
            set.statInfo.setText("No data available yet!")

    def begin_test(self):
        self.test_thread = BatchTestTask(self.al, self.testNumber.value(),
                                         self.targetMaxPicked.value())
        self.test_thread.over.connect(self.end_test)
        self.test_thread.partDone.connect(self.progress_test)
        self.testProgress.setValue(0)
        self.testProgress.show()
        self.test_thread.start()
        self.beginTest.setEnabled(False)
        #self.show_progress('Authorizing on RNG services...')

    def end_test(self, over):
        if over:
            self.testProgress.hide()
            self.update_stat_info()
            self.refresh_plot()
            self.beginTest.setEnabled(True)
            self.testProgress.setValue(0)

            print self.al.ex_stats()

    def progress_test(self, partDone):
        self.testProgress.setValue(partDone)
        #self.update_stat_info()

class BatchTestTask(QThread):
    """
    Perform series of kanji selection tests.
    """
    over = pyqtSignal(bool)
    partDone = pyqtSignal(int)

    def __init__(self, al, limit, rank, parent=None):
        super(BatchTestTask, self).__init__(parent)
        self.al = al
        self.limit = limit
        self.rank = rank

    def run(self):
        try:
            for test in range(1, self.limit):
                kanji_set = []
                while len(kanji_set) != 4:
                    kanji = Kanji.get_random(self.al.random_int())
                    if kanji is not None:
                        if kanji not in kanji_set:
                            kanji_set.append(kanji)
                self.partDone.emit(float(test)/self.limit * 100)
        except Exception as e:
            print e.message

        self.over.emit(True)
