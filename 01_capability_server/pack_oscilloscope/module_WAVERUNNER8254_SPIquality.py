# coding=utf-8
import os
import re
import shutil
import datetime
import sys
import time

from pack_oscilloscope.base.common_WAVERUNNER8254 import WAVERUNNER8254
from pack_oscilloscope.base.spi_signal_quality import SpiSignalQuality

from pack_oscilloscope.base.common_WAVERUNNER8254 import WAVERUNNER8254

import pack_phoneself.module_phone_run as phone


def interface_initial(instrName, DisplayGridMode):
    """
    初始化接口
    恢复默认
    设置单个波形
    关闭2通道
    :return:
    """
    try:
        WAVERUNNER = WAVERUNNER8254(instrName)
        WAVERUNNER.DefaultSetup()
        WAVERUNNER.close_ch(2)
        WAVERUNNER.AutoType("Auto")
        time.sleep(2)
        WAVERUNNER.DisplayGridMode(DisplayGridMode)
        return instrName
    except Exception as err:
        return str(err)


def interface_set_channel_name(instrName, ch, SetChannelName):
    """
    设置通道名称
    :param SetChannelName: 通道名称
    :param ChannelInputB: 将通道设置为InpuB
    :param ch: 通道号
    :param instrName: 示波器ID
    :return:示波器ID
    """
    try:
        WAVERUNNER = WAVERUNNER8254(instrName)
        WAVERUNNER.ChannelInputB(ch, "InputB")
        WAVERUNNER.name_ch(ch, SetChannelName)
        WAVERUNNER.ViewLabels(ch)
        return instrName
    except Exception as err:
        return str(err)


def interface_Set_channel_vertical(instrName, ch, VerScale, VerOffset):
    """
    设置通道垂直刻度及偏置
    :param VerScale: 填写垂直刻度值
    :param ch: 通道号
    :param VerOffset:填写垂直偏置值
    :param instrName: 示波器ID
    :return:示波器ID
    """
    try:
        WAVERUNNER = WAVERUNNER8254(instrName)
        WAVERUNNER.SetVarGain(ch)
        WAVERUNNER.VerScale(ch, VerScale)
        WAVERUNNER.VerOffset(ch, VerOffset)
        return instrName
    except Exception as err:
        return str(err)


def interface_Set_channel_TimeBase(instrName, SetHorOffset, TimeSet, SampleRate):
    """设置通道时基
    :param SetHorOffset: 设置时基偏置
    :param TimeSet:设置每格时间
    :param SampleRate:设置采样率模式,可选择FixedSampleRate（固定采样器10GB/s）/Set Maximum Memory（设置最大内存） 模式
    :param instrName: 示波器ID
    :return:示波器ID
    """
    try:
        WAVERUNNER = WAVERUNNER8254(instrName)
        WAVERUNNER.SetHorOffset(SetHorOffset)
        WAVERUNNER.TimeSet(TimeSet)
        WAVERUNNER.SetSampleRate(SampleRate)
        WAVERUNNER.ActivationChannel("Auto")
        WAVERUNNER.SampleRate(2e+10)
        return instrName
    except Exception as err:
        return str(err)

def interface_Single(instrName):
    """
    单次点击Single触发
    """
    try:
        WAVERUNNER = WAVERUNNER8254(instrName)
        WAVERUNNER.AutoType("Single")
        return instrName
    except Exception as err:
        return str(err)

def interface_AddMeasures_testCase(instrName, testCase):
    """添加测量项
        此处为添加CS信号的测量项
    """
    try:
        WAVERUNNER = WAVERUNNER8254(instrName)
        WAVERUNNER.statistics()
        WAVERUNNER.AddMeasures_testCase(testCase)
        return instrName
    except Exception as err:
        return str(err)


def interface_AddOneMeasure_testCase(instrName, channel_no, measure):
    """添加测量项
        此处为逐个添加测量项
    """
    try:
        WAVERUNNER = WAVERUNNER8254(instrName)
        WAVERUNNER.statistics()
        channel_no = int(channel_no)
        WAVERUNNER.AddOneMeasure_testCase(channel_no, measure)
        return instrName
    except Exception as err:
        return str(err)


def interface_MeasuresResult(instrName, ph, Measure):
    """输出测量项结果
       :param ph:测量项通道，P1-P8
       :param Measure: 要输出的值，如最大值、最小值等
        """
    try:
        WAVERUNNER = WAVERUNNER8254(instrName)
        ph = int(ph)
        result = WAVERUNNER.MeasureResult(ph, Measure)
        return result
    except Exception as err:
        return str(err)


