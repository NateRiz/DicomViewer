import os.path

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QPushButton

from ImageExporter import ImageExporter


class NavigatorActions(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("NavigatorActions")
        self.h_layout = QHBoxLayout()
        self.setLayout(self.h_layout)

        font = QFont("Segoe UI", 12)
        font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)

        self.load_button = QPushButton("Load")
        self.load_button.clicked.connect(self.on_load)
        self.load_button.setDisabled(True)
        self.load_button.setFont(font)
        self.load_button.setStyleSheet("""
        QPushButton{
            color:white;
            border:1px solid #707070;
        }
        QPushButton:Hover{
            background:#3d3d3d;
        }
        QPushButton:Disabled{
            background-color: #a0a0a0;  
            color: #cccccc;  
            border: 1px solid #707070;
        }
        """)
        self.export_button = QPushButton("Export Series")
        self.export_button.clicked.connect(self.on_export)
        self.export_button.setDisabled(True)
        self.export_button.setFont(font)
        self.export_button.setStyleSheet(self.load_button.styleSheet())

        self.export_all_button = QPushButton("Export Study")
        self.export_all_button.clicked.connect(self.on_export_all)
        self.export_all_button.setFont(font)
        self.export_all_button.setStyleSheet(self.load_button.styleSheet())

        self.h_layout.addWidget(self.load_button)
        self.h_layout.addWidget(self.export_all_button)
        self.h_layout.addWidget(self.export_button)

    def set_load_button_enabled(self, is_enabled):
        self.load_button.setEnabled(is_enabled)

    def set_export_button_enabled(self, is_enabled):
        self.export_button.setEnabled(is_enabled)

    def on_load(self):
        study_navigator = self.parent().findChild(QFrame, "StudyNavigator")
        study_navigator.try_load_series()

    def on_export(self):
        study_navigator = self.window().findChild(QFrame, "StudyNavigator")
        study, series = study_navigator.get_selected_series_path()
        if not study or not series:
            print("No series selected. Canceling.")
            return
        ImageExporter(self).save_series(study, series)

    def on_export_all(self):
        study_navigator = self.window().findChild(QFrame, "StudyNavigator")
        ImageExporter(self).save_studies(study_navigator.get_study_paths())
