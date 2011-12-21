# -*- coding=utf-8 -*-
"""
Main application script. Console-less version.
"""

# internal #
import sys

# external #
from PyQt4.QtGui import QApplication, QIcon

# own #
from gui.ui import GUI
from db.store import init_db
from pref.opt import paths

def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(paths['icon']))
    init_db()

    gui = GUI()
    gui.get_all()
    gui.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
