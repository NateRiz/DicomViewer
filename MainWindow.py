import sys

from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow

from MainWidget import MainWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dicom Loader")

        self.open_action = QAction("Open", self)
        self.open_action.triggered.connect(self.on_open_action)

        self.export_action = QAction("Export", self)
        self.export_action.triggered.connect(self.on_export_action)
        self.export_action.setDisabled(True)

        self.exit_action = QAction("Exit", self)
        self.exit_action.triggered.connect(self.on_exit_action)

        file_menu = self.menuBar().addMenu("File")
        self.menuBar().setStyleSheet("""
        QMenuBar {
            background-color: #2C2C2C;
            color: white;
        }
        QMenuBar::item:selected {
            background-color: #33373D;
        }
        QMenu {
            background-color:#2C2C2C;
            color:white;
        }
        QMenu::item:selected {
            background-color: #33373D;
            }
        """)
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.export_action)
        file_menu.addAction(self.exit_action)

        self.main_widget = MainWidget()
        self.setCentralWidget(self.main_widget)

    def on_open_action(self):
        self.main_widget.on_menu_open()

    def on_export_action(self):
        pass

    def on_exit_action(self):
        self.destroy()
        sys.exit(0)
