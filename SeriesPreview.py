import os

from PyQt6.QtCore import Qt, pyqtSignal, QSize, QPoint, QTimer
from PyQt6.QtGui import QPixmap, QFont, QWheelEvent, QCursor
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QScrollArea, QVBoxLayout, QSizePolicy, QApplication

from ScrollBar import ScrollBar

class SeriesButton(QFrame):
    clicked = pyqtSignal()

    def __init__(self, study, series, pixmap):
        super().__init__()
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.study = study
        self.series = series
        self.pixmap = pixmap

        self.v_layout = QVBoxLayout()
        self.setLayout(self.v_layout)
        self.v_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.thumbnail = QLabel()
        self.thumbnail.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.thumbnail.setPixmap(pixmap)

        self.v_layout.addWidget(self.thumbnail)
        text = QLabel(series)
        text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.v_layout.addWidget(text)

        font = QFont("Segoe UI", 12)
        font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
        self.setFont(font)
        self.setStyleSheet("""
        .SeriesButton{
            color:white;
            border: 1px solid #707070;
        }
        .SeriesButton:Hover{
            background:#3d3d3d;
        }
        QLabel{
            background-color:rgba(0,0,0,0);
        }
        """)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.clicked.emit()  # Emit the clicked signal
        self.window().findChild(QFrame, "ImageViewer").setup(self.study, self.series)

        self.window().findChild(QFrame, "StudyNavigator").select_item(self.study, self.series)

class SeriesPreview(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(156)
        self.v_layout = QVBoxLayout()
        self.setLayout(self.v_layout)
        self.v_layout.setSpacing(0)
        self.v_layout.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("border:none")

        self.scroll_area = QScrollArea()
        self.scroll_area.setStyleSheet("border:none")
        self.scrollable_series_preview = ScrollableSeriesPreview(self.scroll_area)
        self.scroll_area.setContentsMargins(0, 0, 0, 0)
        self.scroll_area.setWidget(self.scrollable_series_preview)
        self.scroll_bar = ScrollBar(Qt.Orientation.Horizontal)
        self.scroll_area.setHorizontalScrollBar(self.scroll_bar)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)

        self.scroll_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.v_layout.addWidget(self.scroll_area)


    def setup(self, study):
        self.scrollable_series_preview.setup(study)

    def reset(self):
        self.scrollable_series_preview.reset()

    def wheelEvent(self, event):
        super().wheelEvent(event)
        delta = event.angleDelta().y()
        self.scroll_bar.setValue(self.scroll_bar.value() - delta)
        event.accept()


class ScrollableSeriesPreview(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.h_layout = QHBoxLayout()
        self.setLayout(self.h_layout)
        self.setStyleSheet("""
        ScrollableSeriesPreview{
            border-top: 2px solid #7160E8;
            border-left: 1px solid #2e2e2e;
            border-bottom: 1px solid #2e2e2e;
            border-right: 1px solid #2e2e2e;
        }
        """)

    def setup(self, study):
        self.reset()
        buttons = []
        dicom_adapter = self.window().findChild(QFrame, "MainWidget").dicom_adapter
        series_list = dicom_adapter.get_series_list(study)
        for series in series_list:
            buttons.append(self.create_thumbnail(study, series))

        self.updateGeometry()
        QApplication.processEvents()

        for btn in buttons:
            self.h_layout.addWidget(btn)

    def reset(self):
        while self.h_layout.count():
            item = self.h_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def create_thumbnail(self, study, series):
        dicom_adapter = self.window().findChild(QFrame, "MainWidget").dicom_adapter
        pixmap = dicom_adapter.load_series_preview_image(study, series)
        scaled_pixmap = pixmap.scaled(78, 78)
        return SeriesButton(study, series, scaled_pixmap)
