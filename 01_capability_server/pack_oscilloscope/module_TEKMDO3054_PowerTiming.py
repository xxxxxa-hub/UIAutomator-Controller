# coding=utf-8
import datetime
import time
import os
from pack_oscilloscope.base.common_TekMDO3054 import TekMDO3054
import sys
import pandas as pd
import numpy as np


def interface_initial(instrName):
    """
    初始化接口
    :return:
    """
    try:
        tek = TekMDO3054(instrName)
        tek.set_visa_timeout(100)
        tek.set_date_time()
        return instrName
    except Exception as err:
        return str(err)


def interface_start_acquisitions(instrName):
    """
    设置示波器开始采集
    :param instrName: 示波器ID
    :return:
    """
    try:
        tek = TekMDO3054(instrName)
        tek.set_acquisitions_start()
        return instrName
    except Exception as err:
        return str(err)


def interface_default_setup(instrName):
    """
    示波器恢复默认设置
    :param instrName: 示波器ID
    :return:示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        tek.default_setup()
        return instrName
    except Exception as err:
        return str(err)


def interface_wave_intensity(instrName):
    """
    设置示波器的波形强度
    :param instrName: 示波器ID
    :return:示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        tek.wave_intensity()
        return instrName
    except Exception as err:
        return str(err)


def interface_open_ch(instrName, ch):
    """
    指定那个通道打开
    :param instrName: 示波器ID
    :param ch: 通道号（如，CH1）
    :return:示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        tek.open_ch(ch)
        return instrName
    except Exception as err:
        return str(err)


def interface_close_ch(instrName, ch):
    """
    指定那个通道打开
    :param instrName: 示波器ID
    :param ch: 通道号（如，CH1）
    :return:示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        tek.close_ch(ch)
        return instrName
    except Exception as err:
        return str(err)


def interface_set_record_length(instrName, record_length):
    """
    设置示波器的记录长度
    :param instrName: 示波器ID
    :param record_length:示波器的记录长度
    :return:示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        tek.set_record_length(record_length)
        return instrName
    except Exception as err:
        return str(err)


def interface_set_bandwidth(instrName, ch, bandwidth):
    """
    设置示波器的带宽
    :param instrName: 示波器ID
    :param ch: 通道号（如，CH1）
    :param bandwidth: 带宽值
    :return:示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        tek.set_bandwidth(ch, bandwidth)
        return instrName
    except Exception as err:
        return str(err)


def interface_set_horizontal(instrName, scale, position=50):
    """
    设置水平位置及时基
    :param instrName: 示波器ID
    :param scale: 水平时基
    :param position: 水平位置
    :return:示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        tek.set_horizontal(scale, position)
        return instrName
    except Exception as err:
        return str(err)


def interface_set_horizontal_position(instrName, position_horizontal):
    """
    设置水平位置
    :param instrName: 示波器ID
    :param position_horizontal: 水平位置，50
    :return:示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        tek.set_horizontal_position(position_horizontal)
        return instrName
    except Exception as err:
        return str(err)


def interface_set_horizontal_scale(instrName, scale_horizontal):
    """
    设置水平时基
    :param instrName:  示波器ID
    :param scale_horizontal: 水平时基
    :return:示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        tek.set_horizontal_scale(scale_horizontal)
        return instrName
    except Exception as err:
        return str(err)


def interface_set_channel_label(instrName, ch, label):
    """
    设置通道的标签
    :param instrName: 示波器的ID
    :param ch: 通道号（如，CH1）
    :param label: 通道的标签
    :return:示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        ch = str(ch)
        tek.set_channel_label(ch, label)
        return instrName
    except Exception as err:
        return str(err)


def interface_set_offset(instrName, ch, offset):
    """
    设置偏置
    :param instrName:示波器ID
    :param ch:通道号
    :param offset:偏置值
    :return:示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        tek.set_offset(ch, offset)
        return instrName
    except Exception as err:
        return str(err)


def interface_set_scale(instrName, ch, vertical_scale):
    """
    设置指定通道的垂直比例V/格
    :param instrName: 示波器ID
    :param ch: 通道号
    :param vertical_scale: 垂直比例
    :return:示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        tek.set_scale(ch, vertical_scale)
        return instrName
    except Exception as err:
        return str(err)