def interface_Delete_Measure(instrName):
    try:
        WAVERUNNER = WAVERUNNER8254(instrName)
        WAVERUNNER.Delete_Measure()
        return instrName
    except Exception as err:
        return str(err)

def interface_Auto(instrName):
    try:
        WAVERUNNER = WAVERUNNER8254(instrName)
        WAVERUNNER.AutoType("Auto")
        return instrName
    except Exception as err:
        return str(err)


def interface_Trigger(instrName, trigger_type, trigger_ch, trigger_level):
    """
    :param trigger_type: 上升沿触发或下降沿触发，Negative/Positive二者选一
    :param trigger_ch: 触发源（通道几触发）
    :param trigger_level: 触发电平
    :return:
    """
    try:
        WAVERUNNER = WAVERUNNER8254(instrName)
        WAVERUNNER.set_trigger(trigger_type, trigger_ch, trigger_level)
        return instrName
    except Exception as err:
        return str(err)

def interface_set_trigger_XTirggerType(instrName,trigger_type, trigger_ch, trigger_level):
    """
        单纯的触发设置，不包含触发方式，如Normal，Single
        :param trigger_type: 上升沿触发或下降沿触发，Negative/Positive二者选一
        :param trigger_ch: 触发源（通道几触发）
        :param trigger_level: 触发电平
        :return:
        """
    try:
        WAVERUNNER = WAVERUNNER8254(instrName)
        WAVERUNNER.set_trigger_XTirggerType(trigger_type, trigger_ch, trigger_level)
        return instrName
    except Exception as err:
        return str(err)


def interface_Trigger_Measurement(instrName,trigger_ch,measure, trigger_level):
    """
    :param trigger_type: 上升沿触发或下降沿触发，Negative/Positive二者选一
    :param trigger_ch: 触发源（通道几触发）
    :param trigger_level: 触发电平
    :return:
    """
    try:
        WAVERUNNER = WAVERUNNER8254(instrName)
        WAVERUNNER.set_trigger_Measurement(trigger_ch,measure, trigger_level)
        return instrName
    except Exception as err:
        return str(err)

def interface_SavePicture(instrName, PictureName, SaveRoutePicture):
    """
        设置保存图片
        :param PictureSaveRoute: 图片保存路径
        :param PictureName: 保存图片名称
        :param SavePicture 确认保存图片
        :param instrName: 示波器ID
        :return:示波器ID
        """
    try:
        WAVERUNNER = WAVERUNNER8254(instrName)
        WAVERUNNER.save_screen(PictureName, SaveRoutePicture)
        return instrName
    except Exception as err:
        return str(err)


# def interface_SavePicture_1G(instrName, PictureName, SaveRoute):
#     """
#         设置保存图片
#         :param PictureSaveRoute: 图片保存路径
#         :param PictureName: 保存图片名称
#         :param SavePicture 确认保存图片
#         :param instrName: 示波器ID
#         :return:示波器ID
#         """
#     try:
#         WAVERUNNER = WAVERUNNER8254(instrName)
#         WAVERUNNER.save_screen_1G(PictureName, SaveRoute)
#         return instrName
#     except Exception as err:
#         return str(err)


def interface_SaveWaveform(instrName, WaveformName, SaveRoute):
    """
        :param WaveformName: 保存波形名称
        :param SaveRoute:波形保存路径
        :param instrName: 示波器ID
        :return:示波器ID
        """
    try:
        WAVERUNNER = WAVERUNNER8254(instrName)
        WAVERUNNER.save_Waveform(WaveformName, SaveRoute)
        return instrName
    except Exception as err:
        return str(err)


def interface_SaveWaveform_1GSaveWaveform(instrName, WaveformName, SaveRoute):
    """
        :param WaveformName: 保存波形名称
        :param SaveRoute:波形保存路径
        :param instrName: 示波器ID
        :return:示波器ID
        """
    try:
        WAVERUNNER = WAVERUNNER8254(instrName)
        WAVERUNNER.save_Waveform_1G(WaveformName, SaveRoute)
        return instrName
    except Exception as err:
        return str(err)


