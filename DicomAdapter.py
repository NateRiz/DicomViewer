import os.path

from PyQt6.QtGui import QImage, QPixmap

from dicom import DICOM2PNG
from dicom.Patient import Patient


class DicomAdapter:
    def __init__(self, dicom_path):
        self.patient: Patient = DICOM2PNG.load(dicom_path)

    def get_patient_metadata(self):
        return str(self.patient.patient_name).replace("^", " "), str(self.patient.patient_id)

    def get_studies(self):
        return list(self.patient.studies.keys())

    def get_series_list(self, study):
        return self.patient.studies[study].series.keys()

    def load_images_from_series(self, study, series_name):
        series = self.patient.studies[study].series[series_name]
        return {filename: self.pil_to_pixmap(p) for filename, p in series.load_all_images().items()}

    def load_series_preview_image(self, study, series_name):
        series = self.patient.studies[study].series[series_name]
        pil_img = series.load_first_image()
        return self.pil_to_pixmap(pil_img)

    def pil_to_pixmap(self, pil_image):
        try:
            if pil_image.mode != 'RGBA':
                pil_image = pil_image.convert('RGBA')
            data = pil_image.tobytes("raw", "BGRA")
            q_image = QImage(data, pil_image.width, pil_image.height, QImage.Format.Format_ARGB32)
            pixmap = QPixmap.fromImage(q_image)
            return pixmap
        except Exception as e:
            print(f"Failed to load image: {e}")
        return QPixmap()