def interface_set_position(instrName, ch, vertical_position):
    """
    设置指定通道的垂直位置
    :param instrName: 示波器位置
    :param ch: 通道号
    :param vertical_position: 垂直位置
    :return:示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        tek.set_position(ch, vertical_position)
        return instrName
    except Exception as err:
        return str(err)


def interface_set_coupling(instrName, ch, ch_coupling):
    """
    设置通道的耦合方式
    :param instrName: 示波器ID
    :param ch: 通道号
    :param ch_coupling: 耦合方式
    :return:示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        tek.set_coupling(ch, ch_coupling)
        return instrName
    except Exception as err:
        return str(err)


def interface_set_invert(instrName, ch, invert_state):
    """
    设置反向
    :param instrName:示波器ID
    :param ch: 通道号
    :param invert_state: 反向状态ON或OFF
    :return:示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        tek.set_invert(ch, invert_state)
        return instrName
    except Exception as err:
        return str(err)


def interface_horizontal_delay_state(instrName, state):
    """
    设置延迟状态，打开或关闭
    :param instrName: 示波器ID
    :param state: 延迟状态,ON或OFF
    :return:示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        tek.horizontal_delay_state(state)
        return instrName
    except Exception as err:
        return str(err)


def interface_horizontal_delay(instrName, delay_horizontal):
    """
    设置水平延时时间
    :param instrName: 示波器ID
    :param delay_horizontal: 水平延时时间
    :return: 示波器的ID
    """
    try:
        tek = TekMDO3054(instrName)
        tek.horizontal_delay(delay_horizontal)
        return instrName
    except Exception as err:
        return str(err)


def interface_delay_horizontal(instrName, delay_horizontal):
    """
    打开延迟开关，设置水平延时时间
    :param instrName: 示波器ID
    :param delay_horizontal: 水平延时时间
    :return: 示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        tek.delay_horizontal(delay_horizontal)
        return instrName
    except Exception as err:
        return str(err)


def interface_set_zoom(instrName, zoom_position, zoom_scale):
    """
    设置缩放位置和缩放比例
    :param instrName: 示波器ID
    :param zoom_position: 缩放的位置
    :param zoom_scale: 缩放的水平比例
    :return:示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        tek.set_zoom(zoom_position, zoom_scale)
        return instrName
    except Exception as err:
        return str(err)


def interface_ripple_set(instrName, channelNo, scale):
    """
    设置单条纹波测试项波形参数
    :param instrName: 示波器ID
    :param channelNo: 示波器通道
    :param scale:比例
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


def interface_ripple_ch(instrName, ch, pkpk_max, screenshot_path):
    """
    获取单条通道纹波数据
    :param pkpk_max:峰峰最大值
    :param instrName: 指定的示波器信息
    :param ch: 示波器通道
    :screenshot_path: 截图保存位置
    :return:示波器ID
    """
    try:
        pkpk_max = float(pkpk_max)
        tek = TekMDO3054(instrName)
        # screenshotPath = parameterList['screenshotPath']
        if not os.path.exists(screenshot_path):
            os.mkdir(screenshot_path)
        measure_value = tek.ripple_ch(ch, pkpk_max, screenshot_path)
        return measure_value
    except Exception as err:
        return str(err)


def interface_save_screen(instrName, file_name):
    """
    保存屏幕
    :param instrName: 示波器ID
    :param file_name: 保存图像文件的路径加文件名
    （filename = pic_path + "\\" + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + '.png'）
    :return:示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        file_name = str(file_name)
        tek.save_screen(file_name)
        measure_result = {}
        measure_result['instrName'] = instrName
        measure_result['filename'] = file_name
        return measure_result
    except Exception as err:
        return str(err)


