from pydicom import dcmread
import scipy.io
import matplotlib.pyplot as plt
import os
from get_contour import read_curve_data


def read_and_cut_MRI_and_contour(patient, cancerArea):
    # number of images
    files = os.listdir('patient/'+patient)
    number_of_images = len(files) - 1
    # print("number of images", number_of_images)

    # read and fit contour
    if os.path.isfile('patient/'+patient+'/contour.mat'):
        contour_mat = scipy.io.loadmat('patient/'+patient+'/contour.mat')
        contour = [contour_mat['roi'][::2], contour_mat['roi'][1::2]]
        contour[0] = [point[0] for point in contour[0]]
        contour[1] = [point[0] for point in contour[1]]
    else:
        keyframe = dcmread('patient/'+patient + "/keyframe.dcm")
        contour = read_curve_data(keyframe)
        contour[0] = [point for point in contour[0]]
        contour[1] = [point for point in contour[1]]
    # print(contour)

    # cut images and contour automatically
    # """
    rows_start = int(min(contour[1])-55)
    rows_end = int(max(contour[1])+55)
    columns_start = int(min(contour[0])-55)
    columns_end = int(max(contour[0])+55)
    contour[0] = [point - columns_start for point in contour[0]]
    contour[1] = [point - rows_start for point in contour[1]]
    # print(rows_start, rows_end, columns_start, columns_end)

    """
    # cut images and contour manually
    if patient == "P2":
        rows_start = 200
        rows_end = 400
        columns_start = 50
        columns_end = 200
        contour[0] = [point - columns_start for point in contour[0]]
        contour[1] = [point - rows_start for point in contour[1]]
    if patient == "P3":
        rows_start = 250
        rows_end = 400
        columns_start = 290
        columns_end = 420
        contour[0] = [point - columns_start for point in contour[0]]
        contour[1] = [point - rows_start for point in contour[1]]
    if patient == "P4":
        rows_start = 220
        rows_end = 360
        columns_start = 310
        columns_end = 440
        contour[0] = [point - columns_start for point in contour[0]]
        contour[1] = [point - rows_start for point in contour[1]]
    if patient == "P5":
        rows_start = 270
        rows_end = 410
        columns_start = 290
        columns_end = 440
        contour[0] = [point - columns_start for point in contour[0]]
        contour[1] = [point - rows_start for point in contour[1]]
    if patient == "P7":
        rows_start = 240
        rows_end = 420
        columns_start = 40
        columns_end = 210
        contour[0] = [point - columns_start for point in contour[0]]
        contour[1] = [point - rows_start for point in contour[1]]
    if patient == "P8":
        rows_start = 130
        rows_end = 290
        columns_start = 100
        columns_end = 220
        contour[0] = [point - columns_start for point in contour[0]]
        contour[1] = [point - rows_start for point in contour[1]]
    """

    # read series of MRI pictures
    images = []
    for i in range(1, number_of_images):
        ds = dcmread('patient/'+patient+"/t" + str(i) + ".dcm")
        images.append(ds.pixel_array)

    """
        for subdir, dirs, files in os.walk(patient):
        for file in files:
            if file != "contour.mat" and file != "keyframe.dcm":
                ds = dcmread(patient+"/"+file)  # dcmread(patient+"/t" + str(i) + ".dcm")
                images.append(ds.pixel_array)
    """

    fig = plt.figure()  # make a figure
    if cancerArea:
        # cut the area with cancer from the images
        for i in range(len(images)):
            images[i] = images[i][rows_start:rows_end, columns_start:columns_end]
            fig.add_subplot(2, 3, i+1)
            plt.imshow(images[i], cmap=plt.cm.gray)
            plt.plot(contour[0],contour[1], color='b')
    else:
        # cut the area without cancer from the images (for now only for P2 and P3)
        for i in range(len(images)):
            images[i] = images[i][200:400, 290:440]  # 250:400, 50:200
            fig.add_subplot(2, 3, i + 1)
            plt.imshow(images[i], cmap=plt.cm.gray)
            plt.plot(contour[0], contour[1], color='b')

    fig.tight_layout()
    plt.show()
    return images, contour, number_of_images
