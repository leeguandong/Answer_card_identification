import cv2
import math
from PIL import Image, ImageStat, ImageEnhance


class Brightness(object):
    def __init__(self, config):
        self.threshold = config.threshold

    def __call__(self, img_dict):
        img = img_dict.get("img", None)
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        stat = ImageStat.Stat(img)
        r, g, b = stat.mean
        value = math.sqrt(0.241 * (r ** 2) + 0.691 * (g ** 2) + 0.068 * (b ** 2))
        if value < self.threshold:
            img_dict.update({"brigheness": True})
            return img_dict
        else:
            img_dict.update({"brightness": False})
            return img_dict
