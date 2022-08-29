# coding=utf-8
import os
import time
from pack_oscilloscope.base.common_TekMDO3054 import TekMDO3054
from pack_oscilloscope.base.USB_circuit_board import SerialPort
from pack_oscilloscope.base.scene_library import GoScene    # 调用场景库
from pack_oscilloscope.base import spi_signal_quality
from pack_phoneself.Base import mobile_base

"""
    充电（有线无线自由切换） --- 常一杰       【后续可作为公用方法库使用】
"""


def interface_select_ch(instrName, CH):
    """
    开启指定通道
    :param instrName: 示波器ID
    :param CH: 指定需要开启的通道
    :return:示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        tek.open_ch(CH)      # 打开指定通道
        return instrName
    except Exception as err:
        return str(err)


def interface_set_bandwidth(instrName, CH, bandwidth):
    """
    设置示波器带宽
    @param instrName:示波器ID
    @param CH: 需要设置的通道
    @param bandwidth:设置带宽值
    @return:示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        tek.set_bandwidth(CH, bandwidth)     # 设置CH通道示波器带宽(指定数值或FULL)
        return instrName
    except Exception as err:
        return str(err)


def interface_set_display_intensity(instrName, intensity):
    """
    设置示波器的显示波形强度百分比
    :param instrName: 示波器ID
    :param intensity: 需要设置的显示强度百分比值（值得范围：1-100）
    :return: 示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        tek.set_display_intensity(intensity)
        return instrName
    except Exception as e:
        return str(e)


def interface_set_coupling(instrName, CH, ch_coupling):
    """
    设置通道耦合模式
    @param instrName: 示波器ID
    @param CH: 需要设置的通道
    @param ch_coupling:耦合方式
    @return:示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        tek.set_coupling(CH, ch_coupling)    # 设置示波器CH通道耦合模式
        return instrName
    except Exception as err:
        return str(err)


def interface_set_channel_label(instrName, CH, label):
    """
    设置示波器通道标签名称
    @param instrName: 示波器ID
    @param CH: 需要设置的通道
    @param label: 需要设置的标签名称
    @return: 示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        tek.set_channel_label(CH, label)
        return instrName
    except Exception as err:
        return str(err)


def interface_set_offset(instrName, CH, offset):
    """
    设置示波器偏置值
    @param instrName:示波器ID
    @param CH: 需要设置的通道
    @param offset:需要设置的偏置值
    @return:示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        tek.set_offset(CH, offset)       # 设置示波器CH通道的偏置值
        return instrName
    except Exception as err:
        return str(err)


def interface_compute_only_set_scale(instrName, CH, Voltage):
    """
    ***** 注意： 该方法将根据波形电压设置展示在示波器电压幅值2格以内  *****
    ***** 根据传入的Voltage电压值（单位V），自动计算并设置垂直刻度； *****
    :param instrName: 示波器ID
    :param CH: 示波器通道号
    :param Voltage: 电压值，单位V
    :return: 返回设置垂直刻度
    """
    try:
        tek = TekMDO3054(instrName)
        scale_value = tek.compute_only_set_scale(CH, Voltage)
        return scale_value
    except Exception as err:
        return str(err)


def interface_set_position(instrName, CH, vertical_position):
    """
    设置示波器垂直位置
    @param instrName:示波器ID
    @param CH: 需要设置的通道号
    @param vertical_position:需要设置的垂直位置
    @return:示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        tek.set_position(CH, vertical_position)      # 设置示波器CH通道的垂直位置
        return instrName
    except Exception as err:
        return str(err)


def interface_set_horizontal_scale(instrName, scale_horizontal):
    """
    设置示波器水平时基
    @param instrName:示波器ID
    @param scale_horizontal:需要设置的水平时基参数
    @return:示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        tek.set_horizontal_scale(scale_horizontal)
        return instrName
    except Exception as err:
        return str(err)


def interface_set_record_length(instrName, length):
    """
    设置示波器的记录长度
    @param instrName: 示波器ID
    @param length: 需要设置的长度
    @return: 示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        tek.set_record_length(length)    # 设置示波器的记录长度
        return instrName
    except Exception as err:
        return str(err)


def interface_set_trigger_mode(instrName, acquire_type):
    """
    设置触发模式
    @param instrName: 示波器ID
    @param acquire_type: 触发模式（设置单次触发acquire_type=SEQUENCE，正常运行是acquire_type=RUNSTOP）
    @return:示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        if int(tek.query_acquire_mode()) == 0:
            tek.set_acquisitions_start()
            tek.set_trigger_mode(acquire_type)
        else:
            tek.set_trigger_mode(acquire_type)
        return instrName
    except Exception as err:
        return str(err)


def interface_set_acquisitions_stop(instrName):
    """
    停止示波器采集
    :param instrName: 示波器ID
    :return: 示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        tek.set_acquisitions_stop()
        return instrName
    except Exception as e:
        return str(e)


def interface_charging_panel_control(sequence: dict) -> list:
    """
    充电板控制
    :param sequence: 控制序列，字典类型  例如：{"pc": 1, "svooc": 1, "pd": 0}  其中 1 表示打开， 0 表示关闭；
    :return: 所发送请求指令，16进制列表
    """
    serial = SerialPort()
    return_list = []
    for key, value in sequence.items():     # 打开或关闭指定端口
        if value:
            return_list.append(eval("serial." + key + "_on")())   # eval(serial + "." + key + "_on"
        else:
            return_list.append(eval("serial." + key + "_off")())
    return return_list


def interface_save_screen(instrName, fileName):
    """
    保存示波器屏幕截图
    :param instrName: 示波器ID
    :param fileName: 图片文件保存名称
    :return: 图片保存名称
    """
    try:
        tek = TekMDO3054(instrName)
        save_image = tek.save_screen(fileName)
        return save_image
    except Exception as e:
        return str(e)


def interface_data_caul(instrName, CH):
    """
    获取示波器波形数据
    :param instrName: 示波器ID
    :param CH: 需要采集的通道号
    :return: 数据列表字典
    """
    try:
        tek = TekMDO3054(instrName)
        return tek.data_caul(CH)
    except Exception as e:
        return str(e)


def interface_time_scaling(instrName, zoom_point, zoom_scale):
    """
    根据缩放位置和缩放系数进行缩放
    :param instrName: 示波器ID
    :param zoom_point: 缩放位置（时间点）
    :param zoom_scale: 缩放系数
    :return:
    """
    try:
        tek = TekMDO3054(instrName)
        tek.set_SIM_PositionRateZoom(zoom_point, zoom_scale)
        tek.set_SIM_zoom(zoom_point, zoom_scale)
    except Exception as err:
        return str(err)


def interface_close_zoom(instrName):
    """
    关闭zoom放大
    :param instrName: 示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        tek.close_zoom()
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    instrName = "TCPIP::" + "169.254.5.85" + "::INSTR"
    interface_time_scaling(instrName, -0.7788960000000005, 0.02)
    # print(interface_charging_panel_control({"pc": 1, "svooc": 0, "pd": 0}))
    # print(interface_close_svooc())