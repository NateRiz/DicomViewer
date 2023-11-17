import os

from PyQt6.QtWidgets import QFileDialog, QFrame


class ImageExporter(QFrame):
    def __init__(self, parent):
        super().__init__(parent=parent)

    def save_studies(self, study_paths):
        save_directory = QFileDialog.getExistingDirectory(self, "Select a Directory",
                                                          options=QFileDialog.Option.ShowDirsOnly)
        if not os.path.isdir(save_directory):
            return

        for study_path in study_paths:
            self._save_study(study_path, save_directory)

    def _save_study(self, study, save_directory):
        dicom_adapter = self.window().findChild(QFrame, "MainWidget").dicom_adapter

        for series in dicom_adapter.get_series_list(study):
            sub_save_directory = os.path.join(save_directory, study, series)
            os.makedirs(sub_save_directory, exist_ok=True)
            self._save_series(study, series, save_directory)

    def save_series(self, study, series):
        save_directory = QFileDialog.getExistingDirectory(self, "Select a Directory",
                                                          options=QFileDialog.Option.ShowDirsOnly)
        if not os.path.isdir(save_directory):
            return

        self._save_series(study, series, save_directory)

    def _save_series(self, study, series, save_directory):
        dicom_adapter = self.window().findChild(QFrame, "MainWidget").dicom_adapter
        images = dicom_adapter.load_images_from_series(study, series)

        file_names = []
        sub_save_directory = os.path.join(save_directory, study, series)
        os.makedirs(sub_save_directory, exist_ok=True)
        for file_name, pixmap in images.items():
            file_path = os.path.join(sub_save_directory, f'{file_name}.png')
            file_names.append(file_path)
            pixmap.save(file_path, "PNG")
