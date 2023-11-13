import os

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QHBoxLayout, QWidget, QPushButton, QSizePolicy, QTreeView, \
    QAbstractItemView

from FakeDICOMGetter import FakeDICOMGetter
from ScrollBar import ScrollBar


class SeriesItem(QStandardItem):
    def __init__(self, file_path):
        super().__init__(os.path.basename(file_path))
        self.file_path = file_path
        self.file_name = os.path.basename(file_path)
class StudyNavigator(QFrame):
    def __init__(self, load_series_callback):
        super().__init__()
        self.setObjectName("StudyNavigator")
        self.load_series_callback = load_series_callback
        self.setStyleSheet("""
        QTreeView{
            font-size:12pt;
            color: white;
            border:none
        }
        
        QTreeView::branch:closed:has-children {
            image: url('icons/collapsed.svg'); /* Adjust with your SVG file path */
        }
        
        QTreeView::branch:open:has-children {
            image: url('icons/expanded.svg'); /* Adjust with your SVG file path */
        }
        
        /* Add rules for the last item if it does not have siblings */
        QTreeView::branch:closed:has-children:!has-siblings {
            image: url('icons/collapsed.svg'); /* Adjust with your SVG file path */
        }
        
        QTreeView::branch:open:has-children:!has-siblings {
            image: url('icons/expanded.svg'); /* Adjust with your SVG file path */
        }
        
        QLabel{
            font-size:12pt;
        }

        .StudyNavigator{
            border-top: 2px solid #7160E8;
            border-left: 1px solid #2e2e2e;
            border-bottom: 1px solid #2e2e2e;
            border-right: 1px solid #2e2e2e;        }
        """)

        self.layout_ = QVBoxLayout()
        self.layout_.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout_.setContentsMargins(4, 4, 4, 4)
        self.layout_.setSpacing(0)
        self.setLayout(self.layout_)

        self.title = QLabel("Studies")
        self.title.setContentsMargins(0,0,0,0)

        self.study_tree = QTreeView()
        self.scroll_bar = ScrollBar(Qt.Orientation.Vertical)
        self.study_tree.setVerticalScrollBar(self.scroll_bar)
        self.study_tree.clicked.connect(self.on_tree_clicked)
        self.study_tree.doubleClicked.connect(self.on_tree_double_clicked)
        self.model = QStandardItemModel()
        self.study_tree.setModel(self.model)
        self.study_tree.header().hide()
        self.study_tree.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

        self.layout_.addWidget(self.title)
        self.layout_.addWidget(self.study_tree)

    def on_tree_clicked(self, index):
        navigator_actions = self.parent().findChild(QFrame, "NavigatorActions")
        item = self.model.itemFromIndex(index)
        navigator_actions.set_load_button_enabled(not item.hasChildren())

    def on_tree_double_clicked(self, index):
        self.try_load_series(index)

    def try_load_series(self, index=None):
        if index is None:
            index = self.study_tree.selectionModel().selectedIndexes()[0]

        item = self.model.itemFromIndex(index)

        if item.hasChildren():
            self.study_tree.clearSelection()
            return

        navigator_actions = self.parent().findChild(QFrame, "NavigatorActions")
        navigator_actions.set_export_button_enabled(True)
        self.load_series_callback(item.file_path)

    def load_dicom(self, dicom_path):
        self.model.clear()
        dicom_getter = FakeDICOMGetter()
        studies = dicom_getter.get_studies(dicom_path)
        for study, all_series in studies.items():
            file_name = os.path.basename(study)
            parent = QStandardItem(file_name)
            parent.setFlags(parent.flags() & ~Qt.ItemFlag.ItemIsEditable)

            for series in all_series:
                series_path = os.path.join(study, series)
                child = SeriesItem(series_path)
                child.setFlags(parent.flags() & ~Qt.ItemFlag.ItemIsEditable)
                parent.appendRow(child)
            self.model.appendRow(parent)

    def select_item(self, study, series):
        item = self._findItemByText(self.study_tree.model(), study, series)
        if item is None:
            return

        self.study_tree.selectionModel().clearSelection()
        idx = self.model.indexFromItem(item)
        self.study_tree.selectionModel().select(idx, self.study_tree.selectionModel().SelectionFlag.Select)

    def _findItemByText(self, parent:QStandardItemModel, study, series) -> QStandardItem | None:
        for study_row in range(parent.rowCount()):
            study_item = parent.item(study_row)
            if study_item.text() != study:
                continue

            self.study_tree.expand(self.model.indexFromItem(study_item))
            for series_row in range(study_item.rowCount()):
                series_item = study_item.child(series_row)
                if not series_item:
                    continue

                if series_item.text() == series:
                    return series_item
        return None
