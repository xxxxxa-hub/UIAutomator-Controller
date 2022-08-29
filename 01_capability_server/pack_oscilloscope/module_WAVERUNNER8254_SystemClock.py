# coding=utf-8
import os
import re
import shutil
import datetime
import sys
import time
import uiautomator2 as u2
import threading
import math

from pack_oscilloscope.base.common_WAVERUNNER8254 import WAVERUNNER8254
from pack_oscilloscope.base.spi_signal_quality import SpiSignalQuality
from pack_oscilloscope.module_WAVERUNNER8254_SPIquality import *

from pack_oscilloscope.base.common_WAVERUNNER8254 import WAVERUNNER8254

import pack_phoneself.module_phone_run as phone
def interface_get_measurement_result(instrName, mr, tc, OsSaveRoute, LocalPath, OsPath,SetChannelName):
    """
    创建测量值
    :param instrName:
    :param mr:测量结果列表
    :param tc:测量值列表
    :param OsSaveRoute:示波器保存csv路径
    :param LocalPath:STS所在保存csv路径
    :param OsPath:STS访问示波器所在路径
    :return:
    """
    try:
        interface_Delete_Measure(instrName)
        test_case_len = len(tc)
        PngPath = ''
        PngPath2 = ''
        if test_case_len <= 8:
            for i in range(test_case_len):
                interface_AddOneMeasure_testCase(instrName, i, tc[i])
            time.sleep(1)
            for i in range(test_case_len):
                # 1、取出数据
                mr[tc[i]] = float(interface_MeasuresResult(instrName, i + 1, "max").split()[1])
            # 2、保存图片到示波器
            PngPath = interface_save_file(instrName, OsSaveRoute, LocalPath, OsPath,SetChannelName)
        else:
            index = 0
            # 循环检测多个测量值
            while index <= test_case_len:
                if index == test_case_len:
                    time.sleep(1)
                    PngPath2 = interface_save_file(instrName, OsSaveRoute, LocalPath, OsPath,SetChannelName)
                    for i in range(index - 8):
                        mr[tc[i + 8]] = float(interface_MeasuresResult(instrName, i + 1, "max").split()[1])
                elif index > 8:
                    interface_AddOneMeasure_testCase(instrName, index - 8, tc[index])
                elif index == 8:
                    # 如果是第8个参数
                    time.sleep(1)
                    for i in range(index):
                        # 1、取出数据
                        mr[tc[i]] = float(interface_MeasuresResult(instrName, i + 1, "max").split()[1])
                    # 2、保存图片到示波器
                    PngPath = interface_save_file(instrName, OsSaveRoute, LocalPath, OsPath,SetChannelName)
                    # 2.2 删除所有的测量值l
                    interface_Delete_Measure(instrName)
                    # 2.3 添加新的测量值
                    interface_AddOneMeasure_testCase(instrName, 0, tc[index])
                else:
                    interface_AddOneMeasure_testCase(instrName, index, tc[index])
                index += 1
        if len(PngPath) != 0:
            mr['PngPaths'].append(PngPath)
        if len(PngPath2) != 0:
            mr['PngPaths'].append(PngPath2)
        return mr
    except Exception as err:
        return ("创建测量值异常！"+str(err))