def interface_set_cursor(instrName, cursor_source, position_horizontal1, position_horizontal2, position1, position2):
    """
       设置示波器光标的水平和垂直位置（示波器的光标类型为屏幕）
       :param instrName: 示波器的ID
       :param cursor_source: 光标的源(如，CH1)
       :param position_horizontal1: 光标a的水平位置
       :param position_horizontal2: 光标b的水平位置
       :param position1: 光标a的垂直位置
       :param position2: 光标b的垂直位置
       :return:cursor_value:示波器ID和垂直光标的时间差值
       """
    try:
        tek = TekMDO3054(instrName)
        delta_timing = tek.set_cursor(cursor_source, position_horizontal1, position_horizontal2, position1, position2)
        cursor_value = {}
        cursor_value['instrName'] = instrName
        cursor_value['delta'] = delta_timing
        return cursor_value
    except Exception as err:
        return str(err)


def interface_set_cursor_wave(instrName, cursor_source, position1, position2):
    """
       设置示波器光标(光标类型为波形)
       :param instrName: 示波器的ID
       :param cursor_source: 光标的源(如，CH1)
       :param position1: 光标a的垂直位置
       :param position2: 光标b的垂直位置
       :return:cursor_value:示波器ID和垂直光标的时间差值
       """
    try:
        tek = TekMDO3054(instrName)
        delta_timing = tek.set_cursor_wave(cursor_source, position1, position2)
        cursor_value = {}
        cursor_value['instrName'] = instrName
        cursor_value['delta'] = delta_timing
        return cursor_value
    except Exception as err:
        return str(err)


def interface_set_trigger(instrName, trigger_type, trigger_ch, trigger_level, trigger_delay):
    """
        设置示波器的触发方式(模式：正常)
        :param instrName:示波器的ID
        :param trigger_type: 设置示波器的触发类型
        :param trigger_ch: 设置示波器的触发通道（如，CH1）
        :param trigger_level: 设置触发电平
        :param trigger_delay: 设置触发位置
        :return:示波器ID
        """
    try:
        tek = TekMDO3054(instrName)
        tek.set_trigger(trigger_type, trigger_ch, trigger_level, trigger_delay)
        return instrName
    except Exception as err:
        return str(err)


def interface_set_trigger_pulse(instrName, pulse_source, pulse_condition, pulse_width, trigger_level):
    """
        设置示波器脉宽触发(模式：正常)
        :param instrName:示波器的ID
        :param pulse_source: 触发源（通道几触发）
        :param pulse_condition: 触发条件，LESSthan、MOREthan、EQual、UNEQual、WIThin、OUTside
        :param pulse_width: 脉冲宽度
        :param trigger_level:阈值
        :return:
    """
    try:
        tek = TekMDO3054(instrName)
        tek.set_trigger_pulse(pulse_source, pulse_condition, pulse_width, trigger_level)
        return instrName
    except Exception as err:
        return str(err)
def interface_set_trigger_auto(instrName, trigger_type, trigger_ch, trigger_level, trigger_delay):
    """
        设置示波器的触发方式(模式：自动（无触发滚动）)
        :param instrName:示波器的ID
        :param trigger_type: 设置示波器的触发类型
        :param trigger_ch: 设置示波器的触发通道（如，CH1）
        :param trigger_level: 设置触发电平
        :param trigger_delay: 设置触发位置
        :return:示波器ID
        """
    try:
        tek = TekMDO3054(instrName)
        tek.set_trigger_auto(trigger_type, trigger_ch, trigger_level, trigger_delay)
        return instrName
    except Exception as err:
        return str(err)


