# -*- coding=utf-8 -*-
"""
Main application script. Console-less version.
"""

# internal #
import sys

# external #
from PyQt4.QtGui import QApplication

# own #
from gui.ui import GUI
from db.store import init_db

def main():
    app = QApplication(sys.argv)
    #app.setIcon(QPixmap())
    init_db()

    gui = GUI()
    gui.get_all()
    gui.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
