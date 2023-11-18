import os

from PyQt6.QtCore import QSize
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QHBoxLayout, QFileDialog, QFrame, QApplication, QSizePolicy

from DicomAdapter import DicomAdapter
from ImageNavigator import ImageNavigator
from Navigator import Navigator
from OpenDialog import OpenDialog


class MainWidget(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("MainWidget")
        self.dicom_adapter = None
        self.h_layout = QHBoxLayout()
        self.setLayout(self.h_layout)
        self.open_dialog = OpenDialog(self.on_menu_open)
        self.h_layout.addWidget(self.open_dialog)
        self.setStyleSheet('background-color:#242424')

        self.image_navigator = ImageNavigator()
        self.navigator = Navigator(self.load_series)

    def on_menu_open(self):
        file_dialog = QFileDialog()
        dicom_path, _ = file_dialog.getOpenFileName(self, "Open DICOMDIR File")

        if not dicom_path:
            return

        self.dicom_adapter = DicomAdapter(dicom_path)
        self.window().resize(QSize(1536,1024))
        self.reset_window()
        self.h_layout.addWidget(self.navigator)
        self.h_layout.addWidget(self.image_navigator)
        self.navigator.load_dicom(dicom_path)
        self.recenter_window()

    def recenter_window(self):
        # Process events to force the layout to update the geometry
        QApplication.processEvents()

        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.window().width()) // 2
        y = (screen.height() - self.window().height()) // 2
        self.window().move(x, y)

    def reset_window(self):
        self.image_navigator.reset()
        while self.h_layout.count():
            layout_item = self.h_layout.takeAt(0)
            widget = layout_item.widget()
            if widget:
                widget.setParent(None)

    def load_series(self, study, series):
        self.image_navigator.load_series(study, series)
