import os
import scipy.io
import pandas as pd
import numpy as np
from openpyxl import load_workbook

from algorithm import algorithm

if __name__ == "__main__":
    # read patients list
    # patlist = scipy.io.loadmat('patlist_check.mat')
    # print(patlist['mri_data'])

    """run algorithm for all patients and save the results in patient_res file"""

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

    """make analysis on the results in patient_res file"""

    """calculate for each kind of strip (3,5,7,9) the average and std of the incline from LinearRegression
       for the groups:
         1. patients that the pathological response was successful.
         2. patients that the pathological response was unsuccessful.
         3. patients that the radiological response was successful.
         4. patients that the radiological response was unsuccessful.
       and save the results in patient_res file"""

    # open patient_res file for write in
    # patlist_wb = load_workbook("patient_res.xlsx")
    # patlist_data_sheet = patlist_wb["Data"]
    write_column = 12

    # read patient_res file for calculations
    patient_res = pd.read_excel("patient_res.xlsx", sheet_name="Data")
    # print(patient_info)

    for column in range(4, 8):  # run on all strips
        strip = patient_res.columns[column]

        pathological_successful_treatment_inclines = []
        pathological_unsuccessful_treatment_inclines = []
        radiological_successful_treatment_inclines = []
        radiological_unsuccessful_treatment_inclines = []
    
        for patient in range(len(patient_res)):
            if patient_res.at[patient, "pathological response"] == 0 or patient_res.at[patient, "pathological response"] == 1:
                pathological_successful_treatment_inclines.append(patient_res.at[patient, strip])
            elif patient_res.at[patient, "pathological response"] == 2:
                pathological_unsuccessful_treatment_inclines.append(patient_res.at[patient, strip])
    
            if patient_res.at[patient, "radiological response"] == 0 or patient_res.at[patient, "radiological response"] == 1:
                radiological_successful_treatment_inclines.append(patient_res.at[patient, strip])
            elif patient_res.at[patient, "radiological response"] == 2:
                radiological_unsuccessful_treatment_inclines.append(patient_res.at[patient, strip])

        print(strip, ": ")
        print(pathological_successful_treatment_inclines, pathological_unsuccessful_treatment_inclines)
        print(radiological_successful_treatment_inclines, radiological_unsuccessful_treatment_inclines)

        # write in pathological response - successful treatment
        patlist_data_sheet.cell(6, write_column).value = np.mean(pathological_successful_treatment_inclines, axis=0)
        patlist_data_sheet.cell(7, write_column).value = np.std(pathological_successful_treatment_inclines, axis=0)  # ddof= 1
        write_column += 1

        # write in pathological response - unsuccessful treatment
        patlist_data_sheet.cell(6, write_column).value = np.mean(pathological_unsuccessful_treatment_inclines, axis=0)
        patlist_data_sheet.cell(7, write_column).value = np.std(pathological_unsuccessful_treatment_inclines, axis=0)
        write_column += 1

        # write in radiological response - successful treatment
        patlist_data_sheet.cell(6, write_column).value = np.mean(radiological_successful_treatment_inclines, axis=0)
        patlist_data_sheet.cell(7, write_column).value = np.std(radiological_successful_treatment_inclines, axis=0)
        write_column += 1

        # write in radiological response - unsuccessful treatment
        patlist_data_sheet.cell(6, write_column).value = np.mean(radiological_unsuccessful_treatment_inclines, axis=0)
        patlist_data_sheet.cell(7, write_column).value = np.std(radiological_unsuccessful_treatment_inclines, axis=0)
        write_column += 1

    patlist_wb.save("patient_res.xlsx")
