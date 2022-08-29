import datetime
import os
import sys
import ast
import re
import shutil
import time
import uiautomator2 as u2
import threading
from http_service import HttpService, MessageToCSharpType
import math

# pack:功能块，如示波器，此参数不能省
# module:功能块类型，如示波器MDO3054，此参数不能省
# interface:功能块已经实现的接口，此参数不能省
# 其余参数按照实际需求进行传递
class Component(object):
    def __init__(self, interface):
        self.pack = "pack_oscilloscope"
        self.module = "module_WAVERUNNER8254_SystemClock"
        self.interface = interface

class Component_phone(object):
    def __init__(self, interface):
        self.pack = "pack_phoneself"
        self.module = "module_phone_run"
        self.interface = interface


log = MessageToCSharpType("")
http_service = HttpService()

def wifi_Control():
    if Phone_Control == "wifi_Control":
        while F:
            a = u2.connect_usb()
            a.shell("svc wifi enable")  # 打开WIFI
            time.sleep(1)
            a.shell("svc wifi disable")  # 关闭WIFI
F = 1

def nfc_Control():
    if Phone_Control == "nfc_Control":
        while F:
            a = u2.connect_usb()
            a.shell("svc nfc enable")  # 打开NFC
            time.sleep(1)
            a.shell("svc nfc disable")  # 关闭NFC
F = 1

# 调试脚本
if __name__ == '__main__':
    try:
        strReceive = sys.argv[1]
        # strReceive = r''
        log.log(strReceive)
        parameterList = ast.literal_eval(strReceive)
        log.log(parameterList)
        PngPath2 = ""


        instrName = parameterList["instrName"]
        DisplayGridMode = 'Single'
        ch = parameterList["ch"]
        Phone_Control = parameterList["Phone_Control"]
        SetChannelName = parameterList["SetChannelName"]
        # SetChannelName = "XOI"
        # C_Top = 1.8
        C_Top = float(parameterList["C_Top"])
        C_Freq = float(parameterList["C_Freq"])
        # C_Freq = 38.4E+6
        VerScale = C_Top/8
        VerOffset = -3*VerScale
        SetHorOffset = float(parameterList["SetHorOffset"])
        # Freq = "26E+6"  # 芯片频率标准MHz
        TimeSet1 = 0.5/float(C_Freq)  # 多周期时基
        TimeSet2 = 0.1/float(C_Freq)  # 单周期时基
        SampleRate = parameterList["SampleRate"]
        Measure = "DeltaPeriodAtLevel"
        trigger_type = parameterList["trigger_type"]
        trigger_ch = parameterList["trigger_ch"]
        OpenPersistence = True
        # trigger_level = float(parameterList["trigger_level"])
        trigger_level = 0.45
        HoldoffTime1 = -4 * TimeSet1
        HoldoffTime2 = -4 * TimeSet2
        C_Rise = float(parameterList["C_Rise"])
        # C_Rise = 1E-9
        Risingtimeset = C_Rise
        CursorsType1 = parameterList["CursorsType1"]
        CursorsType2 = parameterList["CursorsType2"]
        Risetime = parameterList["Risetime"]  # TrueorFlase  判断是否有上升时间，用来决定是否测试上升沿触发以及下降沿触发
        OsSaveRoute = parameterList["OsSaveRoute"]
        LocalPath = parameterList["LocalPath"]
        log.log('log.log(LocalPath)=' + LocalPath)
        OsPath = "//" + instrName.split("::")[1] + "/" + OsSaveRoute.split("/")[-2] + "/"
        log.log(OsPath)
        CrossTalk = float(parameterList["CrossTalk"])  # 串扰阈值 v
        OverShoot = float(parameterList["OverShoot"])  # 过冲阈值 v
        threshold = 0.01  # 台阶阈值 V
        # MEASURE = parameterList["MEASURE"]  # MEASURE等于JitterTest则执行抖动测试
        # 选择测试点对应测量值
        MultiPeriod_testCase = ["Freq", "Duty", "Top", "Base"]  # ["Freq", "Duty", "Top", "Base"]  # 多周期测量值
        SingleCycle_testCase = ["Rise", "Top", "Base", "OverShootNegative", "OverShootPositive", "Max", "Min"]  # 单周期测量值
        RisingTrigger_testCase = ["Rise"]  # 上升沿触发测量值
        FallingTrigger_testCase = ["Fall"]  # 下降沿触发测量值
        # TestCase = parameterList["TestCase"].replace(" ", "").split(',')
        # log.log('log.log(TestCase)=' + str(TestCase))
