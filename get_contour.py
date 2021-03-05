from pydicom import dcmread
import array
import matplotlib.pyplot as plt
import numpy as np


def read_curve_data(ds):
    k = 0

    while (0x5000 + (k * 2), 0x3000) in ds:
        curve_data_string = ds[0x5000 + (k * 2), 0x3000].value
        curve_data = np.array(array.array('f', curve_data_string))
        roi = curve_data
        x_data = roi[0::2]
        y_data = roi[1::2]
        k += 1

    return x_data, y_data


if __name__ == "__main__":
    ds1 = dcmread("P3/keyframe.dcm")
    ds2 = dcmread("P3/t2.dcm")
    x, y = read_curve_data(ds1)
    contour = [x, y]
    # print(contour)
    image = ds2.pixel_array
    plt.imshow(image, cmap=plt.cm.gray)
    plt.plot(contour[0], contour[1], color='b')
    plt.show()