def interface_test_overshoot(instrName, mr, OverShoot, TimeSet1, SampleRate, CursorsType1, VerScale, VerOffset, OsSaveRoute, LocalPath, OsPath, SetChannelName):
    """
        判断是否过冲
        :param instrName:
        :param mr:测量结果列表
        :param OverShoot：过冲值
        :param TimeSet1：时基
        :param SampleRate：选择固定采样率
        :param CursorsType1：选择游标方式为垂直相对值
        :param VerScale：垂直刻度
        :param VerOffset：垂直偏置
        :param SetChannelName：信号名称
        :param OsSaveRoute:示波器保存csv路径
        :param LocalPath:STS所在保存csv路径
        :param OsPath:STS访问示波器所在路径
        :return:
        """
    try:
        # 抓取Top、Base、上冲、下冲值
        TopValue = mr['Top']
        BaseValue = mr['Base']
        Positive_OverShoot = mr['OverShootPositive'] * (TopValue - BaseValue) / 100
        Negative_OverShoot = mr['OverShootNegative'] * (TopValue - BaseValue) / 100
        flag = False
        # 判断是否过冲
        voltage = TopValue - BaseValue
        PngPath = ''
        # 过冲，输出测量值
        # 上冲大于0.3v
        # if (Positive_OverShoot >= OverShoot) | (Negative_OverShoot >= OverShoot):
        if Positive_OverShoot >= OverShoot:
            TimeSetDevice = interface_Set_channel_TimeBase(instrName, 0, TimeSet1 / 5, SampleRate)
            overshoot_CursorsPos = interface_Set_CursorsPos(instrName, CursorsType1, 65535, 65535, TopValue,
                                                            TopValue + Positive_OverShoot, VerScale, VerOffset)
            # 保存图片
            PngPath10 = interface_save_file(instrName, OsSaveRoute, LocalPath, OsPath, SetChannelName)
            time.sleep(1)
            MeasureResult['PngPaths'].append(PngPath10)
            time.sleep(1)
            flag = True
        elif Negative_OverShoot >= OverShoot:
            TimeSetDevice = interface_Set_channel_TimeBase(instrName, 0, TimeSet1 / 5, SampleRate)
            overshoot_CursorsPos = interface_Set_CursorsPos(instrName, CursorsType1, 65535, 65535, BaseValue,
                                                            BaseValue - Negative_OverShoot, VerScale, VerOffset)
            # 保存图片
            PngPath10 = interface_save_file(instrName, OsSaveRoute, LocalPath, OsPath, SetChannelName)
            time.sleep(1)
            MeasureResult['PngPaths'].append(PngPath10)
            time.sleep(1)
            flag = True
        return flag
    except Exception as err:
        return ("检查过冲异常！"+ str(err))


def interface_save_csv(instrName, OsSaveRoute, OsPath, LocalPath,SetChannelName):
    """
        保存csv文件
        :param instrName:
        :param SetChannelName:信号名称
        :param OsSaveRoute:示波器保存csv路径
        :param LocalPath:STS所在保存csv路径
        :param OsPath:STS访问示波器所在路径
        :return:
        """
    try:
        # 保存波形
        WaveformName = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        SaveWaveform = interface_SaveWaveform(instrName, SetChannelName + str(WaveformName), OsSaveRoute)
        # 将csv文件保存至本地分析
        time.sleep(2)
        ServerPathWaveform = OsPath + SetChannelName + str(WaveformName) + ".csv"
        CsvPath = LocalPath + SetChannelName + str(WaveformName) + ".csv"
        shutil.copyfile(ServerPathWaveform, CsvPath)
        return CsvPath
    except Exception as err:
        raise Exception("保存csv文件异常！"+str(err))


