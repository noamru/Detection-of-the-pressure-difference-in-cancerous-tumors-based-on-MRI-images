import cv2
import numpy as np


if __name__ == "__main__":
    # contour perimeter calculation test
    contours = np.array([[[20, 30]], [[25, 30]], [[30, 30]], [[30, 20]], [[20, 20]]], dtype=np.int32)
    print(cv2.arcLength(contours, True))
