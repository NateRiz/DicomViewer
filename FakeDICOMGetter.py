import os

class FakeDICOMGetter:
    def __init__(self):
        pass

    def get_studies(self, dicom_path):
        dir_name = os.path.dirname(dicom_path)
        entries = os.listdir(dir_name)
        studies = {}
        for entry in entries:
            path = os.path.join(dir_name, entry)
            if not os.path.isdir(path):
                continue

            for series in os.listdir(path):
                series_path = os.path.join(path, series)
                if not os.path.isdir(series_path):
                    continue

                if path not in studies:
                    studies[path]=[]

                studies[path].append(series)

        return studies
