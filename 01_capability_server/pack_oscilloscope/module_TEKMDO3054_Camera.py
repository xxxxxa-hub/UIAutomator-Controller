# coding=utf-8
import os
import pandas
import time
import uiautomator2 as u2
import threading
from pack_oscilloscope.base.common_TekMDO3054 import TekMDO3054
from pack_oscilloscope.base.scene_library import GoScene
from pack_oscilloscope.module_TEKMDO3054_SPItiming import *
import pack_oscilloscope.module_TEKMDO3054_PowerQuality as pw
import pack_oscilloscope.module_TEKMDO3054_OLEDtiming as ot
from pack_oscilloscope.base.common_TekMDO3054 import TekMDO3054
from pack_oscilloscope.base.spi_signal_quality import SpiSignalQuality
import pack_oscilloscope.base.spi_signal_quality as OpCsv



from pack_oscilloscope.base.common_WAVERUNNER8254 import WAVERUNNER8254
from pack_phoneself.Base import mobile_base

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

def interface_set_Hor_cursor(instrName,cursor_source, position_horizontal_1, position_horizontal_2):
    # 标出水平光标
    try:
        tek = TekMDO3054(instrName)
        tek.set_cursor_horizontal(cursor_source, position_horizontal_1, position_horizontal_2)
        return instrName
    except Exception as e:
        return str(e)

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

def camera_Control():
    if Phone_Control == "camera":
            a = u2.connect_usb()
            a.shell("adb shell am start -a android.media.action.STILL_IMAGE_CAMERA")  # 打开相机
            time.sleep(3)
            a.shell("adb shell input keyevent BACK")  # 返回上一步
        #"adb shell input keyevent BACK"# 返回上一步SSSS

# def interface_test_overshoot():
#     # 抓取Top、Base、上冲、下冲值
#     TopValue = change_type['Top']
#     BaseValue = change_type['Base']
#     Positive_OverShoot = mr['OverShootPositive'] * (TopValue - BaseValue) / 100
#     Negative_OverShoot = mr['OverShootNegative'] * (TopValue - BaseValue) / 100
def interface_check_crosstalk(change_type,CsvPath,CrossTalk,ch):
    try:
        test = SpiSignalQuality()
        flag = False
        TopValue = change_type[4]             # 针对与此信号设置change_type[4] = change_type["HIGH"]
        BaseValue = change_type[3]
        ct_result = test.crosstalk(CsvPath, BaseValue, TopValue)  # 此处开始判断是否有串扰

        # 判断是否串扰
        if (ct_result['low_max'] - ct_result['low_min'] >= CrossTalk) \
                | (ct_result['high_max'] - ct_result['high_min'] >= CrossTalk):  # 有串扰情况
            # 如果有下串扰
            if ct_result['low_max'] - ct_result['low_min'] >= CrossTalk:
                # 则标出游标位置
                overshoot_CursorsPos = interface_set_Hor_cursor(instrName, ch, ct_result['low_max'], ct_result['low_min'])
                change_type["crosstalk"] = str(ct_result['low_max']) + "," + str(ct_result['low_min'])
            # 如果有上串扰
            elif ct_result['high_max'] - ct_result['high_min'] >= CrossTalk:
                overshoot_CursorsPos = interface_set_Hor_cursor(instrName, ch, ct_result['high_max'], ct_result['high_min'])
                change_type["crosstalk"] = str(ct_result['high_max']) + "," + str(ct_result['high_min'])
            # 保存图片
            PngPath10 = pw.interface_save_screen(instrName, file_save("png"))
            time.sleep(1)
            MeasureResult['PngPaths'].append(PngPath10)
            flag = True
        return flag
    except Exception as err:
        return ("串扰检查异常！" + str(err))

def interface_reference_levels(instrName,HighRefSet,LowRefSet):
    try:
        tek = TekMDO3054(instrName)
        tek.set_reference_levels(HighRefSet,LowRefSet)
        return instrName
    except Exception as err:
        return str(err)

