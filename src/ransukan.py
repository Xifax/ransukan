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
from db.store import init_db

def main():
    app = QApplication(sys.argv)

    # Initialize db
    init_db()

    # Create UI instance
    gui = GUI()
    # Get new kanji from db
    gui.get_all()
    # Display dialog
    gui.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    try:
        main()
    except Exception, e:
        print e
