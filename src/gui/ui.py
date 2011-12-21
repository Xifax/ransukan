# -*- coding=utf-8 -*-
"""
Defines main UI dialog.
"""

# internal #
import platform

# own #
from gui.params import KANJI, NAME, WIDTH, HEIGHT, \
                       PRETTY_FONT, KANJI_SIZE, \
                       MESSAGE_HEIGHT, MESSAGE_TIMEOUT, \
                       PROGRESS_HEIGHT, TOOLTIP_FONT_SIZE
from pref.opt import __version__, __author__, app_name, app_about, dbs, paths
from alg.altogether import RandomMess, MessedUpException
from db.kanji import Kanji
from db.jdic import JDIC
from db.store import choose_db, NoDbException
from gui.stats import StatsUI

# external #
from PyQt4.QtGui import QWidget, QGridLayout, \
                        QGroupBox, QLabel, QPushButton, QApplication, QFont, \
                        QComboBox, QProgressBar, QToolTip, QMessageBox, QPixmap

from PyQt4.QtCore import Qt, QObject, QEvent, QTimer, QThread, pyqtSignal, QSize

def parent_up(object):
    """
    Get top parent for child object in case of event handling.
    """
    if isinstance(object, QObject):
        return object.parent().parent()

class LabelEventFilter(QObject):
    """
    Process mouse hover/click events on kanji labels.
    """
    def eventFilter(self, object, event):

        if event.type() == QEvent.HoverEnter:
            object.setStyleSheet("QLabel { color: rgb(125, 125, 255); }")
        if event.type() == QEvent.HoverLeave:
            object.setStyleSheet("QLabel { color: rgb(0, 0, 0); }")
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                try:
                    kanji = None
                    while kanji is None:
                        kanji = Kanji.get_random(parent_up(object).al.random_int())
                    object.setText(kanji.character)
                    if object is parent_up(object).day:
                        parent_up(object).dayLabel.setText('<b>Day:</b> ' + str(kanji.frequency) + ' | '
                                                + str(kanji.dominance) + '%')
                    elif object is parent_up(object).week:
                        parent_up(object).weekLabel.setText('<b>Week:</b> ' + str(kanji.frequency) + ' | '
                                                + str(kanji.dominance) + '%')
                    elif object is parent_up(object).month:
                        parent_up(object).monthLabel.setText('<b>Month:</b> ' + str(kanji.frequency) + ' | '
                                                + str(kanji.dominance) + '%')
                    elif object is parent_up(object).year:
                        parent_up(object).yearLabel.setText('<b>Year:</b> ' + str(kanji.frequency) + ' | '
                                                + str(kanji.dominance) + '%')
                    parent_up(object).kanji_tooltip(object)
                except MessedUpException as e:
                    parent_up(object).show_message_then_hide(e.message)
            elif event.button() == Qt.RightButton:
                found = JDIC.search(object.text())
                if found:
                    parent_up(object).toggle_kanji_info(object, found)
                else:
                    parent_up(object).show_message_then_hide('No such kanji in kanjidic2!')
        return False

