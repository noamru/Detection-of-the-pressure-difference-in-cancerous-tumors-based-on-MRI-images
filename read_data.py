from pydicom import dcmread
import scipy.io
import matplotlib.pyplot as plt
import os
from get_contour import read_curve_data


def read_and_cut_MRI_and_contour(patient, cancerArea):
    # number of images
    files = os.listdir(patient)
    # print(files)
    number_of_images = len(files) - 1
    # print("number of images", number_of_images)

    # read and fit contour
    if os.path.isfile(patient+'/contour.mat'):
        contour_mat = scipy.io.loadmat(patient+'/contour.mat')
        contour = [contour_mat['roi'][::2], contour_mat['roi'][1::2]]
        contour[0] = [point[0] for point in contour[0]]
        contour[1] = [point[0] for point in contour[1]]
    else:
        keyframe = dcmread(patient + "/keyframe.dcm")
        contour = read_curve_data(keyframe)
        contour[0] = [point for point in contour[0]]
        contour[1] = [point for point in contour[1]]
    # print(contour)

    # cut images and contour
    if patient == "P2":
        contour[0] = [point-50 for point in contour[0]]  # contour[0] - 50
        contour[1] = [point-200 for point in contour[1]]  # contour[1] - 200
        rows_start = 200
        rows_end = 400
        columns_start = 50
        columns_end = 200
    if patient == "P3":
        contour[0] = [point-290 for point in contour[0]]  # contour[0] - 290
        contour[1] = [point-250 for point in contour[1]]  # contour[1] - 250
        rows_start = 250
        rows_end = 400
        columns_start = 290
        columns_end = 420

    # read series of MRI pictures
    images = []
    for i in range(1, number_of_images):
        ds = dcmread(patient+"/t" + str(i) + ".dcm")
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
        # cut the area without cancer from the images (fot now only for P2)
        for i in range(len(images)):
            images[i] = images[i][200:400, 290:440]
            # fig.add_subplot(2, 3, i + 1)
            # plt.imshow(images[i], cmap=plt.cm.gray)
            # plt.plot(contour[0], contour[1], color='b')

    fig.tight_layout()
    plt.show()
    return images, contour, number_of_images
