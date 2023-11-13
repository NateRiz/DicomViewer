import typing

from PyQt6.QtCore import Qt, QDir
from PyQt6.QtGui import QPixmap, QWheelEvent, QColor
from PyQt6.QtWidgets import QLabel, QHBoxLayout, QGraphicsDropShadowEffect, QFrame, QSizePolicy

from ImageLoader import ImageLoader
from ScrollBar import ScrollBar


class ImageViewer(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("ImageViewer")
        self.setStyleSheet("background-color:#1e1e1e;")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 160))

        self.images = []
        self.current_index = 0

        self.scrollbar = ScrollBar(Qt.Orientation.Vertical, False)
        self.scrollbar.setMaximum(0)
        self.scrollbar.valueChanged.connect(self._on_scrollbar_value_changed)

        self.current_image = QLabel()
        self.current_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_ = QHBoxLayout()
        self.setLayout(self.layout_)

        self.layout_.addWidget(self.current_image)
        self.layout_.addWidget(self.scrollbar)

    def _show_image(self, index):
        if not self.images:
            return
        pixmap = QPixmap(self.images[index])
        self.current_image.setPixmap(pixmap)

    def _show_next_image(self):
        self.current_index = (self.current_index + 1) % len(self.images)
        self._show_image(self.current_index)

    def setup(self, series_path):
        image_loader = ImageLoader()
        self.images = image_loader.load_from_series(series_path)
        """
        dir_ = QDir(series_path)
        dir_.setNameFilters(['*.png', "*.jpg", "*.jpeg"])
        file_info_list = dir_.entryInfoList()
        self.images = [file_info.filePath() for file_info in file_info_list]
        """
        self.scrollbar.setMaximum(len(self.images) - 1)
        self.current_index = 0
        self._show_image(self.current_index)

    def reset(self):
        self.current_index = 0
        self.images.clear()
        self.current_image.clear()
        self.scrollbar.setMaximum(0)

    def _on_scrollbar_value_changed(self, value):
        self.current_index = value
        self._show_image(self.current_index)

    def wheelEvent(self, event: typing.Optional[QWheelEvent]) -> None:
        if not self.images:
            return
        if event.angleDelta().y() > 0:
            new_val = (self.scrollbar.value() - 1) % self.scrollbar.maximum()
            self.scrollbar.setValue(new_val)
        else:
            new_val = (self.scrollbar.value() + 1) % self.scrollbar.maximum()
            self.scrollbar.setValue(new_val)