def interface_set_trigger_mode(instrName, acquire_type):
    """
    设置是single还是run/stop模式，
    :param instrName: 示波器ID
    :param acquire_type: acquire_type=SEQUENCE为single，acquire_type=RUNSTOP为run/stop
    :return:示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        tek.set_trigger_mode(acquire_type)
        return instrName
    except Exception as err:
        return str(err)


def interface_query_acquire_mode(instrName):
    """
    查询示波器的触发模式
    :param instrName: 示波器ID
    :return acquire_mode:示波器的触发方式
    """
    try:
        tek = TekMDO3054(instrName)
        acquire_mode = tek.query_acquire_mode()
        return acquire_mode
    except Exception as err:
        return str(err)


def interface_set_search(instrName, search_ch, search_type, search_level):
    """
    设置搜索条件，返回搜索值
    :param instrName: 示波器ID
    :param search_ch: 搜索的源（如，CH1）
    :param search_type:搜索的类型（上升沿、下降沿或任意边沿）
    :param search_level: 搜索的阈值
    :return: query_search:示波器ID和搜索值
    """
    try:
        tek = TekMDO3054(instrName)
        query_search = tek.set_search(search_ch,  search_type, search_level)
        search_value = {}
        search_value['instrName'] = instrName
        search_value['query'] = query_search
        return search_value
    except Exception as err:
        return str(err)


def interface_search_position(instrName, query_search):
    """
    根据搜索返回值，将所有标记点的位置坐标收集到mark_position列表里
    :param instrName: 示波器ID
    :param query_search: 搜索返回的值（字符串）
    :return: mark_position：标记点位置坐标列表
    """
    try:
        tek = TekMDO3054(instrName)
        mark_position = tek.search_position(query_search)
        search_position = {}
        search_position['instrName'] = instrName
        search_position['position'] = mark_position
        return search_position
    except Exception as err:
        return str(err)


def interface_query_position(instrName, ch, search_type, search_level):
    """
    找出满足要求的位置坐标
    :param instrName:示波器ID
    :param ch:通道号
    :param search_type:搜索的类型，上升沿、下降沿等
    :param search_level:搜索的阈值
    :return:
    """
    try:
        tek = TekMDO3054(instrName)
        mark_position = tek.query_position(ch, search_type, search_level)
        search_position = {}
        search_position['instrName'] = instrName
        search_position['position'] = mark_position
        return search_position
    except Exception as err:
        return str(err)


def interface_timing_position1(instrName, position_list1, position_list2):
    """
       找出满足时序要求的光标位置（最小值）
       :param instrName:示波器的ID
       :param position_list1:第一个通道的位置坐标列表
       :param position_list2:第二个通道的位置坐标列表
       :return:cursor_position：垂直光标差值(min),光标a的垂直位置,光标b的垂直位置
       """
    try:
        tek = TekMDO3054(instrName)
        min_delta, cursor_position1, cursor_position2 = tek.timing_position1(position_list1, position_list2)
        cursor_position = {}
        cursor_position['instrName'] = instrName
        cursor_position['min_delta'] = min_delta
        cursor_position['position_a'] = cursor_position1
        cursor_position['position_b'] = cursor_position2
        return cursor_position
    except Exception as err:
        return str(err)


def interface_timing_position2(instrName, position_list1, position_list2, t_clock):
    """
    找出满足时序要求的光标位置(最大值)
    :param instrName:示波器的ID
    :param position_list1:第一个通道的位置坐标列表
    :param position_list2:第二个通道的位置坐标列表
    :param t_clock:时钟周期
    :return:cursor_position：垂直光标差值（max）,光标a的垂直位置,光标b的垂直位置
    """
    try:
        tek = TekMDO3054(instrName)
        max_delta, cursor_position1, cursor_position2 = tek.timing_position2(position_list1, position_list2, t_clock)
        cursor_position = {}
        cursor_position['instrName'] = instrName
        cursor_position['max_delta'] = max_delta
        cursor_position['position_a'] = cursor_position1
        cursor_position['position_b'] = cursor_position2
        return cursor_position
    except Exception as err:
        return str(err)


def interface_ch_set(instrName, ch_list, label_list):
    """
    设置示波器各个通道的标签和位置等
    :param instrName: 示波器ID
    :param ch_list: 通道号列表
    :param label_list: 标签列表
    :return:示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        tek.ch_set(ch_list, label_list)
        return instrName
    except Exception as err:
        return str(err)


def interface_data_caul(instrName, ch, save_path):
    """
    获取指定通道数据，保存到指定位置CSV表
    :param instrName:示波器ID
    :param ch: 需要保存的通道号，int类型（1，2，3，4）
    :param save_path:文件保存路径
    :return:success
    """
    try:
        tek = TekMDO3054(instrName)
        res = tek.data_caul(ch)
        tek.save_data_list(res, save_path)
        return res
    except Exception as err:
        return str(err)


