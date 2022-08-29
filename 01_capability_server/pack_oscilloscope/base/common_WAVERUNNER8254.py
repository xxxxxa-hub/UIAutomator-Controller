import datetime
import time
from pack_oscilloscope.base.os_instructions import *
from pack_oscilloscope.base.spi_signal_quality import *
import pyvisa as visa
import re


class WAVERUNNER8254(object):
    def __init__(self, instrname):
        # self.device_name = device_name
        self.rm = visa.ResourceManager()

        # 如果不为空则查询
        # if len(device.strip()) > 0:
        self.inst = self.rm.open_resource(instrname)
        return

    def call_instruction(self, cmd, *args):
        # 通过正则匹配出大括号及其大括号中内容
        instruction = WAVERUNNER8254_instructions.get(cmd)
        regex = re.compile(r'\{.*?\}')
        # 用大括号进行替换
        instruction2 = regex.sub('{}', instruction)
        instruction3 = instruction2.format(*args)
        self.inst.write(instruction3)

    def query_instruction(self, cmd, *args):
        """
        从指令集中获取对应的指令，执行查询功能
        :param cmd:查询指令名称
        :return:
        :query_value:返回搜索值
        """
        # 通过正则匹配出大括号及其大括号中内容
        instruction = WAVERUNNER8254_instructions.get(cmd)
        regex = re.compile(r'\{.*?\}')
        # 用大括号进行替换
        instruction2 = regex.sub('{}', instruction)
        instruction3 = instruction2.format(*args)
        query_value = self.inst.query(instruction3)
        return query_value


    def queryDevice(self):
        """
            :return:查询到的示波器信息
        """
        devices_list = list(self.rm.list_resources())
        for single_resource in devices_list:
            try:
                inst = self.rm.open_resource(single_resource)
                query_name_str = inst.query("*IDN?")
                print(query_name_str)
                if self.device_name in query_name_str:
                    # 返回查到的设备名称
                    return single_resource
            except visa.errors.VisaIOError:
                continue
        return ""

    # 设置恢复默认
    def DefaultSetup(self):
        self.call_instruction("DefaultSetup")

    # 设置界面显示波形
    def DisplayGridMode(self):
        self.call_instruction("Single")

    # 设置示波器触发类型为Auto
    def AutoType(self,AutoType):
        self.call_instruction("AutoType",AutoType)


    def set_visa_timeout(self, num=5):
        """
        :param device:设备名称
        :param self:
        :param num 超时时长,单位为s
        """
        num *= 1000
        self.inst.timeout = num


    # 开启指定通道
    def open_ch(self, ch):
        self.call_instruction(f"vbs 'app.acquisition.C{ch}.View = True'")

    # 关闭指定通道
    def close_ch(self, ch):
        self.call_instruction("ChannelStatus",ch,False)

    # 设置界面显示波形
    def DisplayGridMode(self,DisplayGridMode):
        self.call_instruction("DisplayGridMode",DisplayGridMode)

    def ChannelInputB(self,ch,ChannelInputB):
        self.call_instruction("ChannelInputB",ch,ChannelInputB)


    # UI传入通道参数命名通道
    def name_ch(self, channel, name):
        self.call_instruction("SetChannelName",channel,name)

    # 传入通道名称可见
    def ViewLabels(self,channel):
        self.call_instruction("ViewLabels",channel,True)

    # 勾选VarGain
    def SetVarGain(self,ch):
        self.call_instruction("SetVarGain",ch,True)

    # 设置垂直刻度
    def VerScale(self,ch,VerScale):
        self.call_instruction("VerScale",ch,VerScale)

    # 设置偏置
    def VerOffset(self,ch,VerOffset):
        self.call_instruction("VerOffset",ch,VerOffset)

    # 设置时基偏置
    def SetHorOffset(self,HorOffset):
        self.call_instruction("SetHorOffset",HorOffset)

    # 采样率设置：激活的通道
    def ActivationChannel(self,ActivationChannel):
        self.call_instruction("ActivationChannel",ActivationChannel)

    # 设置采样率为20Gs/s
    def SampleRate(self,SampleRate):
        self.call_instruction("SampleRate",SampleRate)

    # 设置每格时间
    def TimeSet(self,time1):
        self.call_instruction("TimeSet",time1)

    # 设置采样模式
    def SetSampleRate(self,SampleRate):
        """
         :param SampleRate: 可选择FixedSampleRate（固定采样器10GB/s）/Set Maximum Memory（设置最大内存） 模式
         """
        self.call_instruction("SetSampleRate",SampleRate)

    # 打开统计
    def statistics(self):
        self.call_instruction("statistics",True)

    # 添加测量项
    def AddMeasure(self,ch,Measure):
        self.call_instruction("AddMeasure",ch,Measure)


    # 添加CS测量值
    def AddMeasures_testCase(self,testCase):
        for i, v in enumerate(testCase):
            self.call_instruction("TestChannelNo", i + 1, True)
            self.call_instruction("AddMeasure", i + 1, v)


    # 添加CS测量值
    def AddOneMeasure_testCase(self, channel_no, measure):
        self.call_instruction("ShowMeasure",True)
        self.call_instruction("TestChannelNo", channel_no + 1, True)
        self.call_instruction("AddMeasure", channel_no + 1, measure)


    def set_trigger(self, trigger_type, trigger_ch, trigger_level):
        """
        :param trigger_type: 上升沿触发或下降沿触发，Negative/Positive二者选一
        :param trigger_ch: 触发源（通道几触发）
        :param trigger_level: 触发电平
        :return:
        """
        self.call_instruction("TriggerSource", trigger_ch)
        self.call_instruction("SetType", "EDGE")
        self.call_instruction("SetCoupling", "DC")
        self.call_instruction("SetSlope", trigger_type)
        self.call_instruction("SetLevel", trigger_level)
        time.sleep(0.1)
        self.call_instruction("SetTriggermode","Single")

    def set_trigger_XTirggerType(self, trigger_type, trigger_ch, trigger_level):
        """
        :param trigger_type: 上升沿触发或下降沿触发，Negative/Positive二者选一
        :param trigger_ch: 触发源（通道几触发）
        :param trigger_level: 触发电平
        :return:
        """
        self.call_instruction("TriggerSource", trigger_ch)
        self.call_instruction("SetType", "EDGE")
        self.call_instruction("SetCoupling", "DC")
        self.call_instruction("SetSlope", trigger_type)
        self.call_instruction("SetLevel", trigger_level)

    def set_trigger_Measurement(self ,trigger_ch,measure, trigger_level):
        """
               :param trigger_type: 上升沿触发或下降沿触发，Negative/Positive二者选一
               :param trigger_ch: 触发源（通道几触发）
               :param trigger_level: 触发电平
               :return:
               """
        self.call_instruction("SetType", "Measurement")
        self.call_instruction("MeasurementSource",trigger_ch)
        self.call_instruction("TriggerMeasuremant",measure)
        self.call_instruction("MeasurementLevel", trigger_level)
        time.sleep(0.1)
        self.call_instruction("SetTriggermode","Single")



    # 设置带宽为指定数值
    def set_bandwidth(self, ch, bandwidth):
        """
        :param ch: 要设置的通道如CH1
        :param bandwidth: 要设置的带宽 20.0000E+6表示20M带宽
        """
        self.call_instruction("SetBandwidth",ch,bandwidth)

    # 设置触发条件
    def trigger_set(self, Coupling, ch, trigger_type, level):
        self.call_instruction("SetCoupling", Coupling)
        self.call_instruction("TriggerSource", ch)
        self.call_instruction("SetSlope", trigger_type)
        self.call_instruction("SetLevel", level)


    # 示波器显示上升/下降沿上下电测量时间,返回测量值
    def change_time_new(self, ch, change_type):
        """
        :param ch: ch1 - ch4 要测量上电/下电时间的通道
        :param change_type: RISe for 上电, FALL for 下电 上下电类型
        """
        self.call_instruction("TestChannelNo", ch)
        # 选择上升沿为条件2
        self.call_instruction("AddMeasure", change_type)
        # 获取上升沿时间
        origin_data = float(self.inst.query(f"VBS? 'return = app.Measure.P{ch}.ParamEngine'").split()[-1])
        result = round(origin_data, 2)
        result_format = str(round(float(result), 2)) + 'ms'
        return result, result_format, origin_data


    # 保存当前示波器显示的波形,默认保存到当前工作空间D:\LeCoryOs\,保存为图片模式
    def save_screen(self, PictureName, SaveRoutePicture):
        self.call_instruction("SetPictureCounter", False)
        self.call_instruction("SaveMode", "ShowSaveScreenImage")
        self.call_instruction("SetDestination","File")
        self.call_instruction("PictureFormat","PNG")
        self.call_instruction("PictureName", PictureName)
        self.call_instruction("PictureSaveRoute", SaveRoutePicture)
        self.call_instruction("ScreenArea","GridAreaOnly")
        self.call_instruction("SavePicture")


    # 保存当前示波器显示的波形,默认保存到当前工作空间D:\LeCoryOs\,保存为图片模式
    def save_screen_1G(self, PictureName, SaveRoute,ScreenArea):
        self.call_instruction("PictureName", PictureName)
        self.call_instruction("PictureSaveRoute", SaveRoute)
        self.call_instruction("ScreenArea",ScreenArea)
        self.call_instruction("SavePicture")


    # 保存当前示波器波形，默认保存到当前工作空间D:\LeCoryOs\,保存为波形模式
    def save_Waveform(self,WaveformName,SaveRoute):
        self.call_instruction("closeCh", False)
        self.call_instruction("SetWaveformCounter",False)
        self.call_instruction("SaveMode","ShowSaveWaveform")
        self.call_instruction("WaveformSaveFormat","Excel")
        self.call_instruction("WaveformName",WaveformName)
        self.call_instruction("WaveformSaveRoute",SaveRoute)
        self.call_instruction("SaveWaveform")


    # 保存当前示波器波形，默认保存到当前工作空间D:\LeCoryOs\,保存为波形模式
    def save_Waveform_1G(self,WaveformName,SaveRoute):
        self.call_instruction("SaveMode","ShowSaveWaveform")
        self.call_instruction("WaveformSaveFormat","Excel")
        self.call_instruction("WaveformName",WaveformName)
        self.call_instruction("WaveformSaveRoute",SaveRoute)
        self.call_instruction("1.0SaveWaveform")




    # 在示波器上显示要测量的通道信息及测量值
    def change_time_set(self, change_type, ch, source_num=0):
        """
        :param source_num:
        :param change_type: 要添加测量值的类型,RISE上升时间,FALL下降时间,PWIDTH正脉冲宽度,NWIDTH负脉冲宽度
        :param ch: 要捕捉数据的通道名称,CH1等
        """
        source_num = int(ch[-1]) if source_num == 0 else source_num
        self.call_instruction("ShowMeasure",True)
        self.call_instruction("AddMeasure",source_num,change_type)
        self.call_instruction("TestChannelNo",source_num,ch)
        self.call_instruction("MeasureStatus",source_num,True)

    # 输出测量项结果
    def MeasureResult(self,ph,Measure):
        """
                :param ph:测量项通道，P1-P8
                :param Measure: 要输出的值，如最大值、最小值等
                """
        return self.query_instruction("MeasureResult",ph,Measure)


    # 选择指定通道并关闭其他通道
    def select_channel(self, ch):
        """
        :param ch: [1, 2]选择指定通道并关闭其他通道
        """
        all_ch = ["CH1", "CH2", "CH3", "CH4"]
        for i in ch:
            self.call_instruction("ChannelStatus",i,True)
            all_ch.remove(i)
        for j in all_ch:
            self.call_instruction("ChannelStatus",j,False)


    # 设置通道的垂直位置
    def set_position(self, ch, position):
        self.call_instruction("VerOffset",ch,position)

    # 关闭所有测量项
    def close_measure(self, num=8):
        for i in range(1, num):
            self.call_instruction("MeasureStatus",i,False)


    # 删除所有测量值
    def Delete_Measure(self):
        self.call_instruction("DeleteMeasure")
    # 关闭游标
    def Cursors(self):
        self.call_instruction("OpenCursors", False)

    # 设置BothRel游标位置
    def Set_CursorsPos(self, CursorsType, XPos1, XPos2, YPos1, YPos2):
        self.call_instruction("OpenCursors", True)
        self.call_instruction("CursorsType", CursorsType)
        if XPos1 is not None:
            self.call_instruction("CursorsXPos1", XPos1)
        if XPos2 is not None:
            self.call_instruction("CursorsXPos2", XPos2)
        if YPos1 is not None:
            self.call_instruction("CursorsYPos1", YPos1)
        if YPos2 is not None:
            self.call_instruction("CursorsYPos2", YPos2)

    # 查询触发模式/状态
    def TriggerMode(self):
        return self.query_instruction("TriggerMode")

    # 查询余晖次数
    def PersistedNum(self,n,MeasureType):
        return self.query_instruction("PersistedNum",n,MeasureType)


    def ZoomSplitScreen(self):
        self.call_instruction("DisplayGridMode","Dual")
        self.call_instruction("ZoomSplitScreen",1, "YT2")

    # 打开Zoom
    def OpenZoom(self,ch):
        self.call_instruction("OpenZoom",ch,True)
    # 关闭Zoom
    def CloseZoom(self,ch):
        self.call_instruction("OpenZoom",ch,False)

    # 设置Zoom放大至游标位置
    def ZoomSet(self,ch,CenterPoint,ZoomScale):
        self.call_instruction("ZoomSet",ch,CenterPoint)
        self.call_instruction("ZoomScale",ch,ZoomScale)

    # 打开/关闭余晖
    def OpenPersistence(self,TrueOrFlase):
        self.call_instruction("OPenPersisted",TrueOrFlase)

    # 余晖全部锁定
    def AllLockPersistence(self):
        self.call_instruction("AllLock","AllLocked")

    # 余晖模拟
    def PersistenceStyle(self):
        self.call_instruction("PersistenceStyle","Analog")
    # 余晖时间
    def PersistedTime(self,PersistedTime):
        self.call_instruction("PersistedTime",PersistedTime)

    # 触发抑制
    def TriggerHoldoffTime(self,HoldoffTime):
        self.call_instruction("HoldoffTime",HoldoffTime)

    # 触发抑制类型：时间/事件触发
    def TriggerHoldoffType(self,HoldoffType):
        self.call_instruction("HoldoffType",HoldoffType)

    # 查询余晖次数，一般看rise/fall的num次数，主要决定于是上升/下降沿触发
    # def PersistedNum(self,n):   #n为P{n}，rise/fall为第几个测试项
    #     self.call_instruction("PersistedNum",n)

    # 单纯Normal触发
    def NormalType(self):
        self.call_instruction("NormalType","Normal")

    # 停止触发
    def StopType(self):
        self.call_instruction("StopType","Stopped")

    # 抖动开关
    def OpenJitter(self):
        self.call_instruction("OpenJitter",True)

    # 抖动设置
    def SetJitter(self):
        self.call_instruction("SetJitter1",True)
        self.call_instruction("SetJitter2",True)
        self.call_instruction("SetJitter3",True)
        self.call_instruction("SetJitter4",True)

    # 设置触发水平位置
    def TriggerHor(self,TriggerHor):
        self.call_instruction("TriggerHor",TriggerHor)


