import matplotlib.pyplot as plt
import numpy as np

from read_data import read_and_cut_MRI_and_contour
from Registration import registration
from calculate_sum_of_intensities import (calculate_sum_of_intensities_inside_strip,
                                          calculate_sum_of_intensities_inside_mask)
from LinearRegression import LinearRegression_func


def algorithm(patient, strip_thickness, tumorArea=True, rows_start=None, rows_end=None, columns_start=None,
              columns_end=None):
    if not tumorArea:
        print("\npatient " + patient + ", area without tumor:")
    elif strip_thickness == 0:
        print("\npatient " + patient + ", inside tumor:")
    else:
        print("\npatient " + patient + ", strip of " + str(strip_thickness) + " pixels:")

    # Open the image files
    images, contour, number_of_images = read_and_cut_MRI_and_contour(patient=patient, strip_thickness=strip_thickness,
                                                                     tumorArea=tumorArea, rows_start=rows_start,
                                                                     rows_end=rows_end, columns_start=columns_start,
                                                                     columns_end=columns_end)
    # print(contour)

    # """
    # registration
    registrate_images = []
    for i in range(len(images)):
        if i == 1:  # the reference image
            registrate_images.append(images[i])
        else:
            registrate_image = (registration(images[i], images[1], contour, ransacReprojThreshold=4, debug=False))
            registrate_images.append(registrate_image)
    # """

    """
    # check intensity decrease after registration
    x = sum(sum(images[3][10:120,10:120]))
    y = sum(sum(registrate_images[3][10:120,10:120]))
    print(x)
    print(y)
    """

    # calculate sum of pixels intensities in strip, or in the contour by pass 0 in strip_thickness
    intensities_sums = []
    for i in range(len(registrate_images)):
        intensities_sums.append(calculate_sum_of_intensities_inside_strip(contour, registrate_images[i], i + 1,
                                                                          strip_thickness=strip_thickness))
    # print(intensities_sums)

    # calculate changes in intensity between images
    intensities_changes = []
    for i in range(1, len(intensities_sums)):
        intensities_changes.append(intensities_sums[i] - intensities_sums[0])
        # print("change in intensity between image 1 to image " + str(i+1) + ": " + str(intensities_sums[i] - intensities_sums[0]))

    # LinearRegression
    coef, score = LinearRegression_func(np.arange(2, number_of_images), intensities_changes)
    # LinearRegression_func(np.arange(2, number_of_images), np.log(intensities_changes))  # Linear Regression to ln of res

    # show plot of the changes in intensity between images
    plt.plot(range(2, number_of_images), intensities_changes, 'ro')
    plt.xticks(range(2, number_of_images))  # set the x-labels to integers

    if not tumorArea:
        plt.title("increasing of intensity per pixel compared to the first image.\narea without tumor."
                  "\npressure estimate: " + str(round(coef, 3)) + ", success rates: " + str(
            round(score, 3) * 100) + "%")
    elif strip_thickness == 0:
        plt.title("increasing of intensity per pixel compared to the first image.\narea with tumor, inside tumor."
                  "\npressure estimate: " + str(round(coef, 3)) + ", success rates: " + str(
            round(score, 3) * 100) + "%")
    else:
        plt.title("increasing of intensity per pixel compared to the first image.\narea with tumor, inside strip of " +
                  str(strip_thickness) + " pixels.\npressure estimate: " + str(
                   round(coef, 3)) + ", success rates: " + str(round(score, 3) * 100) + "%")
    plt.xlabel("image number")
    plt.ylabel("intensity increase")
    plt.show()

    return round(coef, 3)

    """
    # calculate pixels intensities outside
    intensities_sums = []
    for i in range(len(registrate_images)):
        intensities_sums.append(calculate_sum_of_intensities_inside_mask(registrate_images[i], i + 1))

    # calculate changes in intensity between images
    for i in range(1, len(intensities_sums)):
        print("change in intensity between image 1 to image " + str(i + 1) + ": " + str(intensities_sums[i] - intensities_sums[0]))
    """
