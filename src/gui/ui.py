# -*- coding=utf-8 -*-
"""
Defines main UI dialog.
"""

# own #
from gui.params import KANJI, NAME, WIDTH, HEIGHT, \
                       PRETTY_FONT, KANJI_SIZE, \
                       MESSAGE_HEIGHT, MESSAGE_TIMEOUT, \
                       PROGRESS_HEIGHT
from pref.opt import __version__, dbs
from alg.altogether import RandomMess, MessedUpException
from db.kanji import Kanji
from db.store import choose_db, NoDbException

# external #
from PyQt4.QtGui import QWidget, QGridLayout, \
                        QGroupBox, QLabel, QPushButton, QApplication, QFont, \
                        QComboBox, QProgressBar

from PyQt4.QtCore import Qt, QObject, QEvent, QTimer, QThread, pyqtSignal

def parent_up(object):
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
                        parent_up(object).dayLabel.setText('Day: ' + str(kanji.frequency) + ' | '
                                                + str(kanji.dominance) + '%')
                    elif object is parent_up(object).week:
                        parent_up(object).weekLabel.setText('Week: ' + str(kanji.frequency) + ' | '
                                                + str(kanji.dominance) + '%')
                    elif object is parent_up(object).month:
                        parent_up(object).monthLabel.setText('Month: ' + str(kanji.frequency) + ' | '
                                                + str(kanji.dominance) + '%')
                    elif object is parent_up(object).year:
                        parent_up(object).yearLabel.setText('Year: ' + str(kanji.frequency) + ' | '
                                                + str(kanji.dominance) + '%')
                except MessedUpException as e:
                    parent_up(object).show_message_then_hide(e.message)
            elif event.button() == Qt.RightButton:
                # todo: statistics?
                pass
        return False

class GUI(QWidget):

    def __init__(self, parent=None):
        super(GUI, self).__init__(parent)

        self.layout = QGridLayout()

        self.kanjiGroup = QGroupBox()
        self.kanjiLayout = QGridLayout()

        # Kanji ui group
        self.day = QLabel(KANJI)
        self.week = QLabel(KANJI)
        self.month = QLabel(KANJI)
        self.year = QLabel(KANJI)

        self.dayLabel = QLabel('Day')
        self.weekLabel = QLabel('Week')
        self.monthLabel = QLabel('Month')
        self.yearLabel = QLabel('Year')

        self.kanjiLayout.addWidget(self.day, 0, 0)
        self.kanjiLayout.addWidget(self.week, 0, 1)
        self.kanjiLayout.addWidget(self.dayLabel, 1, 0)
        self.kanjiLayout.addWidget(self.weekLabel, 1, 1)

        self.kanjiLayout.addWidget(self.month, 2, 0)
        self.kanjiLayout.addWidget(self.year, 2, 1)
        self.kanjiLayout.addWidget(self.monthLabel, 3, 0)
        self.kanjiLayout.addWidget(self.yearLabel, 3, 1)

        self.kanjiGroup.setLayout(self.kanjiLayout)

        # Main layout
        # DB controls (top)
        self.showDB = QPushButton('&Change DB (active:)')
        self.availableDB = QComboBox()
        self.changeDB = QPushButton('&Remap')
        # General controls (bottom)
        self.getAll = QPushButton('&Get all')
        self.showStats = QPushButton('&Stats')
        self.quitApp = QPushButton('&Quit')
        self.authGen = QPushButton('&Auth')
        self.methodCombo = QComboBox()
        # Notifications
        self.progressBar = QProgressBar()
        self.statusMessage = QLabel()
        self.layout.addWidget(self.showDB, 0, 0, 1, 2)
        self.layout.addWidget(self.availableDB, 1, 0)
        self.layout.addWidget(self.changeDB, 1, 1)
        self.layout.addWidget(self.kanjiGroup, 2, 0, 1, 2)
        self.layout.addWidget(self.getAll, 3, 0)
        self.layout.addWidget(self.showStats, 3, 1)
        self.layout.addWidget(self.methodCombo, 4, 0)
        self.layout.addWidget(self.authGen, 4, 1)
        self.layout.addWidget(self.quitApp, 5, 0, 1, 2)
        self.layout.addWidget(self.progressBar, 6, 0, 1, 2)
        self.layout.addWidget(self.statusMessage, 7, 0, 1, 2)

        self.setLayout(self.layout)

        self.eFilter = LabelEventFilter()

        # Initializing: window composition, it's contents and event handlers
        self.init_composition()
        self.init_contents()
        self.init_actions()

        # Let's initialize even some stuff!
        self.al = None
        self.auth_thread = None
        self.init_backend()
        choose_db(str(self.availableDB.currentText()))
        self.showDB.setText("&Change DB (active: %s)" % self.availableDB.currentText())

    def init_composition(self):
        self.setWindowTitle(NAME + ' ' + __version__)
        desktop = QApplication.desktop()
        self.setGeometry((desktop.width() - WIDTH)/2, \
                        (desktop.height() - HEIGHT)/2, WIDTH, HEIGHT)

    def init_contents(self):
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

    def init_actions(self):
        self.showDB.clicked.connect(self.show_available_db)
        self.changeDB.clicked.connect(self.change_db)
        self.quitApp.clicked.connect(self.close)
        self.getAll.clicked.connect(self.get_all)
        self.authGen.clicked.connect(self.auth_task)
        self.methodCombo.currentIndexChanged.connect(self.update_alg)

        # Mouse events for labels
        self.day.setAttribute(Qt.WA_Hover, True)
        self.week.setAttribute(Qt.WA_Hover, True)
        self.month.setAttribute(Qt.WA_Hover, True)
        self.year.setAttribute(Qt.WA_Hover, True)
        self.day.installEventFilter(self.eFilter)
        self.week.installEventFilter(self.eFilter)
        self.month.installEventFilter(self.eFilter)
        self.year.installEventFilter(self.eFilter)

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
            while(len(kanji_set) != 4):
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
            self.dayLabel.setText('Day: ' + str(for_a_day.frequency) + ' | '
                                        + str(for_a_day.dominance) + '%')
            self.week.setText(for_a_week.character)
            self.weekLabel.setText('Week: ' + str(for_a_week.frequency) + ' | '
                                        + str(for_a_week.dominance) + '%')
            self.month.setText(for_a_month.character)
            self.monthLabel.setText('Month: ' + str(for_a_month.frequency) + ' | '
                                        + str(for_a_month.dominance) + '%')
            self.year.setText(for_a_year.character)
            self.yearLabel.setText('Year: ' + str(for_a_year.frequency) + ' | '
                                        + str(for_a_year.dominance) + '%')
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


class AuthorizationTask(QThread):
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
