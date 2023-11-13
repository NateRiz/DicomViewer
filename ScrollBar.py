from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QScrollBar


class ScrollBar(QScrollBar):
    def __init__(self, orientation: Qt.Orientation, wheel_enabled=True):
        super().__init__()
        self.setOrientation(orientation)
        self.is_wheel_enabled = wheel_enabled
        self.setStyleSheet("""
        QScrollBar:vertical{
            background-color: #2e2e2e;
            color:#999999;
            width:10px; 
            margin: 0px 0px 0px 0px;
        }
        QScrollBar::handle:vertical {
            background: #656565; /* Set your desired handle color here */
            min-height: 20px; /* Set a minimum height for the handle */
        }
        QScrollBar::handle:vertical:hover {
            background: #787878; /* Handle color on hover */
        }
        QScrollBar::add-line:vertical {
            background: none;
            height: 0px;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
        }
        QScrollBar::sub-line:vertical {
            background: none;
            height: 0px;
            subcontrol-position: top;
            subcontrol-origin: margin;
        }
        QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
            background: none;
        }
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: none;
        }

        QScrollBar:horizontal{
            background-color: #2e2e2e;
            color:#999999;
            height:10px; 
            margin: 0px 0px 0px 0px;
        }
        QScrollBar::handle:horizontal {
            background: #656565; /* Set your desired handle color here */
            min-width: 20px; /* Set a minimum height for the handle */
        }
        QScrollBar::handle:horizontal:hover {
            background: #787878; /* Handle color on hover */
        }
        QScrollBar::add-line:horizontal {
            background: none;
            width: 0px;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
        }
        QScrollBar::sub-line:horizontal {
            background: none;
            width: 0px;
            subcontrol-position: top;
            subcontrol-origin: margin;
        }
        QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal {
            background: none;
        }
        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
            background: none;
        }
        """)

    def wheelEvent(self, event):
        # Ignore wheel events to prevent scrolling
        if self.is_wheel_enabled:
            super().wheelEvent(event)
        else:
            event.ignore()
