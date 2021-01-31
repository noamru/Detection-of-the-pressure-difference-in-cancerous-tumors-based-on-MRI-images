import cv2
import numpy as np
import matplotlib.pyplot as plt


# check create outsider contour
def create_outsider_contour(contour, image):
    # reformat the contour
    cnt = np.array([[0] * 2])
    for i in range(len(contour[0])):
        # cnt.append([[contour[0][i][0], contour[1][i][0]]])
        cnt = np.append(cnt, [[contour[0][i][0], contour[1][i][0]]], axis=0)
    cnt = np.delete(cnt, 0, axis=0)  # delete the unnecessary 0 row

    # create mask of contour
    mask = np.zeros(image.shape, np.uint8)
    ctr = np.array(cnt).reshape((-1, 1, 2)).astype(np.int32)
    cv2.drawContours(mask, [ctr], 0, 255, -1)

    # create the outsider contour
    kernel = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], np.uint8)
    tmp1 = cv2.dilate(mask, kernel, iterations=5)
    tmp2 = cv2.dilate(mask, kernel, iterations=4)
    res = tmp1 - tmp2
    a = np.hstack((mask, res))
    cv2.imshow("mask", a)
    k = cv2.waitKey(0)

    # get the pixels numbers in the strip
    pixelpoints = cv2.findNonZero(res)
    # np.set_printoptions(threshold=np.inf)
    # print(pixelpoints)

    # create the outsider contour
    final_contour = [np.array([[0]], dtype=np.float32), np.array([[0]], dtype=np.float32)]
    for i in range(0, len(pixelpoints), 1):
        final_contour[0] = np.append(final_contour[0], [[pixelpoints[i][0][0]]], axis=0)
        final_contour[1] = np.append(final_contour[1], [[pixelpoints[i][0][1]]], axis=0)
    final_contour[0] = np.delete(final_contour[0], 0, axis=0)  # delete the unnecessary 0 row
    final_contour[1] = np.delete(final_contour[1], 0, axis=0)  # delete the unnecessary 0 row

    plt.title("original")
    plt.plot(contour[0], contour[1], color='b')
    plt.plot(final_contour[0], final_contour[1], color='r')
    plt.imshow(image, cmap=plt.cm.gray)
    plt.show()


# check create outsider contour
def scale_contour(contour, scale):
    cnt = np.array([[0]*2])
    for i in range(len(contour[0])):
        # cnt.append([[contour[0][i][0], contour[1][i][0]]])
        cnt = np.append(cnt, [[contour[0][i][0], contour[1][i][0]]], axis=0)
    cnt = np.delete(cnt, 0, axis=0)  # delete the unnecessary 0 row
    # print(cnt)
    # M = cv2.moments(cnt)
    # print(M)
    cx = np.mean(contour[0])
    cy = np.mean(contour[1])
    # print(cx)
    # print(cy)
    cnt_norm = cnt - [cx, cy]
    # print(cnt_norm)
    cnt_scaled = cnt_norm + 4 * np.sign(cnt_norm)
    cnt_scaled = cnt_scaled + [cx, cy]
    # print(cnt_scaled)
    # cnt_scaled = cnt_scaled.astype(np.int32)
    # print(cnt_scaled)
    final_contour = [np.array([[0]], dtype=np.float32), np.array([[0]], dtype=np.float32)]
    for i in range(len(cnt_scaled)):
        final_contour[0] = np.append(final_contour[0], [[cnt_scaled[i][0]]], axis=0)
        final_contour[1] = np.append(final_contour[1], [[cnt_scaled[i][1]]], axis=0)
    final_contour[0] = np.delete(final_contour[0], 0, axis=0)  # delete the unnecessary 0 row
    final_contour[1] = np.delete(final_contour[1], 0, axis=0)  # delete the unnecessary 0 row
    # print(final_contour)
    return final_contour