def interface_knee_point_rise(instrName, csv_path):
    """
    计算上电波形的拐点
    :param instrName: 示波器ID
    :param csv_path: 波形数据保存路径
    :return: point_position：波形拐点处的时间坐标值
    """
    try:
        tek = TekMDO3054(instrName)
        v_value, knee_position = tek.knee_point_rise_by_dichotomy(csv_path)
        point_position = {}
        point_position['v_value'] = v_value
        point_position['knee_position'] = knee_position
        return point_position
    except Exception as err:
        return str(err)


def interface_knee_point_fall(instrName, csv_path):
    """
    计算下电波形的拐点
    :param instrName: 示波器ID
    :param csv_path: 波形数据保存路径
    :return: point_position：波形拐点处的时间坐标值
    """
    try:
        tek = TekMDO3054(instrName)
        v_value, knee_position = tek.knee_point_fall(csv_path)
        point_position = {}
        point_position['v_value'] = v_value
        point_position['knee_position'] = knee_position
        return point_position
    except Exception as err:
        return str(err)


def interface_search_edge_num(instrName, search_ch, search_type, search_level):
    """
     设置搜索条件，返回满足搜索要求的边沿个数和最后一个边沿的的位置
    :param instrName: 示波器ID
    :param search_ch: 搜索通道
    :param search_type: 搜索的类型，上升沿、下降沿等
    :param search_level: 搜索的阈值
    :return: start_position{num:num, ref_position:ref_position}num：边沿个数,ref_position：最后一个边沿的的位置
    """
    try:
        tek = TekMDO3054(instrName)
        num, ref_position = tek.search_edge_num(search_ch, search_type, search_level)
        start_position = {}
        start_position['num'] = num
        start_position['ref_position'] = ref_position
        return start_position
    except Exception as err:
        return str(err)


def interface_pick_rise_point(instrName, path, scale_horizontal, record_length):
    """
    二分法找到上升沿或下降沿的切换点位置
    :param record_length:
    :param scale_horizontal:
    :param instrName:
    :param path:
    :return:
    """
    try:
        tek = TekMDO3054(instrName)
        index, volt, tim = tek.knee_point_rise_fall_sequence(path, scale_horizontal, record_length)
        point = {'index': index, 'voltage': volt, 'time': tim}
        return point
    except Exception as err:
        return str(err)


def interface_pick_fall_point(instrName, path, scale_horizontal, record_length):
    """
    二分法找到上升沿或下降沿的切换点位置
    :param record_length:
    :param scale_horizontal:
    :param instrName:
    :param path:
    :return:
    """
    try:
        tek = TekMDO3054(instrName)
        index, volt, tim = tek.knee_point_rise_fall_sequence(path, scale_horizontal, record_length)
        point = {'index': index, 'voltage': volt, 'time': tim}
        return point
    except Exception as err:
        return str(err)


def interface_search_num(instrName, search_ch, search_type, search_level):
    """
     设置搜索条件，返回满足搜索要求的边沿个数
    :param instrName: 示波器ID
    :param search_ch: 搜索通道
    :param search_type: 搜索的类型，上升沿、下降沿等
    :param search_level: 搜索的阈值
    :return: num：边沿个数
    """
    try:
        tek = TekMDO3054(instrName)
        num = tek.search_num(search_ch, search_type, search_level)
        return num
    except Exception as err:
        return str(err)


def interface_fall_knee_point(instrName, csv_path, num, start_position):
    """
    计算下电波形的拐点(反复上下电)
    :param csv_path: 波形数据保存路径
    :param num 搜索出的边沿个数
    :param start_position: 开始计算拐点的数据起点
    :return: v_value:幅值的最大值
    :return:knee_position: 波形拐点处的时间坐标值
    """
    try:
        tek = TekMDO3054(instrName)
        v_value, knee_position = tek.fall_knee_point(csv_path, num, start_position)
        point_position = {}
        point_position['v_value'] = v_value
        point_position['knee_position'] = knee_position
        return point_position
    except Exception as err:
        return str(err)


def interface_find_mean_value(instrName, csv_path):
    """
    计算波形的最大值
    :param csv_path: 波形数据保存路径
    :return: v_mean:幅值的平均值
    """
    try:
        tek = TekMDO3054(instrName)
        v_mean = tek.find_mean_value(csv_path)
        return v_mean
    except Exception as err:
        return str(err)


