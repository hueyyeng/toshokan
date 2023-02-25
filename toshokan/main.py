import sys

from PySide6.QtWidgets import *

from toshokan.honbako import Honbako


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Toshokan")
    app.setApplicationDisplayName("Toshokan")
    honbako_app = Honbako()
    honbako_app.show()
    exit(app.exec())


if __name__ == '__main__':
    main()
