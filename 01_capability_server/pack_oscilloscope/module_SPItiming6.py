# coding=utf-8
import datetime
import os
from pack_oscilloscope.base.common_TekMDO3054 import TekMDO3054


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
        return instrName
    except Exception as err:
        return str(err)


def interface_set_cursor(instrName, cursor_source, position_horizontal1, position_horizontal2, position1, position2):
    """
       设置示波器光标的水平和垂直位置
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


def interface_set_trigger(instrName, trigger_type, trigger_ch, trigger_level, horizontal_delay):
    """
        设置示波器的触发方式
        :param instrName:示波器的ID
        :param trigger_type: 设置示波器的触发类型
        :param trigger_ch: 设置示波器的触发通道（如，CH1）
        :param trigger_level: 设置触发电平
        :param horizontal_delay: 设置触发位置
        :return:示波器ID
        """
    try:
        tek = TekMDO3054(instrName)
        tek.set_trigger(trigger_type, trigger_ch, trigger_level, horizontal_delay)
        return instrName
    except Exception as err:
        return str(err)


def interface_set_trigger_mode(instrName, acquire_type):
    """
    设置是single还是run/stop模式，
    :param instrName: 示波器ID
    :param acquire_type: acquire_type=SEQUENCE为single，acquire_type=RUNSTOP为run/sto
    :return:示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        tek.set_trigger_mode(acquire_type)
        return instrName
    except Exception as err:
        return str(err)


def interface_set_search(instrName, ch, search_type, search_level):
    """
    设置搜索条件，返回搜索值
    :param instrName: 示波器ID
    :param ch: 搜索的源（如，CH1）
    :param search_type:搜索的类型（上升沿、下降沿或任意边沿）
    :param search_level: 搜索的阈值
    :return: query_search:示波器ID和搜索值
    """
    try:
        tek = TekMDO3054(instrName)
        query_search = tek.set_search(ch,  search_type, search_level)
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


if __name__ == '__main__':
    instrName = "TCPIP::" + "169.254.8.23" + "::INSTR"
    OsDevice = interface_initial(instrName)
    interface_set_record_length(instrName, 5.0E6)
    ch_arr = 'CH1,CH2,CH3,CH4'
    ch_label = 'CS,CLK,MISO,MOSI'
    interface_ch_set(instrName, ch_arr, ch_label)
    # 关闭用不到的通道
    interface_close_ch(instrName, "CH1")
    interface_close_ch(instrName, "CH4")
    # 设置时基
    interface_set_horizontal_scale(instrName, 40E-9)
    # 调用set_trigger函数设置触发类型
    interface_set_trigger(instrName, "FALL", "CH3", 0.64, 250E-9)
    # 设置为单次触发
    interface_set_trigger_mode(instrName, "SEQUENCE")
    # 搜索通道4标记点的位置坐标,调用search_position函数实现
    mark_position1 = interface_set_search(instrName, "CH2", "RISE", 1.26)
    # 搜索通道2标记点的位置坐标
    mark_position2 = interface_set_search(instrName,  "CH3", "RISE", 1.26)
    # 调用timing_position函数获得光标a和光标b的位置坐标
    position_return = interface_timing_position2(instrName, mark_position1['query'], mark_position2['query'], 40E-9)
    position_a = position_return['position_a']
    position_b = position_return['position_b']
    horizontal_position = float((position_a + position_b) / 2)
    interface_delay_horizontal(instrName, horizontal_position)
    cursor_return = interface_set_cursor(instrName, "CH2", 1.26, 3.26, position_a, position_b)
    # 保存图片
    delta = position_return['max_delta']
    cursor_delta = cursor_return['delta']
    delta = round((delta * 10 ** 9), 2)
    cursor_delta = round((cursor_delta * 10 ** 9), 2)
    if abs(delta - cursor_delta) < 1:
        pic_path = r'E:\test1'
        filename = pic_path + "\\" + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + '.png'
        filename = interface_save_screen(instrName, filename)
        print(filename)



