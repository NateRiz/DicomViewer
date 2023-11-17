from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor, QFontMetrics
from PyQt6.QtWidgets import  QVBoxLayout, QLabel, QFrame, QHBoxLayout, QLineEdit, QSizePolicy

class ReadOnlyQLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setReadOnly(True)
        self.setCursor(QCursor(Qt.CursorShape.IBeamCursor))

class Metadata(QFrame):
    def __init__(self):
        super().__init__()
        self.layout_ = QVBoxLayout()
        self.layout_.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout_.setContentsMargins(4, 4, 4, 4)
        self.layout_.setSpacing(0)
        self.setLayout(self.layout_)

        self.setStyleSheet("""
        QLabel{
            font-size:12pt;
        }
        QLineEdit{
            color:white;
            font-size:12pt;
            border:None;
        }
        .Metadata{
            border-top: 2px solid #7160E8;
            border-left: 1px solid #2e2e2e;
            border-bottom: 1px solid #2e2e2e;
            border-right: 1px solid #2e2e2e;
        }
        """)

        self.title = QLabel("Patient")
        self.title.setContentsMargins(0,0,0,16)
        self.layout_.addWidget(self.title)
        self.patient_name = self.add_row("Name", "")
        self.patient_id = self.add_row("ID", "")
        # self.patient_dob = self.add_row("DOB", "")
        self.set_patient_information("N/A", "-1", "00-00-0000")

    def add_row(self, key, val):
        frame = QFrame()
        h_layout = QHBoxLayout()
        h_layout.setContentsMargins(16,0,0,4)
        frame.setLayout(h_layout)

        key_label = QLabel(key)
        key_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        h_layout.addWidget(key_label)

        val_line_edit = ReadOnlyQLineEdit(val)
        val_line_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        h_layout.addWidget(val_line_edit)

        self.layout_.addWidget(frame)
        return val_line_edit

    def set_patient_information(self, name, id_, dob):
        self.patient_name.setText(name)
        self.patient_id.setText(id_)
        # self.patient_dob.setText(dob)
        longest_text = sorted([name, id_, dob],key=lambda n:len(n), reverse=True)[0]
        font_metrics = QFontMetrics(self.patient_name.font())
        text_width = font_metrics.horizontalAdvance(longest_text) + 32
        self.patient_name.setMinimumWidth(text_width)
        self.patient_id.setMinimumWidth(text_width)
        # self.patient_dob.setMinimumWidth(text_width)
