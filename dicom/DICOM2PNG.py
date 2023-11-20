import os

from pydicom import dcmread
from pydicom.data import get_testdata_file

try:
    from dicom.Patient import Patient
    from dicom.Series import Series
except ImportError:
    from Patient import Patient
    from Series import Series

def main():
    file_path = input("DICOMDIR full file path:").strip()
    if file_path == "test":
        file_path = get_testdata_file("DICOMDIR")
    if file_path == "testdcm":
        _load_test_dcm(get_testdata_file("rtplan.dcm"))
        return
    patient = load(file_path)
    patient.export_all()
    print(f"Successfully saved to {os.getcwd()}")

def load(file_path):
    ds = dcmread(file_path)
    print(f"Successfully loaded DICOMDIR at {file_path}")
    if len(ds.patient_records) != 1:
        print("WARNING: Exactly only one patient is supported per dicom. Defaulting to first...")

    return Patient(ds.patient_records[0], file_path)

def _load_test_dcm(file_path):
    ds = dcmread(file_path)
    MAX_FILE_NAME_LENGTH = 64
    series_name = str(ds.SeriesNumber)
    if "SeriesDescription" in ds:
        series_name = "".join([c for c in ds.SeriesDescription if c.isalnum()][:MAX_FILE_NAME_LENGTH])
    series_id = str(ds.SeriesNumber)
    series = Series(ds, series_name, "", series_id, file_path)
    series.export()



if __name__ == "__main__":
    main()