def interface_Set_CursorsPos(instrName, CursorsType, XPos1, XPos2, YPos1, YPos2, VerScale, VerOffset):
    """
            :param VerScale: 垂直刻度
            :param VerOffset: 偏置电压
            :param XPos1: 横坐标1的坐标
            :param XPos2:横坐标2的坐标
            :param YPos1: 竖坐标1的位置
            :param YPos2: 竖坐标2的位置
            :param instrName: 示波器ID
            :return:示波器ID
            """
    try:
        XPos1 = None if XPos1 is None else float(XPos1)
        XPos2 = None if XPos2 is None else float(XPos2)
        YPos1 = None if YPos1 is None else float(YPos1)
        YPos2 = None if YPos2 is None else float(YPos2)
        VerScale = float(VerScale)
        VerOffset = float(VerOffset)
        WAVERUNNER = WAVERUNNER8254(instrName)
        YPos1 = (YPos1 + VerOffset) / VerScale
        YPos2 = (YPos2 + VerOffset) / VerScale
        WAVERUNNER.Set_CursorsPos(CursorsType, XPos1, XPos2, YPos1, YPos2)
        return instrName
    except Exception as err:
        return str(err)


def interface_TriggerMode(instrName):
    """
        查询触发模式/状态
        """
    try:
        WAVERUNNER = WAVERUNNER8254(instrName)
        result = WAVERUNNER.TriggerMode()
        return result
    except Exception as err:
        return str(err)


def interface_PersistedNum(instrName,n,MeasureType):
    """
            查询余晖次数
            """
    try:
        WAVERUNNER = WAVERUNNER8254(instrName)
        result = WAVERUNNER.PersistedNum(n,MeasureType)
        return result
    except Exception as err:
        return str(err)


def interface_save_file(instrName, OsSaveRoute, LocalPath, OsPath,SetChannelName):
    """
    保存示波器波形图片，并将波形图片copy到本地
    :param instrName:示波器IP
    :param OsSaveRoute:如 D:\\osFile\\
    :param LocalPath:本地地址 如 D:\\
    :param SetChannelName :信号名称
    :param OsPath:本地访问示波器的地址  如 \\169.254.8.199\osFile
    :return:
    """
    picture_name = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    # 如果是最后一个测量值则保存图片
    interface_SavePicture(instrName, SetChannelName + str(picture_name), OsSaveRoute)
    time.sleep(0.5)
    # 2.1、 copy图片到本地
    log_pic = LocalPath + SetChannelName + str(picture_name) + ".png"
    server_pic = OsPath + SetChannelName + str(picture_name) + ".png"
    shutil.copyfile(server_pic, log_pic)
    time.sleep(1)
    return log_pic


def interface_crosstalk(CsvPath, BaseValue, TopValue):
    """
    返回串扰数据信息
    :param CsvPath:数据文件路径
    :param BaseValue: 低电平有效值
    :param TopValue: 高电平有效值
    :return:
    """
    BaseValue = float(BaseValue)
    TopValue = float(TopValue)
    test = SpiSignalQuality()
    return test.crosstalk(CsvPath, BaseValue, TopValue)


def interface_check_back(CsvPath, BaseValue, TopValue):
    """
    返回串扰数据信息
    :param CsvPath:数据文件路径
    :param BaseValue: 低电平有效值
    :param TopValue: 高电平有效值
    :return:
    """
    BaseValue = float(BaseValue)
    TopValue = float(TopValue)
    test = SpiSignalQuality()
    return test.check_back(CsvPath, BaseValue, TopValue)

def interface_check_step(CsvPath, BaseValue, TopValue, threshold):
    """
    返回台阶数据信息
    :param CsvPath:数据文件路径
    :param BaseValue: 低电平有效值
    :param TopValue: 高电平有效值
    :return:
    """
    BaseValue = float(BaseValue)
    TopValue = float(TopValue)
    threshold = float(threshold)
    test = SpiSignalQuality()
    # for var in cs_result:
    #     print("left=" + str(var[2]))
    #     print("right=" + str(var[3]))
    #     print("result=" + str(var[4]))
    # # 用log.log在平台端输出结果但不做判定
    # # 若结果为空则代表无台阶
    # print(cs_result)
    return test.check_step(CsvPath, BaseValue, TopValue, threshold)


