import typing

from PyQt6.QtCore import Qt, QDir
from PyQt6.QtGui import QPixmap, QWheelEvent, QColor
from PyQt6.QtWidgets import QLabel, QHBoxLayout, QGraphicsDropShadowEffect, QFrame, QSizePolicy, QScrollArea, QWidget

from ImageLoader import ImageLoader
from ScrollBar import ScrollBar


class ImageViewer(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("ImageViewer")
        self.setStyleSheet("background-color:#1e1e1e;")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setContentsMargins(0, 0, 0, 0)

        self.images = []
        self.current_index = 0

        self.scrollbar = ScrollBar(Qt.Orientation.Vertical)
        self.scrollbar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.scrollbar.setMaximum(0)
        self.scrollbar.valueChanged.connect(self._on_scrollbar_value_changed)

        self.unscaled_pixmap = QPixmap()
        self.scale_factor = 1.0

        self.image_container = QFrame()
        self.image_container.setLayout(QHBoxLayout())

        self.current_image = QLabel()
        self.image_container.layout().addWidget(self.current_image)
        self.current_image.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.current_image.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.image_container)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMouseTracking(True)
        self.dragging=False
        self.drag_start_point=None

        self.layout_ = QHBoxLayout()
        self.layout_.setContentsMargins(0,0,0,0)
        self.layout_.setSpacing(0)
        self.setLayout(self.layout_)

        self.layout_.addWidget(self.scroll_area)
        self.layout_.addWidget(self.scrollbar)

    def _show_image(self, index):
        if not self.images:
            return
        self.unscaled_pixmap = QPixmap(self.images[index])
        self.update_pixmap_with_scale()

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
        self.scale_factor=1.0
        self.unscaled_pixmap = QPixmap()

    def _on_scrollbar_value_changed(self, value):
        self.current_index = value
        self._show_image(self.current_index)

    def update_pixmap_with_scale(self):
        size = self.unscaled_pixmap.size()
        scaled_size = size * self.scale_factor
        scaled_pixmap = self.unscaled_pixmap.scaled(scaled_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.current_image.setPixmap(scaled_pixmap)

    def wheelEvent(self, event: typing.Optional[QWheelEvent]) -> None:
        if not self.images:
            return
        scale = 0.35
        if event.angleDelta().y() > 0:
            self.scale_factor += scale # Zoom in
        else:
            self.scale_factor -= scale  # Zoom out

        self.update_pixmap_with_scale()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.drag_start_point = event.pos()
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
            event.accept()

    def mouseMoveEvent(self, event):
        if self.dragging:
            delta = event.pos() - self.drag_start_point
            self.drag_start_point = event.pos()
            self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().value() - delta.y())
            self.scroll_area.horizontalScrollBar().setValue(self.scroll_area.horizontalScrollBar().value() - delta.x())
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
            self.setCursor(Qt.CursorShape.ArrowCursor)
            event.accept()
