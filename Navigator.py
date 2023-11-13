from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QSizePolicy

from Metadata import Metadata
from NavigatorActions import NavigatorActions
from StudyNavigator import StudyNavigator


class Navigator(QFrame):
    def __init__(self, load_series_callback):
        super().__init__()
        self.setObjectName("Navigator")
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.setFixedWidth(350)
        self.v_layout = QVBoxLayout()
        self.v_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.v_layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.v_layout)

        self.metadata = Metadata()
        self.studies = StudyNavigator(load_series_callback)
        self.navigator_actions = NavigatorActions()

        self.v_layout.addWidget(self.metadata)
        self.v_layout.addSpacing(16)
        self.v_layout.addWidget(self.studies)
        self.v_layout.addSpacing(16)
        self.v_layout.addWidget(self.navigator_actions)


    def load_dicom(self, dicom_path):
        self.studies.load_dicom(dicom_path)
