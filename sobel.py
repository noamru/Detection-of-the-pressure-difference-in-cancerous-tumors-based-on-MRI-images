from skimage import data, io, filters
import cv2

if __name__ == "__main__":
    image = cv2.imread("coins.png")
    # ... or any other NumPy array!
    edges1 = filters.sobel(image)
    edges2 = filters.prewitt(image)
    io.imshow(image)
    io.show()
    io.imshow(edges1)
    io.show()
    io.imshow(edges2)
    io.show()
