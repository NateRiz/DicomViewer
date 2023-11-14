import os

from PyQt6.QtWidgets import QFileDialog, QFrame

from ImageLoader import ImageLoader


class ImageExporter(QFrame):
    def __init__(self):
        super().__init__()

    def save_series(self, path):
        directory = QFileDialog.getExistingDirectory(self, "Select a Directory", options=QFileDialog.Option.ShowDirsOnly)
        if not os.path.isdir(directory):
            return

        image_loader = ImageLoader()
        images = image_loader.load_from_series(path)
        study = os.path.basename(os.path.dirname(path))
        file_names = []
        for file_name, pixmap in images.items():
            file_path = os.path.join(directory, f'{study}_{file_name}')
            file_names.append(file_path)
            pixmap.save(file_path, "PNG")

        self.save_html(directory, file_names)
    def save_html(self, directory, file_names):
        file_path = os.path.join(directory, "series.html")
        with open(file_path, "w") as file:
            [file.write(F"<imgtag>{f}</imgtag>\n") for f in file_names]
