from tqdm import tqdm
try:
    from dicom.Study import Study
except ImportError:
    from Study import Study


class Patient:
    def __init__(self, patient, dicom_path):
        self.studies = {}
        self.dicom_path = dicom_path
        self.patient_id = patient.PatientID
        self.patient_name = patient.PatientName

        MAX_FILE_NAME_LENGTH = 64
        for i in patient.children:
            if i.DirectoryRecordType == "STUDY":
                study_name = "".join([c for c in i.StudyDescription if c.isalnum()][:MAX_FILE_NAME_LENGTH])

                self.studies[study_name] = Study(i, study_name, dicom_path)

    def get_studies(self):
        return self.studies

    def export_all(self):
        for s in tqdm(self.studies.values(), desc="Processing", ascii=False, ncols=75):
            s.export_all()