def interface_Zoom_set(instrName, ch, CenterPoint, ZoomScale):
    # instrName, ch, True, CenterPoint, TimeSet1 / 25
    try:
        WAVERUNNER = WAVERUNNER8254(instrName)
        WAVERUNNER.ZoomSplitScreen()
        WAVERUNNER.OpenZoom(ch)
        WAVERUNNER.ZoomSet(ch, CenterPoint, ZoomScale)
        return instrName
    except Exception as err:
        return str(err)

def interface_ZoomAndCursors(instrName,ch):
    try:
        WAVERUNNER = WAVERUNNER8254(instrName)
        time.sleep(1)
        WAVERUNNER.Cursors(False)
        # WAVERUNNER.CloseZoom(ch,True)
        time.sleep(1)
        WAVERUNNER.CloseZoom(ch, False)
        return instrName
    except Exception as err:
        return str(err)


def interface_Persistence_set(instrName,OpenPersistence,PersistedTime):
    """
    余晖设置
    :param OpenPersistence:打开余晖
    :param AllLockPersistence: 全部锁定
    :param PersistenceStyle: 余晖设置为模拟
    :param PersistedTime：设置余晖时间，此处固定为无限
    :return:
    """
    try:
        WAVERUNNER = WAVERUNNER8254(instrName)
        WAVERUNNER.OpenPersistence(OpenPersistence)
        WAVERUNNER.AllLockPersistence()
        WAVERUNNER.PersistenceStyle()
        WAVERUNNER.PersistedTime(PersistedTime)
        return instrName
    except Exception as err:
        return str(err)


def interface_TriggerHoldoffTime(instrName,HoldoffTime):
    """
        触发抑制
        :param HoldoffTime:抑制时间设置
        :return:
        """
    try:
        WAVERUNNER = WAVERUNNER8254(instrName)
        WAVERUNNER.TriggerHoldoffType("Time")
        WAVERUNNER.TriggerHoldoffTime(HoldoffTime)
        return instrName
    except Exception as err:
        return str(err)

def interface_NormalType(instrName):
    """
            单纯Normal触发
            :return:
            """
    try:
        WAVERUNNER = WAVERUNNER8254(instrName)
        WAVERUNNER.NormalType()
        return instrName
    except Exception as err:
        return str(err)

def interface_StopType(instrName):
    """
            停止触发
            :return:
            """
    try:
        WAVERUNNER = WAVERUNNER8254(instrName)
        WAVERUNNER.StopType()
        return instrName
    except Exception as err:
        return str(err)

def interface_Jitter_Set(instrName):
    """
                抖动测试设置
                :return:
                """
    try:
        WAVERUNNER = WAVERUNNER8254(instrName)
        WAVERUNNER.SetJitter()
        return instrName
    except Exception as err:
        return str(err)



