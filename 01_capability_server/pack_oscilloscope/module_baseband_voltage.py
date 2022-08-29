# coding=utf-8
import os

from pack_oscilloscope.base.common_TekMDO3054 import TekMDO3054


def interface_initial(instrName):
    """
    初始化接口
    :return:示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        tek.set_visa_timeout(100)
        tek.set_date_time()
        return instrName
    except Exception as err:
        return str(err)


def interface_set_channel_name(instrName, channelNo, name):
    """
    设置通道名称
    :param name: 通道名称
    :param channelNo: 通道号
    :param instrName: 示波器ID
    :return:示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        tek.name_ch(channelNo, name)
        return instrName
    except Exception as err:
        return str(err)


def interface_set_record_length(instrName, length):
    """
    设置示波器记录长度
    :param instrName: 设备ID
    :param length: 长度
    :return:示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        tek.set_record_length(length)
        measure_value = {}
        measure_value['instrName'] = instrName
        measure_value['length'] = length
        return measure_value
    except Exception as err:
        return str(err)


def interface_set_horizontal(instrName, scale, position=50):
    """
    设置水平位置及比例
    :param position:位置
    :param scale:比例
    :param instrName:示波器ID
    :return:示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        tek.set_horizontal(scale, position)
        return instrName
    except Exception as err:
        return str(err)


def interface_ripple_set(instrName, channelNo, scale):
    """
    设置单条纹波测试项波形参数
    # param instrName: 指定的示波器信息
    # param channelNo: 示波器通道
    # param scale:比例
    :return:示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        num = str(channelNo)
        ch = f'CH{num}'
        tek.set_bandwidth(ch, 20.0000E+6)
        tek.vertical_ch(ch, scale)
        tek.set_position(ch, -3)
        tek.close_measure()
        return instrName
    except Exception as err:
        return str(err)


def interface_select_channel(instrName, channelNo):
    """
    选择指定通道并关闭其他通道
    param instrName: 指定的示波器信息
    param channelNo: 示波器通道
    return:示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        num = str(channelNo)
        ch = f'CH{num}'
        tek.select_channel([ch, ])
        return instrName
    except Exception as err:
        return str(err)


def interface_ripple_ch(instrName, channelNo, pkpk_max, screenshotPath):
    """
    获取单条通道纹波数据
    param pkpk_max:峰峰最大值
    param instrName: 指定的示波器信息
    param channelNo: 示波器通道
    screenshotPath: 截图保存位置
    :return:示波器ID
    """
    try:
        pkpk_max = float(pkpk_max)
        tek = TekMDO3054(instrName)
        # screenshotPath = parameterList['screenshotPath']
        if not os.path.exists(screenshotPath):
            os.mkdir(screenshotPath)
        num = str(channelNo)
        ch = f'CH{num}'
        MeasureValue = tek.ripple_ch(ch, pkpk_max, screenshotPath)
        return MeasureValue
    except Exception as err:
        return str(err)


def interface_set_bandwidth(instrName, channelNo):
    """
    设置带宽为指定数值
    :param instrName:示波器ID
    :param channelNo:示波器通道
    :return:示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        num = str(channelNo)
        ch = f'CH{num}'
        tek.set_bandwidth(ch, 500.0000E+6)
        return instrName
    except Exception as err:
        return str(err)


if __name__ == '__main__':
    instrName = "TCPIP::" + "169.254.5.85" + "::INSTR"
    OsDevice = interface_initial(instrName)
    # instrName, length
    lengthDevice = interface_set_record_length(instrName, 1000000)
    # instrName, channel, name
    channelDevice = interface_set_channel_name(instrName, '1', 'LSLTest')
    # instrName, scale, position=50
    horDevice = interface_set_horizontal(instrName, 0.1, 60)
    # instrName, channelNo, scale
    rippleDevice = interface_ripple_set(instrName, 1, 0.5)
    # instrName, channelNo
    channelDevice = interface_select_channel(instrName, 1)
    # instrName, channelNo, pkpk_max
    measureValue = interface_ripple_ch(instrName, 1, 0.2,os.getcwd() + "\\Screenshot\\")
    # instrName, channelNo
    bandDevice = interface_set_bandwidth(instrName, 1)

    # set_visa_timeout(instMDO3054, 100)
