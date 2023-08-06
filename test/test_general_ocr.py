import os
from pathlib import Path
# from app.engineer_log import log
import cv2
import numpy as np
from app.auxiliary.general_ocr.OCR_SERVICE import OCR_SERVICE


def Imgpath2ImgBinary(img_path):
    """
    有图像路径，返回图像的二进制编码的字符串
    """
    with open(img_path, 'rb') as f:
        img_binary = f.read()
    imgdata = img_binary.decode("latin-1")  # Bytes->str
    return imgdata


def cv2ImgBinary(img):
    return np.array(cv2.imencode('.png', img)[1]).tobytes()


def get_img_paths(img_dir):
    path = img_dir
    img_formats = ['.jpg', ".png", ".JPG", ".PNG"]
    p = Path(path)
    img_paths = p.rglob('*.*')
    img_paths = [x for x in img_paths if str(x)[-4:] in img_formats and "ipynb_checkpoints" not in str(x)]
    img_paths = [str(x) for x in img_paths]
    return img_paths


exe_cwd = os.getcwd()
# log.info(f"exe_cwd is {exe_cwd}")
file_cwd = os.path.split(os.path.realpath(__file__))[0]  # 该文件所在目录
# log.info(f"file_cwd is {file_cwd}")

# config_path = os.path.join(file_cwd, "app/auxiliary/general_ocr/config/config.yaml")
config_path = "../app/auxiliary/general_ocr/config/config.yaml"
ocr_service = OCR_SERVICE(config_path)  # 全局变量


def apply(input_dict):
    res = ocr_service(input_dict)
    return res


if __name__ == "__main__":
    img_path = "../data/test_imgs/general.jpg"
    # print(img_path)
    img_binary = Imgpath2ImgBinary(img_path)
    input_dict = {'imgs': img_binary,
                  # "service_id": "0001"
                  "detectAngle": True,
                  "vis": True
                  }
    res = apply(input_dict)
    print(res)