def os_play(close_list):
    # 恢复默认设置
    ot.interface_set_Factory(instrName)
    # 设置通道标签
    interface_ch_set(instrName, ch_arr, ch_label)
    change_type = {1: "Amplitude", 2: "RISe", 3: "LOW", 4: "HIGH"}
    # 打开通道
    interface_open_ch(instrName, close_list[0])
    ch = close_list[0]
    for j in range(1,4):
        interface_close_ch(instrName, close_list[j])

    # 设置波形亮度为100%
    ot.interface_set_DisplayIntensity(instrName, 100)
    # 设置时基
    interface_set_horizontal_scale(instrName, 50E-6)
    # 设置记录长度为5M
    interface_set_record_length(instrName,5.0E6)
    # 设置为全带宽
    interface_set_bandwidth(instrName, ch, "FULL")
    # 耦合方式选DC耦合
    interface_set_coupling(instrName, ch, "DC")
    # 设置偏置0
    interface_set_offset(instrName, ch, 0)
    # 设置垂直刻度500mV
    pw.interface_set_scale(instrName, 4,ch)
    # 垂直位置设为-2格
    interface_set_position(instrName, ch, -2)
    # 添加“幅值”、和“上升时间”测量项
    for i in change_type:
        pw.interface_change_time_set(instrName, change_type[i], i, ch)
    # 高电平参考设为100%，低电平参考设为0%
    interface_reference_levels(instrName, 100, 0)
    # 设置触发
    interface_set_trigger(instrName, "RISE", ch, 0.9, 0)
    # 设置单次触发
    pw.interface_set_trigger_mode(instrName, "SEQUENCE")
    # 手机控制
    if Phone_Control == "camera":
        a = u2.connect_usb()
        a.shell("am start -a android.media.action.STILL_IMAGE_CAMERA")  # 打开相机
        time.sleep(2)
        a.shell("input keyevent 3")  # 返回主界面
        # interface_save_screen(instrName, file_save)
    time.sleep(2)
    value_tup={}
    # 获取测量值
    time.sleep(3)
    for i in range(1, len(change_type)+1):
        change_type[i] = tek.get_observed_value(i, "VALue")
    print(change_type)
    # 保存通道波形
    filepath1 = file_save("csv")
    filepath2 = file_save("png")
    pw.interface_data_caul(instrName, filepath1, low_v=None, high_v=None, CH=ch)
    time.sleep(5)
    # 保存图片
    PngPath4 = pw.interface_save_screen(instrName, filepath2)
    MeasureResult['PngPaths'].append(PngPath4)

    # 判断Slew Rate（斜率）是否符合标准 (单位mV/us)
    SlewRate = float(change_type[1])*1000 / float(change_type[2]*1000000)
    if SlewRate <=100:
        print(SlewRate)
        print("判断斜率符合标准")
    else:
        print(SlewRate)
        print("判断斜率不符合标准")



    # 用光标标出上升时间（0%-100%）
    data = interface_get_RiseEdge(filepath1, 0.05, 0.95)
    time_a = float(data[0])
    time_b = float(data[1])
    ot.interface_adjust_scale(instrName, time_a, time_b, siterate=False)  # 此处的time_a, time_b为水平位置，需改为垂直位置
    ot.interface_set_simcursor(instrName, ch, time_a, time_b)

    # 判断波纹数据回勾、台阶、过冲
    # interface_check_back(filePath, float(level["LOW"])-0.3, float(level["HIGH"])+0.3)   # 传进获取的高、低电平值

    #判断是否存在回勾
    '''check_back = pw.interface_check_back(filepath1,  float(change_type[3]), float(change_type[4]))
    if len(check_back) == 0:
        print("检查波形不存在回勾")
    else:
        pw.interface_set_cursor(instrName,check_back['x1'], check_back['x2'], check_back['y1'], check_back['y2'],ch)
        # 保存图片
        PngPath3 = pw.interface_save_screen(instrName, filepath2)
        MeasureResult['PngPaths'].append(PngPath3)
        print("判断波形存在回勾")

    # 判断是否存在台阶
    check_step = pw.interface_check_step(filepath1, float(change_type[3]), float(change_type[4]), 0.01)
    if len(check_step) != 0:
        MeasureResult["step"] = str(check_step)
        print("判断波形存在台阶")
    else:
        print("检查波形不存在台阶")

    # 判断是否存在串扰
    flag = interface_check_crosstalk(change_type,filepath1,0.2,ch) # 如果有串扰
    print("判断波形存在串扰")
    if flag is True:      # 如果没有串扰
        print("判断波形不存在串扰")

    # 删除之前所有测量项
    ot.interface_clear_measure(instrName)

    # ------------------------------------------------------------------------------
    # 添加上冲，下冲测量项
    change_type2 = {1:"POVERSHOOT",2:"NOVERSHOOT",3: "LOW", 4: "HIGH"}
    for i in change_type2:
        pw.interface_change_time_set(instrName, change_type2[i], i, ch)
    # 获取测量项
    time.sleep(3)
    for i in range(1, len(change_type2) + 1):
        change_type2[i] = tek.get_observed_value(i, "VALue")
    print(change_type2)
    TopValue = change_type2[4]
    BaseValue = change_type2[3]
    Positive_OverShoot = change_type2[1] * (TopValue - BaseValue) / 100
    Negative_OverShoot = change_type2[2] * (TopValue - BaseValue) / 100
    flag = False
    # 判断是否过冲
    # 上冲大于0.3v
    if Positive_OverShoot >= OverShoot:
        overshoot_CursorsPos = interface_set_Hor_cursor(instrName, ch, TopValue,TopValue + Positive_OverShoot)
        # 保存光标图片
        PngPath10 = pw.interface_save_screen(instrName, filepath2)
        MeasureResult['PngPaths'].append(PngPath10)
        time.sleep(1)
        flag = True
    # 下冲大于0.3V
    elif Negative_OverShoot >= OverShoot:
        overshoot_CursorsPos = interface_set_Hor_cursor(instrName, ch, BaseValue,BaseValue - Negative_OverShoot)
        # 保存图片
        PngPath10 = pw.interface_save_screen(instrName, filepath2)
        time.sleep(1)
        MeasureResult['PngPaths'].append(PngPath10)
        time.sleep(1)
        flag = True'''


