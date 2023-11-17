from dicom.Series import Series


class Study:
    def __init__(self, study, study_name, dicom_path):
        self.series = {}
        self.study_name = study_name
        self.dicom_path = dicom_path

        MAX_FILE_NAME_LENGTH = 64
        for i in study.children:
            if i.DirectoryRecordType == "SERIES":
                series_name = str(i.SeriesNumber)
                if "SeriesDescription" in i:
                    series_name = "".join([c for c in i.SeriesDescription if c.isalnum()][:MAX_FILE_NAME_LENGTH])
                series_id = str(i.SeriesNumber)
                self.series[series_name] = Series(i, series_name, self.study_name, series_id, dicom_path)

    def get_series(self):
        return self.series

    def export_all(self):
        for s in self.series:
            s.export()
