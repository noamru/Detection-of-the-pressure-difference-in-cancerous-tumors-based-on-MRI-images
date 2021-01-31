import numpy as np
import matplotlib.pyplot as plt


from read_data import read_and_cut_MRI_and_contour
from Registration import registration
from calculate_sum_of_intensities import (calculate_sum_of_intensities_inside_strip,
                                          calculate_sum_of_intensities_inside_mask)


if __name__ == "__main__":
    # read patients list
    # patlist = scipy.io.loadmat('patlist_check.mat')
    # print(patlist['mri_data'])

    # Open the image files
    images, contour = read_and_cut_MRI_and_contour(cancerArea=True)

    # registration
    registrate_images = []
    for i in range(len(images)):
        if i == 1:  # the reference image
            registrate_images.append(images[i])
        else:
            registrate_image = (registration(images[i], images[1], ransacReprojThreshold=3, debug=False))
            registrate_images.append(registrate_image)
    
    """
    # check intensity decrease after registration
    x = sum(sum(images[3][10:120,10:120]))
    y = sum(sum(registrate_images[3][10:120,10:120]))
    print(x)
    print(y)
    """

    # calculate sum of pixels intensities in strip
    intensities_sums = []
    for i in range(len(registrate_images)):
        intensities_sums.append(calculate_sum_of_intensities_inside_strip(contour, registrate_images[i], i+1, strip_thickness=9))

    # calculate changes in intensity between images
    intensities_changes = []
    for i in range(1, len(intensities_sums)):
        intensities_changes.append(intensities_sums[i] - intensities_sums[0])
        print("change in intensity between image 1 to image " + str(i+1) + ": " + str(intensities_sums[i] - intensities_sums[0]))

    # show plot of the changes in intensity between images
    plt.plot(range(2, 6), intensities_changes, color='r')
    plt.xticks(range(2, 6))  # set the x-labels to integers
    plt.title("increasing of intensity per pixel compared to the first image.\narea with cancer")
    plt.xlabel("image number")
    plt.ylabel("intensity increase")
    plt.show()

    """
    # calculate pixels intensities outside
    intensities_sums = []
    for i in range(len(registrate_images)):
        intensities_sums.append(calculate_sum_of_intensities_inside_mask(registrate_images[i], i + 1))

    # calculate changes in intensity between images
    for i in range(1, len(intensities_sums)):
        print("change in intensity between image 1 to image " + str(i + 1) + ": " + str(intensities_sums[i] - intensities_sums[0]))
    """
