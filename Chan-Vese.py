import matplotlib.pyplot as plt
from skimage import data, img_as_float
from skimage.segmentation import (chan_vese, checkerboard_level_set, disk_level_set)
import cv2
import numpy as np
import random

if __name__ == "__main__":
    image = cv2.imread("cloud2.png", 0)
    # """
    contour = np.zeros(image.shape)
    # cv2.rectangle(contour, (325, 40), (780, 350), (255, 255, 255), -1)  # create white rectangle in the image
    # contour = cv2.circle(contour, (552,195), 240, color=(255,255,255), thickness=-1)
    contour = cv2.ellipse(contour, (552, 195), (300, 200), 0.0, 0.0, 360.0, color=(255, 255, 255), thickness=1)
    cv2.imshow("a", contour)
    k = cv2.waitKey()
    # """

    """
    contour = np.zeros(image.shape)
    contour[50:350, 250:800] = 1
    cv2.imshow("b", contour)
    k = cv2.waitKey()
    """

    """
    # init_ls = disk_level_set(image.shape, radius=230)
    init_ls = checkerboard_level_set(image.shape, 6)
    print(init_ls)
    cv2.imshow("c", init_ls)
    k = cv2.waitKey()
    """

    # Feel free to play around with the parameters to see how they impact the result
    cv = chan_vese(image, mu=0.05, lambda1=1, lambda2=1, tol=1e-3, max_iter=200,
                   dt=0.5, init_level_set=contour, extended_output=True)

    fig, axes = plt.subplots(2, 2, figsize=(8, 8))
    ax = axes.flatten()

    ax[0].imshow(image, cmap="gray")
    ax[0].set_axis_off()
    ax[0].set_title("Original Image", fontsize=12)

    ax[1].imshow(cv[0], cmap="gray")
    ax[1].set_axis_off()
    title = "Chan-Vese segmentation - {} iterations".format(len(cv[2]))
    ax[1].set_title(title, fontsize=12)

    ax[2].imshow(cv[1], cmap="gray")
    ax[2].set_axis_off()
    ax[2].set_title("Final Level Set", fontsize=12)
    ax[2].contour(contour, [0.5], colors='r')

    # ret, thresh = cv2.threshold(cv[1], 127, 255, 0)
    # im2, contours, hierarchy = cv2.findContours(thresh, cv2.CV_RETR_FLOODFILL, cv2.CHAIN_APPROX_SIMPLE)
    # cv.drawContours(im2, contours, -1, (0, 255, 0), 3)


    ax[3].plot(cv[2])
    ax[3].set_title("Evolution of energy over iterations", fontsize=12)

    fig.tight_layout()
    plt.show()
