# coding=utf-8
import cv2
import numpy as np
from matplotlib import pyplot as plt
import tkinter.messagebox as msgbox
import tkinter


def get_position(source_image):
    """
    寻找roi有效区域的上下左右值
    :param source_image:图片数据
    :return:
    """
    # cv2.imshow("source_image", source_image)
    # 转换为HSV空间
    hsv = cv2.cvtColor(source_image, cv2.COLOR_BGR2HSV)
    # 灰色HSV
    lower_yellow1 = np.array([0, 0, 46])
    upper_yellow1 = np.array([180, 43, 220])

    # Threshold the HSV image to get only yellow colors
    mask = cv2.inRange(hsv, lower_yellow1, upper_yellow1)
    # cv2.imshow("mask", mask)

    height = mask.shape[0]
    top = 0
    # left = 0
    # right = source_image.
    bottom = height
    for i in range(height):
        if list(mask[i]).count(255) >= 1100:
            top = i
            break

    left = list(mask[top]).index(255)

    for j in range(height - 1, -1, -1):
        if 1100 <= list(mask[j]).count(255) <= 1220:
            bottom = j
            break
    tt = list(mask[bottom])
    tt.reverse()
    New_list = tt
    index = New_list.index(255)
    right = len(mask[bottom]) - index

    measure_value = {'top': top, 'bottom': bottom, 'left': left, 'right': right}
    return measure_value


def max_to_min(image_path, voltage_range):
    """
    返回力科截图计算的电压最大与最小值量程
    :param image_path: 图片路径
    :param voltage_range: 示波器当前截图所显示的电压量程
    :return:
    """
    # 垂直像素点偏置，roi从第三个像素点开始
    source_image = cv2.imread(image_path)

    # 计算有效区域的位置
    position = get_position(source_image)
    # 获取ROI区域
    imaROI = source_image[position["top"]:position["bottom"], position["left"]:position["right"]]
    # cv2.imshow("imaROI", imaROI)
    # 转换为HSV空间
    hsv = cv2.cvtColor(imaROI, cv2.COLOR_BGR2HSV)

    # define range of yellow color in HSV
    lower_yellow = np.array([26, 43, 46])
    upper_yellow = np.array([34, 255, 255])

    # Threshold the HSV image to get only yellow colors
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    height = mask.shape[0]
    top = 0
    bottom = height
    for i in range(height):
        if mask[i].max() >= 255:
            top = i
            break

    for j in range(height - 1, -1, -1):
        if mask[j].max() >= 255:
            bottom = j
            break

    measure_value = {}

    scale = bottom - top + 1
    w = source_image.shape[1]
    if scale >= 0:
        # 开始划线位置
        startLine = measure_value['startLine'] = top + position["top"]
        # 结束划线位置
        endLine = measure_value['endLine'] = bottom + position["top"]
        voltage = measure_value['voltage'] = float(scale) * voltage_range / imaROI.shape[0]
        cv2.line(source_image, (0, startLine - 1), (w - 1, startLine - 1), (0, 0, 255), 1)
        cv2.line(source_image, (0, endLine + 1), (w - 1, endLine + 1), (0, 0, 255), 1)
        cv2.putText(source_image, 'voltage=' + str(voltage), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2,
                    cv2.LINE_AA)
        measure_value['image'] = source_image
    return measure_value


def message_askyesno(message):
    top = tkinter.Tk()  # *********
    top.withdraw()  # ****实现主窗口隐藏
    top.update()  # *********需要update一下
    txt = tkinter.messagebox.askyesno("提示", message)
    top.destroy()
    return txt


def test(mr):
    if not mr.__contains__('save_pic'):
        mr['save_pic'] = []
    mr['save_pic'].append('1')
    mr['save_pic'].append('2')


if __name__ == '__main__':
    img_path = 'src/4.png'
    data = max_to_min(img_path, 1.584)

    cv2.imshow("image", data['image'])

    key = cv2.waitKey(0)
    if key == 27:  # 按esc键时，关闭所有窗口
        print('关闭所有窗口')
        cv2.destroyAllWindows()