class GUI(QWidget):

    def __init__(self, parent=None):
        super(GUI, self).__init__(parent)

        self.create_ui_components()
        self.compose_ui()

        # Initializing: window composition, it's contents and event handlers
        self.init_composition()
        self.init_contents()
        self.init_actions()

        self.on_start()

    def create_ui_components(self):
        """
        Create layouts and qt controls.
        """
        self.layout = QGridLayout()

        self.kanjiGroup = QGroupBox()
        self.kanjiLayout = QGridLayout()

        # Kanji ui group
        self.day, self.week, self.month, self.year = \
        QLabel(KANJI), QLabel(KANJI), QLabel(KANJI), QLabel(KANJI)

        self.dayLabel, self.weekLabel, self.monthLabel, self.yearLabel = \
        QLabel('<b>Day</b>'), QLabel('<b>Week</b>'), \
        QLabel('<b>Month</b>'), QLabel('<b>Year</b>')

        # Main layout
        self.showAbout = QPushButton('A&bout')
        # DB controls (top)
        self.showDB, self.availableDB, self.changeDB = \
        QPushButton('&Change DB (active:)'), QComboBox(), QPushButton('&Remap')
        # General controls (bottom)
        self.getAll, self.showStats, self.quitApp, self.authGen, self.methodCombo = \
        QPushButton('&Get all'), QPushButton('&Stats'), QPushButton('&Quit'), \
        QPushButton('&Auth'), QComboBox()
        # Notifications
        self.progressBar = QProgressBar()
        self.statusMessage = QLabel()
        # About
        self.aboutBox = QMessageBox()

    def compose_ui(self):
        """
        Fill layouts and groups, initialize filters.
        """
        self.kanjiLayout.addWidget(self.day, 0, 0)
        self.kanjiLayout.addWidget(self.week, 0, 1)
        self.kanjiLayout.addWidget(self.dayLabel, 1, 0)
        self.kanjiLayout.addWidget(self.weekLabel, 1, 1)

        self.kanjiLayout.addWidget(self.month, 2, 0)
        self.kanjiLayout.addWidget(self.year, 2, 1)
        self.kanjiLayout.addWidget(self.monthLabel, 3, 0)
        self.kanjiLayout.addWidget(self.yearLabel, 3, 1)

        self.kanjiGroup.setLayout(self.kanjiLayout)

        self.layout.addWidget(self.showDB, 0, 0, 1, 2)
        self.layout.addWidget(self.availableDB, 1, 0)
        self.layout.addWidget(self.changeDB, 1, 1)
        self.layout.addWidget(self.kanjiGroup, 2, 0, 1, 2)
        self.layout.addWidget(self.getAll, 3, 0)
        self.layout.addWidget(self.showStats, 3, 1)
        self.layout.addWidget(self.methodCombo, 4, 0)
        self.layout.addWidget(self.authGen, 4, 1)
        #self.layout.addWidget(self.quitApp, 5, 0, 1, 2)
        self.layout.addWidget(self.quitApp, 5, 0)
        self.layout.addWidget(self.showAbout, 5, 1)
        self.layout.addWidget(self.progressBar, 6, 0, 1, 2)
        self.layout.addWidget(self.statusMessage, 7, 0, 1, 2)

        self.setLayout(self.layout)

        self.eFilter = LabelEventFilter()

    def on_start(self):
        """
        Additional procedures run on application start.
        """
        # Let's initialize even some stuff!
        self.stats = StatsUI(self)
        self.al = None
        self.auth_thread = None
        self.init_backend()
        choose_db(str(self.availableDB.currentText()))
        self.showDB.setText("&Change DB (active: %s)" % self.availableDB.currentText())

    def init_composition(self):
        """
        Window composition and general params.
        """
        self.setWindowTitle(NAME + ' ' + __version__)
        desktop = QApplication.desktop()
        self.setGeometry((desktop.width() - WIDTH)/2,
                        (desktop.height() - HEIGHT)/2, WIDTH, HEIGHT)

    def init_contents(self):
        """
        Setting up qt controls.
        """
        self.changeDB.hide()
        self.availableDB.hide()
        self.availableDB.addItems(dbs.keys())

        self.kanjiGroup.setAlignment(Qt.AlignCenter)
        self.kanjiGroup.setStyleSheet("QGroupBox { border: 1px solid gray; border-radius: 3px; }")

        self.day.setAlignment(Qt.AlignCenter)
        self.week.setAlignment(Qt.AlignCenter)
        self.month.setAlignment(Qt.AlignCenter)
        self.year.setAlignment(Qt.AlignCenter)
        self.dayLabel.setAlignment(Qt.AlignCenter)
        self.weekLabel.setAlignment(Qt.AlignCenter)
        self.monthLabel.setAlignment(Qt.AlignCenter)
        self.yearLabel.setAlignment(Qt.AlignCenter)

        self.day.setFont(QFont(PRETTY_FONT, KANJI_SIZE))
        self.week.setFont(QFont(PRETTY_FONT, KANJI_SIZE))
        self.month.setFont(QFont(PRETTY_FONT, KANJI_SIZE))
        self.year.setFont(QFont(PRETTY_FONT, KANJI_SIZE))

        self.methodCombo.addItems(RandomMess.algs.keys())
        self.methodCombo.setCurrentIndex(1)

        self.statusMessage.setAlignment(Qt.AlignCenter)
        self.statusMessage.hide()
        self.statusMessage.setMaximumHeight(MESSAGE_HEIGHT)
        self.statusMessage.setStyleSheet("QLabel { color: rgb(255, 69, 0); background-color: transparent;  \
                                                   border: 1px solid gray; border-radius: 3px; }")

        self.progressBar.setMaximum(0)
        self.progressBar.setMaximumHeight(PROGRESS_HEIGHT)
        self.progressBar.hide()

        QToolTip.setFont(QFont(PRETTY_FONT, TOOLTIP_FONT_SIZE))

        self.getAll.setToolTip('Randomly select all 4 kanji')
        self.methodCombo.setToolTip('Choose algorithm for randomness')
        self.authGen.setToolTip('Authorize on remote RNG services')
        self.showStats.setToolTip('Show/hide dialog with comprehensive statistics')
        self.quitApp.setToolTip('Close application')
        self.showDB.setToolTip('Show/hide available databases')
        self.availableDB.setToolTip('Available kanji frequency charts db')
        self.changeDB.setToolTip('Pick new kanji from currently selected db')

        # About dialog
        self.aboutBox.layout().itemAt(1).widget().setAlignment(Qt.AlignLeft)

        self.aboutBox.setTextFormat(Qt.RichText)
        self.aboutBox.setText('Version:\t<b>' + __version__ + '</b><br/>Python:\t<b>' + platform.python_version() + '</b>' +
                                '<br/>Platform:\t<b>' + platform.system() + ' ' + platform.release() + '</b>' +
                                '<br/>Author:\t<b>' + __author__ + '</b>' + app_about)
        self.aboutBox.setWindowTitle('About ' + app_name)
        self.aboutBox.setIconPixmap(QPixmap(paths['icon']))

    def init_actions(self):
        """
        Binding events/handlers.
        """
        self.showDB.clicked.connect(self.show_available_db)
        self.changeDB.clicked.connect(self.change_db)

        self.quitApp.clicked.connect(self.close)
        self.getAll.clicked.connect(self.get_all)
        self.authGen.clicked.connect(self.auth_task)
        self.showStats.clicked.connect(self.show_stats)
        self.methodCombo.currentIndexChanged.connect(self.update_alg)

        self.showAbout.clicked.connect(self.app_help)

        # Mouse events for labels
        self.day.setAttribute(Qt.WA_Hover, True)
        self.week.setAttribute(Qt.WA_Hover, True)
        self.month.setAttribute(Qt.WA_Hover, True)
        self.year.setAttribute(Qt.WA_Hover, True)
        self.day.installEventFilter(self.eFilter)
        self.week.installEventFilter(self.eFilter)
        self.month.installEventFilter(self.eFilter)
        self.year.installEventFilter(self.eFilter)

    ##### actions #####

    def show_stats(self):
        if self.stats.isVisible():
            self.stats.hide()
        else:
            self.stats.show()

    def show_available_db(self):
        if self.availableDB.isVisible():
            self.availableDB.hide()
            self.changeDB.hide()
        else:
            self.availableDB.show()
            self.changeDB.show()

    def change_db(self):
        try:
            choose_db(str(self.availableDB.currentText()))
            self.availableDB.hide()
            self.changeDB.hide()
            self.show_message_then_hide("DB successfully remaped!", False)
            self.showDB.setText("&Change DB (active: %s)" % self.availableDB.currentText())
        except NoDbException as e:
            self.show_message_then_hide(e.message)

    def get_all(self):
        try:
            kanji_set = []
            while len(kanji_set) != 4:
                kanji = Kanji.get_random(self.al.random_int())
                if kanji is not None:
                    # Should not get the same kanji in one set
                    if kanji not in kanji_set:
                        kanji_set.append(kanji)

            for_a_day = kanji_set.pop()
            for_a_week = kanji_set.pop()
            for_a_month = kanji_set.pop()
            for_a_year = kanji_set.pop()

            self.day.setText(for_a_day.character)
            self.dayLabel.setText('<b>Day:</b> ' + str(for_a_day.frequency) + ' | '
                                        + str(for_a_day.dominance) + '%')
            self.week.setText(for_a_week.character)
            self.weekLabel.setText('<b>Week:</b> ' + str(for_a_week.frequency) + ' | '
                                        + str(for_a_week.dominance) + '%')
            self.month.setText(for_a_month.character)
            self.monthLabel.setText('<b>Month:</b> ' + str(for_a_month.frequency) + ' | '
                                        + str(for_a_month.dominance) + '%')
            self.year.setText(for_a_year.character)
            self.yearLabel.setText('<b>Year:</b> ' + str(for_a_year.frequency) + ' | '
                                        + str(for_a_year.dominance) + '%')

            self.kanji_tooltip(self.day)
            self.kanji_tooltip(self.week)
            self.kanji_tooltip(self.month)
            self.kanji_tooltip(self.year)
        except MessedUpException as e:
            self.show_message_then_hide(e.message)

    def pretty_font(self):
        pass

    def update_alg(self):
        self.al.set_active(str(self.methodCombo.currentText()))

    def init_backend(self):
        self.al = RandomMess()
        self.update_alg()

    def auth_task(self):
        self.auth_thread = AuthorizationTask(self.al)
        self.auth_thread.done.connect(self.auth_complete)
        #self.auth_thread.run()
        # IT DOESN't work on windows as it should!
        self.auth_thread.start()
        self.show_progress('Authorizing on RNG services...')

    def auth_complete(self, success):
        self.hide_message()
        self.hide_progress()
        if success:
            self.show_message_then_hide("Successfully authenticated!", False)
        else:
            self.show_message_then_hide("Sorry, could not authenticate.")

    def show_message_then_hide(self, message, error=True):
        if error:
            self.statusMessage.setStyleSheet("QLabel { color: rgb(255, 69, 0); background-color: transparent; \
                                                       border: 1px solid gray; border-radius: 3px; }")
        else:
            self.statusMessage.setStyleSheet("QLabel { color: rgb(50, 205, 50); background-color: transparent; \
                                                       border: 1px solid gray; border-radius: 3px; }")

        self.statusMessage.setText(message)
        self.statusMessage.show()
        QTimer.singleShot(MESSAGE_TIMEOUT, self.hide_message)

    def show_progress(self, message):
        self.statusMessage.setStyleSheet("QLabel { color: rgb(50, 205, 50); background-color: transparent; \
                                                       border: 1px solid gray; border-radius: 3px; }")
        self.statusMessage.setText(message)
        self.statusMessage.show()
        self.progressBar.show()

    def hide_message(self):
        self.statusMessage.setText('')
        self.statusMessage.hide()

    def hide_progress(self):
        self.progressBar.hide()

    def toggle_kanji_info(self, label, info):
        label.setToolTip(info.info())

    def kanji_tooltip(self, label):
        found = JDIC.search(label.text())
        if found:
            label.setToolTip(found.info())
        else:
            label.setToolTip('No such kanji in kanjidic2!')

    def kanji_info(self, kanji):
        pass

    def app_help(self):
        self.aboutBox.show()

        #### Utility events ####

    def resizeEvent(self, QResizeEvent):
        self.updateStatsPosition()
        self.updateStatsSize()

    def moveEvent(self, QMoveEvent):
        self.updateStatsPosition()
        self.updateStatsSize()

    def updateStatsPosition(self):
        self.stats.move(self.x() + self.width() + 20, self.y())

    def updateStatsSize(self):
        self.stats.resize(QSize(self.stats.width(), self.height()))

class AuthorizationTask(QThread):
    """
    Remote RNG authorization task, run in separate thread.
    """
    done = pyqtSignal(bool)

    def __init__(self, al, parent=None):
        super(AuthorizationTask, self).__init__(parent)
        self.al = al
        self.success = False

    def run(self):
        try:
            self.al.auth()
            self.success = True
        except Exception as e:
            pass

        self.done.emit(self.success)

class RandomNumberTask(QThread):
    """
    Get random number from one of the RNG services.
    """
    number = pyqtSignal(int)

    def __init__(self, al, praent=None):
        super(RandomNumberTask, self).__init__(parent)
        self.al = al
        self.result = None

    def run(self):
        try:
            self.result = self.al.random_int()
        except Exception as e:
            pass

        self.done.emit(self.result)