def interface_adjust_scale(instrName, pos_a, pos_b):
    """
    根据计算出的光标要卡的位置对波形进行缩放
    :param instrName:
    :param pos_a:计算出的a光标放置的位置
    :param pos_b:计算出的b光标放置的位置
    :return:
    """
    try:
        tek = TekMDO3054(instrName)
        zoom_point = float((pos_a + pos_b) / 2)
        delta = float(abs(pos_a - pos_b))
        old_scale = tek.query_horsacle()
        if delta < float(old_scale):
            zoom_scale = float(delta)
            # zoom_scale = float(old_scale/delta)
            tek.set_zoom(zoom_point, zoom_scale)
    except Exception as err:
        return str(err)


def interface_set_oscilloscope(instrName, record_length):
    """
    示波器恢复默认设置，并设置示波器的记录长度
    :param instrName:
    :param record_length:
    :return:
    """
    try:
        tek = TekMDO3054(instrName)
        tek.default_setup()
        tek.wave_intensity()
        tek.set_record_length(record_length)
        return instrName
    except Exception as err:
        return str(err)


def interface_ch_set1(instrName, ch_label, ch_vertical):
    """
    配置示波器的各个通道
    :param instrName: 示波器ID
    :param ch_label: 示波器的通道标签列表
    :return: 示波器的ID
    """
    try:
        tek = TekMDO3054(instrName)
        ch_arr = ['CH1', 'CH2', 'CH3', 'CH4']
        ch_label1 = ch_label
        for i in range(len(ch_arr)):
            tek.open_ch(ch_arr[i])
            tek.set_channel_label(ch_arr[i], ch_label1[i])
            tek.set_coupling(ch_arr[i], "DC")
            tek.set_invert(ch_arr[i], "OFF")
            tek.set_bandwidth(ch_arr[i], "FULL")
            tek.set_scale(ch_arr[i], ch_vertical[i])
            tek.set_offset(ch_arr[i], 0)
            tek.set_position(ch_arr[i], -i)
        return instrName
    except Exception as err:
        return str(err)