def interface_test_crosstalk(instrName, mr, CrossTalk, CursorsType1, VerScale, VerOffset, CsvPath, OsSaveRoute, LocalPath, OsPath, SetChannelName):
    """
        判断是否串扰
        :param instrName:
        :param mr:测量结果列表
        :param CrossTalk：串扰值标准
        :param CursorsType1：选择游标为垂直相对值
        :param SampleRate：选择固定采样率
        :param CursorsType1：选择游标方式为垂直相对值
        :param VerScale：垂直刻度
        :param VerOffset：垂直偏置
        :param SetChannelName：信号名称
        :param OsSaveRoute:示波器保存csv路径
        :param LocalPath:STS所在保存csv路径
        :param OsPath:STS访问示波器所在路径
        :return:
        """
    try:
        test = SpiSignalQuality()
        flag = False
        TopValue = mr['Top']
        BaseValue = mr['Base']
        ct_result = test.crosstalk(CsvPath, BaseValue, TopValue)  # 此处开始判断是否有串扰

        # 判断是否串扰
        if (ct_result['low_max'] - ct_result['low_min'] >= CrossTalk) \
                | (ct_result['high_max'] - ct_result['high_min'] >= CrossTalk):  # 有串扰情况
            # 改变时基
            # TimeSetDevice = interface_Set_channel_TimeBase(instrName, 0, 5E-5, SampleRate)  # 注：MISO时基调整与CLK不同

            if ct_result['low_max'] - ct_result['low_min'] >= CrossTalk:
                interface_Set_CursorsPos(instrName, CursorsType1, None, None,
                                         ct_result['low_max'], ct_result['low_min'], VerScale, VerOffset)
                mr["crosstalk"] = str(ct_result['low_max']) + "," + str(ct_result['low_min'])
                # 有串扰则标出游标位置
                ct_CursorsPos = interface_Set_CursorsPos(instrName, CursorsType1, 65535, 65535, ct_result['low_max'],
                                                         ct_result['low_min'], VerScale, VerOffset)

            elif ct_result['high_max'] - ct_result['high_min'] >= CrossTalk:
                interface_Set_CursorsPos(instrName, CursorsType1, None, None,
                                         ct_result['high_max'], ct_result['high_min'], VerScale, VerOffset)
                mr["crosstalk"] = str(ct_result['high_max']) + "," + str(ct_result['high_min'])
                # 有串扰则标出游标位置
                ct_CursorsPos = interface_Set_CursorsPos(instrName, CursorsType1, 65535, 65535, ct_result['high_max'],
                                                         ct_result('high_min'), VerScale, VerOffset)
            # 保存图片
            PngPath9 = interface_save_file(instrName, OsSaveRoute, LocalPath, OsPath, SetChannelName)
            time.sleep(1)
            # 关闭Zoom以及游标
            interface_ZoomAndCursors(instrName,ch)
            MeasureResult['PngPaths'].append(PngPath9)
            flag = True
        return flag
    except Exception as err:
        return ("串扰检查异常！"+ str(err))


def interface_test_back(instrName, mr, CursorsType2, VerScale, VerOffset, ch, TimeSet1, CsvPath, OsSaveRoute, LocalPath, OsPath, SetChannelName):
    try:
        test = SpiSignalQuality()
        flag = False
        TopValue = mr['Top']
        BaseValue = mr['Base']
        cb_result = test.check_back(CsvPath, BaseValue, TopValue)
        if len(cb_result) != 0:
            flag = True
            # 有回勾则标出游标位置
            cb_CursorsPos = interface_Set_CursorsPos(instrName, CursorsType2, cb_result['x1'], cb_result['x2'],
                                                     cb_result['y1'],
                                                     cb_result['y2'], VerScale, VerOffset)
            CenterPoint = cb_result['x1']
            interface_Zoom_set(instrName, ch, CenterPoint, TimeSet1 / 25)
            mr["back"] = str(cb_result)
            # 保存图片
            PngPath11 = interface_save_file(instrName, OsSaveRoute, LocalPath, OsPath, SetChannelName)
            time.sleep(3)
            # 关闭Zoom以及游标
            interface_ZoomAndCursors(instrName,ch)
            MeasureResult['PngPaths'].append(PngPath11)
        return flag
    except Exception as err:
        return ("回沟检查异常！"+ str(err))


def interface_test_step(mr, threshold, CsvPath):
    try:
        flag = False
        test = SpiSignalQuality()
        TopValue = mr['Top']
        BaseValue = mr['Base']
        cs_result = test.check_step(CsvPath, BaseValue, TopValue, threshold)
        if len(cs_result) != 0:
            # log.log有台阶，输出台阶电压
            mr["step"] = str(cs_result)
            # 关闭Zoom以及游标
            time.sleep(1)
            interface_ZoomAndCursors(instrName, ch)
            flag = True
        return flag
    except Exception as err:
        return ("台阶检查异常！"+ str(err))

def wifi_Control():
    if Phone_Control == "wifi_Control":
        while F:
            a = u2.connect_usb()
            a.shell("svc wifi enable")  # 打开WIFI
            time.sleep(2)
            a.shell("svc wifi disable")  # 关闭WIFI
