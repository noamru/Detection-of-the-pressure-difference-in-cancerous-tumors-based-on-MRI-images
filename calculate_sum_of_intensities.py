import cv2
import numpy as np


# calculate sum of pixels intensities in strip in one image
def calculate_sum_of_intensities_inside_strip(contour, image, image_index, strip_thickness):
    # reformat the contour
    cnt = np.array([[0] * 2])
    for i in range(len(contour[0])):
        # cnt.append([[contour[0][i][0], contour[1][i][0]]])
        cnt = np.append(cnt, [[contour[0][i], contour[1][i]]], axis=0)
    cnt = np.delete(cnt, 0, axis=0)  # delete the unnecessary 0 row

    # create mask of contour
    mask = np.zeros(image.shape, np.uint8)
    ctr = np.array(cnt).reshape((-1, 1, 2)).astype(np.int32)
    cv2.drawContours(mask, [ctr], 0, 255, -1)

    # check if the requested sum is inside the contour or inside a strip
    if strip_thickness == 0:
        strip = mask
    else:
        # create the strip around the contour
        kernel = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], np.uint8)
        dilate_mask = cv2.dilate(mask, kernel, iterations=strip_thickness)
        strip = dilate_mask - mask
    # a = np.hstack((mask, strip))
    # cv2.imshow("mask", a)
    # k = cv2.waitKey(0)

    # get the pixels numbers in the strip
    pixelpoints = cv2.findNonZero(strip)
    # np.set_printoptions(threshold=np.inf)
    # print(pixelpoints)

    # sum the intensities of the pixels in the strip
    intensities_sum = 0
    for i in range(len(pixelpoints)):
        intensities_sum += image[pixelpoints[i][0][1], pixelpoints[i][0][0]]

    # normalization
    intensities_sum /= len(pixelpoints)

    # print("intensity between contours in image " + str(image_index) + ": " + str(intensities_sum))
    return intensities_sum


# calculate pixels intensities inside mask
def calculate_sum_of_intensities_inside_mask(image, image_index):
    # create mask
    mask = np.zeros(image.shape, np.uint8)
    mask[50:60, 100:110] = 255
    # a = np.hstack((mask, np.uint8(image)))
    # cv2.imshow("mask", a)
    # k = cv2.waitKey(0)

    # get the pixels numbers in the mask
    pixelpoints = cv2.findNonZero(mask)

    # sum the intensities of the pixels in the strip
    intensities_sum = 0
    for i in range(len(pixelpoints)):
        intensities_sum += image[pixelpoints[i][0][0], pixelpoints[i][0][1]]

    # normalization
    intensities_sum /= len(pixelpoints)

    print("intensity in mask in image " + str(image_index) + ": " + str(intensities_sum))
    return intensities_sum
