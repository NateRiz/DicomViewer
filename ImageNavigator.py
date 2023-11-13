from PyQt6.QtWidgets import QVBoxLayout, QFrame, QSizePolicy

from ImageViewer import ImageViewer
from SeriesPreview import SeriesPreview


class ImageNavigator(QFrame):
    def __init__(self):
        super().__init__()
        self.v_layout = QVBoxLayout()
        self.setLayout(self.v_layout)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.image_viewer = ImageViewer()
        self.series_preview = SeriesPreview()
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.v_layout.addWidget(self.image_viewer)
        self.v_layout.addSpacing(16)
        self.v_layout.addWidget(self.series_preview)

    def reset(self):
        self.image_viewer.reset()
        self.series_preview.reset()

    def load_series(self, series_path):
        self.image_viewer.setup(series_path)
        self.series_preview.setup(series_path)
