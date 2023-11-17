import os.path
import sys

from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtWidgets import QApplication

from MainWindow import MainWindow


def main():
    app = QApplication(sys.argv)

    font = QFont("Segoe UI", 10)
    font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
    app.setFont(font)
    app.setStyleSheet("QLabel { color : white; }")

    window = MainWindow()
    icon = QIcon(os.path.join(os.getcwd(), "icons", "patient.svg"))
    window.setWindowIcon(icon)
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()

# TODO
"""
- export to single dicom in open dialog
"""