if __name__ == '__main__':
    instrName = "TCPIP::" + "169.254.4.96" + "::INSTR"
    # flag = "POWER ON"
    flag = "POWER OFF"

    # 初始化示波器
    OsDevice = interface_initial(instrName)
    """
    # 示波器恢复默认设置
    interface_default_setup(instrName)
    # 设置示波器的波形强度
    interface_wave_intensity(instrName)
    # 设置示波器记录长度
    interface_set_record_length(instrName, 1.0E6)
    """
    interface_set_oscilloscope(instrName, 1.0E6)
    ch_arr = ['CH1', 'CH2', 'CH3', 'CH4']
    ch_label = 'VX022, VAUX18, VCORE, VS2'
    # ch_label = ch_label.split(',')
    # 设置四个通道的标签等
    interface_ch_set1(instrName, ch_label)
    """
    for i in range(len(ch_arr)):
        interface_open_ch(instrName, ch_arr[i])
        interface_set_channel_label(instrName, ch_arr[i], ch_label[i])
        interface_set_coupling(instrName, ch_arr[i], "DC")
        interface_set_invert(instrName, ch_arr[i], "OFF")
        interface_set_bandwidth(instrName, ch_arr[i], "FULL")
        interface_set_scale(instrName, ch_arr[i], 1)
        interface_set_offset(instrName, ch_arr[i], 0)
        interface_set_position(instrName, ch_arr[i], -i)
    """
    # 设置时基
    interface_set_horizontal_scale(instrName, 0.04)
    # 调用set_trigger函数设置触发类型
    if flag == "POWER ON":
        interface_set_trigger(instrName, "RISE", "CH1", 0.5, 0)
    if flag == "POWER OFF":
        interface_set_trigger(instrName, "FALL", "CH2", 0.5, 0)
    # 设置为单次触发
    interface_start_acquisitions(instrName)
    interface_set_trigger_mode(instrName, "SEQUENCE")
    print("请开机")
    # 等待波形触发
    time.sleep(20)
    print("等待波形触发")

    # 导出波形数据，并根据波形数据计算波形的拐点位置
    ch_Value = []
    knee_position = []
    save_path = 'F:/test1/datasheet.csv'
    for i in range(1, 5):
        point_position = {}
        # 导出波形数据
        result = interface_data_caul(instrName, i, save_path)
        if flag == "POWER ON":
            # 判断是否有重复上电
            num = interface_search_num(instrName, f'CH{i}', 'FALL', 0.5)
            if num > 0:
                print("反复上电：", ch_label[i - 1])
            # 计算拐点的位置和波形的幅值，幅值,保存到列表ch_Value中，波形拐点,保存到列表knee_position中
            point_position = interface_knee_point_rise(instrName, save_path)
        if flag == "POWER OFF":
            # 计算正常工作时的平均值
            # search_value = interface_find_mean_value(instrName, save_path)
            # 判断是否有反复下电
            num = interface_search_num(instrName, f'CH{i}', 'RISE', 0.5)
            """
            start_position = interface_search_edge_num(instrName, f'CH{i}', 'RISE', search_value)
            num = start_position['num']
            start_point = start_position['ref_position']
            """
            if num > 0:
                print("反复下电：", ch_label[i-1])
                # 计算拐点的位置和波形的幅值，幅值,保存到列表ch_Value中，波形拐点,保存到列表knee_position中
                # point_position = interface_knee_point_fall(instrName, save_path, start_point)
            point_position = interface_knee_point_fall(instrName, save_path)
        ch_Value.append(point_position['v_value'])
        knee_position.append(point_position['knee_position'])
        print(result)
        print(point_position)

    # 根据计算出的拐点，设置光标位置,保存图片
    for i in range(3):
        position_a = knee_position[i]
        position_b = knee_position[i+1]
        # interface_adjust_scale(instrName, position_a, position_b)
        cursor_return = interface_set_cursor_wave(instrName, f'CH{i+1}', knee_position[i], knee_position[i+1])
        print(ch_label[i] + "-" + ch_label[i+1] + ':', cursor_return['delta'])
        if flag == "POWER ON":
            if knee_position[i] < knee_position[i + 1]:
                print("上电时序为：", ch_label[i] + ">" + ch_label[i + 1])
            else:
                print("上电时序错误")
        if flag == "POWER OFF":
            if knee_position[i+1] < knee_position[i]:
                print("下电时序为：", ch_label[i+1] + ">" + ch_label[i])
            else:
                print("下电时序错误")
        pic_path = r'F:\test1'
        if flag == "POWER ON":
            file_name = pic_path + "\\" + ch_label[i] + "-" + ch_label[i + 1] + '(poweron)' + '.png'
        if flag == "POWER OFF":
            file_name = pic_path + "\\" + ch_label[i+1] + "-" + ch_label[i] + '(poweroff)' + '.png'
        filename = interface_save_screen(instrName, file_name)

    """
    ch_arr = ['CH1', 'CH2', 'CH3', 'CH4']
    ch_label = ['V1', 'V2', 'V3', 'V4']
    save_path = 'F:/test1/123.csv'
    point_position = interface_knee_point_rise(instrName, save_path)
    ch_Value = point_position['v_value']
    knee_position = point_position['knee_position']
    print(point_position)
    # print(ch_Value)
    # print(knee_position)
    if ch_Value > 3.5:
        interface_set_scale(instrName, 'CH1', 2)
    elif ch_Value < 1.8:
        interface_set_scale(instrName, 'CH1', 0.5)
    else:
        interface_set_scale(instrName, 'CH1', 1)
    cursor_return = interface_set_cursor_wave(instrName, 'CH1', knee_position, knee_position)
    pic_path = r'F:\test1'
    file_name = pic_path + "\\" + ch_label[0] + "-" + ch_label[0] + '.png'
    filename = interface_save_screen(instrName, file_name)
    """
    """
    data = pd.read_csv(save_path)
    data.columns = ['time', 'voltage']
    v_max = max(data['voltage'])
    data = data.apply(pd.to_numeric, errors='coerce')
    data1 = data.drop_duplicates(subset=['voltage'])
    data2 = data1[data1['voltage'] >= (0.1 * v_max)]
    data3 = data2.iloc[0, [0, 1]]
    knee_position = data3["time"]
    print(v_max)
    print(data3)
    print(knee_position)
    """
















