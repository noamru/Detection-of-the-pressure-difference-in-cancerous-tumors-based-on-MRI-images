import scipy.io
import matplotlib.pyplot as plt
import os
import math
from pydicom import dcmread
from get_contour import read_curve_data


def read_and_cut_MRI_and_contour(patient, strip_thickness, tumorArea, rows_start, rows_end, columns_start, columns_end):
    # number of images
    files = os.listdir('patient/' + patient)
    number_of_images = len(files) - 1
    # print("number of images", number_of_images)

    """
    # cut images and contour manually
    if patient == "P2":
        tumor_rows_start = 200
        tumor_rows_end = 400
        tumor_columns_start = 50
        tumor_columns_end = 200
        contour[0] = [point - tumor_columns_start for point in contour[0]]
        contour[1] = [point - tumor_rows_start for point in contour[1]]
    if patient == "P3":
        tumor_rows_start = 250
        tumor_rows_end = 400
        tumor_columns_start = 290
        tumor_columns_end = 420
        contour[0] = [point - tumor_columns_start for point in contour[0]]
        contour[1] = [point - tumor_rows_start for point in contour[1]]
    if patient == "P4":
        tumor_rows_start = 220
        tumor_rows_end = 360
        tumor_columns_start = 310
        tumor_columns_end = 440
        contour[0] = [point - tumor_columns_start for point in contour[0]]
        contour[1] = [point - tumor_rows_start for point in contour[1]]
    if patient == "P5":
        tumor_rows_start = 270
        tumor_rows_end = 410
        tumor_columns_start = 290
        tumor_columns_end = 440
        contour[0] = [point - tumor_columns_start for point in contour[0]]
        contour[1] = [point - tumor_rows_start for point in contour[1]]
    if patient == "P7":
        tumor_rows_start = 240
        tumor_rows_end = 420
        tumor_columns_start = 40
        tumor_columns_end = 210
        contour[0] = [point - tumor_columns_start for point in contour[0]]
        contour[1] = [point - tumor_rows_start for point in contour[1]]
    if patient == "P8":
        tumor_rows_start = 130
        tumor_rows_end = 290
        tumor_columns_start = 100
        tumor_columns_end = 220
        contour[0] = [point - tumor_columns_start for point in contour[0]]
        contour[1] = [point - tumor_rows_start for point in contour[1]]
    """

    # read series of MRI pictures
    images = []
    for i in range(1, number_of_images):
        ds = dcmread('patient/' + patient + "/t" + str(i) + ".dcm")
        images.append(ds.pixel_array)

    fig = plt.figure()  # make a figure
    number_of_images_in_row = 3

    if tumorArea:  # cut the area with tumor from the images
        if strip_thickness == 0:
            fig.suptitle("patient " + patient + ", inside tumor", fontsize=16)
        else:
            fig.suptitle("patient " + patient + ", strip of " + str(strip_thickness) + " pixels", fontsize=16)

        # read and fit contour
        if os.path.isfile('patient/' + patient + '/contour.mat'):
            contour_mat = scipy.io.loadmat('patient/' + patient + '/contour.mat')
            contour = [contour_mat['roi'][::2], contour_mat['roi'][1::2]]
            contour[0] = [point[0] for point in contour[0]]
            contour[1] = [point[0] for point in contour[1]]
        else:
            keyframe = dcmread('patient/' + patient + "/keyframe.dcm")
            contour = read_curve_data(keyframe)
            contour[0] = [point for point in contour[0]]
            contour[1] = [point for point in contour[1]]
        # print(contour)

        # cut images and fit contour automatically according to the location of the contour
        tumor_rows_start = int(min(contour[1]) - 55)
        tumor_rows_end = int(max(contour[1]) + 55)
        tumor_columns_start = int(min(contour[0]) - 55)
        tumor_columns_end = int(max(contour[0]) + 55)
        contour[0] = [point - tumor_columns_start for point in contour[0]]
        contour[1] = [point - tumor_rows_start for point in contour[1]]

        for i in range(len(images)):
            images[i] = images[i][tumor_rows_start:tumor_rows_end, tumor_columns_start:tumor_columns_end]
            fig.add_subplot(math.ceil(number_of_images / number_of_images_in_row), number_of_images_in_row, i + 1)
            plt.title("t" + str(i + 1))
            plt.imshow(images[i], cmap=plt.cm.gray)
            plt.plot(contour[0], contour[1], color='b')

    else:  # cut the area without tumor from the images
        fig.suptitle("patient " + patient + ", area without tumor", fontsize=16)

        #  make a square contour in the middle of the image
        image_width = (columns_end - columns_start) / 2
        image_height = (rows_end - rows_start) / 2
        contour = [[], []]
        contour[0] = [image_width - 10, image_width + 10, image_width + 10, image_width - 10, image_width - 10]
        contour[1] = [image_height - 10, image_height - 10, image_height + 10, image_height + 10, image_height - 10]

        for i in range(len(images)):
            images[i] = images[i][rows_start:rows_end, columns_start:columns_end]
            fig.add_subplot(math.ceil(number_of_images / number_of_images_in_row), number_of_images_in_row, i + 1)
            plt.title("t" + str(i + 1))
            plt.imshow(images[i], cmap=plt.cm.gray)
            plt.plot(contour[0], contour[1], color='b')

    fig.tight_layout()
    plt.show()
    return images, contour, number_of_images
