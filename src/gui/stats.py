# -*- coding=utf-8 -*-
"""
Kanji selection statistics UI dialog.
"""

# external #
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QWidget, QGridLayout, QPushButton, \
                        QLabel, QProgressBar, QSpinBox
#import numpy as np

# own #
from graphWidget import MplWidget
from db.kanji import Kanji
from gui.params import PLOT_WIDTH

class StatsUI(QWidget):
    def __init__(self, parent=None):
        super(StatsUI, self).__init__(parent)

        self.create_ui_components()
        self.compose_ui()
        self.init_composition()
        self.init_components()
        self.init_actions()

    def create_ui_components(self):
        self.layout = QGridLayout()

        self.statPlot = MplWidget()
        (self.refreshPlot, self.runTest, self.clearStats,
        self.switchFreqDom, self.statInfo, self.testNumber,
        self.targetMaxPicked, self.beginTest, self.testProgress) = \
        (QPushButton('&Refresh'), QPushButton('&Test'), QPushButton('&Clear'),
        QPushButton('&Switch'), QLabel(''), QSpinBox(), QSpinBox(), QPushButton('&Go!'),
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

    def init_actions(self):
        self.refreshPlot.clicked.connect(self.refresh_plot)
        self.clearStats.clicked.connect(self.reset_stats)
        self.runTest.clicked.connect(self.batch_test)
        self.switchFreqDom.clicked.connect(self.switch_freq_dom)

    ##### actions #####

    def refresh_plot(self):
        self.statPlot.kanjiStats(Kanji.freq_stats())
        self.update_stat_info()
        #self.statPlot.clearCanvas()
        #picked, freqs = Kanji.freq_stats()
        ##print max(picked), max(freqs)
        ##self.statPlot.canvas.ax.hist(picked, freqs, histtype='bar')
        ##self.statPlot.canvas.ax.hist(picked, 50, histtype='bar')

        ##hist, bins = np.histogram(picked, bins=100)
        ## will lag
        ##self.statPlot.canvas.ax.bar(freqs, picked)
        #self.statPlot.canvas.ax.plot(freqs, picked)

        #self.statPlot.canvas.ax.set_xlabel('Frequency')
        #self.statPlot.canvas.ax.set_ylabel('Number of times picked')
        #self.statPlot.canvas.ax.set_title('Distribution of (pseudo)randomly selected kanji')
        ##self.statPlot.canvas.ax.text(max(freqs)/2, max(picked),
                                    ##"""This distribution illustrates how much times (max %d)
                                    ##kanji with different frequencies (max %d) has been picked"""
                                    ##% (max(picked), max(freqs)), bbox=dict(facecolor='blue', alpha=0.1))
        #self.statPlot.canvas.ax.grid(True)
        #self.statPlot.canvas.ax.fill_between(freqs, picked, 1,
                                            #facecolor='blue', alpha=0.5)
        #self.statPlot.canvas.draw()

    def batch_test(self):
        if self.beginTest.isVisible():
            self.testNumber.hide()
            self.targetMaxPicked.hide()
            self.beginTest.hide()
            self.testProgress.hide()
        else:
            self.testNumber.show()
            self.targetMaxPicked.show()
            self.beginTest.show()
            #self.testProgress.show()

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
Max frequency: <b>%d</b> | Picked more than once: <b>%d</b>" %
                    (count, max(picked), max(freqs), picked_count))
            self.update()
        except ValueError:
            pass
