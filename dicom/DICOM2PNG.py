import os

from dicom.Patient import Patient
from pydicom import dcmread
from pydicom.data import get_testdata_file


def main():
    file_path = input("DICOMDIR full file path:").strip()
    if file_path == "test":
        file_path = get_testdata_file("DICOMDIR")
    patient = load(file_path)
    patient.export_all()
    print(f"Successfully saved to {os.getcwd()}")

def load(file_path):
    ds = dcmread(file_path)
    print(f"Successfully loaded DICOMDIR at {file_path}")
    if len(ds.patient_records) != 1:
        print("WARNING: Exactly only one patient is supported per dicom. Defaulting to first...")

    return Patient(ds.patient_records[0], file_path)




if __name__ == "__main__":
    main()