# 测试SPI信号
if __name__ == '__main__':
    instrName = "TCPIP::" + "169.254.8.199" + "::INSTR"
    WAVERUNNER = WAVERUNNER8254(instrName)
    lis = {"n", "DisplayGridMode", "TrueOrFalse", "SetChannelName", "VerScale", "VerOffset", "Time1", "SetSampleRate",
           "TestChannelNo", "Measure", "Type", "Source", "Coupling", "SetSlope", "SetLevel", "SetTriggermode",
           "SaveMode", "PictureName", "PictureSaveRoute", "WaveformSaveFormat", "WaveformSaveFormat",
           "WaveformSaveRoute"}
    value = WAVERUNNER.query_instruction("AcquisitionVerScale", 1)
    # 恢复默认
    WAVERUNNER.call_instruction("DefaultSetup")
    # 设置界面显示波形
    WAVERUNNER.call_instruction("DisplayGridMode","Single")
    # 关闭2通道
    WAVERUNNER.call_instruction("ChannelStatus", 2, False)
    # 设置为Auto
    WAVERUNNER.call_instruction("AutoType","Auto")
    # 设置通道名称
    WAVERUNNER.call_instruction("SetChannelName", 1, "CLK")
    # 设置名称是否可见
    WAVERUNNER.call_instruction("ViewLabels",1, True)
    # 勾选VarGain（才可设置400mV）
    WAVERUNNER.call_instruction("SetVarGain",1 , True)
    # 设置垂直刻度
    WAVERUNNER.call_instruction("VerScale", 1, 0.4)
    # 设置偏置
    WAVERUNNER.call_instruction("VerOffset", 1, -1)
    # 设置时基偏置
    WAVERUNNER.call_instruction("SetHorOffset", -1e-6)
    # 设置每格时间
    WAVERUNNER.call_instruction("TimeSet", 5E-7)
    # 设置采样率模式
    WAVERUNNER.call_instruction("SetSampleRate", "FixedSampleRate")
    # 打开统计
    WAVERUNNER.call_instruction("statistics", True)
    # 打开通道，添加测量
    testCaseClk = {"Ampl", "Top", "Base", "Period", "Freq", "Duty", "Width", "Widn"}
    testCaseCS = {"Ampl", "Top", "Base", "Max", "Min", "OverShootNegative", "OverShootPositive"}
    testCaseMISO = {"Ampl", "Top", "Base", "Max", "Min", "Duty","OverShootNegative", "OverShootPositive"}
    testCaseMOSI = {"Ampl", "Top", "Base", "Max", "Min", "OverShootNegative", "OverShootPositive"}
    for i,v in enumerate(testCaseClk):
        WAVERUNNER.call_instruction("TestChannelNo", i+1, True)
        WAVERUNNER.call_instruction("AddMeasure", i+1, v)
    # 设置触发类型
    WAVERUNNER.call_instruction("TriggerMeasuremant","Measurement")

    # WAVERUNNER.call_instruction("SetType", "Edge")
    # 设置触发源
    WAVERUNNER.call_instruction("TriggerSource", "C1")
    # 设置耦合方式
    # WAVERUNNER.call_instruction("SetCoupling", "DC")
    # 设置触发方式
    # WAVERUNNER.call_instruction("SetSlope", "Negative")
    # 设置触发电平
    WAVERUNNER.call_instruction("SetLevel", 1)
    # 设置触发模式
    WAVERUNNER.call_instruction("SetTriggermode", "Single")
    # 设置保存图片
    WAVERUNNER.call_instruction("SaveMode","ShowSaveScreenImage")
    # 图片保存路径
    WAVERUNNER.call_instruction("PictureSaveRoute", "D:\\LeCoryOs\\")
    # 保存图片名称
    pic_path = "D:\\LeCoryOs\\"
    PicName = pic_path + "\\" + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + '.png'
    WAVERUNNER.call_instruction("PictureName",PicName)
    # 延时5s
    time.sleep(5)
    # 确认保存图片
    WAVERUNNER.call_instruction("SavePicture")
    # 设置保存波形
    WAVERUNNER.call_instruction("SaveMode","ShowSaveWaveform")
    # 设置波形保存格式
    WAVERUNNER.call_instruction("WaveformSaveFormat","Excel")
    # 波形保存路径
    WAVERUNNER.call_instruction("WaveformSaveRoute", "D:\\LeCoryOs\\")
    # 波形名称
    pic_path = "D:\\LeCoryOs\\"
    filename = pic_path + "\\" + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + '.csv'
    WAVERUNNER.call_instruction("WaveformName",filename)
    # 延时5s
    time.sleep(5)
    # 确认保存波形
    WAVERUNNER.call_instruction("SaveWaveform")
    # 返回测量值
    value = WAVERUNNER.query_instruction("AcquisitionVerScale", 1)




''' 
a = 'result'
    if a == True:
        WAVERUNNER.call_instruction("SetHorOffset", 1, 0)
        WAVERUNNER.call_instruction("TimeSet", 5E-5)
        WAVERUNNER.call_instruction("SetTriggermode", "Single")  
    else:
        WAVERUNNER.call_instruction("SetTriggermode", "Single")
        WAVERUNNER.call_instruction("SavePicture")
        WAVERUNNER.call_instruction("WaveformName","CLK")
        WAVERUNNER.call_instructi("SetSlope", "Positive")
        WAVERUNNER.call_instruction("SetTriggermode", "Single") 
        '''
