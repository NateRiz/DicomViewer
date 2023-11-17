import os
from os import path, mkdir
from dicom import pydicom_PIL
from pydicom import dcmread
from dicom.html_exporter import HTMLExporter


class Series:
    def __init__(self, series, series_name, study_name, series_id, dicom_path):
        self.series_id = series_id
        self.study_name = study_name
        self.series_name = series_name
        self.images = {}
        self.metadata = [i for i in series.children if i.DirectoryRecordType == "IMAGE"]
        self.file_paths = {}
        for i in self.metadata:
            idx = str(i["InstanceNumber"].value)
            data_elem = i["ReferencedFileID"]
            file_path = path.join(path.dirname(dicom_path), *data_elem.value)
            self.file_paths[idx] = file_path

    def load_all_images(self) -> dict:
        for idx, fp in self.file_paths.items():
            try:
                file_name = F"{idx.zfill(6)}{path.basename(fp)}"
                if file_name not in self.images:
                    self.images[file_name] = self._open_dicom(fp)
            except Exception as e:
                print(f"could not open file:{fp}\n{e}")

        return self.images

    def load_first_image(self):
        for _, fp in self.file_paths.items():
            try:
                return self._open_dicom(fp)
            except Exception as e:
                print(f"could not open file:{fp}\n{e}")

        return self.images

    def export(self):
        self.load_all_images()

        save_path = path.join(os.getcwd(), "ExportedPNGs", self.study_name, self.series_name)
        os.makedirs(save_path, exist_ok=True)
        for fp, img in self.images.items():
            img_path = path.join(save_path, f"{fp}.png")
            img.save(img_path, "PNG")

        html_exporter = HTMLExporter()
        html_exporter.export(save_path, self.series_id)

    def get_images(self):
        return self.images

    def _open_dicom(self, file_path):
        ds = dcmread(file_path)
        return pydicom_PIL.get_PIL_image(ds)
