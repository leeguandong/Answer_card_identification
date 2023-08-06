import cv2
import numpy as np


class Laplacian(object):
    def __init__(self, config):
        self.manner = config.manner
        self.threshold = config.threshold

    def __call__(self, img_dict):
        img = img_dict.get("img", None)
        if self.manner == "var":
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # gray = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
            value = cv2.Laplacian(gray, cv2.CV_64F).var()
            if value < self.threshold:
                img_dict.update({"laplacian": True})
                return img_dict
            else:
                img_dict.update({"laplacian": False})
                return img_dict

        if self.manner == "max":
            # gray = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            value = np.max(cv2.convertScaleAbs(cv2.Laplacian(gray, 3)))
            if value < self.threshold:
                img_dict.update({"laplacian": True})
                return img_dict
            else:
                img_dict.update({"laplacian": False})
                return img_dict
