# coding=utf-8
import time
import datetime
import sys
from charset_normalizer import detect
import pandas
import os
import pack_oscilloscope.base.spi_signal_quality as OpCsv
import pack_oscilloscope.module_TEKMDO3054_SPItiming as MTS
import pack_oscilloscope.base.scene_library as Scene
from pack_oscilloscope.base.common_TekMDO3054 import TekMDO3054
from pack_oscilloscope.base import spi_signal_quality

def interface_set_PowerSource(instrName, OLEDTest, CH_ARR, ch_label, trigger_type, trigger_ch):
    """
     设置示波器各个通道的标签和位置 (适用： 电源上电 | 电源下电)
     :param instrName: 示波器ID
     :param OLEDTest: 测试项
     :param CH_ARR: 通道
     :param ch_label: 通道标签
     :param trigger_type: 触发类型
     :param trigger_ch: 触发通道
     :return:
     """
    if OLEDTest == '电源上电':
        if ch_label == 'ELVDD,' or ch_label == 'ELVSS,':
            scale_list = [1, 1, 1, 5]  # 各通道的垂直刻度
        else:
            scale_list = [0.5, 0.3, 1, 2]  # 各通道的垂直刻度
        position_list_a = [-0.5, -1, -1.5, -2]  # VDDR|VDDI|VCI|AVDD 各通道的垂直位置
        if ch_label == 'ELVDD,':
            position_list_b = [-0.9, 3, 0, 0]  # ELVDD 各通道的垂直位置
        else:
            position_list_b = [3, 3, 0, 0]  # ELVSS 各通道的垂直位置
    else:
        if ch_label == 'ELVDD,':
            scale_list = [1, 1, 2, 5]  # 各通道的垂直刻度
        else:
            scale_list = [0.5, 0.3, 1, 2]  # 各通道的垂直刻度
        position_list_a = [-0.2, -1.3, -0.72, -1.48]  # VDDR|VDDI|VCI|AVDD 各通道的垂直位置
        if ch_label == 'ELVDD,':
            position_list_b = [-1, -3, 0, 0]  # ELVDD 各通道的垂直位置
        else:
            position_list_b = [3, -3, 0, 0]   # ELVSS 各通道的垂直位置


    OsDevice = MTS.interface_initial(instrName)
    MTS.interface_start_acquisitions(instrName)
    MTS.interface_set_record_length(instrName, 5.0E6)

    interface_clear_measure(instrName)        #  删除所有测量项；

    if ch_label[0] == 'V':
        interface_ch_OLEDset(instrName, CH_ARR, position_list_a, ch_label, scale_list)                # [VDDR-->AVDD]信号初步进行示波器信号通道垂直位置等的设置
    else:
        interface_ch_OLEDset(instrName, CH_ARR, position_list_b, ch_label, scale_list)                # [ELVDD|ELVSS]信号通道垂直位置的设置
    # 设置示波器水平时基为20ms/div
    MTS.interface_set_horizontal_scale(instrName, 20.0E-3)
    if ch_label[0] == 'E':
        MTS.interface_open_ch(instrName, "CH1")
        MTS.interface_close_ch(instrName, "CH2")
        MTS.interface_close_ch(instrName, "CH3")
        MTS.interface_close_ch(instrName, "CH4")
    if ch_label[-2] == 'S':
        # 设置示波器触发类型
        MTS.interface_set_trigger(instrName, trigger_type, trigger_ch, -0.3, 0)
    else:
        # 设置示波器触发类型
        MTS.interface_set_trigger(instrName, trigger_type, trigger_ch, 0.3, 0)
    # 设置示波器触发模式（单次）
    MTS.interface_set_trigger_mode(instrName, "SEQUENCE")

def interface_set_DriveIC_DCDC(instrName, OLEDTest, CH_ARR, ch_label):
    """
     设置示波器各个通道的标签和位置 (适用： 驱动IC上电 | 驱动IC下电 | DCDC上下电)
     :param instrName: 示波器ID
     :param OLEDTest: 测试项
     :return:
     """
    OsDevice = MTS.interface_initial(instrName)
    interface_set_Factory(instrName)
    MTS.interface_start_acquisitions(instrName)
    MTS.interface_set_record_length(instrName, 5.0E6)
    scale_list_a = [1, 0.5, 2, 1]             #  驱动IC各通道的垂直刻度 1@VDDI_2@VDDR_3@VCI_4@LCDRST
    scale_list_b = [2, 1, 1, 0.5]             #  驱动IC各通道的垂直刻度 1@MIPI_2@VDDR_3@VCI_4@LCDRST
    scale_list_c = [1, 1, 2, 1]               #  DCDC各通道的垂直刻度 1@AS_2@ES_3@ELVDD_4@ELVSS
    if "驱动" in OLEDTest:
        position_list = [1, 0, -1, -2]            #  [驱动IC]各通道的水平位置
    else:
        position_list = [1, 0, -1, -0.3]            #  [DCDC]各通道的水平位置
    if ch_label[1] == 'D':
        interface_ch_OLEDset(instrName, CH_ARR, position_list, ch_label, scale_list_a)
    elif ch_label[1] == 'C':
        interface_ch_OLEDset(instrName, CH_ARR, position_list, ch_label, scale_list_b)
    else:
        interface_ch_OLEDset(instrName, CH_ARR, position_list, ch_label, scale_list_c)
    # 设置示波器水平时基为400ms/div
    MTS.interface_set_horizontal_scale(instrName, 400.0E-3)
    # 设置示波器余晖状态为 OFF
    interface_Set_PERSistence_status(instrName, "OFF")
    # 设置示波器屏幕亮度为 100
    interface_set_DisplayIntensity(instrName, 100)
    # 设置示波器触发模式（滚动模式）
    # MTS.interface_set_trigger_mode(instrName, "RUNSTOP")

    # 设置示波器停止采集波形
    # interface_set_StopAcquire(instrName)
    # 保存各测试项波形图片
    pic_path = r'E:\test1'
    if OLEDTest == '驱动IC上电':
        if ch_label[1] == 'D':
            filename = pic_path + "\\" + 'boot_1@VDDI_2@VDDR_3@VCI_4@LCDRST' + '.png'
            filename = MTS.interface_save_screen(instrName, filename)
        else:
            filename = pic_path + "\\" + 'boot_1@MIPI_2@VDDR_3@VCI_4@LCDRST' + '.png'
            filename = MTS.interface_save_screen(instrName, filename)
    elif OLEDTest == '驱动IC下电':
        if ch_label[1] == 'D':
            filename = pic_path + "\\" + 'shutdown_1@VDDI_2@VDDR_3@VCI_4@LCDRST' + '.png'
            filename = MTS.interface_save_screen(instrName, filename)
        else:
            filename = pic_path + "\\" + 'shutdown_1@MIPI_2@VDDR_3@VCI_4@LCDRST' + '.png'
            filename = MTS.interface_save_screen(instrName, filename)
    elif OLEDTest == 'DCDC上电':
        filename = pic_path + "\\" + 'Screen On_1@AS_2@ES_3@ELVDD_4@ELVSS' + '.png'
        filename = MTS.interface_save_screen(instrName, filename)
    else:
        filename = pic_path + "\\" + 'Screen Off_1@AS_2@ES_3@ELVDD_4@ELVSS' + '.png'
        filename = MTS.interface_save_screen(instrName, filename)

def interface_set_StopDrive(instrName):
    # 设置示波器停止采集波形
    interface_set_StopAcquire(instrName)