if __name__ == '__main__':
    instrName = "TCPIP::" + "169.254.8.199" + "::INSTR"
    DisplayGridMode = 'Single'
    Phone_Control = ''
    ch = 1
    SetChannelName = 'CLK'
    VerScale = 0.4
    VerOffset = -1
    SetHorOffset = -1e-6
    TimeSet = 5E-7
    SampleRate = "FixedSampleRate"
    measure = "Measurement"
    Measure = "DeltaPeriodAtLevel"
    trigger_type = "Negative"
    trigger_ch = "C1"
    trigger_level = 1
    CursorsType1 = "VertRel"
    CursorsType2 = "BothRel"
    OsSaveRoute = "D:\\osFile\\"
    LocalPath = "d:\\tmp\\"
    OsPath = "//169.254.8.199/osFile/"
    CrossTalk = 0.2  # 串扰阈值 v
    OverShoot = 0.3  # 过冲阈值 v
    threshold = 0.01 # 台阶阈值 V
    # 选择测试点对应测量值
    testCaseClk = ["Ampl", "Top", "Base", "OverShootNegative", "OverShootPositive", "Duty", "Width", "Widn", "Max",
                   "Min", "Period", "Freq", "Rise", "Fall"]
    testCaseCS = ["Ampl", "Top", "Base", "Max", "Min", "Duty", "OverShootNegative", "OverShootPositive"]
    testCaseMISO = ["Ampl", "Top", "Base", "Max", "Min", "Duty", "OverShootNegative", "OverShootPositive"]
    testCaseMOSI = ["Ampl", "Top", "Base", "Max", "Min", "OverShootNegative", "OverShootPositive"]
    TestCase = testCaseClk


    # TestCase = ["ampl", "Top", "Base", "OverShootNegative", "OverShootPositive", "Duty", "Width", "Widn", "max", "min",
    #             "Period", "Freq"]

    OsDevice = interface_initial(instrName, DisplayGridMode)
    # 设置通道名称(ch, SetChannelName)
    ChannelName = interface_set_channel_name(instrName, ch, SetChannelName)
    # 设置垂直(ch,VerScale,VerOffset)
    VerticalDevice = interface_Set_channel_vertical(instrName, ch, VerScale, VerOffset)
    # 设置时基(ch,HorOffset,TimeSet,SampleRate)
    TimeSetDevice = interface_Set_channel_TimeBase(instrName, SetHorOffset, TimeSet, SampleRate)
    # 设置触发(instrName,trigger_type, trigger_ch, trigger_level)
    if measure == "Measurement":
        TriggerDevices = interface_Trigger_Measurement(instrName,trigger_ch,Measure, trigger_level)
    else:
        TriggerDevices = interface_Trigger(instrName, trigger_type, trigger_ch, trigger_level)

    if Phone_Control == "NFC":
        phone.interface_NFC()

    # 等待波形触发
    count = 0
    while True:
        count += 1
        time.sleep(1)
        TriMode = interface_TriggerMode(instrName)
        if TriMode.split()[1] == "Stopped":
            break
        if count >= 20:
            raise Exception("在20s之内未能捕捉到正确的波形，请重新测试")

    MeasureResult = {'PngPaths': []}
    test_case_len = len(TestCase)
    PngPath = ''
    PngPath2 = ''
    if test_case_len <= 8:
        for i in range(test_case_len):
            interface_AddOneMeasure_testCase(instrName, i, TestCase[i])
        time.sleep(1)
        for i in range(test_case_len):
            # 1、取出数据
            MeasureResult[TestCase[i]] = float(interface_MeasuresResult(instrName, i + 1, "max").split()[1])
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
                    MeasureResult[TestCase[i + 8]] = float(interface_MeasuresResult(instrName, i + 1, "max").split()[1])
            elif index > 8:
                interface_AddOneMeasure_testCase(instrName, index - 8, TestCase[index])
            elif index == 8:
                # 如果是第8个参数
                time.sleep(1)
                for i in range(index):
                    # 1、取出数据
                    MeasureResult[TestCase[i]] = float(interface_MeasuresResult(instrName, i + 1, "max").split()[1])
                # 2、保存图片到示波器
                PngPath = interface_save_file(instrName, OsSaveRoute, LocalPath, OsPath,SetChannelName)
                # 2.2 删除所有的测量值
                interface_Delete_Measure(instrName)
                # 2.3 添加新的测量值
                interface_AddOneMeasure_testCase(instrName, 0, TestCase[index])
            else:
                interface_AddOneMeasure_testCase(instrName, index, TestCase[index])
            index += 1
    if len(PngPath) != 0:
        MeasureResult['PngPaths'].append(PngPath)
    if len(PngPath2) != 0:
        MeasureResult['PngPaths'].append(PngPath2)

    # 抓取Top、Base、上冲、下冲值
    TopValue = MeasureResult['Top']
    BaseValue = MeasureResult['Base']
    Positive_OverShoot = MeasureResult['OverShootPositive'] * (TopValue - BaseValue) / 100
    Negative_OverShoot = MeasureResult['OverShootNegative'] * (TopValue - BaseValue) / 100
    # 保存波形
    WaveformName = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    SaveWaveform = interface_SaveWaveform(instrName, WaveformName, OsSaveRoute)
    # 2.5G
    # SaveWaveform = interface_SaveWaveform(instrName, WaveformName, SaveRoute)
    # SavePicture = interface_SavePicture(instrName, PictureName, SaveRoute)

    # 将csv文件保存至本地分析
    time.sleep(2)
    ServerPathWaveform = OsPath + WaveformName + ".csv"
    CsvPath = LocalPath + WaveformName + ".csv"
    shutil.copyfile(ServerPathWaveform, CsvPath)

    # 判断是否过冲
    voltage = TopValue - BaseValue
    # 过冲，输出测量值
    # 上冲大于0.3v
    # if (Positive_OverShoot >= OverShoot) | (Negative_OverShoot >= OverShoot):        
    if Positive_OverShoot >= OverShoot:
        TimeSetDevice = interface_Set_channel_TimeBase(instrName, 0, TimeSet / 5, SampleRate)
        overshoot_CursorsPos = interface_Set_CursorsPos(instrName, CursorsType1, 65535, 65535, TopValue,
                                                         TopValue + Positive_OverShoot, VerScale, VerOffset)
    #     interface_Zoom_set(instrName, ch, 0, TimeSet/5)
        time.sleep(1)
        PngPath3 = interface_save_file(instrName, OsSaveRoute, LocalPath, OsPath,SetChannelName)
    elif Negative_OverShoot >= OverShoot:
        TimeSetDevice = interface_Set_channel_TimeBase(instrName, 0, TimeSet / 5, SampleRate)
        overshoot_CursorsPos = interface_Set_CursorsPos(instrName, CursorsType1, 65535, 65535, BaseValue,
                                                         BaseValue - Negative_OverShoot, VerScale, VerOffset)
    #     interface_Zoom_set(instrName, ch, 0, TimeSet/5)
        time.sleep(1)
        PngPath3 = interface_save_file(instrName, OsSaveRoute, LocalPath, OsPath,SetChannelName)
        time.sleep(1)
        MeasureResult['PngPaths'].append(PngPath3)

    test = SpiSignalQuality()
    ct_result = test.crosstalk(CsvPath, BaseValue, TopValue)  # 此处开始判断是否有串扰
    # 判断是否串扰
    if (ct_result['low_max'] - ct_result['low_min'] >= CrossTalk) \
            | (ct_result['high_max'] - ct_result['high_min'] >= CrossTalk):  # 有串扰情况
        # 改变时基
        # TimeSetDevice = interface_Set_channel_TimeBase(instrName, 0, 5E-5, SampleRate)  # 注：MISO时基调整与CLK不同

        if ct_result['low_max'] - ct_result['low_min'] >= CrossTalk:
            interface_Set_CursorsPos(instrName, CursorsType1, None, None,
                                     ct_result['low_max'], ct_result['low_min'], VerScale, VerOffset)
            MeasureResult["crosstalk"] = str(ct_result['low_max']) + "," + str(ct_result['low_min'])
            # 有串扰则标出游标位置
            ct_CursorsPos = interface_Set_CursorsPos(instrName, CursorsType1, 65535, 65535, ct_result['low_max'],
                                                     ct_result['low_min'], VerScale, VerOffset)

        elif ct_result['high_max'] - ct_result['high_min'] >= CrossTalk:
            interface_Set_CursorsPos(instrName, CursorsType1, None, None,
                                     ct_result['high_max'], ct_result['high_min'], VerScale, VerOffset)
            MeasureResult["crosstalk"] = str(ct_result['high_max']) + "," + str(ct_result['high_min'])
            # 有串扰则标出游标位置
            ct_CursorsPos = interface_Set_CursorsPos(instrName, CursorsType1, 65535, 65535, ct_result['high_max'],
                                                     ct_result('high_min'), VerScale, VerOffset)

        # 保存图潘，copy到本地
        time.sleep(1)
        PngPath4 = interface_save_file(instrName, OsSaveRoute, LocalPath, OsPath,SetChannelName)
        time.sleep(1)
        MeasureResult['PngPaths'].append(PngPath4)

    # 判断是否有回沟
    cb_result = test.check_back(CsvPath, BaseValue, TopValue)
    if len(cb_result) != 0:
        # 有回勾则标出游标位置
        cb_CursorsPos = interface_Set_CursorsPos(instrName, CursorsType2, cb_result['x1'], cb_result['x2'],
                                                 cb_result['y1'],
                                                 cb_result['y2'], VerScale, VerOffset)
        CenterPoint = cb_result['x1']
        interface_Zoom_set(instrName, ch, CenterPoint, TimeSet/25)
        time.sleep(1)
        PngPath5 = interface_save_file(instrName, OsSaveRoute, LocalPath, OsPath,SetChannelName)
        time.sleep(1)
        MeasureResult['PngPaths'].append(PngPath5)
        MeasureResult["back"] = str(cb_result)
        # 2.5G
        # SavePicture = interface_SavePicture(instrName, PictureName, SaveRoute)

    # 判断是否有台阶
    cs_result = test.check_step(CsvPath, BaseValue, TopValue,threshold)
    if len(cs_result) != 0:
        # log.log有台阶，输出台阶电压
        MeasureResult["step"] = str(cs_result)

    # MeasureResult["PngPath"] = PngPath
    # MeasureResult["PngPath2"] = PngPath2


    print(MeasureResult)
