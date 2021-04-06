import cv2
import numpy as np
import imutils
import matplotlib.pyplot as plt


def registration(image, reference_image, contour, ransacReprojThreshold, debug=False):
    height, width = reference_image.shape

    # make black and white image for more accurate registration
    ret, threshold_image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)
    ret, threshold_reference_image = cv2.threshold(reference_image, 128, 255, cv2.THRESH_BINARY)
    # cv2.imshow("threshold", np.hstack((np.uint8(threshold_image), np.uint8(image))))
    # cv2.waitKey()

    # Create ORB detector with 1000 features.
    orb_detector = cv2.ORB_create(1000)

    # Find keypoints and descriptors.
    # The first arg is the image, second arg is the mask
    #  (which is not reqiured in this case).
    kp1, d1 = orb_detector.detectAndCompute(np.uint8(threshold_image), None)
    kp2, d2 = orb_detector.detectAndCompute(np.uint8(threshold_reference_image), None)

    # Match features between the two images.
    # We create a Brute Force matcher with
    # Hamming distance as measurement mode.
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # Match the two sets of descriptors.
    matches = matcher.match(d1, d2)

    # Sort matches on the basis of their Hamming distance.
    matches.sort(key=lambda x: x.distance)

    # Take the top 90 % matches forward.
    matches = matches[:int(len(matches) * 90)]
    no_of_matches = len(matches)

    # test - yehuda
    # print(matches[0].queryIdx)
    # print(matches[0].trainIdx)
    # print(kp1[matches[0].queryIdx].pt)
    # print(kp2[matches[0].trainIdx].pt)

    # check to see if we should visualize the matched keypoints
    if debug:
        matchedVis = cv2.drawMatches(np.uint8(threshold_image), kp1, np.uint8(threshold_reference_image), kp2, matches, None)
        matchedVis = imutils.resize(matchedVis, width=1000)
        cv2.imshow("Matched Keypoints", matchedVis)
        cv2.waitKey(0)

    # Define empty matrices of shape no_of_matches * 2.
    p1 = np.zeros((no_of_matches, 2))
    p2 = np.zeros((no_of_matches, 2))

    for i in range(len(matches)):
        p1[i, :] = kp1[matches[i].queryIdx].pt
        p2[i, :] = kp2[matches[i].trainIdx].pt

    # Find the homography matrix.
    # using Random sample consensus alg
    homography, mask = cv2.findHomography(p1, p2, method=cv2.RANSAC, ransacReprojThreshold=ransacReprojThreshold)

    # Use this matrix to transform the
    # colored image wrt the reference image.
    transformed_img = cv2.warpPerspective(image, homography, (width, height))

    # show the image before registration, image after registration and the reference image for check the registration
    # """
    fig = plt.figure()  # make a figure
    fig.add_subplot(1, 3, 1)
    plt.title("image before\nregistration")
    plt.plot(contour[0],contour[1], color='b')
    # plt.plot(contour1[0], contour1[1], color='r')
    plt.imshow(image, cmap=plt.cm.gray)

    fig.add_subplot(1, 3, 2)
    plt.title("image after\nregistration")
    plt.plot(contour[0], contour[1], color='b')
    plt.imshow(transformed_img, cmap=plt.cm.gray)

    fig.add_subplot(1, 3, 3)
    plt.title("the reference\nimage")
    plt.plot(contour[0], contour[1], color='b')
    plt.imshow(reference_image, cmap=plt.cm.gray)

    fig.tight_layout()
    plt.show()
    # """
    """
    # check registration
    overlay = np.uint8(reference_image.copy())
    output = np.uint8(transformed_img.copy())
    cv2.addWeighted(overlay, 0.5, output, 0.5, 0, output)
    res = np.hstack((np.uint8(transformed_img), output, np.uint8(reference_image)))
    cv2.imshow("Image Alignment Overlay", res)
    cv2.waitKey(0)
    """

    # check
    """
    a = transformed_img - image  # regisration - original
    b = transformed_img - reference_image  # regisration - reference
    cv2.imshow("res", np.hstack((np.uint8(a), np.uint8(b))))
    k = cv2.waitKey(0)
    """

    return transformed_img
