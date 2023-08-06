import cv2
import numpy as np
from pathlib import Path
from app.utils.utils import four_point_transform


class Correction_v1(object):
    """
    opencv中的simpledetector检测
    """

    def __init__(self, config):
        self.minthreshold = config.threshold
        self.debug = config.debug

        self.paramsOut = cv2.SimpleBlobDetector_Params()
        # Filter by Area.
        # self.paramsOut.filterByArea = True  # 斑点面积限制变量
        # self.paramsOut.minArea = 5000  # 斑点最小面积，设置minarea=100将滤除所有少于100个像素的斑点
        # self.paramsOut.maxArea = 10e3  # 斑点最大面积
        # self.paramsOut.minDistBetweenBlobs = 25

        # self.paramsOut.filterByColor = True  # 斑点颜色限制变量，blobcolor=0可选择较暗的blob，blobcolor=255可选择较浅的blob

        # tweak these as you see fit
        # Filter by Circularity
        self.paramsOut.filterByCircularity = False  # 斑点圆度限制变量
        self.paramsOut.minCircularity = 1  # 斑点最小圆度，圆的圆度为1，正方形的圆度为pi/4
        # self.params.blobColor = 0

        # Filter by Convexity
        # self.params.filterByConvexity = True # 按凸性，斑点的面积/凸包的面积，现在，形状的“凸包”是最紧密的凸形，它完全包围了该形状，用不严谨的话来讲，给定二维平面上的点集，凸包就是将最外层的点连接起来构成的凸多边形，它能包含点集中所有的点。直观感受上，凸性越高则里面“奇怪的部分”越少。要按凸度过滤，需设置filterByConvexity = true，minConvexity、maxConvexity应该属于[0,1]，而且maxConvexity> minConvexity。
        # self.params.minConvexity = 1
        # self.paramsOut.filterByConvexity = False
        # self.paramsOut.minThreshold = 10
        # self.paramsOut.maxThreshold = 30*2.5

        # Filter by Inertia
        # self.params.filterByInertia = True # 按惯性比：这个词汇比较抽象。我们需要知道Ratio可以衡量形状的伸长程度。简单来说。对于圆，此值是1，对于椭圆，它在0到1之间，对于直线，它是0。按惯性比过滤，设置filterByInertia = true，并设置minInertiaRatio、maxInertiaRatio同样属于[0,1]并且maxConvexity> minConvexity。
        # self.params.filterByInertia = False
        # self.params.minInertiaRatio = 0.1

        self.detector = cv2.SimpleBlobDetector_create(self.paramsOut)

    def run(self, img_dict, template):
        img = img_dict.get("img", None)
        img_name = Path(img_dict.get("img_path", None)).stem
        anchor_points = template.anchor_points
        corner = template.corner

        # 1.矫正图片
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.threshold(gray, self.minthreshold, 255, cv2.THRESH_BINARY)[1]
        # gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        # gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 15)
        kernel = np.ones((3, 3), dtype=np.uint8)
        gray = cv2.dilate(gray, kernel, 1)  # 可执行几次膨胀操作
        gray = cv2.erode(gray, kernel, 1)

        keypoints = self.detector.detect(gray)

        try:
            cnts = [kp.pt for kp in keypoints]
            cnts = sorted(cnts, key=lambda b: b[1])

            # TODO 如何规范和设计模型的输出关键点？关键点标注问题,前2个
            #
            warp_img = four_point_transform(gray, np.array([cnts[0], cnts[1], cnts[-2], cnts[-1]]))

            # 此外要对原图进行填充，根据corner扩充  top,bottom,left,right
            expand_wrap_img = cv2.copyMakeBorder(warp_img, corner[1], corner[1], corner[0], corner[0],
                                                 cv2.BORDER_CONSTANT, value=[255, 255, 255])

            img_dict.update({"correct_wrap_img": expand_wrap_img})
            img_dict.update({"correct_keypoints": cnts})

            if self.debug:
                img_with_keypoints = cv2.drawKeypoints(gray, keypoints, np.array([]), (255, 0, 0),
                                                       cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
                cv2.imwrite(f"{img_name}_with_keypoints.png", img_with_keypoints)
                cv2.imwrite(f"{img_name}_expand_wrap.png", expand_wrap_img)

        except:
            img_dict.update({"correct_wrap_img": img})
            img_dict.update({"correct_keypoints": []})

        # 2.评估图片是否偏移过大
        self.multi_point_judement(img_dict, anchor_points)

        return img_dict

    def multi_point_judement(self, img_dict, anchor_jude_points):
        pass
