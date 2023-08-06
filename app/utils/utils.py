import cv2
import numpy as np

def order_points(pts):
    """4边形4点排序函数

    Args:
        pts ([type]): 4边形任意顺序的4个顶点

    Returns:
        [type]: 按照一定顺序的4个顶点
    """

    rect = np.zeros((4, 2), dtype="float32")  # 按照左上、右上、右下、左下顺序初始化坐标

    s = pts.sum(axis=1)  # 计算点xy的和
    rect[0] = pts[np.argmin(s)]  # 左上角的点的和最小
    rect[2] = pts[np.argmax(s)]  # 右下角的点的和最大

    diff = np.diff(pts, axis=1)  # 计算点xy之间的差
    rect[1] = pts[np.argmin(diff)]  # 右上角的差最小
    rect[3] = pts[np.argmax(diff)]  # 左下角的差最小
    return rect  # 返回4个顶点的顺序


def four_point_transform(image, pts):
    """4点变换

    Args:
        image ([type]): 原始图像
        pts ([type]): 4个顶点

    Returns:
        [type]: 变换后的图像
    """

    rect = order_points(pts)  # 获得一致的顺序的点并分别解包他们
    (tl, tr, br, bl) = rect

    # 计算新图像的宽度(x)
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))  # 右下和左下之间距离
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))  # 右上和左上之间距离
    maxWidth = max(int(widthA), int(widthB))  # 取大者

    # 计算新图像的高度(y)
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))  # 右上和右下之间距离
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))  # 左上和左下之间距离
    maxHeight = max(int(heightA), int(heightB))

    # 有了新图像的尺寸, 构造透视变换后的顶点集合
    dst = np.array(
        [
            [0, 0],  # -------------------------左上
            [maxWidth - 1, 0],  # --------------右上
            [maxWidth - 1, maxHeight - 1],  # --右下
            [0, maxHeight - 1]
        ],  # ------------左下
        dtype="float32")

    M = cv2.getPerspectiveTransform(rect, dst)  # 计算透视变换矩阵
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))  # 执行透视变换

    return warped  # 返回透视变换后的图像