import os
import scipy.io
import pandas as pd
from openpyxl import load_workbook

from algorithm import algorithm

if __name__ == "__main__":
    # read patients list
    # patlist = scipy.io.loadmat('patlist_check.mat')
    # print(patlist['mri_data'])

    # open patient_res file
    patlist_wb = load_workbook("patient_res.xlsx")
    patlist_data_sheet = patlist_wb["Data"]
    row = 2

    # read patient_info file
    patient_info = pd.read_excel("patient_info.xlsx", sheet_name="Data", index_col="patient")
    # print(patient_info)

    for dir in os.listdir("patient"):
        patient_data = [dir, patient_info.at[dir, 'pathological response'],
                        patient_info.at[dir, 'radiological response']]

        # incline inside the tumor
        patient_data.append(algorithm(patient=dir, strip_thickness=0))

        # incline inside strips around the tumor
        for strip in range(3, 10, 2):
            patient_data.append(algorithm(patient=dir, strip_thickness=strip))

        # incline in area without tumor
        patient_data.append(algorithm(patient=dir, strip_thickness=0, tumorArea=False,
                                      rows_start=patient_info.at[dir, 'rows start'],
                                      rows_end=patient_info.at[dir, 'rows end'],
                                      columns_start=patient_info.at[dir, 'columns start'],
                                      columns_end=patient_info.at[dir, 'columns end']))

        print(patient_data)
        for i in range(len(patient_data)):
            patlist_data_sheet.cell(row, i + 1).value = patient_data[i]
        row += 1

    patlist_wb.save("patient_res.xlsx")
