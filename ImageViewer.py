import typing

from PyQt6.QtCore import Qt, QDir
from PyQt6.QtGui import QPixmap, QWheelEvent, QColor, QFont
from PyQt6.QtWidgets import QLabel, QHBoxLayout, QGraphicsDropShadowEffect, QFrame, QSizePolicy, QScrollArea, QWidget, \
    QPushButton

from ImageLoader import ImageLoader
from ScrollBar import ScrollBar

class ImageScrollArea(QScrollArea):
    def __init__(self):
        super().__init__()
        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
    def wheelEvent(self, event) -> None:
        event.ignore()

class ImageViewer(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("ImageViewer")
        self.setStyleSheet("""
        ImageViewer{
            background-color:#1e1e1e;
        }
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
        }""")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setContentsMargins(0, 0, 0, 0)

        self.images = []
        self.file_names = []
        self.current_index = 0

        self.scrollbar = ScrollBar(Qt.Orientation.Vertical, False)
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

        self.scroll_area = ImageScrollArea()
        self.scroll_area.setWidget(self.image_container)
        self.setMouseTracking(True)
        self.dragging = False
        self.drag_start_point = None

        self.layout_ = QHBoxLayout()
        self.layout_.setContentsMargins(0, 0, 0, 0)
        self.layout_.setSpacing(0)
        self.setLayout(self.layout_)

        self.layout_.addWidget(self.scroll_area)
        self.layout_.addWidget(self.scrollbar)

        self.current_file_name = QLabel("", self.scroll_area)
        self.current_file_name.setStyleSheet(
            "font-family: Segoe UI; color:white; font-size:12pt; background-color:rgb(0,0,0,0)")
        self.current_file_name.move(self.scroll_area.x() + 8, self.scroll_area.y() + 8)
        self.current_index_label = QLabel("", self.scroll_area)
        self.current_index_label.setStyleSheet(self.current_file_name.styleSheet())
        self.current_index_label.move(self.current_file_name.x(), self.current_file_name.rect().bottom() + 16)

        font = QFont("Segoe UI", 16)
        font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
        self.zoom_in = QPushButton("+", parent=self.scroll_area.viewport())
        self.zoom_in.setFixedSize(32, 32)
        self.zoom_in.clicked.connect(lambda:self._zoom_in_out(1))
        self.zoom_in.setFont(font)
        self.zoom_in.hide()

        self.zoom_out = QPushButton("-", parent=self.scroll_area.viewport())
        self.zoom_out.setFixedSize(32, 32)
        self.zoom_out.clicked.connect(lambda:self._zoom_in_out(-1))
        self.zoom_out.setFont(font)
        self.zoom_out.hide()

    def _show_image(self, index):
        if not self.images:
            return

        self.unscaled_pixmap = QPixmap(self.images[self.file_names[self.current_index]])
        self.update_pixmap_with_scale()

    def _show_next_image(self):
        self.current_index = (self.current_index + 1) % len(self.images)
        self._show_image(self.current_index)

    def setup(self, series_path):
        image_loader = ImageLoader()
        self.images = image_loader.load_from_series(series_path)
        self.file_names = list(self.images.keys())
        self.scrollbar.setMaximum(len(self.images) - 1)
        self.current_index = 0
        self._show_image(self.current_index)

        right_edge = self.scroll_area.viewport().width()
        self.zoom_in.move(right_edge - self.zoom_in.width() - 8, self.scroll_area.y() + 8)
        self.zoom_out.move(right_edge - self.zoom_out.width() - 8, self.scroll_area.y() + 8 + self.zoom_out.height() + 8)
        self.zoom_in.show()
        self.zoom_out.show()

    def reset(self):
        self.current_index = 0
        self.images.clear()
        self.current_image.clear()
        self.scrollbar.setMaximum(0)
        self.scale_factor = 1.0
        self.unscaled_pixmap = QPixmap()
        self.file_names.clear()
        self.current_index_label.clear()
        self.current_file_name.clear()

    def _on_scrollbar_value_changed(self, value):
        self.current_index = value
        self._show_image(self.current_index)

    def update_pixmap_with_scale(self):
        size = self.unscaled_pixmap.size()
        scaled_size = size * self.scale_factor
        scaled_pixmap = self.unscaled_pixmap.scaled(scaled_size, Qt.AspectRatioMode.KeepAspectRatio,
                                                    Qt.TransformationMode.SmoothTransformation)
        self.current_image.setPixmap(scaled_pixmap)

        self.current_file_name.setText(self.file_names[self.current_index])
        self.current_index_label.setText(f'{self.current_index + 1} / {len(self.file_names)}')
        metrics = self.current_file_name.fontMetrics()
        width = metrics.horizontalAdvance(self.current_file_name.text())
        self.current_file_name.setFixedWidth(width)
        self.current_index_label.setFixedWidth(width)

    def wheelEvent(self, event: typing.Optional[QWheelEvent]) -> None:
        if not self.images:
            return
        if event.angleDelta().y() > 0:
            new_val = (self.scrollbar.value() - 1) % self.scrollbar.maximum()
            self.scrollbar.setValue(new_val)
        else:
            new_val = (self.scrollbar.value() + 1) % self.scrollbar.maximum()
            self.scrollbar.setValue(new_val)

    def _zoom_in_out(self, multiplier):
        if not self.images:
            return
        scale = .75 * multiplier
        self.scale_factor = max(self.scale_factor + scale, 1.0)  # Zoom out
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
