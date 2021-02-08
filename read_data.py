from pydicom import dcmread
import scipy.io
import matplotlib.pyplot as plt


def read_and_cut_MRI_and_contour(cancerArea):
    # read and fit contour
    contour_mat = scipy.io.loadmat('contour.mat')
    contour = [contour_mat['roi'][::2], contour_mat['roi'][1::2]]
    print(contour)
    contour[0] = contour[0] - 50
    contour[1] = contour[1] - 200

    # read series of MRI pictures
    images = []
    for i in range(1, 6):
        ds = dcmread("t" + str(i) + ".dcm")
        images.append(ds.pixel_array)

    # fig = plt.figure()  # make a figure
    if cancerArea:
        # cut the area with cancer from the images
        for i in range(len(images)):
            images[i] = images[i][200:400, 50:200]
            # fig.add_subplot(2, 3, i+1)
            # plt.imshow(images[i], cmap=plt.cm.gray)
            # plt.plot(contour[0],contour[1], color='b')
    else:
        # cut the area without cancer from the images
        for i in range(len(images)):
            images[i] = images[i][200:400, 290:440]
            # fig.add_subplot(2, 3, i + 1)
            # plt.imshow(images[i], cmap=plt.cm.gray)
            # plt.plot(contour[0], contour[1], color='b')

    # fig.tight_layout()
    # plt.show()
    return images, contour
