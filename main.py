import os
import scipy.io

from algorithm import algorithm


if __name__ == "__main__":
    # read patients list
    # patlist = scipy.io.loadmat('patlist_check.mat')
    # print(patlist['mri_data'])

    for dir in os.listdir("patient"):

        algorithm(patient=dir, strip_thickness=0)  # inside tumor
        for strip in range(3, 10, 2):
            algorithm(patient=dir, strip_thickness=strip)
