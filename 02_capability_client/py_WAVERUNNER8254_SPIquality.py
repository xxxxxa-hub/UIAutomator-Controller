import datetime
import os
import sys
import ast
import shutil
import time

from http_service import HttpService, MessageToCSharpType


# pack:功能块，如示波器，此参数不能省
# module:功能块类型，如示波器MDO3054，此参数不能省
# interface:功能块已经实现的接口，此参数不能省
# 其余参数按照实际需求进行传递
class Component(object):
    def __init__(self, interface):
        self.pack = "pack_oscilloscope"
        self.module = "module_WAVERUNNER8254_SPIquality"
        self.interface = interface

class Component_phone(object):
    def __init__(self, interface):
        self.pack = "pack_phoneself"
        self.module = "module_phone_run"
        self.interface = interface


log = MessageToCSharpType("")
http_service = HttpService()

# 调试脚本
if __name__ == '__main__':
    try:
        strReceive = r'{"clockchn":"CH1","datachn":"CH2","oscillographName":"lsltest",' \
                     r'"instrName":"TCPIP::169.254.8.199::INSTR","instrModel":"Tektronix MDO3000 Series",' \
                     r'"prjname":"21121","prjver":"Ver.A","signaltyp":"","LoopTimes":"1","datasignal":"NA",' \
                     r'"clksignal":"NA","expectAddress":"","autoTrig":"False","needInitScope":"False",' \
                     r'"TestCaseName":"JV0301(CNA402)\u003c--JV0301(CNA402)","TestUnit":"屏下指纹","rechipname":"JV0301",' \
                     r'"rechipnum":"CNA402","trchipname":"JV0301","trchipnum":"CNA402","prjdescr":"",' \
                     r'"useClkChannel":"True","useDataChannel":"True","testSceneName":"","DataSignalName":"NA",' \
                     r'"ClkSignalName":"NA","ChipAddress":"","loop_index":"1","TimeSet":"5E-7","trigger_ch":"C1",' \
                     r'"CrossTalk":"0.2","SampleRate":"FixedSampleRate","Phone_Control":"","measure":"","ch":"1",' \
                     r'"VerScale":"0.4","VerOffset":"-1","trigger_level":"1","CursorsType1":"VertRel",' \
                     r'"SetChannelName":"CLK","CursorsType2":"BothRel","SetHorOffset":"-1e-6","OverShoot":"0.3",' \
                     r'"trigger_type":"Negative","TestCase":"Ampl, Top, Base, OverShootNegative, OverShootPositive, ' \
                     r'Duty, Width, Widn, Max,Min, Period, Freq","LocalPath":"d:/tmp/","OsSaveRoute":"D:/osFile/",' \
                     r'"Python_File_Name":"Py_WaveRunner8254_SPIQuality.py",' \
                     r'"screenshotPath":"D:\\Documents\\Desktop\\0414\\sts\\01_Code\\STS\\Debug\\Testresult\\21121' \
                     r'\\Ver.A"} '
        log.log(strReceive)
        parameterList = ast.literal_eval(strReceive)
        log.log(parameterList)
        PngPath2 = ""
        # Phone_Control = "NFC"
        Phone_Control = parameterList["Phone_Control"]


        instrName = parameterList["instrName"]
        DisplayGridMode = 'Single'
        ch = parameterList["ch"]
        Phone_Control = parameterList["Phone_Control"]
        SetChannelName = parameterList["SetChannelName"]
        VerScale = float(parameterList["VerScale"])
        VerOffset = float(parameterList["VerOffset"])
        SetHorOffset = float(parameterList["SetHorOffset"])
        TimeSet = float(parameterList["TimeSet"])
        SampleRate = parameterList["SampleRate"]
        measure = parameterList["measure"]
        trigger_type = parameterList["trigger_type"]
        trigger_ch = parameterList["trigger_ch"]
        trigger_level = int(parameterList["trigger_level"])
        CursorsType1 = parameterList["CursorsType1"]
        CursorsType2 = parameterList["CursorsType2"]
        OsSaveRoute = parameterList["OsSaveRoute"]
        LocalPath = parameterList["screenshotPath"] + "\\"
        log.log('log.log(LocalPath)=' + LocalPath)
        OsPath = "//" + instrName.split("::")[1] + "/" + OsSaveRoute.split("/")[-2] + "/"
        log.log(OsPath)
        CrossTalk = float(parameterList["CrossTalk"])  # 串扰阈值 v
        OverShoot = float(parameterList["OverShoot"])  # 过冲阈值 v
        threshold = 0.01 # 台阶阈值 V
        # 选择测试点对应测量值
        # testCaseClk = parameterList["testCaseClk"]
        # testCaseCS = parameterList["testCaseCS"]
        # testCaseMISO = parameterList["testCaseMISO"]
        # testCaseMOSI = parameterList["testCaseMOSI"]
        TestCase = parameterList["TestCase"].replace(" ", "").split(',')
        log.log('log.log(TestCase)=' + str(TestCase))

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
        com.TimeSet = TimeSet
        com.SampleRate = SampleRate
        result1 = http_service.post_message(com)

        log.log("设置示波器触发")
        if measure == "Measurement":
            com = Component("interface_Trigger_Measurement")
            com.instrName = instrName
            com.trigger_ch = trigger_ch
            com.measure = measure
            com.trigger_level = trigger_level
            result1 = http_service.post_message(com)
        else:
            com = Component("interface_Trigger")
            com.instrName = instrName
            com.trigger_type = trigger_type
            com.trigger_ch = trigger_ch
            com.trigger_level = trigger_level
            result1 = http_service.post_message(com)

        if Phone_Control == "NFC":
            log.log("设置手机控制-NFC")
            com = Component_phone("interface_NFC")
            result1 = http_service.post_message(com)

        # 等待波形触发
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

        log.log("波形触发成功，可松开测试点")
        MeasureResult = {'PngPaths': []}
        test_case_len = len(TestCase)
        PngPath = ''
        PngPath2 = ''

        if test_case_len <= 8:
            for i in range(test_case_len):
                com = Component("interface_AddOneMeasure_testCase")
                com.instrName = instrName
                com.channel_no = i
                com.measure = TestCase[i]
                http_service.post_message(com)
            time.sleep(1)
            for i in range(test_case_len):
                com = Component("interface_MeasuresResult")
                com.instrName = instrName
                com.ph = i + 1
                com.Measure = "max"
                float_tmp = http_service.post_message(com)
                # 1、取出数据
                MeasureResult[TestCase[i]] = float(float_tmp.split()[1])
            # 2、保存图片到示波器
            com = Component("interface_save_file")
            com.instrName = instrName
            com.OsSaveRoute = OsSaveRoute
            com.LocalPath = LocalPath
            com.OsPath = OsPath
            PngPath = http_service.post_message(com)
        else:
            index = 0
            # 循环检测多个测量值
            while index <= test_case_len:
                if index == test_case_len:
                    time.sleep(1)
                    com = Component("interface_save_file")
                    com.instrName = instrName
                    com.OsSaveRoute = OsSaveRoute
                    com.LocalPath = LocalPath
                    com.OsPath = OsPath
                    PngPath2 = http_service.post_message(com)
                    for i in range(index - 8):
                        com = Component("interface_MeasuresResult")
                        com.instrName = instrName
                        com.ph = i + 1
                        com.Measure = "max"
                        float_tmp = http_service.post_message(com)
                        MeasureResult[TestCase[i + 8]] = float(float_tmp.split()[1])
                elif index > 8:
                    com = Component("interface_AddOneMeasure_testCase")
                    com.instrName = instrName
                    com.channel_no = index - 8
                    com.measure = TestCase[index]
                    http_service.post_message(com)
                elif index == 8:
                    # 如果是第8个参数
                    time.sleep(1)
                    for i in range(index):
                        # 1、取出数据
                        com = Component("interface_MeasuresResult")
                        com.instrName = instrName
                        com.ph = i + 1
                        com.Measure = "max"
                        float_tmp = http_service.post_message(com)
                        MeasureResult[TestCase[i]] = float(float_tmp.split()[1])
                    # 2、保存图片到示波器
                    com = Component("interface_save_file")
                    com.instrName = instrName
                    com.OsSaveRoute = OsSaveRoute
                    com.LocalPath = LocalPath
                    com.OsPath = OsPath
                    PngPath = http_service.post_message(com)
                    # 2.2 删除所有的测量值
                    com = Component("interface_Delete_Measure")
                    com.instrName = instrName
                    http_service.post_message(com)
                    # 2.3 添加新的测量值
                    com = Component("interface_AddOneMeasure_testCase")
                    com.instrName = instrName
                    com.channel_no = 0
                    com.measure = TestCase[index]
                    http_service.post_message(com)
                else:
                    # 添加新的测量值
                    com = Component("interface_AddOneMeasure_testCase")
                    com.instrName = instrName
                    com.channel_no = index
                    com.measure = TestCase[index]
                    http_service.post_message(com)
                index += 1
        if len(PngPath) != 0:
            MeasureResult['PngPaths'].append(PngPath)
        if len(PngPath2) != 0:
            MeasureResult['PngPaths'].append(PngPath2)

        # 抓取Top、Base、上冲、下冲值
        TopValue = MeasureResult['Top']
        BaseValue = MeasureResult['Base']
        log.log("上冲值：")
        log.log(MeasureResult['OverShootPositive'])
        log.log("下冲值：")
        log.log(MeasureResult['OverShootNegative'])
        Positive_OverShoot = MeasureResult['OverShootPositive'] * (TopValue - BaseValue) / 100
        Negative_OverShoot = MeasureResult['OverShootNegative'] * (TopValue - BaseValue) / 100
        # 保存波形
        WaveformName = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        com = Component("interface_SaveWaveform")
        com.instrName = instrName
        com.WaveformName = WaveformName
        com.SaveRoute = OsSaveRoute
        SaveWaveform = http_service.post_message(com)

        # 将csv文件保存至本地分析
        time.sleep(2)
        ServerPathWaveform = OsPath + WaveformName + ".csv"
        CsvPath = LocalPath + WaveformName + ".csv"
        shutil.copyfile(ServerPathWaveform, CsvPath)

        time.sleep(3)
        log.log("判断是否过冲")
        # 判断是否过冲
        voltage = TopValue - BaseValue
        if Positive_OverShoot >= OverShoot:
            com = Component("interface_Set_channel_TimeBase")
            com.instrName = instrName
            com.SetHorOffset = 0
            com.TimeSet = TimeSet/5
            com.SampleRate = SampleRate
            result1 = http_service.post_message(com)

            com = Component("interface_Set_CursorsPos")
            com.instrName = instrName
            com.CursorsType = CursorsType1
            com.XPos1 = 65535
            com.XPos2 = 65535
            com.YPos1 = TopValue
            com.YPos2 = TopValue + Positive_OverShoot
            com.VerScale = VerScale
            com.VerOffset = VerOffset
            PngPath3 = http_service.post_message(com)
            # MeasureResult["OverShoot"] =  str(Positive_OverShoot)

            time.sleep(1)
            com = Component("interface_save_file")
            com.instrName = instrName
            com.OsSaveRoute = OsSaveRoute
            com.LocalPath = LocalPath
            com.OsPath = OsPath
            PngPath3 = http_service.post_message(com)

        elif Negative_OverShoot >= OverShoot:
            com = Component("interface_Set_channel_TimeBase")
            com.instrName = instrName
            com.SetHorOffset = 0
            com.TimeSet = TimeSet / 5
            com.SampleRate = SampleRate
            result1 = http_service.post_message(com)

            com = Component("interface_Set_CursorsPos")
            com.instrName = instrName
            com.CursorsType = CursorsType1
            com.XPos1 = 65535
            com.XPos2 = 65535
            com.YPos1 = BaseValue
            com.YPos2 = BaseValue - Negative_OverShoot
            com.VerScale = VerScale
            com.VerOffset = VerOffset
            PngPath3 = http_service.post_message(com)
            # MeasureResult["OverShoot"] = str(Positive_OverShoot)

            com = Component("interface_save_file")
            com.instrName = instrName
            com.OsSaveRoute = OsSaveRoute
            com.LocalPath = LocalPath
            com.OsPath = OsPath
            PngPath3 = http_service.post_message(com)
            time.sleep(1)
            MeasureResult['PngPaths'].append(PngPath3)

            # 过冲，输出测量值
            # MeasureResult["OverShoot"] = str(Positive_OverShoot) + "," + str(Negative_OverShoot)
            # print(Positive_OverShoot, Negative_OverShoot)

        com = Component("interface_crosstalk")
        com.CsvPath = CsvPath
        com.BaseValue = BaseValue
        com.TopValue = TopValue
        ct_result = http_service.post_message(com)  # 此处开始判断是否有串扰
        
        log.log("判断是否串扰")
        # 判断是否串扰
        if (ct_result['low_max'] - ct_result['low_min'] >= CrossTalk) \
                | (ct_result['high_max'] - ct_result['high_min'] >= CrossTalk):  # 有串扰情况
            # 改变时基
            # TimeSetDevice = interface_Set_channel_TimeBase(instrName, 0, 5E-5, SampleRate)  # 注：MISO时基调整与CLK不同

            if ct_result['low_max'] - ct_result['low_min'] >= CrossTalk:
                com = Component("interface_Set_CursorsPos")
                com.instrName = instrName
                com.CursorsType = CursorsType1
                com.XPos1 = 65535
                com.XPos2 = 65535
                com.YPos1 = ct_result['low_max']
                com.YPos2 = ct_result['low_min']
                com.VerScale = VerScale
                com.VerOffset = VerOffset
                PngPath4 = http_service.post_message(com)
                MeasureResult["crosstalk"] = str(ct_result['low_max']) + "," + str(ct_result['low_min'])
                # 有串扰则游标标出位置
                com = Component("interface_Set_CursorsPos")
                com.instrName = instrName
                com.CursorsType = CursorsType1
                com.XPos1 = 65535
                com.XPos2 = 65535
                com.YPos1 = ct_result['low_max']
                com.YPos2 = ct_result['low_min']
                com.VerScale = VerScale
                com.VerOffset = VerOffset
                ct_CursorsPos = http_service.post_message(com)
            elif ct_result['high_max'] - ct_result['high_min'] >= CrossTalk:
                com = Component("interface_Set_CursorsPos")
                com.instrName = instrName
                com.CursorsType = CursorsType1
                com.XPos1 = 65535
                com.XPos2 = 65535
                com.YPos1 = ct_result['high_max']
                com.YPos2 = ct_result['high_min']
                com.VerScale = VerScale
                com.VerOffset = VerOffset
                PngPath4 = http_service.post_message(com)
                MeasureResult["crosstalk"] = str(ct_result['high_max']) + "," + str(ct_result['high_min'])
                # 有串扰则游标标出位置
                com = Component("interface_Set_CursorsPos")
                com.instrName = instrName
                com.CursorsType = CursorsType1
                com.XPos1 = 65535
                com.XPos2 = 65535
                com.YPos1 = ct_result['high_max']
                com.YPos2 = ct_result['high_min']
                com.VerScale = VerScale
                com.VerOffset = VerOffset
                ct_CursorsPos = http_service.post_message(com)
            # 保存图潘，copy到本地
            time.sleep(1)
            com = Component("interface_save_file")
            com.instrName = instrName
            com.OsSaveRoute = OsSaveRoute
            com.LocalPath = LocalPath
            com.OsPath = OsPath
            PngPath4 = http_service.post_message(com)
            time.sleep(1)
            MeasureResult['PngPaths'].append(PngPath4)

        # 判断是否有回沟
        com = Component("interface_check_back")
        com.CsvPath = CsvPath
        com.BaseValue = BaseValue
        com.TopValue = TopValue
        cb_result = http_service.post_message(com)
        if len(cb_result) != 0:
            # 有回勾则标出游标位置
            com = Component("interface_Set_CursorsPos")
            com.instrName = instrName
            com.CursorsType = CursorsType2
            com.XPos1 = cb_result['x1']
            com.XPos2 = cb_result['x2']
            com.YPos1 = cb_result['y1']
            com.YPos2 = cb_result['y2']
            com.VerScale = VerScale
            com.VerOffset = VerOffset
            cb_CursorsPos = http_service.post_message(com)
            log.log("放大回勾位置")
            CenterPoint = cb_result['x1']
            com = Component("interface_Zoom_set")
            com.instrName = instrName
            com.ch = ch
            com.CenterPoint = CenterPoint
            com.ZoomScale = 10E-9
            PngPath5 = http_service.post_message(com)

            time.sleep(1)
            com = Component("interface_save_file")
            com.instrName = instrName
            com.OsSaveRoute = OsSaveRoute
            com.LocalPath = LocalPath
            com.OsPath = OsPath
            PngPath5 = http_service.post_message(com)
            time.sleep(1)
            MeasureResult['PngPaths'].append(PngPath5)
            MeasureResult["back"] = str(cb_result)

        log.log("判断是否有台阶")
        com = Component("interface_check_step")
        com.CsvPath = CsvPath
        com.BaseValue = BaseValue
        com.TopValue = TopValue
        com.threshold = threshold
        cs_result = http_service.post_message(com)
        if len(cs_result) != 0:
            # 有台阶，输出台阶电压
            MeasureResult["step"] = str(cs_result)


            # 2.5G
            # SavePicture = interface_SavePicture(instrName, PictureName, SaveRoute)

        # MeasureResult["PngPath"] = PngPath
        # MeasureResult["PngPath2"] = PngPath2
        log.log(str(MeasureResult))

        log.success(MeasureResult)

    except Exception as err:
        log.exception(str(err))