def interface_set_DriveIC_DCDC_test(instrName, OLEDTest, CH_ARR, ch_label):
    """
     设置示波器各个通道的标签和位置 (适用： 驱动IC上电 | 驱动IC下电 | DCDC上下电)
     :param instrName: 示波器ID
     :param OLEDTest: 测试项
     :return:
     """
    OsDevice = MTS.interface_initial(instrName)
    interface_set_Factory(instrName)
    MTS.interface_start_acquisitions(instrName)
    MTS.interface_set_record_length(instrName, 5.0E6)
    scale_list_a = [1, 0.5, 2, 1]             #  驱动IC各通道的垂直刻度 1@VDDI_2@VDDR_3@VCI_4@LCDRST
    scale_list_b = [2, 1, 1, 0.5]             #  驱动IC各通道的垂直刻度 1@MIPI_2@VDDR_3@VCI_4@LCDRST
    scale_list_c = [1, 1, 2, 2]               #  DCDC各通道的垂直刻度 1@AS_2@ES_3@ELVDD_4@ELVSS
    position_list = [1, 0, -1, -2]            #  各通道的水平位置
    if ch_label[1] == 'D':
        interface_ch_OLEDset(instrName, CH_ARR, position_list, ch_label, scale_list_a)
    elif ch_label[1] == 'C':
        interface_ch_OLEDset(instrName, CH_ARR, position_list, ch_label, scale_list_b)
    else:
        interface_ch_OLEDset(instrName, CH_ARR, position_list, ch_label, scale_list_c)
    # 设置示波器水平时基为400ms/div
    MTS.interface_set_horizontal_scale(instrName, 400.0E-3)
    # 设置示波器余晖状态为 OFF
    interface_Set_PERSistence_status(instrName, "OFF")
    # 设置示波器屏幕亮度为 100
    interface_set_DisplayIntensity(instrName, 100)
    # 设置示波器触发模式（滚动模式）
    MTS.interface_set_trigger_mode(instrName, "RUNSTOP")

    # 保存各测试项波形图片
    # pic_path = r'E:\test1'
    # if OLEDTest == '驱动IC上电':
    #     if ch_label[1] == 'D':
    #         filename = pic_path + "\\" + 'boot_1@VDDI_2@VDDR_3@VCI_4@LCDRST' + '.png'
    #         filename = MTS.interface_save_screen(instrName, filename)
    #     else:
    #         filename = pic_path + "\\" + 'boot_1@MIPI_2@VDDR_3@VCI_4@LCDRST' + '.png'
    #         filename = MTS.interface_save_screen(instrName, filename)
    # elif OLEDTest == '驱动IC下电':
    #     if ch_label[1] == 'D':
    #         filename = pic_path + "\\" + 'shutdown_1@VDDI_2@VDDR_3@VCI_4@LCDRST' + '.png'
    #         filename = MTS.interface_save_screen(instrName, filename)
    #     else:
    #         filename = pic_path + "\\" + 'shutdown_1@MIPI_2@VDDR_3@VCI_4@LCDRST' + '.png'
    #         filename = MTS.interface_save_screen(instrName, filename)
    # elif OLEDTest == 'DCDC上电':
    #     filename = pic_path + "\\" + 'Screen On_1@AS_2@ES_3@ELVDD_4@ELVSS' + '.png'
    #     filename = MTS.interface_save_screen(instrName, filename)
    # else:
    #     filename = pic_path + "\\" + 'Screen Off_1@AS_2@ES_3@ELVDD_4@ELVSS' + '.png'
    #     filename = MTS.interface_save_screen(instrName, filename)

def interface_set_Stopacquire(instrName):
    # 设置示波器停止采集波形
    interface_set_StopAcquire(instrName)

def interface_set_Factory(instrName):
    """
     恢复示波器默认设置，相等于 点击示波器 （Default Setup）按钮
     :param instrName: 示波器ID
     :return:
    """
    tek = TekMDO3054(instrName)
    tek.default_setup()

