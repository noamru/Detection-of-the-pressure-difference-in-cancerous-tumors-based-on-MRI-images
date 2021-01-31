import cv2
from matplotlib import pyplot as plt
from skimage import filters

if __name__ == "__main__":
    img = cv2.imread('cloud2.png',0)

    laplacian = cv2.Laplacian(img,cv2.CV_64F)
    sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=5)
    sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=5)
    filters_sobel = filters.sobel(img)
    filters_prewitt = filters.prewitt(img)

    plt.subplot(3, 3, 1), plt.imshow(img, cmap='gray')
    plt.title('Original'), plt.xticks([]), plt.yticks([])
    plt.subplot(3, 3, 2), plt.imshow(laplacian, cmap='gray')
    plt.title('Laplacian'), plt.xticks([]), plt.yticks([])
    plt.subplot(3, 3, 3), plt.imshow(sobelx, cmap='gray')
    plt.title('Sobel X'), plt.xticks([]), plt.yticks([])
    plt.subplot(3, 3, 4), plt.imshow(sobely, cmap='gray')
    plt.title('Sobel Y'), plt.xticks([]), plt.yticks([])
    plt.subplot(3, 3, 5), plt.imshow(sobelx + sobely, cmap='gray')
    plt.title('sobelx + sobely'), plt.xticks([]), plt.yticks([])
    plt.subplot(3, 3, 6), plt.imshow(filters_sobel, cmap='gray')
    plt.title('filters.sobel'), plt.xticks([]), plt.yticks([])
    plt.subplot(3, 3, 7), plt.imshow(filters_prewitt + sobely, cmap='gray')
    plt.title('filters.prewitt'), plt.xticks([]), plt.yticks([])

    plt.show()