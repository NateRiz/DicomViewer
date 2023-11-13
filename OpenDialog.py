import os
import sys

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QPixmap, QPainter, QIcon, QColor, QFontMetrics
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QSizePolicy


class DialogButton(QPushButton):
    def __init__(self, title, description, icon_file_name):
        super().__init__()
        self.setFixedSize(364, 78)
        self.setStyleSheet("""
        QPushButton{
            background-color:#383838;
            border: 1px solid #424242;
        }
        QPushButton:hover{
            background-color:#221D46;
            border: 1px solid #7160E7;
        }
        * {
            background-color: rgba(0,0,0,0)
        }
        """)

        self.h_layout = QHBoxLayout()
        self.setLayout(self.h_layout)

        self.icon = QLabel()
        self.create_icon(icon_file_name)
        self.h_layout.addWidget(self.icon)

        self.text_container = QWidget()
        self.text_container_layout = QVBoxLayout()
        self.title = QLabel(title)
        self.description = QLabel(description)
        self.create_button_text()

        self.h_layout.addWidget(self.text_container)

    def create_button_text(self):
        self.text_container.setLayout(self.text_container_layout)

        font = QFont("Segoe UI", 14)
        self.title.setFont(font)
        self.title.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        metrics = QFontMetrics(font)
        text_height = metrics.height()
        self.title.setMinimumHeight(text_height)

        self.text_container_layout.addWidget(self.title)
        self.text_container_layout.addWidget(self.description)

    def create_icon(self, icon_file_name):
        path = os.path.join(os.getcwd(), "icons", icon_file_name)
        svg_renderer = QSvgRenderer(path)
        pixmap = QPixmap(QSize(36, 36))  # Specify the desired size
        pixmap.fill(Qt.GlobalColor.transparent)  # Start with a transparent pixmap
        painter = QPainter(pixmap)
        svg_renderer.render(painter)
        painter.end()

        # Set the pixmap to the label
        self.icon.setPixmap(pixmap)
        self.icon.setMaximumSize(self.height(), self.height())
        self.icon.setAlignment(Qt.AlignmentFlag.AlignCenter)


class OpenDialog(QWidget):
    def __init__(self, on_menu_open_callback):
        super().__init__()
        self.on_menu_open_callback = on_menu_open_callback
        self.v_layout = QVBoxLayout()
        self.setLayout(self.v_layout)
        self.setStyleSheet("background-color:black;")

        self.open_button = DialogButton("Open a DICOMDIR file", "Extract from a local DICOMDIR file", "file_open.svg")
        self.open_button.clicked.connect(self.on_menu_open_callback)
        self.export_button = DialogButton("Export from a DICOMDIR file", "Unimplemented...", "export.svg")
        self.export_button.setStyleSheet(self.export_button.styleSheet()+"QPushButton{background-color:#4d4d4d}")
        self.export_button.setDisabled(True)
        self.exit_button = DialogButton("Exit", "Exit out of this program", "exit.svg")
        self.exit_button.clicked.connect(self.quit)

        self.v_layout.addWidget(self.open_button)
        self.v_layout.addSpacing(16)
        self.v_layout.addWidget(self.export_button)
        self.v_layout.addSpacing(16)
        self.v_layout.addWidget(self.exit_button)

    def quit(self):
        self.destroy()
        sys.exit(0)
