# -*- coding=utf-8 -*-
"""
Main application script.
"""

# internal #
import sys

# external #
from PyQt4.QtGui import QApplication

# own #
from gui.ui import GUI

def main():
    app = QApplication(sys.argv)

    gui = GUI()
    gui.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    try:
        main()
    except Exception, e:
        print e