def interface_ch_OLEDset(instrName, ch_list, position_list, label_list, scale_list):
    """
    设置示波器各个通道的标签和位置等（初步设置，确认波形的正确）
    :param instrName: 示波器ID
    :param ch_list: 通道号列表
    :param label_list: 标签列表
    :return:示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        tek.ch_OLEDdset(ch_list, position_list, label_list, scale_list)
        return instrName
    except Exception as err:
        return str(err)

def interface_set_position(instrName, ch, vertical_position ):
    """
    设置示波器各通道的水平位置
   :param instrName: 波形文件保存路径
   :param ch: 示波器通道
   :param vertical_position: 水平刻度值
   :return:
   """
    try:
        tek = TekMDO3054(instrName)
        tek.set_position(ch, vertical_position)
    except Exception as err:
        return str(err)

def interface_clear_measure(instrName):
    """
    清除所有的测量项
    :param instrName: 示波器ID
    :return:
    """
    try:
        tek = TekMDO3054(instrName)
        tek.clear_Measure_type()
        return instrName
    except Exception as err:
        return str(err)

def interface_change_time_set(instrName, change_type, ch, source_num=0):
    """
    设置示波器，添加测量项
    @param instrName: 示波器ID
    @param change_type: 需要添加设置的测量项，高：HIGH / 低：LOW / 上升：RISe / 下降：FALL
    @return: 示波器ID
    """
    # change_time_new 示波器显示上升/下降沿上下电测量时间,返回测量值
    try:
        tek = TekMDO3054(instrName)
        tek.change_time_set(change_type, ch, source_num)
        return instrName
    except Exception as err:
        return str(err)

def interface_get_MEASUrement_data(instrName):
    """
    获取测量项的测量结果值
    :return: 示波器ID
    """
    MEASUrement_type = ["HIGH", "LOW"]
    try:
        tek = TekMDO3054(instrName)
        res = tek.get_MEASUrement_data(MEASUrement_type)
        return res
    except Exception as err:
        return str(err)

def interface_get_RiseEdge(save_path, min_per, max_per):
    """
    通过的CSV文件获取通道中间 10% 和 90% 两个点的time；(使用电源上电测试项)
    :param save_path: 波形文件保存路径
    :param testChName: 通道的标签
    :param low: 高电平*10%
    :param high: 高电平*90%
    :return: 触发沿数据：data_analyse
    """
    df = OpCsv.read_data(save_path)
    df.columns = ["Time", "Vel"]
    data = df.apply(pandas.to_numeric, errors='coerce')  # 将所有字符串转为数字

    max_vel = data["Vel"].max()  # CSV文件Vel最大值
    min_vel = data["Vel"].min()  # CSV文件Vel最小值
    num_long = max_vel - min_vel  # CSV文件Vel最大值 与 最小值之间的距离
    low_point = num_long * min_per + min_vel   # 低电平点位
    high_point = num_long * max_per + min_vel  # 高电平点位

    data_analyse_a = data[(data.Vel < low_point)]
    data_analyse_b = data[(data.Vel > high_point)]

    horizontala = data_analyse_a.iloc[-1]['Time']
    horizontalb = data_analyse_b.iloc[0]['Time']
    return (horizontala, horizontalb)

def interface_get_FallEdge(save_path, min_per, max_per):
    """
    通过的CSV文件获取通道中间 10% 和 90% 两个点的time；(使用电源上电测试项)
    :param save_path: 波形文件保存路径
    :param testChName: 通道的标签
    :param low: 高电平*10%
    :param high: 高电平*90%
    :return: 触发沿数据：data_analyse
    """
    df = OpCsv.read_data(save_path)
    df.columns = ["Time", "Vel"]
    data = df.apply(pandas.to_numeric, errors='coerce')  # 将所有字符串转为数字

    max_vel = data["Vel"].max()  # CSV文件Vel最大值
    min_vel = data["Vel"].min()  # CSV文件Vel最小值
    num_long = max_vel - min_vel  # CSV文件Vel最大值 与 最小值之间的距离
    low_point = num_long * min_per + min_vel   # 低电平点位
    high_point = num_long * max_per + min_vel  # 高电平点位

    data_analyse_a = data[(data.Vel > high_point)]
    data_analyse_b = data[(data.Vel < low_point)]

    horizontala = data_analyse_a.iloc[-1]['Time']
    horizontalb = data_analyse_b.iloc[0]['Time']
    return (horizontala, horizontalb)

def interface_data_caul(instrName, ch, save_path):
    """
    获取1个通道的波形数据保存为CSV文件；
    :param instrName: 示波器ID
    :param save_path: 波形文件保存路径
    :return: 提示语：保存CSV文件是否成功： res
    """
    print("开始获取波纹数据！")
    try:
        tek = TekMDO3054(instrName)
        res = tek.data_caul(ch)
        rel = tek.save_data_list(res, save_path)
        return rel
    except Exception as err:
        return str(err)

def interface_set_simcursor(instrName, cursor_source, position_horizontal1, position_horizontal2 ):
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
        delta_timing = tek.set_cursor_wave(cursor_source, position_horizontal1, position_horizontal2)
        cursor_value = {}
        cursor_value['instrName'] = instrName
        cursor_value['delta'] = delta_timing
        return cursor_value
    except Exception as err:
        return str(err)

def interface_adjust_scale(instrName, pos_a, pos_b, siterate):
    """
    根据计算出的光标要卡的位置对波形进行缩放
    :param instrName:
    :param pos_a:计算出的a光标放置的位置
    :param pos_b:计算出的b光标放置的位置
    :return:
    """
    try:
        pos_a = float(pos_a)
        pos_b = float(pos_b)
        tek = TekMDO3054(instrName)
        zoom_point = float((pos_a+pos_b)/2)     #  缩放的位置
        delta = float(abs(pos_a - pos_b))       #  缩放的比例
        old_scale = tek.query_horsacle()
        if delta < float(old_scale):            #  判读当前屏幕是否需要缩放
            zoom_scale = float(delta)
        if siterate:
            tek.set_SIM_PositionRateZoom(zoom_point, zoom_scale)
        else:
            tek.set_SIM_zoom(zoom_point, zoom_scale)
    except Exception as err:
        return str(err)


def interface_part_adjust_scale(instrName, pos_a, pos_b, k, siterate):
    """
    根据计算出的光标要卡的位置并对波形进行局部缩放 [缩放比例剩倍数-达到局部缩放]
    :param instrName:
    :param pos_a:计算出的a光标放置的位置
    :param pos_b:计算出的b光标放置的位置
    :return:
    """
    try:
        pos_a = float(pos_a)
        pos_b = float(pos_b)
        tek = TekMDO3054(instrName)
        zoom_point = float((pos_a+pos_b)/2)     #  缩放的位置
        delta = float(abs(pos_a - pos_b)*k)       #  缩放的比例 * 6
        old_scale = tek.query_horsacle()
        if delta < float(old_scale):            #  判读当前屏幕是否需要缩放
            zoom_scale = float(delta)
        if siterate:
            tek.set_SIM_PositionRateZoom(zoom_point, zoom_scale)
        else:
            tek.set_SIM_zoom(zoom_point, zoom_scale)
    except Exception as err:
        return str(err)


def interface_check_back(csv_path, base: float, top: float):
    """
    判断回勾
    :param csv_path: 文件路径
    :param base: 低电平位置
    :param top: 高电平位置
    :return: 返回回勾数据
    """
    check_res = spi_signal_quality.SpiSignalQuality()
    res = check_res.check_back(csv_path, base, top)  # 传进获取的高、低电平值
    return res

def interface_check_step(csv_path, base, top, threshold):
    """
    判断台阶
    :param csv_path: 文件路径
    :param base: 低电平位置
    :param top: 高电平位置
    :param threshold: 低于阈值才算台阶
    :return: 台阶数据
    """
    check_step = spi_signal_quality.SpiSignalQuality()
    check_res = check_step.check_step(csv_path, float(base), float(top), threshold)
    # print(check_res)
    return check_res

def interface_set_DisplayIntensity(instrName,intensity):
    """
    示波器波形亮度的调节开关
    :param instrName: 示波器ID
    :param intensity: 需要设置的显示强度百分比值（值得范围：1-100）
    :return:
    """
    tek = TekMDO3054(instrName)
    tek.set_display_intensity(intensity)

def interface_set_StopAcquire(instrName):
    """
   示波器波形停止采集开关 (Run/Stop按钮)
   :param instrName: 示波器ID
   :return:
   """
    tek = TekMDO3054(instrName)
    tek.set_acquisitions_stop()

    def interface_secondpoint(querylist):
        """
        获取通道的第二个触发沿数据；
        :param querylist: 波形query字符串
        :return: 第二个触发沿数据： string
        """
        A = []
        i, m = 0, 0
        if querylist.count(";") >= 2:
            for a in querylist:
                m = m + 1
                if a == ";":
                    i = i + 1
                    A.append(m)
                if i == 2:
                    break
            secondpoint = querylist[A[0]:A[1] - 1]
        else:
            for a in querylist:
                m = m + 1
                if a == ";":
                    A.append(m)
                    break
            secondpoint = querylist[A[0]:-1]
        print(secondpoint)
        return secondpoint

def interface_Set_PERSistence_status(instrName, status):
    """
      设置示波器余晖状态
      :param status: {CLEAR|AUTO|INFInite|OFF}
      :return: None
      """
    tek = TekMDO3054(instrName)
    tek.set_persistence_status(status)

def interface_ClockStoptiming_position1(instrName, position_list_all):
    """
    找出满足时序要求的光标位置（两个通道的第一个上升沿）
    :param instrName:示波器的ID
    :param position_list1:第一个通道的位置坐标列表
    :param position_list2:第二个通道的位置坐标列表
    :return:cursor_position：垂直光标差值(min),光标a的垂直位置,光标b的垂直位置
    """
    try:
        tek = TekMDO3054(instrName)
        cursor_simposition = tek.SIMCardtiming_positionAll(position_list_all)
        cursor_position = {}
        cursor_position['instrName'] = instrName
        print(len(cursor_simposition))
        if len(cursor_simposition) == 1:
            cursor_position['position_a'] = cursor_simposition[0]
        if len(cursor_simposition) == 2:
            cursor_position['position_a'] = cursor_simposition[0]
            cursor_position['position_b'] = cursor_simposition[1]
        if len(cursor_simposition) == 3:
            cursor_position['position_a'] = cursor_simposition[0]
            cursor_position['position_b'] = cursor_simposition[1]
            cursor_position['position_c'] = cursor_simposition[2]
        elif len(cursor_simposition) == 4:
            cursor_position['position_a'] = cursor_simposition[0]
            cursor_position['position_b'] = cursor_simposition[1]
            cursor_position['position_c'] = cursor_simposition[2]
            cursor_position['position_d'] = cursor_simposition[3]
        return cursor_position
    except Exception as err:
        return str(err)

def interface_get_continuelevel(path):
    """
    读取波形csv，返回波形中相邻间隔最大的两个point的time
    :param csv_path:
    :return: horizontal_position_a，horizontal_position_b
    """
    with open(path, 'rb+') as fp:
        content = fp.read()
        encoding = detect(content)['encoding']
        # df = pandas.read_csv(csv_path, encoding=encoding)
        content = content.decode(encoding).encode('utf8')
        fp.seek(0)
        fp.write(content)
        # yield from asyncio.sleep(1)

    data = pandas.read_csv(path, encoding='utf8', low_memory=False)

    # 获取子表'坐标'和‘测试结果’列的数
    data.columns = ['time', 'voltage']  # 设置纵坐标
    data = data.apply(pandas.to_numeric, errors='coerce')  # 将所有字符串转为数字
    lower = data["voltage"].values.min()
    topper = data["voltage"].values.max()
    middle_value = (lower + topper)/2
    lower_point = middle_value - 0.3
    topper_point = middle_value + 0.3
    data = data[(data.voltage > lower_point) & (data.voltage < topper_point)]    # 获取voltage在(lower,topper)之间的所有数据
    data_a = data["time"].diff()                                     # data["time"]列相邻上下两行做差
    data_max = data_a.max()
    data["Time_diff"] = data_a                                       # 将做差后的列加到原数据中
    data.index = range(len(data))                                    # 重置data的索引
    horizontal_position_b = data["time"][data["Time_diff"].values == data_max].values        # 时间间隔最大的 上time值（b光标）
    time_min_index = data["time"][data["Time_diff"].values == data_max].index-1              # 时间间隔最大的 下time索引值
    horizontal_position_a = data.loc[time_min_index].time                                    # 时间间隔最大的 下time值（a光标）
    print(horizontal_position_a)
    print(horizontal_position_b)

    horizontal_position_a = float(horizontal_position_a)
    horizontal_position_b = float(horizontal_position_b)
    print(horizontal_position_a,horizontal_position_b)
    return (horizontal_position_a,horizontal_position_b)

def interface_PercentageVol_point(csv_path, volpoint, percentage):
    """
       通过的CSV文件获取通道最后一个点的 time；
       :param save_path: 波形文件保存路径
       :return: 触发沿数据：data_analyse
       """
    df = OpCsv.read_data(csv_path)
    df.columns = ["Time", "Vel"]
    data = df.apply(pandas.to_numeric, errors='coerce')  # 将所有字符串转为数字
    # 获取voltage在(lower,topper)之间的所有数据
    point = volpoint * percentage
    data_analyse = data[(data.Vel > point)]
    # data_mean = pandas.DataFrame(data_analyse).rolling(window=300).mean().dropna()
    horizontal = data_analyse.iloc[0]['Time']
    return horizontal

def interface_secondpoint(querylist):
        """
        获取通道的第二个触发沿数据；
        :param querylist: 波形query字符串
        :return: 第二个触发沿数据： string
        """
        A = []
        i, m = 0, 0
        if querylist.count(";") >= 2:
            for a in querylist:
                m = m + 1
                if a == ";":
                    i = i + 1
                    A.append(m)
                if i == 2:
                    break
            secondpoint = querylist[A[0]:A[1] - 1]
        else:
            for a in querylist:
                m = m + 1
                if a == ";":
                    A.append(m)
                    break
            secondpoint = querylist[A[0]:-1]
        print(secondpoint)
        return secondpoint

def interface_laststr(str1):
    """
    找出满足要求的最后一个边缘数据
    :param str1:所有字符集
    :return:Laststr：搜索通道的最后一个边缘数据
    """
    label_a = ';'
    m = str1.count(label_a)
    A = -1
    a = []
    for i in range(m):
        A = str1.find(label_a, A + 1, len(str1))
        a.append(A)
    Lastsrt = str1[a[-1] + 1:-1]
    return Lastsrt

def interface_lastsecondstr(str1):
    """
    找出满足要求的最后第二个边缘数据
    :param str1:所有字符集
    :return:lastsecondstr：搜索通道的最后第二个边缘数据
    """
    A,a = [0],0
    for i in str1:
        a+=1
        if i == ';':
            A.append(a)
    return (str1[A[-2]:A[-1]])

def interface_IConA_LCDRST(instrName, ch):
    """
    找出满足时序要求的所有LCDRST光标位置（使用于驱动IC上电波形1）
    :param instrName:示波器的ID
    :param ch:通道
    :return:position_return:所有光标time 位置集
    """
    mark_a = MTS.interface_set_search(instrName, ch, "FALL", 1)
    mark_b = MTS.interface_set_search(instrName, ch, "RISE", 1)
    # 截取 LCDRST-通道4的第 2 个上升沿为数据/第 1 个 [上升|下降] 数据
    if ";" in mark_b['query']:
        mark_c = interface_secondpoint(mark_b['query'])
    if ";" in mark_a['query']:
        mark_a['query'] = (mark_a['query'][:mark_a['query'].index(';')])
    if ";" in mark_b['query']:
        mark_b['query'] = (mark_b['query'][:mark_b['query'].index(';')])
    mark_all = []
    mark_all.append(mark_b['query'])        #  LCDRST第一个上升沿点
    mark_all.append(mark_a['query'])        #  LCDRST第一个下降沿点
    mark_all.append(mark_c)                 #  LCDRST第二个上升沿点
    position_return = interface_ClockStoptiming_position1(instrName, mark_all)
    return position_return

def interface_IConB_LCDRST(instrName, ch):
    """
    找出满足时序要求的所有LCDRST光标位置（使用于驱动IC上电波形2）
    :param instrName:示波器的ID
    :param ch:通道
    :return:position_return:所有光标time 位置集
    """
    # LCDRST 触发沿数据
    mark_fLCDRST = MTS.interface_set_search(instrName, ch, "FALL", 1)
    mark_rLCDRST = MTS.interface_set_search(instrName, ch, "RISE", 1)

    # 截取 LCDRST-通道3最后1个上升沿点数据
    if ";" in mark_rLCDRST['query']:
        lastRise_LCDRST = interface_laststr(mark_rLCDRST['query'])

    # 截取 LCDRST-通道3第1个上升沿点数据
    if ";" in mark_rLCDRST['query']:
        firstRise_LCDRST = (mark_rLCDRST['query'][:mark_rLCDRST['query'].index(';')])

    mark_all = []
    mark_all.append(lastRise_LCDRST)            #  LCDRST Last-Rise
    mark_all.append(firstRise_LCDRST)           #  LCDRST First-Rise
    position_all = interface_ClockStoptiming_position1(instrName, mark_all)
    return position_all

def interface_IConB_MIPI(instrName, ch, path):
    """
    找出满足时序要求的所有LCDRST光标位置（使用于驱动IC上电波形2）
    :param instrName:示波器的ID
    :param ch:通道
    :return:position_return:所有光标time 位置集
    """
    #  存放MIPI信号文件
    print(interface_data_caul(instrName, ch, path))

    df = OpCsv.read_data(path)
    df.columns = ["Time", "Vel"]
    data = df.apply(pandas.to_numeric, errors='coerce')  # 将所有字符串转为数字
    Vel_max = data["Vel"].max()
    Vel_min = data["Vel"].min()
    Vel_middle = (Vel_min + Vel_max)/2

    mark_fMIPI = MTS.interface_set_search(instrName, ch, "FALL", Vel_middle)
    mark_rMIPI = MTS.interface_set_search(instrName, ch, "RISE", Vel_middle)

    # 截取 MIPI-通道4的第1个下降沿点数据
    if ";" in mark_fMIPI['query']:
        firstFall_MIPI = (mark_fMIPI['query'][:mark_fMIPI['query'].index(';')])

    # 截取 MIPI-通道4的第1个上升沿点数据
    if ";" in mark_rMIPI['query']:
        firstRise_MIPI = (mark_rMIPI['query'][:mark_rMIPI['query'].index(';')])
    mark_all = []
    mark_all.append(firstFall_MIPI)         #  MIPI-First-fall
    mark_all.append(firstRise_MIPI)         #  MIPI-First-rise
    position_all = interface_ClockStoptiming_position1(instrName, mark_all)

    #  获取MIPI通道中相邻最长的两个上升和下降沿数据

    t5_time = interface_get_continuelevel(path)
    #  将对应的time值存入 position_all 字典中
    position_all['position_c'] = t5_time[0]     #  MIPI-t5-Firstpoint
    position_all['position_d'] = t5_time[1]     #  MIPI-t5-Secondpoint

    return position_all

def interface_ICoff_LCDRST(instrName, ch):
    """
    找出满足时序要求的所有LCDRST光标位置（使用于驱动IC下电波形）
    :param instrName:示波器的ID
    :param ch:通道
    :return:position_return:所有光标time 位置集
    """
    # LCDRST 触发沿数据
    mark_fLCDRST = MTS.interface_set_search(instrName, ch, "FALL", 1)

    # 截取 LCDRST-通道4第1个上升沿点数据
    if ";" in mark_fLCDRST['query']:
        mark_fLCDRST['query'] = (mark_fLCDRST['query'][:mark_fLCDRST['query'].index(';')])

    mark_all = []
    mark_all.append(mark_fLCDRST['query'])            #  LCDRST First-Fall
    position_all = interface_ClockStoptiming_position1(instrName, mark_all)
    return position_all

def interface_ICoff_MIPI(instrName, ch):
    """
    找出满足时序要求的所有MIPI光标位置（使用于驱动IC上电波形2）
    :param instrName:示波器的ID
    :param ch:通道
    :return:position_return:所有光标time 位置集
    """
    mark_fMIPI = MTS.interface_set_search(instrName, ch, "FALL", 0.5)

    # 截取 MIPI-通道4最后第二个下降沿点数据
    if ";" in mark_fMIPI['query']:
        lastsecondFall_MIPI = interface_lastsecondstr(mark_fMIPI['query'])
    mark_all = []
    mark_all.append(lastsecondFall_MIPI)
    position_all = interface_ClockStoptiming_position1(instrName, mark_all)
    return position_all

def interface_DCDCon_ES(instrName, ch):
    """
    找出满足时序要求的所有ES光标位置（使用于DCDC上电波形）
    :param instrName:示波器的ID
    :param ch:通道
    :return:position_return:所有光标time 位置集
    """
    time_all = {}
    # ES 触发沿数据
    mark_rES = MTS.interface_set_search(instrName, ch, "RISE", 1)
    lastRise_ES = interface_laststr(mark_rES['query'])

    mark_rFirstES = (mark_rES['query'][:mark_rES['query'].index(';')])
    mark_all = []
    mark_all.append(mark_rFirstES)
    mark_all.append(lastRise_ES)

    position_all = interface_ClockStoptiming_position1(instrName, mark_all)
    time_all['ES_First_Rise'] = position_all['position_a']          #  ES-First-Rise
    time_all['ES_Last_Rise'] = position_all['position_b']           #  ES-Last-Rise

    # ES 周期内持续低|高电平数据
    stra = mark_rES['query']
    A, j = [0], 0
    for i in stra:
        j += 1
        if i == ";":
            A.append(j)
    strA = []
    for k in range(len(A) - 1):
        strA.append(stra[A[k]:A[k + 1]])
    mark_a = strA[20]
    mark_b = strA[21]
    mark_all = []
    mark_all.append(mark_a)
    mark_all.append(mark_b)
    position_all = interface_ClockStoptiming_position1(instrName, mark_all)
    time_a = float(position_all["position_a"])
    time_c = float(position_all["position_b"])
    time_b = (time_a + time_c) / 2
    time_ab = time_a + (time_b - time_a)*0.9  # 半周期内的 9/10位置 高电平
    time_cb = time_b + (time_c - time_b)*0.9  # 半周期内的 9/10位置 低电平

    time_all['ES_tHIGH_a'] = time_a
    time_all['ES_tHIGH_b'] = time_ab

    time_all['ES_tLOW_a'] = time_b
    time_all['ES_tLOW_b'] = time_cb
    return time_all

def interface_DCDCon_ELVSS(save_path):
    """
    找出满足时序要求的所有ELVSS光标位置（使用于DCDC上电波形）
    :param path  CSV文件存放路径
    :return:position_return:所需光标time
    """
    data = OpCsv.read_data(save_path)
    data.columns = ['Time', 'Vel']
    data = data.apply(pandas.to_numeric, errors='coerce')  # 将所有字符串转为数字
    Vel_min = data['Vel'].min()
    Vel_last = data.iloc[-1]['Vel']
    Vel_middle = Vel_min + (Vel_last-Vel_min)/2

    # if Vel_min < 0:
    #     Vel_min_point = Vel_min * 0.5
    # else:
    #     Vel_min_point = Vel_min * 1.1
    data_analy = data[(data.Vel < Vel_middle)]
    time = data_analy.iloc[-1]['Time']
    return time

def interface_DCDCoff_ES(instrName, ch):
    """
    找出满足时序要求的所有ES光标位置（使用于DCDC上电波形）
    :param instrName  示波器ID
    :param ch  通道
    :return:position_all:  所需光标time
    """
    # ES 触发沿数据
    mark_rES = MTS.interface_set_search(instrName, ch, "FALL", 1)
    if ';' in mark_rES['query']:
        mark_rES['query'] = (mark_rES['query'][:mark_rES['query'].index(';')])
    mark_all = []
    mark_all.append(mark_rES['query'])
    position_all = interface_ClockStoptiming_position1(instrName, mark_all)
    return position_all

# ------------------------------------------------------------ 场景接口 -------------------------------------------------------
def interface_set_PowerOnOff(item, scene):
    GS = Scene.GoScene()
    cc = GS.switch_test_item(item, scene)
    tt = Scene.GoScene()
    eval("tt." + cc)()

def adb_commond(scene):
    if scene == "亮屏":
        result = os.popen('adb shell "input keyevent 26"').read()
        result2 = os.popen('adb shell "input swipe 600 1800 600 500"').read()
    if scene == "亮灭屏":
        result = os.popen('adb shell "input keyevent 26"').read()
    if scene == "重启":
        result = os.popen('adb reboot').read()
    return result

def interface_set_BlankScreen(scene):
    GS = Scene.GoScene()
    cc = GS.switch_test_item("procedure", scene)
    return eval("GS." + cc)()


# ------------------------------------------------------------ 电源上电|下电信号 -------------------------------------------------------
def VDDI(instrName,OLEDTest):                 # 第1种情况执行的函数(默认执行函数)
    """
      VDDI电源|下电时序测试
     :param instrName: 示波器ID
     :param OLEDTest: 测试项
     :return:
    """
    if OLEDTest == "电源上电":
        print('VDDI电源上电测试')
    else:
        print('VDDI电源下电测试')
    MTS.interface_open_ch(instrName, "CH1")
    MTS.interface_close_ch(instrName, "CH2")
    MTS.interface_close_ch(instrName, "CH3")
    MTS.interface_close_ch(instrName, "CH4")
    # 删除所有测量项；
    interface_clear_measure(instrName)
    # 添加高、低、上升时间测量项；
    meter_list = {1: "HIGH", 2: "LOW", 3: "RISe"}
    for i in meter_list:
        interface_change_time_set(instrName, meter_list[i], 'CH1', i)
    path = f"E:\\test1\\VDDI.csv"
    print(interface_data_caul(instrName, 'CH1', path))
    # res_a = interface_check_back(path, low, high)  # 回沟判断
    # print(res_a)
    # res_b = interface_check_step(path, low, high, 0.01)  # 台阶判断
    # print(res_b)
    if OLEDTest == "电源上电":
        data = interface_get_RiseEdge(path, 0.15, 0.8)
    else:
        data = interface_get_FallEdge(path, 0.1, 0.9)
    time_a = float(data[0])
    time_b = float(data[1])
    interface_adjust_scale(instrName, time_a, time_b, siterate=False)
    cursor_data = interface_set_simcursor(instrName, 'CH1', time_a, time_b)
    return cursor_data
    # pic_path = r'E:\test1'
    # filename = pic_path + "\\" + 'PowerOn_VDDI' + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + '.png'
    # filename = MTS.interface_save_screen(instrName, filename)

def DVDD(instrName,OLEDTest):                 # 第2种情况执行的函数
    """
     DVDD电源上|下电时序测试
     :param instrName: 示波器ID
     :param OLEDTest: 测试项
     :return:
   """
    if OLEDTest == "电源上电":
        print('DVDD电源上电测试')
    else:
        print('DVDD电源下电测试')
    MTS.interface_open_ch(instrName, "CH2")
    MTS.interface_close_ch(instrName, "CH1")
    MTS.interface_close_ch(instrName, "CH3")
    MTS.interface_close_ch(instrName, "CH4")
    # 删除所有测量项；
    interface_clear_measure(instrName)
    # 添加高、低、上升时间测量项；
    meter_list = {1: "HIGH", 2: "LOW", 3: "RISe"}
    for i in meter_list:
        interface_change_time_set(instrName, meter_list[i], 'CH2', i)
    path = f"E:\\test1\\test2.csv"
    print(interface_data_caul(instrName, 'CH2', path))
    # res_a = interface_check_back(path, low, high)  # 回沟判断
    # print(res_a)
    # res_b = interface_check_step(path, low, high, 0.01)  # 台阶判断
    # print(res_b)
    if OLEDTest == "电源上电":
        data = interface_get_RiseEdge(path, 0.2, 0.8)
    else:
        data = interface_get_FallEdge(path, 0.1, 0.9)
    time_a = float(data[0])
    time_b = float(data[1])
    interface_adjust_scale(instrName, time_a, time_b, siterate=False)
    cursor_data = interface_set_simcursor(instrName, 'CH2', time_a, time_b)
    return cursor_data
    # pic_path = r'E:\test1'
    # filename = pic_path + "\\" + 'PowerOn_DVDD' + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + '.png'
    # filename = MTS.interface_save_screen(instrName, filename)

def VCI(instrName, OLEDTest):  # 第3种情况执行的函数
    """
     VCI上电时序测试（待定，可能VCI的所有相关测试整合）
     :param instrName: 示波器ID
     :return:
   """
    if OLEDTest == '电源上电':
        print('VCI电源上电测试')
    else:
        print('VCI电源下电测试')
    MTS.interface_open_ch(instrName, "CH3")
    MTS.interface_close_ch(instrName, "CH1")
    MTS.interface_close_ch(instrName, "CH2")
    MTS.interface_close_ch(instrName, "CH4")
    # 删除所有测量项；
    interface_clear_measure(instrName)
    # 添加高、低、上升时间测量项；
    meter_list = {1: "HIGH", 2: "LOW", 3: "RISe"}
    for i in meter_list:
        interface_change_time_set(instrName, meter_list[i], 'CH3', i)
    path = f"E:\\test1\\VCI.csv"
    print(interface_data_caul(instrName, 'CH3', path))
    # res_a = interface_check_back(path, low, high)  # 回沟判断
    # print(res_a)
    # res_b = interface_check_step(path, low, high, 0.01)  # 台阶判断
    # print(res_b)
    if OLEDTest == '电源上电':
        data = interface_get_RiseEdge(path, 0.15, 0.8)
    else:
        data = interface_get_FallEdge(path, 0.2, 0.8)
    time_a = float(data[0])
    time_b = float(data[1])
    interface_adjust_scale(instrName, time_a, time_b, siterate=False)
    cursor_data = interface_set_simcursor(instrName, 'CH3', time_a, time_b)
    return cursor_data
    # pic_path = r'E:\test1'
    # filename = pic_path + "\\" + 'PowerOn_VCI' + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + '.png'
    # filename = MTS.interface_save_screen(instrName, filename)

def AVDD(instrName, OLEDTest):  # 第4种情况执行的函数
    """
     AVDD上电时序测试（待定，可能AVDD的所有相关测试整合）
     :param instrName: 示波器ID
     :return:
   """
    if OLEDTest == "电源上电":
        print('AVDD电源上电测试')
    else:
        print('AVDD电源下电测试')
    MTS.interface_open_ch(instrName, "CH4")
    MTS.interface_close_ch(instrName, "CH1")
    MTS.interface_close_ch(instrName, "CH2")
    MTS.interface_close_ch(instrName, "CH3")
    # 删除所有测量项；
    interface_clear_measure(instrName)
    # 添加高、低、上升时间测量项；
    meter_list = {1: "HIGH", 2: "LOW", 3: "RISe"}
    for i in meter_list:
        interface_change_time_set(instrName, meter_list[i], 'CH4', i)
    path = f"E:\\test1\\AVDD.csv"
    print(interface_data_caul(instrName, 'CH4', path))
    # res_a = interface_check_back(path, low, high)        # 回沟判断
    # print(res_a)
    # res_b = interface_check_step(path, low, high, 0.01)  # 台阶判断
    # print(res_b)
    if OLEDTest == '电源上电':
        data = interface_get_RiseEdge(path, 0.2, 0.9)
    else:
        data = interface_get_FallEdge(path, 0.1, 0.9)
    time_a = float(data[0])
    time_b = float(data[1])
    interface_adjust_scale(instrName, time_a, time_b, siterate=False)
    cursor_data = interface_set_simcursor(instrName, 'CH4', time_a, time_b)
    return cursor_data
    # pic_path = r'E:\test1'
    # filename = pic_path + "\\" + 'PowerOn_AVDD' + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + '.png'
    # filename = MTS.interface_save_screen(instrName, filename)

def ELVDD(instrName, OLEDTest):                     # 第5种情况执行的函数
    """
     ELVDD上电时序测试（待定，可能ELVDD的所有相关测试整合）
     :param instrName: 示波器ID
     :return:
    """
    if OLEDTest == "电源上电":
        print('ELVDD驱动IC上电测试')
    else:
        print('ELVDD驱动IC下电测试')
    MTS.interface_open_ch(instrName, "CH1")
    MTS.interface_close_ch(instrName, "CH2")
    MTS.interface_close_ch(instrName, "CH3")
    MTS.interface_close_ch(instrName, "CH4")
    # 删除所有测量项；
    interface_clear_measure(instrName)
    # 添加高、低、上升时间测量项；
    meter_list = {1: "HIGH", 2: "LOW", 3: "RISe"}
    for i in meter_list:
        interface_change_time_set(instrName, meter_list[i], 'CH1', i)
    if OLEDTest == "电源上电":
        path = f"E:\\test1\\ELVDDon.csv"
    else:
        path = f"E:\\test1\\ELVDDoff.csv"
    #  保存通道1 ELVDD 的VSC文件
    print(interface_data_caul(instrName, 'CH1', path))
    # res_a = interface_check_back(path, low, high)        # 回沟判断
    # print(res_a)
    # res_b = interface_check_step(path, low, high, 0.01)  # 台阶判断
    # print(res_b)
    if OLEDTest == '电源上电':
        data = interface_get_RiseEdge(path, 0.05, 0.95)
    else:
        data = interface_get_FallEdge(path, 0.05, 0.95)
    time_a = float(data[0])
    time_b = float(data[1])
    interface_adjust_scale(instrName, time_a, time_b, siterate=False)
    cursor_data = interface_set_simcursor(instrName, 'CH1', time_a, time_b)
    return cursor_data
    # if OLEDTest == "电源上电":
    #     pic_path = r'E:\test1'
    #     filename = pic_path + "\\" + 'PowerOn_ELVDD' + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + '.png'
    #     filename = MTS.interface_save_screen(instrName, filename)
    # else:
    #     pic_path = r'E:\test1'
    #     filename = pic_path + "\\" + 'PowerOff_ELVDD' + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + '.png'
    #     filename = MTS.interface_save_screen(instrName, filename)

def ELVSS(instrName, OLEDTest):                # 第6种情况执行的函数
    """
     ELVSS上电时序测试（待定，可能ELVSS的所有相关测试整合）
     :param instrName: 示波器ID
     :return:
   """
    if OLEDTest == "电源上电":
        print('ELVDD驱动IC上电测试')
    else:
        print('ELVDD驱动IC下电测试')
    # 删除所有测量项；
    interface_clear_measure(instrName)
    # 添加高、低、上升时间测量项；
    meter_list = {1: "HIGH", 2: "LOW", 3: "RISe"}
    for i in meter_list:
        interface_change_time_set(instrName, meter_list[i], 'CH1', i)
    if OLEDTest == "电源上电":
        path = f"E:\\test1\\ELVSSon.csv"
    else:
        path = f"E:\\test1\\ELVSSoff.csv"
    print(interface_data_caul(instrName, 'CH1', path))
    # res_a = interface_check_back(path, low, high)        # 回沟判断
    # print(res_a)
    # res_b = interface_check_step(path, low, high, 0.01)  # 台阶判断
    # print(res_b)
    if OLEDTest == '电源上电':
        data = interface_get_FallEdge(path, 0.05, 0.95)
    else:
        data = interface_get_RiseEdge(path, 0.05, 0.95)
    time_a = float(data[0])
    time_b = float(data[1])
    print(time_a, time_b)
    interface_adjust_scale(instrName, time_a, time_b, siterate=False)
    cursor_data = interface_set_simcursor(instrName, 'CH1', time_a, time_b)
    return cursor_data

# ------------------------------------------------------------- 驱动IC上电|下电信号 -----------------------------------------------

def ton1(instrName, time_a, time_b):
    print('驱动IC上电测试VDDI90%--->VDDR10%')
    time_a = float(time_a)
    time_b = float(time_b)
    interface_adjust_scale(instrName, time_a, time_b, siterate=False)
    cursor_data = interface_set_simcursor(instrName, 'CH1', time_a, time_b)
    return cursor_data
    # pic_path = r'E:\test1'
    # filename = pic_path + "\\" + 'boot_1@VDDI_2@VDDR_3@VCI_4@LCDRST_ton1' + '.png'
    # filename = MTS.interface_save_screen(instrName, filename)

def ton2(instrName, time_a, time_b):
    print('驱动IC上电测试VDDR90%--->VCI10%')
    time_a = float(time_a)
    time_b = float(time_b)
    interface_adjust_scale(instrName, time_a, time_b, siterate=False)
    cursor_data = interface_set_simcursor(instrName, 'CH1', time_a, time_b)
    return cursor_data
    # pic_path = r'E:\test1'
    # filename = pic_path + "\\" + 'boot_1@VDDI_2@VDDR_3@VCI_4@LCDRST_ton2' + '.png'
    # filename = MTS.interface_save_screen(instrName, filename)

def t1(instrName, time_a, time_b):
    print('驱动IC上电测试VCI90%--->LCDRST0%')
    time_a = float(time_a)
    time_b = float(time_b)
    interface_adjust_scale(instrName, time_a, time_b, siterate=False)
    cursor_data = interface_set_simcursor(instrName, 'CH1', time_a, time_b)
    return cursor_data
    # pic_path = r'E:\test1'
    # filename = pic_path + "\\" + 'boot_1@VDDI_2@VDDR_3@VCI_4@LCDRST_t1' + '.png'
    # filename = MTS.interface_save_screen(instrName, filename)

def t4(instrName, time_a, time_b):
    print('驱动IC上电测试LCDRST持续低电平')
    time_a = float(time_a)
    time_b = float(time_b)
    interface_adjust_scale(instrName, time_a, time_b, siterate=False)
    cursor_data = interface_set_simcursor(instrName, 'CH1', time_a, time_b)
    return cursor_data
    # pic_path = r'E:\test1'
    # filename = pic_path + "\\" + 'boot_1@VDDI_2@VDDR_3@VCI_4@LCDRST_t4' + '.png'
    # filename = MTS.interface_save_screen(instrName, filename)

def t2(instrName, time_a, time_b):
    print('驱动IC上电测试LCDRST--->MIPI')
    time_a = float(time_a)
    time_b = float(time_b)
    interface_adjust_scale(instrName, time_a, time_b, siterate=False)
    cursor_data = interface_set_simcursor(instrName, 'CH1', time_a, time_b)
    return cursor_data
    # pic_path = r'E:\test1'
    # filename = pic_path + "\\" + 'boot_1@MIPI_2@VDDR_3@VCI_4@LCDRST_t2' + '.png'
    # filename = MTS.interface_save_screen(instrName, filename)

def t3(instrName, time_a, time_b):
    print('驱动IC上电测试VCI90%--->MIPI0%')
    time_a = float(time_a)
    time_b = float(time_b)
    interface_adjust_scale(instrName, time_a, time_b, siterate=False)
    cursor_data = interface_set_simcursor(instrName, 'CH1', time_a, time_b)
    return cursor_data
    # pic_path = r'E:\test1'
    # filename = pic_path + "\\" + 'boot_1@MIPI_2@VDDR_3@VCI_4@LCDRST_t3' + '.png'
    # filename = MTS.interface_save_screen(instrName, filename)

def t5(instrName, time_a, time_b):
    print('驱动IC上电测试MIPI持续高电平')
    time_a = float(time_a)
    time_b = float(time_b)
    interface_adjust_scale(instrName, time_a, time_b, siterate=False)
    cursor_data = interface_set_simcursor(instrName, 'CH1', time_a, time_b)
    return cursor_data
    # pic_path = r'E:\test1'
    # filename = pic_path + "\\" + 'boot_1@MIPI_2@VDDR_3@VCI_4@LCDRST_t5' + '.png'
    # filename = MTS.interface_save_screen(instrName, filename)

def tof1(instrName, time_a, time_b):
    print('驱动IC下电测试VDDR10%--->VDDI90%')
    time_a = float(time_a)
    time_b = float(time_b)
    interface_adjust_scale(instrName, time_a, time_b, siterate=False)
    cursor_data = interface_set_simcursor(instrName, 'CH1', time_a, time_b)
    return cursor_data
    # pic_path = r'E:\test1'
    # filename = pic_path + "\\" + 'Shutdown_1@VDDI_2@VDDR_3@VCI_4@LCDRST_tof1' + '.png'
    # filename = MTS.interface_save_screen(instrName, filename)

def tof2(instrName, time_a, time_b):
    print('驱动IC下电测试VCI10%--->VDDR90%')
    time_a = float(time_a)
    time_b = float(time_b)
    interface_part_adjust_scale(instrName, time_a, time_b, k=6, siterate=False)
    cursor_data = interface_set_simcursor(instrName, 'CH1', time_a, time_b)
    return cursor_data
    # pic_path = r'E:\test1'
    # filename = pic_path + "\\" + 'Shutdown_1@VDDI_2@VDDR_3@VCI_4@LCDRST_tof2' + '.png'
    # filename = MTS.interface_save_screen(instrName, filename)

def t12(instrName, time_a, time_b):
    print('驱动IC下电测试LCDRST0%--->VCI90%')
    time_a = float(time_a)
    time_b = float(time_b)
    interface_adjust_scale(instrName, time_a, time_b, siterate=False)
    cursor_data = interface_set_simcursor(instrName, 'CH1', time_a, time_b)
    return cursor_data
    # pic_path = r'E:\test1'
    # filename = pic_path + "\\" + 'Shutdown_1@VDDI_2@VDDR_3@VCI_4@LCDRST_t12' + '.png'

def t13(instrName, time_a, time_b):
    print('驱动IC下电测试MIPI--->LCDRST')
    time_a = float(time_a)
    time_b = float(time_b)
    interface_adjust_scale(instrName, time_a, time_b, siterate=False)
    cursor_data = interface_set_simcursor(instrName, 'CH1', time_a, time_b)
    return cursor_data
    # pic_path = r'E:\test1'
    # filename = pic_path + "\\" + 'Shutdown _1@MIPI_2@VDDR_3@VCI_4@LCDRST_t13' + '.png'
    # filename = MTS.interface_save_screen(instrName, filename)

def t14(instrName, time_a, time_b):
    print('驱动IC下电测试MIPI[Sleep-In]---> LCDRST')
    time_a = float(time_a)
    time_b = float(time_b)
    interface_adjust_scale(instrName, time_a, time_b, siterate=False)
    cursor_data = interface_set_simcursor(instrName, 'CH1', time_a, time_b)
    return cursor_data
    # pic_path = r'E:\test1'
    # filename = pic_path + "\\" + 'Shutdown _1@MIPI_2@VDDR_3@VCI_4@LCDRST_t14' + '.png'
    # filename = MTS.interface_save_screen(instrName, filename)

# ------------------------------------------------------------- DCDC上电|下电信号 --------------------------------------------------
def tINT(instrName, time_a, time_b):
    print('DCDC上电测试ES--->ELVDD ')
    time_a = float(time_a)
    time_b = float(time_b)
    interface_part_adjust_scale(instrName, time_a, time_b, k=6, siterate=False)
    cursor_data = interface_set_simcursor(instrName, 'CH1', time_a, time_b)
    return cursor_data
    # pic_path = r'E:\test1'
    # filename = pic_path + "\\" + 'ScreenOn_1@AS_2@ES_3@ELVDD_4@ELVSS_tINT' + '.png'
    # filename = MTS.interface_save_screen(instrName, filename)

def tSS1(instrName, time_a, time_b):
    print('DCDC上电测试ELVDD0%--->ELVDD100% ')
    time_a = float(time_a)
    time_b = float(time_b)
    interface_adjust_scale(instrName, time_a, time_b, siterate=False)
    cursor_data = interface_set_simcursor(instrName, 'CH1', time_a, time_b)
    return cursor_data
    # pic_path = r'E:\test1'
    # filename = pic_path + "\\" + 'ScreenOn_1@AS_2@ES_3@ELVDD_4@ELVSS_tSS1' + '.png'
    # filename = MTS.interface_save_screen(instrName, filename)

def tDELAY(instrName, time_a, time_b):
    print('DCDC上电测试ELVDD100%--->ELVDD100% ')
    time_a = float(time_a)
    time_b = float(time_b)
    interface_adjust_scale(instrName, time_a, time_b, siterate=False)
    cursor_data = interface_set_simcursor(instrName, 'CH1', time_a, time_b)
    return cursor_data
    # pic_path = r'E:\t est1'
    # filename = pic_path + "\\" + 'ScreenOn_1@AS_2@ES_3@ELVDD_4@ELVSS_tDELAY' + '.png'
    # filename = MTS.interface_save_screen(instrName, filename)

def tSS2(instrName, time_a, time_b):
    print('DCDC上电测试ELVSS100%--->ELVSS0% ')
    time_a = float(time_a)
    time_b = float(time_b)
    interface_adjust_scale(instrName, time_a, time_b, siterate=False)
    cursor_data = interface_set_simcursor(instrName, 'CH1', time_a, time_b)
    return cursor_data
    # pic_path = r'E:\test1'
    # filename = pic_path + "\\" + 'ScreenOn_1@AS_2@ES_3@ELVDD_4@ELVSS_tSS2' + '.png'
    # filename = MTS.interface_save_screen(instrName, filename)

def tHIGH(instrName, time_a, time_b):
    print('DCDC上电测试ES周期性高电平 ')
    time_a = float(time_a)
    time_b = float(time_b)
    interface_adjust_scale(instrName, time_a, time_b, siterate=False)
    cursor_data = interface_set_simcursor(instrName, 'CH1', time_a, time_b)
    return cursor_data
    # pic_path = r'E:\test1'
    # filename = pic_path + "\\" + 'ScreenOn_1@AS_2@ES_3@ELVDD_4@ELVSS_tHIGH' + '.png'
    # filename = MTS.interface_save_screen(instrName, filename)

def tLOW(instrName, time_a, time_b):
    print('DCDC上电测试ES周期性低电平 ')
    time_a = float(time_a)
    time_b = float(time_b)
    interface_adjust_scale(instrName, time_a, time_b, siterate=False)
    cursor_data = interface_set_simcursor(instrName, 'CH1', time_a, time_b)
    return cursor_data
    # pic_path = r'E:\test1'
    # filename = pic_path + "\\" + 'ScreenOn_1@AS_2@ES_3@ELVDD_4@ELVSS_tLOW' + '.png'
    # filename = MTS.interface_save_screen(instrName, filename)

def tSTORE(instrName, time_a, time_b):
    print('DCDC上电测试tES--->ELVSS')
    time_a = float(time_a)
    time_b = float(time_b)
    interface_part_adjust_scale(instrName, time_a, time_b, k=6, siterate=False)
    cursor_data = interface_set_simcursor(instrName, 'CH1', time_a, time_b)
    return cursor_data
    # pic_path = r'E:\test1'
    # filename = pic_path + "\\" + 'ScreenOn_1@AS_2@ES_3@ELVDD_4@ELVSS_tLOW' + '.png'
    # filename = MTS.interface_save_screen(instrName, filename)

def tOFF(instrName, time_a, time_b):
    print('DCDC下电测试tES--->ELVDD/ELVSS')
    time_a = float(time_a)
    time_b = float(time_b)
    interface_part_adjust_scale(instrName, time_a, time_b, k=6, siterate=False)
    cursor_data = interface_set_simcursor(instrName, 'CH1', time_a, time_b)
    return cursor_data
    # pic_path = r'E:\test1'
    # filename = pic_path + "\\" + 'Screen Off_1@AS_2@ES_3@ELVDD_4@ELVSS_tOFF' + '.png'
    # filename = MTS.interface_save_screen(instrName, filename)

def tDISCHG(instrName, time_a, time_b):
    print('DCDC下电测试ELVDD/ELVSS下电时间')
    time_a = float(time_a)
    time_b = float(time_b)
    interface_adjust_scale(instrName, time_a, time_b, siterate=False)
    cursor_data = interface_set_simcursor(instrName, 'CH1', time_a, time_b)
    return cursor_data
    # pic_path = r'E:\test1'
    # filename = pic_path + "\\" + 'Screen Off_1@AS_2@ES_3@ELVDD_4@ELVSS_ tDISCHG' + '.png'
    # filename = MTS.interface_save_screen(instrName, filename)


# if __name__ == '__main__':
#     adb_commond("重启")
#     instrName = "TCPIP::" + "169.254.8.23" + "::INSTR"
#     interface_part_adjust_scale(instrName, 0.6134616, 0.6134136, siterate=False)
#     interface_set_simcursor(instrName, 'CH1', 0.6134616, 0.6134136)
#     interface_set_BlankScreen("黑屏手势")
#     try:
#         instrName = "TCPIP::" + "169.254.8.23" + "::INSTR"
#         CH_ARR = 'CH1,CH2,CH3,CH4'
#         # 电源上下电 信号
#         CH_LABEL_A = 'VDDI,DVDD,VCI,AVDD'
#         CH_LABEL_DD = 'ELVDD,'
#         CH_LABEL_SS = 'ELVSS,'
#         # 驱动IC上下电 信号
#         CH_LABEL_C = 'VDDI,VDDR,VCI,LCDRST'
#         CH_LABEL_D = 'VCI,VDDR,LCDRST,MIPI'
#         # DCDC上下电 信号
#         CH_LABEL_E = 'AS,ES,ELVDD,ELVSS'
#
#         t_clock = ""          #待定变量
#         STANDARD_MIN_VOL = ''
#         STANDARD_MAX_VOL = ''
#         standard_Typ = ''
# # ------------------------------------------------------------- OLED时序测试 -----------------------------------------------
#         OLEDTest = "DCDC下电"
#         if OLEDTest == "电源上电":
#             interface_set_PowerSource(instrName, OLEDTest, CH_LABEL_A, trigger_type="RISE", trigger_ch="CH1")
#             VDDI(instrName, OLEDTest)
#             DVDD(instrName, OLEDTest)
#             VCI(instrName, OLEDTest)
#             AVDD(instrName, OLEDTest)
#
#             testtask = input("是否执行[ELVDD]测试任务：（Y|N）")
#             if testtask == "Y":
#                 interface_set_PowerSource(instrName, OLEDTest, CH_LABEL_DD, trigger_type="RISE", trigger_ch="CH1")
#                 ELVDD(instrName, OLEDTest)
#
#             testtask = input("是否执行[ELVSS]测试任务：（Y|N）")
#             if testtask == "Y":
#                 interface_set_PowerSource(instrName, OLEDTest, CH_LABEL_SS, trigger_type="FALL", trigger_ch="CH1")
#                 ELVSS(instrName, OLEDTest)
#
#         elif OLEDTest == "电源下电":
#             interface_set_PowerSource(instrName, OLEDTest, CH_ARR, CH_LABEL_A, trigger_type="FALL", trigger_ch="CH1")
#             VDDI(instrName, OLEDTest)
#             DVDD(instrName, OLEDTest)
#             VCI(instrName, OLEDTest)
#             AVDD(instrName, OLEDTest)
#
#             testtask = input("是否执行[ELVDD]测试任务：（Y|N）")
#             if testtask == "Y":
#                 interface_set_PowerSource(instrName, OLEDTest, CH_ARR, CH_LABEL_DD, trigger_type="FALL", trigger_ch="CH1")
#                 ELVDD(instrName, OLEDTest, time_all=None)
#             testtask = input("是否执行[ELVSS]测试任务：（Y|N）")
#             if testtask == "Y":
#                 interface_set_PowerSource(instrName, OLEDTest, CH_ARR, CH_LABEL_SS, trigger_type="RISE", trigger_ch="CH1")
#                 # ELVSS(instrName, OLEDTest)
#
#         elif OLEDTest == "驱动IC上电":
#             print("执行波形1：1@VDDI_2@VDDR_3@VCI_4@LCDRST测试任务：")
#             interface_set_Factory(instrName)
#             # interface_clear_measure(instrName)
#             interface_set_DriveIC_DCDC(instrName, OLEDTest, CH_LABEL_C)
#             testtask = input("确定驱动IC波形1是否正确！（Y|N）")
#             if testtask == "Y":
#                 time_all = interface_get_allposition_one(instrName)
#
#             testtask = input("是否执行波形2：1@MIPI_2@VDDR_3@ VCI _4@LCDRST测试任务：（Y|N）")
#             if testtask == "Y":
#                 interface_set_DriveIC_DCDC(instrName, OLEDTest, CH_LABEL_D)
#                 testtask = input("确定驱动IC波形2是否正确！（Y|N）")
#                 if testtask == "Y":
#                     pass
#
#         elif OLEDTest == "驱动IC下电":
#             interface_set_DriveIC_DCDC(instrName, OLEDTest, CH_ARR, CH_LABEL_C)
#             testtask = input("确定驱动IC下电波形1是否正确！（Y|N）")
#             if testtask == "Y":
#                 time_all = interface_get_allposition_one()
#
#                 exit()
#             testtask = input("是否执行波形2：1@MIPI_2@VDDR_3@ VCI _4@LCDRST测试任务：（Y|N）")
#             if testtask == "Y":
#                 interface_clear_measure(instrName)
#                 interface_set_DriveIC_DCDC(instrName, OLEDTest, CH_LABEL_C)
#                 testtask = input("确定驱动IC下电波形2是否正确！（Y|N）")
#                 if testtask == "Y":
#                     time_all = interface_get_allposition_two(instrName, OLEDTest)
#
#         elif OLEDTest == "DCDC上电":
#             interface_clear_measure(instrName)
#             interface_set_DriveIC_DCDC(instrName, OLEDTest, CH_ARR, CH_LABEL_E)
#
#         elif OLEDTest == "DCDC下电":
#             time_all = interface_get_allposition_four(instrName)
#             tOFF(instrName,time_all)
#             tDISCHG(instrName,time_all)
#     except Exception as err:
#        print(str(err))