if __name__ == '__main__':
    # 获取时间，提供日志、图片、文件使用；
    def get_time():
        return str(time.strftime("%Y-%m-%d %H:%M:%S  ", time.localtime(time.time())))

    def file_save(mode, pic_path=r"D:\\"):
        return pic_path + f"\\{get_time()[:-2].replace(':', '-')}.{mode}"

    instrName = "TCPIP::" + "169.254.8.103" + "::INSTR"
    tek = TekMDO3054(instrName)


    #filePath = f"E:\\POST\\Data.csv"
    # OsDevice = interface_initial(instrName)
    ch_arr = 'CH1,CH2,CH3,CH4'
    ch_label = 'AVDD1,AVDD2,DVDD,VIO'
    trigger_type = "RISE" # RISE或FALL 触发
    Phone_Control = 'camera'
    OverShoot = 0.3 # 过冲阈值 <300mV
    close_ch1 = ["CH1","CH2","CH3","CH4"]
    close_ch2 = ["CH2","CH1","CH3","CH4"]
    close_ch3 = ["CH3","CH1","CH2","CH4"]
    close_ch4 = ["CH4","CH1","CH2","CH3"]
    #***********************共用示波器操作*******************
    # 测试单个通道信号
    MeasureResult = {"PngPaths": []}  # 用于总测量值存放
    MeasureResult2 = {"slew_rate":[]}
    slew_rate1 = os_play(close_ch1)  # 打开通道1
    MeasureResult["slew_rate1"] = slew_rate1
    slew_rate2 = os_play(close_ch2)
    MeasureResult["slew_rate2"] = slew_rate2
    slew_rate3 = os_play(close_ch3)
    MeasureResult["slew_rate3"] = slew_rate3
    slew_rate4 = os_play(close_ch4)
    MeasureResult["slew_rate4"] = slew_rate4

# ------------------------上下时序测试---------------------------
    # 打开所有通道
    # ch_label = 'AVDD1,AVDD2,DVDD,VIO'
    interface_open_ch(instrName, "CH1")
    interface_open_ch(instrName, "CH2")
    interface_open_ch(instrName, "CH3")
    interface_open_ch(instrName, "CH4")

    # 设置AVDD1垂直刻度为1V
    pw.interface_set_scale(instrName, 8,"CH1")
    # 垂直位置设为0格
    interface_set_position(instrName, "CH1", 0)
    # 设置AVDD2垂直刻度为2V
    pw.interface_set_scale(instrName, 16, "CH2")
    # 垂直位置设为-1格
    interface_set_position(instrName, "CH2", -1)
    # 设置DVDD垂直刻度为1V
    pw.interface_set_scale(instrName, 8, "CH3")
    # 垂直位置设为1格
    interface_set_position(instrName, "CH3", 1)
    # 设置IOVDD垂直刻度为1V
    pw.interface_set_scale(instrName, 8, "CH4")
    # 垂直位置设为-2格
    interface_set_position(instrName, "CH4", -2)
    # 设置时基
    interface_set_horizontal_scale(instrName, 100E-3)
    # 设置记录长度为5M
    interface_set_record_length(instrName,5.0E6)
    # 设置触发
    interface_set_trigger(instrName, "RISE", "CH1", 0.9, 0)
    # 耦合方式设为DC耦合
    interface_set_coupling(instrName, "CH1", "DC")
    # 设置单次触发
    pw.interface_set_trigger_mode(instrName, "SEQUENCE")
# ----------------------------开机场景------------------------------------------
    # 弹框：请将手机开机


    # 设置保存图片名称
    filename1 = pic_path + "\\" + '开机_1@AVDD1_2@AVDD2_3@DVDD_4@VIO' + '.png'
    # 保存图片
    filename = pw.interface_save_screen(instrName, filename1)

#----------------------------开启摄像头场景------------------------------------------
    # 设置单次触发
    pw.interface_set_trigger_mode(instrName, "SEQUENCE")
    # 设置打开摄像头
    if Phone_Control == "camera":
        a = u2.connect_usb()
        a.shell("am start -a android.media.action.STILL_IMAGE_CAMERA")  # 打开相机
        time.sleep(2)
        a.shell("input keyevent 3")  # 返回主界面
    # 设置保存图片名称
    filename2 = pic_path + "\\" + '开启摄像头_1@AVDD1_2@AVDD2_3@DVDD_4@VIO' + '.png'
    # 保存图片
    filename = pw.interface_save_screen(instrName, filename2)

# ----------------------------后置切前置场景------------------------------------------
    # 设置单次触发
    pw.interface_set_trigger_mode(instrName, "SEQUENCE")
    # 设置后置摄像头切换前置


    # 设置保存图片名称
    filename1 = pic_path + "\\" + '后置切前置_1@AVDD1_2@AVDD2_3@DVDD_4@VIO' + '.png'
    # 保存图片
    filename = pw.interface_save_screen(instrName, filename)





