F = 1

def nfc_Control():
    if Phone_Control == "nfc_Control":
        while F:
            a = u2.connect_usb()
            a.shell("svc nfc enable")  # 打开NFC
            time.sleep(2)
            a.shell("svc nfc disable")  # 关闭NFC
F = 1

def interface_TriggerHor(instrName,TriggerHor):
    try:
        WAVERUNNER = WAVERUNNER8254(instrName)
        WAVERUNNER.TriggerHor(TriggerHor)
        return instrName
    except Exception as err:
        return str(err)


if __name__ == '__main__':
    instrName = "TCPIP::" + "169.254.8.199" + "::INSTR"
    DisplayGridMode = 'Single'
    ch = 1
    SetChannelName = 'XOI'
    SetHorOffset = 0
    # C_Top = float("")
    Voltage = 1.8
    VerScale = Voltage/8
    VerOffset = -3*VerScale
    Freq = "19.2E+6"  # 芯片频率标准MHz
    # C_Freq = float("")
    TimeSet1 = 0.5/float(Freq) # 5周期时基
    TimeSet2 = 0.1/float(Freq) # 单周期时基
    SampleRate = "FixedSampleRate"
    # measure = "Measurement"
    Measure = "DeltaPeriodAtLevel"
    trigger_type = "Negative"
    trigger_ch = "C1"
    OpenPersistence = True
    trigger_level = 0.45
    HoldoffTime1 = -4*TimeSet1
    HoldoffTime2 = -4*TimeSet2
    CursorsType1 = "VertRel"
    CursorsType2 = "BothRel"
    OsSaveRoute = "D:\\osFile\\"
    LocalPath = "d:\\tmp\\"
    OsPath = "//169.254.8.199/osFile/"
    Risetime = "True" # TrueorFlase  判断是否有上升时间，用来决定是否测试上升沿触发以及下降沿触发
    CrossTalk = 0.2  # 串扰阈值 v
    OverShoot = 0.3  # 过冲阈值 v
    threshold = 0.01 # 台阶阈值
    MEASURE = ""  # MEASURE等于JitterTest则执行抖动测试
    Phone_Control = "wifi_Control"
    # 选择测试点对应测量值
    MultiPeriod_testCase = [ "Freq","Duty","Top","Base"] #["Freq", "Duty", "Top", "Base"]  # 多周期测量值
    SingleCycle_testCase = ["Rise", "Top", "Base", "OverShootNegative", "OverShootPositive", "Max","Min","Fall"] # 单周期测量值
    RisingTrigger_testCase = ["Rise"] # 上升沿触发测量值
    FallingTrigger_testCase = ["Fall"] # 下降沿触发测量值
    # TestCase = MultiPeriod_testCase
    MeasureResult1 = {'PngPaths': []}
    # interface_get_measurement_result(instrName, MeasureResult1, MultiPeriod_testCase, OsSaveRoute, LocalPath, OsPath)

    # ******************************************************************************************************************
    # --------------------------------------------此处为多周期触发---------------------------------------------------------
    # ******************************************************************************************************************

    OsDevice = interface_initial(instrName, DisplayGridMode)
    # 设置通道名称(ch, SetChannelName)
    ChannelName = interface_set_channel_name(instrName, ch, SetChannelName)
    # 设置垂直(ch,VerScale,VerOffset)
    VerticalDevice = interface_Set_channel_vertical(instrName, ch, VerScale, VerOffset)
    # 设置时基(ch,HorOffset,TimeSet,SampleRate)
    TimeSetDevice = interface_Set_channel_TimeBase(instrName, SetHorOffset, TimeSet1, SampleRate)
    # 设置触发(instrName,trigger_type, trigger_ch, trigger_level)
    TriggerDevices = interface_Trigger(instrName, trigger_type, trigger_ch, trigger_level)
    # 设置触发抑制
    TriggerHold = interface_TriggerHoldoffTime(instrName, HoldoffTime1)

    # 等待波形触发
    # 加入手机控制
    if Phone_Control == "nfc_Control":
        t = threading.Thread(target=nfc_Control, name='phone')
        t.start()
    elif Phone_Control == "wifi_Control":
        t = threading.Thread(target=wifi_Control, name='phone')
        t.start()
    # 此处触发的为5周期波形
    count = 0
    while True:
        count += 1
        time.sleep(1)
        TriMode = interface_TriggerMode(instrName)
        if TriMode.split()[1] == "Stopped":
            break
        if count >= 20:
            raise Exception("在20s之内未能捕捉到正确的波形，请重新测试")

    MeasureResult1 = {}
    test_case_len = len(MultiPeriod_testCase)

    # 创建图片保存列表
    MeasureResult1 = {'PngPaths': []}

    # 得出“freq”、“duty”、“high”和“low”与芯片规格对比
    interface_get_measurement_result(instrName, MeasureResult1, MultiPeriod_testCase, OsSaveRoute, LocalPath, OsPath,SetChannelName)
    # # 保存csv文件
    # CsvPath = save_csv(instrName, OsSaveRoute, OsPath, LocalPath)

    # ******************************************************************************************************************
    # --------------------------------------------此处为单周期触发---------------------------------------------------------
    # ******************************************************************************************************************
    # 再次设置，触发单周期波形
    # 设置时基(ch,HorOffset,TimeSet2,SampleRate)
    TimeSetDevice = interface_Set_channel_TimeBase(instrName, SetHorOffset, TimeSet2, SampleRate)
    # 设置余晖
    # PersistenceDevice = interface_Persistence_set(instrName, OpenPersistence,5)
    # 设置触发
    TriggerDevices = interface_set_trigger_XTirggerType(instrName, trigger_type, trigger_ch, trigger_level)
    # 设置触发位置
    TriggerHor = interface_TriggerHor(instrName, -4*TimeSet2)
    # 打开触发抑制
    TriggerHold = interface_TriggerHoldoffTime(instrName, HoldoffTime2)
    # 选择触发类型为Normal
    TriggerType = interface_NormalType(instrName)

    # 创建图片保存列表
    MeasureResult2 = {'PngPaths': []}
    # 输入测量值
    test_case_len = len(SingleCycle_testCase)
    interface_get_measurement_result(instrName, MeasureResult2, SingleCycle_testCase, OsSaveRoute, LocalPath, OsPath,SetChannelName)
    MeasureResult2['PngPaths'].clear()
    # 当余晖num为200时停止
    # while 1:
    #     time.sleep(0.5)
    #     PersistedNum = interface_PersistedNum(instrName,1,"num")
    #     print(float(interface_MeasuresResult(instrName, 2, "max").split()[1]))
    #     if int(re.findall('\d+', PersistedNum)[0]) > 200:
    #         TriMode = interface_StopType(instrName)
    #         break
    #     else:
    #         TriggerType = interface_NormalType(instrName)

    # 余晖5s
    interface_Persistence_set(instrName,OpenPersistence,5)
    time.sleep(5)
    interface_StopType(instrName)
    PngPath2 = interface_save_file(instrName, OsSaveRoute, LocalPath, OsPath,SetChannelName)
    time.sleep(1)
    MeasureResult2['PngPaths'].append(PngPath2)

    # 保存波形
    WaveformName = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")

    SaveWaveform = interface_SaveWaveform(instrName, SetChannelName + str(WaveformName), OsSaveRoute)
    # 将csv文件保存至本地分析
    time.sleep(2)
    ServerPathWaveform = OsPath + SetChannelName + str(WaveformName) + ".csv"
    CsvPath = LocalPath + SetChannelName + str(WaveformName) + ".csv"
    shutil.copyfile(ServerPathWaveform, CsvPath)

    # 判断余晖Top/Base值标准
    # 拉出top的最大最小值，用来判断余晖后的数据是否重合
    Top_max = (float(interface_MeasuresResult(instrName, 2, "max").split()[1]))
    Top_min = (float(interface_MeasuresResult(instrName, 2, "min").split()[1]))
    # print(Top)

    # 拉出Rise的最大最小值，用来判断余晖后的数据是否重合
    Rise_max = (float(interface_MeasuresResult(instrName, 1, "max").split()[1]))
    Rise_min = (float(interface_MeasuresResult(instrName, 1, "min").split()[1]))

    # 拉出Fall的最大最小值，用来判断余晖后的数据是否重合
    Fall_max = (float(interface_MeasuresResult(instrName, 8, "max").split()[1]))
    Fall_min = (float(interface_MeasuresResult(instrName, 8, "min").split()[1]))

    Base_max = (float(interface_MeasuresResult(instrName, 3, "max").split()[1]))
    Base_min = (float(interface_MeasuresResult(instrName, 3, "min").split()[1]))
    # print(Base)
    # 判断余晖高电平最大值以及低电平最小值
    # TopV = interface_PersistedNum(instrName,2,"Max")
    # Top = int(re.findall('\d+', TopV)[0])
    # BaseV = interface_PersistedNum(instrName,3,"Min")
    # Base = int(re.findall('\d+', BaseV)[0])
    # print("*********")
    # print(Top)
    # print(Base)

    # 测试过冲
    flag = interface_test_overshoot(instrName, MeasureResult2, OverShoot, TimeSet2, SampleRate, CursorsType1, VerScale, VerOffset,OsSaveRoute,LocalPath,OsPath,SetChannelName)
    if flag:
        PngPath3 = interface_save_file(instrName, OsSaveRoute, LocalPath, OsPath,SetChannelName)
        time.sleep(1)
        MeasureResult2['PngPaths'].append(PngPath3)

    # 判断是否有串扰
    flag = interface_test_crosstalk(instrName, MeasureResult2, CrossTalk, CursorsType1, VerScale, VerOffset, CsvPath,OsSaveRoute,LocalPath,OsPath,SetChannelName)
    if flag:
        PngPath4 = interface_save_file(instrName, OsSaveRoute, LocalPath, OsPath,SetChannelName)
        time.sleep(1)
        MeasureResult2['PngPaths'].append(PngPath4)

    # 判断是否有回沟
    flag = interface_test_back(instrName, MeasureResult2, CursorsType2, VerScale, VerOffset, ch, TimeSet2, CsvPath,OsSaveRoute,LocalPath,OsPath,SetChannelName)
    if flag:
        PngPath5 = interface_save_file(instrName, OsSaveRoute, LocalPath, OsPath,SetChannelName)
        time.sleep(1)
        MeasureResult2['PngPaths'].append(PngPath5)
        interface_Zoom_set(instrName, ch, False, 0, TimeSet1 / 25)

    # 判断是否有台阶
    flag = interface_test_step(MeasureResult2, threshold, CsvPath)
    if flag:
        PngPath6 = interface_save_file(instrName, OsSaveRoute, LocalPath, OsPath,SetChannelName)
        time.sleep(1)
        MeasureResult2['PngPaths'].append(PngPath6)


    # ******************************************************************************************************************
    # --------------------------------------------此处为上升沿触发---------------------------------------------------------
    # ******************************************************************************************************************
    # 创建图片保存列表
    MeasureResult3 = {'PngPaths': []}
    MeasureResult4 = {'PngPaths': []}
    if Risetime == "True":
        # 加入如果标准有上升时间，则触发
        # 再次设置，触发上升沿波形
        # 设置时基(ch,HorOffset,TimeSet2,SampleRate)
        TimeSetDevice = interface_Set_channel_TimeBase(instrName, SetHorOffset, 1e-9, SampleRate)
        # 关闭余晖
        PersistenceDevice = interface_Persistence_set(instrName, False,5)
        # 设置触发
        TriggerDevices = interface_set_trigger_XTirggerType(instrName, "Positive", trigger_ch, trigger_level)
        # 打开触发抑制
        TriggerHold = interface_TriggerHoldoffTime(instrName, 0)
        TriggerHor = interface_TriggerHor(instrName, 0)
        # 选择触发类型为Normal
        TriggerType = interface_NormalType(instrName)
        test_case_len = len(RisingTrigger_testCase)

        # 输入测量值   此处拉出上升时间对比标准
        interface_get_measurement_result(instrName, MeasureResult3, RisingTrigger_testCase, OsSaveRoute, LocalPath,
                                         OsPath,SetChannelName)
        MeasureResult3['PngPaths'].clear()
        # 设置余晖,余晖5s
        PersistenceDevice = interface_Persistence_set(instrName,OpenPersistence,5)
        # # 当余晖num为200时停止
        # while 1:
        #     time.sleep(0.5)
        #     PersistedNum = interface_PersistedNum(instrName, 1, "num")
        #     # print(float(interface_MeasuresResult(instrName, 2, "max").split()[1]))
        #     if int(re.findall('\d+', PersistedNum)[0]) > 200:
        #         TriMode = interface_StopType(instrName)
        #         break
        #     else:
        #         TriggerType = interface_NormalType(instrName)

        PngPath7 = interface_save_file(instrName, OsSaveRoute, LocalPath, OsPath,SetChannelName)
        MeasureResult3['PngPaths'].append(PngPath7)
        print(MeasureResult3)

    # ******************************************************************************************************************
    # --------------------------------------------此处为下降沿触发---------------------------------------------------------
    # ******************************************************************************************************************
        # 加入如果标准有上升时间，则触发
        # 再次设置，触发下降沿波形
        # 设置时基(ch,HorOffset,TimeSet2,SampleRate)
        TimeSetDevice = interface_Set_channel_TimeBase(instrName, SetHorOffset, TimeSet2/2, SampleRate)
        # 设置余晖
        PersistenceDevice = interface_Persistence_set(instrName, OpenPersistence,5)
        # 设置触发
        TriggerDevices = interface_set_trigger_XTirggerType(instrName, trigger_type, trigger_ch, trigger_level)
        # 打开触发抑制
        TriggerHold = interface_TriggerHoldoffTime(instrName, 0)
        # 设置触发位置
        TriggerHor = interface_TriggerHor(instrName, 0)
        # 选择触发类型为Normal
        TriggerType = interface_NormalType(instrName)

        test_case_len = len(FallingTrigger_testCase)


        # 输入测量值   此处拉出下降时间对比标准
        interface_get_measurement_result(instrName, MeasureResult4, FallingTrigger_testCase, OsSaveRoute, LocalPath, OsPath,SetChannelName)
        print(MeasureResult4)
        MeasureResult4['PngPaths'].clear()
        time.sleep(2)

        # # 当余晖num为200时停止
        # while 1:
        #     time.sleep(0.5)
        #     PersistedNum = interface_PersistedNum(instrName, 1, "num")
        #     # print(float(interface_MeasuresResult(instrName, 2, "max").split()[1]))
        #     if int(re.findall('\d+', PersistedNum)[0]) > 200:
        #         TriMode = interface_StopType(instrName)
        #         break
        #     else:
        #         TriggerType = interface_NormalType(instrName)

        PngPath8 = interface_save_file(instrName, OsSaveRoute, LocalPath, OsPath,SetChannelName)
        MeasureResult4['PngPaths'].append(PngPath8)




    # 停止手机控制
    F = 0

    # 输出所有测量值结果
    png_pahts = MeasureResult1['PngPaths'] + MeasureResult2['PngPaths'] + MeasureResult3['PngPaths'] + \
                MeasureResult4['PngPaths']
    MeasureResult = {"Top": Top, "Base": Base}
    MeasureResult1.pop('PngPaths')
    MeasureResult2.pop('PngPaths')
    MeasureResult3.pop('PngPaths')
    MeasureResult4.pop('PngPaths')
    MeasureResultAll = dict(
        MeasureResult1.items() | MeasureResult2.items() | MeasureResult3.items() | MeasureResult4.items() | MeasureResult.items())
    MeasureResultAll['PngPaths'] = png_pahts
    print(MeasureResultAll)