# if __name__ == '__main__':
#     try:
#         instrName = "TCPIP::" + "169.254.8.199" + "::INSTR"
#         DisplayGridMode = 'Single'
#         ch = 1
#         SetChannelName = ''
#         VerScale = 0.4
#         VerOffset = -1
#         SetHorOffset = 0
#         Freq = "26E+6"  # 芯片频率标准MHz
#         TimeSet1 = 0.5/float(Freq)  # 5周期时基
#         TimeSet2 = 0.1/float(Freq)  # 单周期时基
#         SampleRate = "FixedSampleRate"
#         # measure = "Measurement"
#         Measure = "DeltaPeriodAtLevel"
#         trigger_type = "Negative"
#         trigger_ch = "C1"
#         OpenPersistence = True
#         trigger_level = 0.9
#         HoldoffTime = 80E-9
#         CursorsType1 = "VertRel"
#         CursorsType2 = "BothRel"
#         OsSaveRoute = "D:\\osFile\\"
#         LocalPath = "d:\\tmp\\"
#         OsPath = "//169.254.8.199/osFile/"
#         Risetime = "false" # TrueorFlase  判断是否有上升时间，用来决定是否测试上升沿触发以及下降沿触发
#         CrossTalk = 0.2  # 串扰阈值 v
#         OverShoot = 0.3  # 过冲阈值 v
#         threshold = 0.01 # 台阶阈值
#         Phone_Control = "wifi_Control"
#         # 选择测试点对应测量值
#         MultiPeriod_testCase = ["Freq","Duty","Top","Base"] #["Freq", "Duty", "Top", "Base"]  # 多周期测量值
#         SingleCycle_testCase = ["Rise", "Top", "Base", "OverShootNegative", "OverShootPositive", "Max","Min"] # 单周期测量值
#         RisingTrigger_testCase = ["Rise"] # 上升沿触发测量值
#         FallingTrigger_testCase = ["Fall"] # 下降沿触发测量值
#         TestCase = MultiPeriod_testCase

        # **************************************************************************************************************
        # --------------------------------------------此处为多周期触发-----------------------------------------------------
        # **************************************************************************************************************
        MeasureResult1 = {}
        test_case_len = len(MultiPeriod_testCase)
        # 创建图片保存列表
        MeasureResult1 = {'PngPaths': []}

        log.log("初始化示波器")
        com = Component("interface_initial")
        com.instrName = instrName
        time.sleep(5)
        com.DisplayGridMode = DisplayGridMode
        device = http_service.post_message(com)

        log.log("设置示波器通道名称")
        com = Component("interface_set_channel_name")
        com.instrName = instrName
        com.ch = ch
        com.SetChannelName = SetChannelName
        result1 = http_service.post_message(com)

        log.log("设置示波器垂直")
        com = Component("interface_Set_channel_vertical")
        com.instrName = instrName
        com.ch = ch
        com.VerScale = VerScale
        com.VerOffset = VerOffset
        result1 = http_service.post_message(com)

        log.log("设置示波器时基")
        com = Component("interface_Set_channel_TimeBase")
        com.instrName = instrName
        com.SetHorOffset = SetHorOffset
        com.TimeSet = TimeSet1
        com.SampleRate = SampleRate
        result1 = http_service.post_message(com)

        log.log("设置示波器触发")
        com = Component("interface_Trigger")
        com.instrName = instrName
        com.trigger_type = trigger_type
        com.trigger_ch = trigger_ch
        com.trigger_level = trigger_level
        result1 = http_service.post_message(com)

        log.log("设置波形抑制")
        com = Component("interface_TriggerHoldoffTime")
        com.instrName = instrName
        com.HoldoffTime = HoldoffTime1
        result1 = http_service.post_message(com)

        # 等待波形触发
        # 加入手机控制
        if Phone_Control == "nfc_Control":
            t = threading.Thread(target=nfc_Control, name='phone')
            t.start()
        elif Phone_Control == "wifi_Control":
            t = threading.Thread(target=wifi_Control, name='phone')
            t.start()
        count = 0
        log.log("等待波形触发")
        while True:
            count += 1
            time.sleep(1)
            com = Component("interface_TriggerMode")
            com.instrName = instrName
            TriMode = http_service.post_message(com)
            if TriMode.split()[1] == "Stopped":
                break
            if count >= 20:
                raise Exception("在20s之内未能捕捉到正确的波形，请重新测试")

        MeasureResult1 = {}
        test_case_len = len(MultiPeriod_testCase)
        # 创建图片保存列表
        MeasureResult1 = {'PngPaths': []}

        log.log("添加得出测量值")
        com = Component("interface_get_measurement_result")
        com.instrName = instrName
        com.mr = MeasureResult1
        com.tc = MultiPeriod_testCase
        com.OsSaveRoute = OsSaveRoute
        com.LocalPath = LocalPath
        com.OsPath = OsPath
        com.SetChannelName = SetChannelName
        MeasureResult1 = http_service.post_message(com)

        # **************************************************************************************************************
        # --------------------------------------------此处为单周期触发-----------------------------------------------------
        # **************************************************************************************************************
        log.log("设置示波器时基")
        com = Component("interface_Set_channel_TimeBase")
        com.instrName = instrName
        com.SetHorOffset = SetHorOffset
        com.TimeSet = TimeSet2
        com.SampleRate = SampleRate
        result1 = http_service.post_message(com)

        log.log("设置示波器余晖")
        com = Component("interface_Persistence_set")
        com.instrName = instrName
        com.OpenPersistence = OpenPersistence
        result1 = http_service.post_message(com)

        log.log("设置示波器触发")
        com = Component("interface_set_trigger_XTirggerType")
        com.instrName = instrName
        com.trigger_type = trigger_type
        com.trigger_ch = trigger_ch
        com.trigger_level = trigger_level
        result1 = http_service.post_message(com)

        # 设置触发位置
        log.log("设置触发水平位置")
        com = Component("interface_TriggerHor")
        com.instrName = instrName
        com.TriggerHor = -4 * TimeSet2
        result1 = http_service.post_message(com)

        log.log("设置波形抑制")
        com = Component("interface_TriggerHoldoffTime")
        com.instrName = instrName
        com.HoldoffTime = HoldoffTime2
        result1 = http_service.post_message(com)

        log.log("选择触发类型为Normal")
        com = Component("interface_NormalType")
        com.instrName = instrName
        result1 = http_service.post_message(com)

        # 创建图片保存列表
        MeasureResult2 = {'PngPaths': []}
        # 输入测量值
        test_case_len = len(SingleCycle_testCase)

        log.log("添加得出测量值")
        com = Component("interface_get_measurement_result")
        com.instrName = instrName
        com.mr = MeasureResult2
        com.tc = SingleCycle_testCase
        com.OsSaveRoute = OsSaveRoute
        com.LocalPath = LocalPath
        com.OsPath = OsPath
        com.SetChannelName = SetChannelName
        MeasureResult2 = http_service.post_message(com)
        # MeasureResult2['PngPaths'].clear()

        log.log("设置余晖大于200次时停止累积")
        while 1:
            time.sleep(1)
            com = Component("interface_PersistedNum")
            com.instrName = instrName
            com.n = 1
            com.MeasureType = "num"
            PersistedNum = http_service.post_message(com)
            if int(re.findall('\d+', PersistedNum)[0]) > 200:
                log.log("停止累积")
                com = Component("interface_StopType")
                com.instrName = instrName
                result1 = http_service.post_message(com)
                break

        log.log("保存图片")
        com = Component("interface_save_file")
        com.instrName = instrName
        com.OsSaveRoute = OsSaveRoute
        com.LocalPath = LocalPath
        com.OsPath = OsPath
        com.SetChannelName = SetChannelName
        PngPath2 = http_service.post_message(com)
        time.sleep(1)
        MeasureResult2['PngPaths'].append(PngPath2)

        log.log("保存波形")
        WaveformName = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        com = Component("interface_SaveWaveform")
        com.instrName = instrName
        com.WaveformName = WaveformName
        com.SaveRoute = OsSaveRoute
        SaveWaveform = http_service.post_message(com)

        log.log("将csv文件保存至本地分析")
        time.sleep(2)
        ServerPathWaveform = OsPath + WaveformName + ".csv"
        CsvPath = LocalPath + WaveformName + ".csv"
        shutil.copyfile(ServerPathWaveform, CsvPath)

        log.log("判断余晖Top值")
        com = Component("interface_MeasuresResult")
        com.instrName = instrName
        com.ph = 2
        com.Measure = "max"
        float_tmp = http_service.post_message(com)
        Top = float(float_tmp.split()[1])

        log.log("判断余晖Base值")
        com = Component("interface_MeasuresResult")
        com.instrName = instrName
        com.ph = 3
        com.Measure = "min"
        float_tmp = http_service.post_message(com)
        Base = float(float_tmp.split()[1])

        log.log("判断是否过冲")
        com = Component("interface_test_overshoot")
        com.instrName = instrName
        com.mr = MeasureResult2
        com.OverShoot = OverShoot
        com.TimeSet1 = TimeSet2
        com.SampleRate = SampleRate
        com.CursorsType1 = CursorsType1
        com.VerScale = VerScale
        com.VerOffset = VerOffset
        flag = http_service.post_message(com)

        if flag:
            log.log("保存图片")
            com = Component("interface_save_file")
            com.instrName = instrName
            com.OsSaveRoute = OsSaveRoute
            com.LocalPath = LocalPath
            com.OsPath = OsPath
            com.SetChannelName = SetChannelName
            PngPath3 = http_service.post_message(com)
            time.sleep(1)
            MeasureResult2['PngPaths'].append(PngPath3)

        log.log("判断是否有串扰")
        com = Component("interface_test_crosstalk")
        com.instrName = instrName
        com.mr = MeasureResult2
        com.CrossTalk = CrossTalk
        com.CursorsType1 = CursorsType1
        com.VerScale = VerScale
        com.VerOffset = VerOffset
        com.CsvPath = CsvPath
        flag = http_service.post_message(com)

        if flag:
            log.log("保存图片")
            com = Component("interface_save_file")
            com.instrName = instrName
            com.OsSaveRoute = OsSaveRoute
            com.LocalPath = LocalPath
            com.OsPath = OsPath
            com.SetChannelName = SetChannelName
            PngPath4 = http_service.post_message(com)
            time.sleep(1)
            MeasureResult2['PngPaths'].append(PngPath4)

        log.log("判断是否有回勾")
        com = Component("interface_test_back")
        com.instrName = instrName
        com.mr = MeasureResult2
        com.CursorsType2 = CursorsType2
        com.VerScale = VerScale
        com.VerOffset = VerOffset
        com.ch = ch
        com.TimeSet1 = TimeSet2
        com.CsvPath = CsvPath
        flag = http_service.post_message(com)

        if flag:
            log.log("保存图片")
            com = Component("interface_save_file")
            com.instrName = instrName
            com.OsSaveRoute = OsSaveRoute
            com.LocalPath = LocalPath
            com.OsPath = OsPath
            com.SetChannelName = SetChannelName
            PngPath5 = http_service.post_message(com)
            time.sleep(1)
            MeasureResult2['PngPaths'].append(PngPath5)

        log.log("判断是否有台阶")
        com = Component("interface_test_step")
        com.mr = MeasureResult2
        com.threshold = threshold
        com.CsvPath = CsvPath
        flag = http_service.post_message(com)

        if flag:
            log.log("保存图片")
            com = Component("interface_save_file")
            com.instrName = instrName
            com.OsSaveRoute = OsSaveRoute
            com.LocalPath = LocalPath
            com.OsPath = OsPath
            com.SetChannelName = SetChannelName
            PngPath6 = http_service.post_message(com)
            time.sleep(1)
            MeasureResult2['PngPaths'].append(PngPath6)

        # **************************************************************************************************************
        # --------------------------------------------此处为上升沿触发-----------------------------------------------------
        # **************************************************************************************************************
        # 创建图片保存列表
        MeasureResult3 = {'PngPaths': []}
        MeasureResult4 = {'PngPaths': []}
        if Risetime == "True":
            # 加入如果标准有上升时间，则触发
            # 再次设置，触发上升沿波形
            log.log("设置示波器触发")
            com = Component("interface_set_trigger_XTirggerType")
            com.instrName = instrName
            com.trigger_type = "Positive"
            com.trigger_ch = trigger_ch
            com.trigger_level = trigger_level
            result1 = http_service.post_message(com)

            log.log("设置示波器时基")
            com = Component("interface_Set_channel_TimeBase")
            com.instrName = instrName
            com.SetHorOffset = SetHorOffset
            com.TimeSet = Risingtimeset  # 由于CLK上升/下降时间相同，因此直接采用上升时间
            com.SampleRate = SampleRate
            result1 = http_service.post_message(com)

            log.log("设置示波器余晖")
            com = Component("interface_Persistence_set")
            com.instrName = instrName
            com.OpenPersistence = OpenPersistence
            result1 = http_service.post_message(com)

            log.log("设置波形抑制")
            com = Component("interface_TriggerHoldoffTime")
            com.instrName = instrName
            com.HoldoffTime = 0
            result1 = http_service.post_message(com)

            # 设置触发位置
            log.log("设置触发水平位置")
            com = Component("interface_TriggerHor")
            com.instrName = instrName
            com.TriggerHor = 0
            result1 = http_service.post_message(com)

            log.log("选择触发类型为Normal")
            com = Component("interface_NormalType")
            com.instrName = instrName
            result1 = http_service.post_message(com)

            MeasureResult3 = {}
            test_case_len = len(RisingTrigger_testCase)

            # 创建图片保存列表
            MeasureResult3 = {'PngPaths': []}

            log.log("添加得出测量值")
            com = Component("interface_get_measurement_result")
            com.instrName = instrName
            com.mr = MeasureResult3
            com.tc = RisingTrigger_testCase
            com.OsSaveRoute = OsSaveRoute
            com.LocalPath = LocalPath
            com.OsPath = OsPath
            com.SetChannelName = SetChannelName
            MeasureResult3 = http_service.post_message(com)
            # MeasureResult3['PngPaths'].clear()

            log.log("设置余晖大于200次时停止累积")
            while 1:
                time.sleep(2)
                com = Component("interface_PersistedNum")
                com.instrName = instrName
                com.n = 1
                com.MeasureType = "num"
                PersistedNum = http_service.post_message(com)
                if int(re.findall('\d+', PersistedNum)[0]) > 200:
                    log.log("停止累积")
                    com = Component("interface_StopType")
                    com.instrName = instrName
                    result1 = http_service.post_message(com)
                    break
            log.log("保存图片")
            com = Component("interface_save_file")
            com.instrName = instrName
            com.OsSaveRoute = OsSaveRoute
            com.LocalPath = LocalPath
            com.OsPath = OsPath
            com.SetChannelName = SetChannelName
            PngPath7 = http_service.post_message(com)
            time.sleep(1)
            MeasureResult3['PngPaths'].append(PngPath7)

            # **************************************************************************************************************
            # --------------------------------------------此处为下降沿触发-----------------------------------------------------
            # **************************************************************************************************************
            # 加入如果标准有上升时间，则触发
            # 再次设置，触发下降沿波形
            # 设置时基(ch,HorOffset,TimeSet2,SampleRate)
            log.log("设置示波器时基")
            com = Component("interface_Set_channel_TimeBase")
            com.instrName = instrName
            com.SetHorOffset = SetHorOffset
            com.TimeSet = Risingtimeset
            com.SampleRate = SampleRate
            result1 = http_service.post_message(com)

            log.log("设置示波器余晖")
            com = Component("interface_Persistence_set")
            com.instrName = instrName
            com.OpenPersistence = OpenPersistence
            result1 = http_service.post_message(com)

            log.log("设置示波器触发")
            com = Component("interface_set_trigger_XTirggerType")
            com.instrName = instrName
            com.trigger_type = trigger_type
            com.trigger_ch = trigger_ch
            com.trigger_level = trigger_level
            result1 = http_service.post_message(com)

            # 设置触发位置
            log.log("设置触发水平位置")
            com = Component("interface_TriggerHor")
            com.instrName = instrName
            com.TriggerHor = 0
            result1 = http_service.post_message(com)

            log.log("设置波形抑制")
            com = Component("interface_TriggerHoldoffTime")
            com.instrName = instrName
            com.HoldoffTime = 0
            result1 = http_service.post_message(com)

            log.log("选择触发类型为Normal")
            com = Component("interface_NormalType")
            com.instrName = instrName
            result1 = http_service.post_message(com)

            log.log("添加得出测量值")
            com = Component("interface_get_measurement_result")
            com.instrName = instrName
            com.mr = MeasureResult4
            com.tc = FallingTrigger_testCase
            com.OsSaveRoute = OsSaveRoute
            com.LocalPath = LocalPath
            com.OsPath = OsPath
            com.SetChannelName = SetChannelName
            MeasureResult4 = http_service.post_message(com)
            # MeasureResult4['PngPaths'].clear()

            log.log("设置余晖大于200次时停止累积")
            while 1:
                time.sleep(1)
                com = Component("interface_PersistedNum")
                com.instrName = instrName
                com.n = 1
                com.MeasureType = "num"
                PersistedNum = http_service.post_message(com)
                if int(re.findall('\d+', PersistedNum)[0]) > 200:
                    log.log("停止累积")
                    com = Component("interface_StopType")
                    com.instrName = instrName
                    result1 = http_service.post_message(com)
                    break

            log.log("保存图片")
            com = Component("interface_save_file")
            com.instrName = instrName
            com.OsSaveRoute = OsSaveRoute
            com.LocalPath = LocalPath
            com.OsPath = OsPath
            com.SetChannelName = SetChannelName
            PngPath8 = http_service.post_message(com)
            time.sleep(1)
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
        log.success(MeasureResultAll)

    except Exception as err:
        log.exception(str(err))






























