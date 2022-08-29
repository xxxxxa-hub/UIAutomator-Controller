import os
import time
import datetime
from http_service import HttpService, MessageToCSharpType, MessageBox
import ast
import sys

# pack:功能块，如示波器，此参数不能省
# module:功能块类型，如示波器MDO3054，此参数不能省
# interface:功能块已经实现的接口，此参数不能省
# 其余参数按照实际需求进行传递

# 定义三个class (OLEDtiming本身 | SIPtiming接口应用 | jpg保存接口)
class Component(object):
    def __init__(self, interface):
        self.pack = "pack_oscilloscope"
        self.module = "module_TEKMDO3054_OLEDtiming"
        self.interface = interface


class Component_SIPTiming(object):
    def __init__(self, interface):
        self.pack = "pack_oscilloscope"
        self.module = "module_TEKMDO3054_SPItiming"
        self.interface = interface


class Componentpic(object):
    def __init__(self, interface):
        self.pack = "pack_demo"
        self.module = "module_demo"
        self.interface = interface

def gettime():
    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return t
log = MessageToCSharpType("")
http_service = HttpService()

# 调试脚本
if __name__ == '__main__':
    try:
        instrName = "TCPIP::" + "169.254.8.23" + "::INSTR"
        record_length = 5E6
        CH_ARR = 'CH1,CH2,CH3,CH4'

        # 电源上下电 信号
        CH_LABEL_A = 'VDDI,DVDD,VCI,AVDD'
        CH_LABEL_DD = 'ELVDD,'
        CH_LABEL_SS = 'ELVSS,'
        # 驱动IC上下电 信号
        CH_LABEL_C = 'VDDI,VDDR,VCI,LCDRST'
        CH_LABEL_D = 'VCI,VDDR,LCDRST,MIPI'
        # DCDC上下电 信号
        CH_LABEL_E = 'AS,ES,ELVDD,ELVSS'

        acquire_type = 'SEQUENCE'
        open_ch = ["CH1", "CH2", "CH3", "CH4"]
        close_ch1 = "CH1"
        close_ch2 = "CH2"
        close_ch3 = "CH3"
        close_ch4 = "CH4"

        t_clock = ""  # 待定变量
        STANDARD_MIN_VOL = 0.2
        STANDARD_MAX_VOL = 2
        standard_Typ = 2.5

        message_box = MessageBox()  # 弹出框判断选择

        # pic_path = parameterList['screenshotPath'] + "\\"
        pic_path = r'E:\test1' + "\\"
        #  约定为这个变量名称，存储返回结果的字典
        test_result = {'PngPaths': []}

        OLEDTest = "电源上电"
# --------------------------------------电源上电---------------------------------------------------
        if OLEDTest == "电源上电":
            log.log(gettime() + " >>>【执行波形1：PowerOn_1@VDDI_2@DVDD_3@VCI_4@AVDD测试任务】")
            com = Component("interface_set_Factory")
            com.instrName = instrName
            devices1 = http_service.post_message(com)

            log.log(gettime() + " >>>【电源上电[VDDI-DVDD-VCI-AVDD]测试示波器设置】")
            com = Component("interface_set_PowerSource")
            com.instrName = instrName
            com.OLEDTest = OLEDTest
            com.CH_ARR = CH_ARR
            com.ch_label = CH_LABEL_A
            com.trigger_type = "RISE"
            com.trigger_ch = "CH1"
            device1 = http_service.post_message(com)

            log.log(gettime() + " >>>【连接手机启动亮灭屏动作】")
            t_a = time.time()
            while True:
                com = Component("interface_set_PowerOnOff")
                com.item = "procedure"
                com.scene = "亮灭屏"
                relust = http_service.post_message(com)
                time.sleep(1)
                com = Component_SIPTiming("interface_query_acquire_mode")
                com.instrName = instrName
                acquire_mode = http_service.post_message(com)
                t_b = time.time()
                if acquire_mode == '0\n':
                    log.log(gettime() + " >>>【波形已经触发】")
                    break
                if t_b - t_a >= 20:
                    log.fail(gettime() + " >>>【在20s之内未能捕捉到正确的波形，请重新测试】")
                    sys.exit()

            log.log(gettime() + " >>>【示波器通道垂直位置进行调整同一位置】")
            position_list = [-1, -1, -1, -1]            # 各通道的水平位置
            com = Component("interface_ch_OLEDset")
            com.instrName = instrName
            com.ch_list = CH_ARR
            com.position_list = position_list
            com.label_list = None
            com.scale_list = None
            device2 = http_service.post_message(com)    # 进一步对示波器通道垂直位置进行调整

            log.log(gettime() + " >>>【VDDI信号检测中】")
            com = Component("VDDI")
            com.instrName = instrName
            com.OLEDTest = OLEDTest
            PowerOn1 = http_service.post_message(com)
            test_result["PowerOn_VDDI"] = float(PowerOn1['delta'])

            log.log(gettime() + " >>>【保存VDDI信号】")
            file_name = pic_path + "PowerOn_VDDI" + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + '.png'
            com = Component_SIPTiming("interface_save_screen")
            com.instrName = instrName
            com.file_name = file_name
            result1 = http_service.post_message(com)
            test_result['PngPaths'].append(result1['filename'])
            log.log(str(test_result))

            log.log(gettime() + " >>>【DVDD信号检测中】")
            com = Component("DVDD")
            com.instrName = instrName
            com.OLEDTest = OLEDTest
            PowerOn2 = http_service.post_message(com)
            test_result["PowerOn_DVDD"] = float(PowerOn2['delta'])

            log.log(gettime() + " >>>【保存DVDD信号】")
            file_name = pic_path + "PowerOn_DVDD" + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + '.png'
            com = Component_SIPTiming("interface_save_screen")
            com.instrName = instrName
            com.file_name = file_name
            result2 = http_service.post_message(com)
            test_result['PngPaths'].append(result2['filename'])
            log.log(str(test_result))

            log.log(gettime() + " >>>【VCI信号检测中】")
            com = Component("VCI")
            com.instrName = instrName
            com.OLEDTest = OLEDTest
            PowerOn3 = http_service.post_message(com)
            test_result["PowerOn_VCI"] = float(PowerOn3['delta'])

            log.log(gettime() + " >>>【保存VCI信号】")
            file_name = pic_path + "PowerOn_VCI" + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + '.png'
            com = Component_SIPTiming("interface_save_screen")
            com.instrName = instrName
            com.file_name = file_name
            result3 = http_service.post_message(com)
            test_result['PngPaths'].append(result3['filename'])
            log.log(str(test_result))

            log.log(gettime() + " >>>【AVDD信号检测中】")
            com = Component("AVDD")
            com.instrName = instrName
            com.OLEDTest = OLEDTest
            PowerOn4 = http_service.post_message(com)
            test_result["PowerOn_AVDD"] = float(PowerOn4['delta'])

            log.log(gettime() + " >>>【保存AVDD信号】")
            file_name = pic_path + "PowerOn_AVDD" + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + '.png'
            com = Component_SIPTiming("interface_save_screen")
            com.instrName = instrName
            com.file_name = file_name
            result4 = http_service.post_message(com)
            test_result['PngPaths'].append(result4['filename'])
            log.log(str(test_result))

            flag = message_box.askyesno('任务确认', '是否继续执行[ELVDD]测试，请确认CH1探针接触点位？')
            if flag:
                log.log(gettime() + " >>>【电源上电[ELVDD]测试示波器设置】")
                com = Component("interface_set_PowerSource")
                com.instrName = instrName
                com.CH_ARR = CH_ARR
                com.OLEDTest = OLEDTest
                com.ch_label = CH_LABEL_DD
                com.trigger_type = "RISE"
                com.trigger_ch = "CH1"
                device3 = http_service.post_message(com)

                log.log(gettime() + " >>>【连接手机启动亮灭屏动作】")
                t_a = time.time()
                while True:
                    com = Component("interface_set_PowerOnOff")
                    com.item = "procedure"
                    com.scene = "亮灭屏"
                    relust = http_service.post_message(com)
                    time.sleep(1)
                    com = Component_SIPTiming("interface_query_acquire_mode")
                    com.instrName = instrName
                    acquire_mode = http_service.post_message(com)
                    t_b = time.time()
                    if acquire_mode == '0\n':
                        log.log(gettime() + " >>>【波形已经触发】")
                        break
                    if t_b - t_a >= 20:
                        log.fail(gettime() + " >>>【在20s之内未能捕捉到正确的波形，请重新测试】")
                        sys.exit()

                log.log(gettime() + ">>>【ELVDD信号检测中】")
                com = Component("ELVDD")
                com.instrName = instrName
                com.OLEDTest = OLEDTest
                PowerOn5 = http_service.post_message(com)
                test_result["PowerOn_ELVDD"] = float(PowerOn5['delta'])

                log.log(gettime() + " >>>【保存ELVDD信号】")
                file_name = pic_path + "PowerOn_ELVDD" + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + '.png'
                com = Component_SIPTiming("interface_save_screen")
                com.instrName = instrName
                com.file_name = file_name
                result5 = http_service.post_message(com)
                test_result['PngPaths'].append(result5['filename'])
                log.log(str(test_result))

            flag = message_box.askyesno('测试确认', '是否继续执行[ELVSS]测试，请确认CH1探针接触点位？')
            if flag:
                log.log(gettime() + " >>>【电源上电[ELVSS]测试示波器设置】")
                com = Component("interface_set_PowerSource")
                com.instrName = instrName
                com.CH_ARR = CH_ARR
                com.OLEDTest = OLEDTest
                com.ch_label = CH_LABEL_SS
                com.trigger_type = "FALL"
                com.trigger_ch = "CH1"
                device4 = http_service.post_message(com)

                log.log(gettime() + " >>>【连接手机启动亮灭屏动作】")
                t_a = time.time()
                while True:
                    com = Component("interface_set_PowerOnOff")
                    com.item = "procedure"
                    com.scene = "亮灭屏"
                    relust = http_service.post_message(com)
                    time.sleep(1)
                    com = Component_SIPTiming("interface_query_acquire_mode")
                    com.instrName = instrName
                    acquire_mode = http_service.post_message(com)
                    t_b = time.time()
                    if acquire_mode == '0\n':
                        log.log(gettime() + " >>>【波形已经触发】")
                        break
                    if t_b - t_a >= 20:
                        log.fail(gettime() + " >>>【在20s之内未能捕捉到正确的波形，请重新测试】")
                        sys.exit()

                log.log(gettime() + " >>>【ELVSS信号检测中】")
                com = Component("ELVSS")
                com.instrName = instrName
                com.OLEDTest = OLEDTest
                PowerOn6 = http_service.post_message(com)
                test_result["PowerOn_ELVSS"] = float(PowerOn6['delta'])

                log.log(gettime() + " >>>【保存ELVSS信号】")
                file_name = pic_path + "PowerOn_ELVSS" + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + '.png'
                com = Component_SIPTiming("interface_save_screen")
                com.instrName = instrName
                com.file_name = file_name
                result6 = http_service.post_message(com)
                test_result['PngPaths'].append(result6['filename'])
                log.log(str(test_result))

        elif OLEDTest == "电源下电":
            log.log(gettime() + " >>>【电源下电[VDDI-DVDD-VCI-AVDD]测试示波器设置】")
            com = Component("interface_set_PowerSource")
            com.instrName = instrName
            com.OLEDTest = OLEDTest
            com.CH_ARR = CH_ARR
            com.ch_label = CH_LABEL_A
            com.trigger_type = "FALL"
            com.trigger_ch = "CH1"
            device1 = http_service.post_message(com)

            log.log(gettime() + " >>>【连接手机启动亮灭屏动作】")
            t_a = time.time()
            while True:
                com = Component("interface_set_PowerOnOff")
                com.item = "procedure"
                com.scene = "亮灭屏"
                relust = http_service.post_message(com)
                time.sleep(1)
                com = Component_SIPTiming("interface_query_acquire_mode")
                com.instrName = instrName
                acquire_mode = http_service.post_message(com)
                t_b = time.time()
                if acquire_mode == '0\n':
                    log.log(gettime() + " >>>【波形已经触发】")
                    break
                if t_b - t_a >= 20:
                    log.fail(gettime() + " >>>【在20s之内未能捕捉到正确的波形，请重新测试】")
                    sys.exit()

            log.log(gettime() + " >>>【示波器通道垂直位置进行调整同一位置】")
            position_list = [1, 1, 1, 1]  # 各通道的水平位置
            com = Component("interface_ch_OLEDset")
            com.instrName = instrName
            com.ch_list = CH_ARR
            com.position_list = position_list
            com.label_list = None
            com.scale_list = None  # 进一步对示波器通道垂直位置进行调整
            device2 = http_service.post_message(com)

            log.log(gettime() + " >>>【VDDI信号检测中】")
            com = Component("VDDI")
            com.instrName = instrName
            com.OLEDTest = OLEDTest
            PowerOff1 = http_service.post_message(com)
            test_result["PowerOff_VDDI"] = float(PowerOff1['delta'])

            log.log(gettime() + " >>>【保存VDDI信号】")
            file_name = pic_path + "PowerOff_VDDI" + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + '.png'
            com = Component_SIPTiming("interface_save_screen")
            com.instrName = instrName
            com.file_name = file_name
            result11 = http_service.post_message(com)
            test_result['PngPaths'].append(result11['filename'])
            log.log(str(test_result))

            log.log(gettime() + " >>>【DVDD信号检测中】")
            com = Component("DVDD")
            com.instrName = instrName
            com.OLEDTest = OLEDTest
            PowerOff2 = http_service.post_message(com)
            test_result["PowerOff_DVDD"] = float(PowerOff2['delta'])

            log.log(gettime() + " >>>【保存DVDD信号】")
            file_name = pic_path + "PowerOff_DVDD" + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + '.png'
            com = Component_SIPTiming("interface_save_screen")
            com.instrName = instrName
            com.file_name = file_name
            result12 = http_service.post_message(com)
            test_result['PngPaths'].append(result12['filename'])
            log.log(str(test_result))

            log.log(gettime() + " >>>【VCI信号检测中】")
            com = Component("VCI")
            com.instrName = instrName
            com.OLEDTest = OLEDTest
            PowerOff3 = http_service.post_message(com)
            test_result["PowerOff_VCI"] = float(PowerOff3['delta'])

            log.log(gettime() + " >>>【保存VCI信号】")
            file_name = pic_path + "PowerOff_VCI" + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + '.png'
            com = Component_SIPTiming("interface_save_screen")
            com.instrName = instrName
            com.file_name = file_name
            result13 = http_service.post_message(com)
            test_result['PngPaths'].append(result13['filename'])
            log.log(str(test_result))

            log.log(gettime() + " >>>【AVDD信号检测中】")
            com = Component("AVDD")
            com.instrName = instrName
            com.OLEDTest = OLEDTest
            PowerOff4 = http_service.post_message(com)
            test_result["PowerOff_AVDD"] = float(PowerOff4['delta'])

            log.log(gettime() + " >>>【保存AVDD信号】")
            file_name = pic_path + "PowerOff_AVDD" + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + '.png'
            com = Component_SIPTiming("interface_save_screen")
            com.instrName = instrName
            com.file_name = file_name
            result14 = http_service.post_message(com)
            test_result['PngPaths'].append(result14['filename'])
            log.log(str(test_result))

            flag = message_box.askyesno('任务确认', '是否继续执行[ELVDD]测试，请确认CH1探针接触点位？')
            if flag:
                log.log(gettime() + " >>>【电源下电[ELVDD]测试示波器设置】")
                com = Component("interface_set_PowerSource")
                com.instrName = instrName
                com.OLEDTest = OLEDTest
                com.CH_ARR = CH_ARR
                com.ch_label = CH_LABEL_DD
                com.trigger_type = "FALL"
                com.trigger_ch = "CH1"
                device2 = http_service.post_message(com)

                log.log(gettime() + " >>>【连接手机启动亮灭屏动作】")
                t_a = time.time()
                while True:
                    com = Component("interface_set_PowerOnOff")
                    com.item = "procedure"
                    com.scene = "亮灭屏"
                    relust = http_service.post_message(com)
                    time.sleep(1)
                    com = Component_SIPTiming("interface_query_acquire_mode")
                    com.instrName = instrName
                    acquire_mode = http_service.post_message(com)
                    t_b = time.time()
                    if acquire_mode == '0\n':
                        log.log(gettime() + " >>>【波形已经触发】")
                        break
                    if t_b - t_a >= 20:
                        log.fail(gettime() + " >>>【在20s之内未能捕捉到正确的波形，请重新测试】")
                        sys.exit()

                log.log(gettime() + " >>>【ELVDD信号检测中】")
                com = Component("ELVDD")
                com.instrName = instrName
                com.OLEDTest = OLEDTest
                PowerOff5 = http_service.post_message(com)
                test_result["PowerOff_ELVDD"] = float(PowerOff5['delta'])

                log.log(gettime() + " >>>【保存ELVDD信号】")
                file_name = pic_path + "PowerOff_ELVDD" + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + '.png'
                com = Component_SIPTiming("interface_save_screen")
                com.instrName = instrName
                com.file_name = file_name
                result15 = http_service.post_message(com)
                test_result['PngPaths'].append(result15['filename'])
                log.log(str(test_result))

                flag = message_box.askyesno('任务确认', '是否继续执行[ELVSS]测试，请确认CH1探针接触点位？')
                if flag:
                    log.log(gettime() + " >>>【电源下电[ELVSS]测试示波器设置】")
                    com = Component("interface_set_PowerSource")
                    com.instrName = instrName
                    com.OLEDTest = OLEDTest
                    com.CH_ARR = CH_ARR
                    com.ch_label = CH_LABEL_SS
                    com.trigger_type = "RISE"
                    com.trigger_ch = "CH1"
                    device2 = http_service.post_message(com)

                    log.log(gettime() + " >>>【连接手机启动亮灭屏动作】")
                    t_a = time.time()
                    while True:
                        com = Component("interface_set_PowerOnOff")
                        com.item = "procedure"
                        com.scene = "亮灭屏"
                        relust = http_service.post_message(com)
                        time.sleep(1)
                        com = Component_SIPTiming("interface_query_acquire_mode")
                        com.instrName = instrName
                        acquire_mode = http_service.post_message(com)
                        t_b = time.time()
                        if acquire_mode == '0\n':
                            log.log(gettime() + " >>>【波形已经触发】")
                            break
                        if t_b - t_a >= 20:
                            log.fail(gettime() + " >>>【在20s之内未能捕捉到正确的波形，请重新测试】")
                            sys.exit()

                    log.log(gettime() + " >>>【ELVSS信号检测中】")
                    com = Component("ELVSS")
                    com.instrName = instrName
                    com.OLEDTest = OLEDTest
                    PowerOff6 = http_service.post_message(com)
                    test_result["PowerOff_ELVSS"] = float(PowerOff6['delta'])

                    log.log(gettime() + " >>>【保存ELVSS信号】")
                    file_name = pic_path + "PowerOff_ELVSS" + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + '.png'
                    com = Component_SIPTiming("interface_save_screen")
                    com.instrName = instrName
                    com.file_name = file_name
                    result16 = http_service.post_message(com)
                    test_result['PngPaths'].append(result16['filename'])
                    log.log(str(test_result))

        elif OLEDTest == "驱动IC上电":
            log.log(gettime() + " >>>【执行波形1：Shuton1@VDDI_2@VDDR_3@VCI_4@LCDRST测试任务：】")
            com = Component("interface_set_Factory")
            com.instrName = instrName
            devices1 = http_service.post_message(com)

            log.log(gettime() + " >>>【示波器参数设置：】")
            com = Component("interface_set_DriveIC_DCDC")
            com.instrName = instrName
            com.OLEDTest = OLEDTest
            com.CH_ARR = CH_ARR
            com.ch_label = CH_LABEL_C
            devices2 = http_service.post_message(com)

            flag = message_box.askyesno('波形确认', '确认各路通道波形是否正常触发！')
            if flag:

                log.log(gettime() + " >>>【保存波形1-boot_1@VDDI_2@VDDR_3@VCI_4@LCDRST信号】")
                file_name = pic_path + "boot_1@VDDI_2@VDDR_3@VCI_4@LCDRST" + '.png'
                com = Component_SIPTiming("interface_save_screen")
                com.instrName = instrName
                com.file_name = file_name
                result21 = http_service.post_message(com)
                test_result['PngPaths'].append(result21['filename'])
                log.log(str(test_result))

                log.log(gettime() + " >>>【保存CH1@VDDI波形CSV文件】")
                path = f"E:\\test1\\ICOn_VDDI.csv"
                com = Component("interface_data_caul")
                com.instrName = instrName
                com.ch = "CH1"
                com.save_path = path
                log.log(gettime() + http_service.post_message(com))

                log.log(gettime() + " >>>【获取CH1@VDDI上升沿的两个点位：（10%|90%）】")
                com = Component("interface_get_RiseEdge")
                com.save_path = path
                com.min_per = 0.2
                com.max_per = 0.8
                ICOn_VDDI = http_service.post_message(com)       #  PowerOn_VDDI[0]: VDDI10% | PowerOn_VDDI[1]: VDDI90%

                log.log(gettime() + " >>>【保存CH2@VDDR波形CSV文件】")
                path = f"E:\\test1\\ICOn_VDDR.csv"
                com = Component("interface_data_caul")
                com.instrName = instrName
                com.ch = "CH2"
                com.save_path = path
                log.log(gettime() + http_service.post_message(com))

                log.log(gettime() + " >>>【获取CH2@VDDR上升沿的两个点位：（10%|90%）】")
                com = Component("interface_get_RiseEdge")
                com.save_path = path
                com.min_per = 0.2
                com.max_per = 0.8
                ICOn_VDDR = http_service.post_message(com)       # ICOn_VDDR[0]: VDDI10% | ICOn_VDDR[1]: VDDI90%

                log.log(gettime() + " >>>【进行【ton1】光标卡时间测试中】")
                com = Component("ton1")
                com.instrName = instrName
                com.time_a = ICOn_VDDI[1]
                com.time_b = ICOn_VDDR[0]
                ICOn1 = http_service.post_message(com)
                test_result["ton1"] = float(ICOn1['delta'])

                log.log(gettime() + " >>>【保存boot--->ton1信号】")
                file_name = pic_path + "boot_1@VDDI_2@VDDR_3@VCI_4@LCDRST_ton1" + '.png'
                com = Component_SIPTiming("interface_save_screen")
                com.instrName = instrName
                com.file_name = file_name
                result22 = http_service.post_message(com)
                test_result['PngPaths'].append(result22['filename'])
                log.log(str(test_result))

                log.log(gettime() + " >>>【保存CH3@VCI波形CSV文件】")
                path = f"E:\\test1\\ICOn_VCI.csv"
                com = Component("interface_data_caul")
                com.instrName = instrName
                com.ch = "CH3"
                com.save_path = path
                log.log(gettime() + http_service.post_message(com))

                log.log(gettime() + " >>>【获取CH3@VCI上升沿的两个点位：（10%|90%）】")
                com = Component("interface_get_RiseEdge")
                com.save_path = path
                com.min_per = 0.2
                com.max_per = 0.8
                ICOn_VCI = http_service.post_message(com)       # ICOn_VCI[0]: VDDI10% | ICOn_VCI[1]: VDDI90%

                log.log(gettime() + " >>>【进行【ton2】光标卡时间测试中】")
                com = Component("ton2")
                com.instrName = instrName
                com.time_a = ICOn_VDDR[1]
                com.time_b = ICOn_VCI[0]
                ICOn2 = http_service.post_message(com)
                test_result["ton2"] = ICOn2["delta"]

                log.log(gettime() + " >>>【保存boot--->ton2信号】")
                file_name = pic_path + "boot_1@VDDI_2@VDDR_3@VCI_4@LCDRST_ton2" + '.png'
                com = Component_SIPTiming("interface_save_screen")
                com.instrName = instrName
                com.file_name = file_name
                result23 = http_service.post_message(com)
                test_result['PngPaths'].append(result23['filename'])
                log.log(str(test_result))

                log.log(gettime() + " >>>【获取CH4@LCDRST所有点位：（第二个下降沿|第一个上升沿|第一个下降沿）】")
                com = Component("interface_IConA_LCDRST")
                com.instrName = instrName
                com.ch = "CH4"
                ICOn_LCDRST = http_service.post_message(com)        # ICOn_LCDRST[0]:  | ICOn_VCI[1]: VDDI90%

                log.log(gettime() + " >>>【进行【t1】光标卡时间测试中】")
                com = Component("t1")
                com.instrName = instrName
                com.time_a = ICOn_VCI[1]
                com.time_b = ICOn_LCDRST["position_a"]
                ICOn3 = http_service.post_message(com)
                test_result["t1"] = ICOn3["delta"]

                log.log(gettime() + " >>>【保存boot--->t1信号】")
                file_name = pic_path + "boot_1@VDDI_2@VDDR_3@VCI_4@LCDRST_t1" + '.png'
                com = Component_SIPTiming("interface_save_screen")
                com.instrName = instrName
                com.file_name = file_name
                result24 = http_service.post_message(com)
                test_result['PngPaths'].append(result24['filename'])
                log.log(str(test_result))

                log.log(gettime() + " >>>【进行【t4】时间测试中】")
                com = Component("t4")
                com.instrName = instrName
                com.time_a = ICOn_LCDRST["position_b"]
                com.time_b = ICOn_LCDRST["position_c"]
                ICOn4 = http_service.post_message(com)
                test_result["t4"] = ICOn4["delta"]

                log.log(gettime() + " >>>【保存boot--->t4信号】")
                file_name = pic_path + "boot_1@VDDI_2@VDDR_3@VCI_4@LCDRST_t4" + '.png'
                com = Component_SIPTiming("interface_save_screen")
                com.instrName = instrName
                com.file_name = file_name
                result25 = http_service.post_message(com)
                test_result['PngPaths'].append(result25['filename'])
                log.log(str(test_result))

            flag = message_box.askyesno('任务确认', '是否继续执行波形2boot_1@VCI--->4@MIPI测试，请确认各通道探针接触点位？')
            if flag:
                log.log(gettime() + " >>>【执行波形2：boot_1@VCI_2@VDDR_3@LCDRST_4@MIPI测试任务：】")
                com = Component("interface_set_Factory")
                com.instrName = instrName
                devices1 = http_service.post_message(com)

                log.log(gettime() + " >>>【示波器参数设置：】")
                com = Component("interface_set_DriveIC_DCDC")
                com.instrName = instrName
                com.OLEDTest = OLEDTest
                com.CH_ARR = CH_ARR
                com.ch_label = CH_LABEL_D
                devices2 = http_service.post_message(com)

                flag = message_box.askyesno('波形确认', '确认各路通道波形是否正常触发！')
                if flag:
                    log.log(gettime() + " >>>【保存波形2-boot_1@VCI_2@VDDR_3@LCDRST_4@MIPI信号】")
                    file_name = pic_path + "boot_1@VCI_2@VDDR_3@LCDRST_4@MIPI" + '.png'
                    com = Component_SIPTiming("interface_save_screen")
                    com.instrName = instrName
                    com.file_name = file_name
                    result26 = http_service.post_message(com)
                    test_result['PngPaths'].append(result26['filename'])
                    log.log(str(test_result))

                    log.log(gettime() + " >>>【获取CH3@LCDRST所有点位：（最后一个上升沿|第一个上升沿）】")
                    com = Component("interface_IConB_LCDRST")
                    com.instrName = instrName
                    com.ch = "CH3"
                    ICOn_LCDRST = http_service.post_message(com)
                    # ICOn_LCDRST["position_a"]: LCDRST-Last-Rise | ICOn_LCDRST["position_b"]: LCDRST-First-Rise

                    log.log(gettime() + " >>>【获取CH4@MIPI所有点位：（第一个下降沿|第一个上升沿| t5第一个点|t5第二个点）】")
                    com = Component("interface_IConB_MIPI")
                    com.instrName = instrName
                    com.ch = "CH4"
                    ICOn_MIPI = http_service.post_message(com)
                    # ICOn_MIPI["position_a"]: MIPI-First-fall | ICOn_MIPI["position_b"]: MIPI-First-rise | ICOn_MIPI["position_c"]: t5-First-point | ICOn_MIPI["position_d"]: t5-second-point

                    log.log(gettime() + " >>>【进行【t2】光标卡时间测试中】")
                    com = Component("t2")
                    com.instrName = instrName
                    com.time_a = ICOn_LCDRST["position_a"]
                    com.time_b = ICOn_MIPI["position_a"]
                    ICOn5 = http_service.post_message(com)
                    test_result["t2"] = ICOn5["delta"]

                    log.log(gettime() + " >>>【保存boot--->t2信号】")
                    file_name = pic_path + "boot_1@VCI_2@VDDR_3@LCDRST_4@MIPI_t2" + '.png'
                    com = Component_SIPTiming("interface_save_screen")
                    com.instrName = instrName
                    com.file_name = file_name
                    result27 = http_service.post_message(com)
                    test_result['PngPaths'].append(result27['filename'])
                    log.log(str(test_result))

                    log.log(gettime() + " >>>【进行【t3】时间测试中】")
                    com = Component("t3")
                    com.instrName = instrName
                    com.time_a = ICOn_LCDRST["position_b"]
                    com.time_b = ICOn_MIPI["position_b"]
                    ICOn6 = http_service.post_message(com)
                    test_result["t3"] = ICOn6["delta"]

                    log.log(gettime() + " >>>【保存boot--->t3信号】")
                    file_name = pic_path + "boot_1@VCI_2@VDDR_3@LCDRST_4@MIPI_t3" + '.png'
                    com = Component_SIPTiming("interface_save_screen")
                    com.instrName = instrName
                    com.file_name = file_name
                    result28 = http_service.post_message(com)
                    test_result['PngPaths'].append(result28['filename'])
                    log.log(str(test_result))

                    log.log(gettime() + " >>>【进行【t5】时间测试中】")
                    com = Component("t5")
                    com.instrName = instrName
                    com.time_a = ICOn_MIPI["position_c"]
                    com.time_b = ICOn_MIPI["position_d"]
                    ICOn7 = http_service.post_message(com)
                    test_result["t5"] = ICOn7["delta"]

                    log.log(gettime() + " >>>【保存boot--->t5信号】")
                    file_name = pic_path + "boot_1@VCI_2@VDDR_3@LCDRST_4@MIPI_t5" + '.png'
                    com = Component_SIPTiming("interface_save_screen")
                    com.instrName = instrName
                    com.file_name = file_name
                    result29 = http_service.post_message(com)
                    test_result['PngPaths'].append(result29['filename'])
                    log.log(str(test_result))

        elif OLEDTest == "驱动IC下电":
            log.log(gettime() + " >>>【执行波形1：Shutdown1@VDDI_2@VDDR_3@VCI_4@LCDRST测试任务：】")
            com = Component("interface_set_Factory")
            com.instrName = instrName
            devices1 = http_service.post_message(com)

            log.log(gettime() + " >>>【示波器参数设置：】")
            com = Component("interface_set_DriveIC_DCDC")
            com.instrName = instrName
            com.OLEDTest = OLEDTest
            com.CH_ARR = CH_ARR
            com.ch_label = CH_LABEL_C
            devices2 = http_service.post_message(com)
            flag = message_box.askyesno('波形确认', '确认各路通道波形是否正常触发！')
            if flag:
                log.log(gettime() + " >>>【保存波形Shutdown1@VDDI_2@VDDR_3@VCI_4@LCDRST信号】")
                file_name = pic_path + "Shutdown1@VDDI_2@VDDR_3@VCI_4@LCDRST" + '.png'
                com = Component_SIPTiming("interface_save_screen")
                com.instrName = instrName
                com.file_name = file_name
                result31 = http_service.post_message(com)
                test_result['PngPaths'].append(result31['filename'])
                log.log(str(test_result))

                log.log(gettime() + " >>>【保存CH1@VDDI波形CSV文件】")
                path = f"E:\\test1\\ICOff_VDDI.csv"
                com = Component("interface_data_caul")
                com.instrName = instrName
                com.ch = "CH1"
                com.save_path = path
                log.log(gettime() + http_service.post_message(com))

                log.log(gettime() + " >>>【获取CH1@VDDI下降沿的两个点位：（90%|10%）】")
                com = Component("interface_get_FallEdge")
                com.save_path = path
                com.min_per = 0.2
                com.max_per = 0.8
                ICOff_VDDI = http_service.post_message(com)  # ICOff_VDDI[0]: VDDI90% | ICOff_VDDI[1]: VDDI10%

                log.log(gettime() + " >>>【保存CH2@VDDR波形CSV文件】")
                path = f"E:\\test1\\ICOff_VDDR.csv"
                com = Component("interface_data_caul")
                com.instrName = instrName
                com.ch = "CH2"
                com.save_path = path
                log.log(gettime() + http_service.post_message(com))

                log.log(gettime() + " >>>【获取CH2@VDDR下降沿的两个点位：（90%|10%）】")
                com = Component("interface_get_FallEdge")
                com.save_path = path
                com.min_per = 0.2
                com.max_per = 0.8
                ICOff_VDDR = http_service.post_message(com)  # ICOff_VDDR[0]: VDDR90% | ICOff_VDDR[1]: VDDR10%

                log.log(gettime() + " >>>【进行【tof1】光标卡时间测试中】")
                com = Component("tof1")
                com.instrName = instrName
                com.time_a = ICOff_VDDR[1]
                com.time_b = ICOff_VDDI[0]
                ICOff1 = http_service.post_message(com)
                test_result["tof1"] = ICOff1["delta"]

                log.log(gettime() + " >>>【保存Shutdown--->tof1信号】")
                file_name = pic_path + "Shutdown_1@VDDI_2@VDDR_3@VCI_4@LCDRST_tof1" + '.png'
                com = Component_SIPTiming("interface_save_screen")
                com.instrName = instrName
                com.file_name = file_name
                result32 = http_service.post_message(com)
                test_result['PngPaths'].append(result32['filename'])
                log.log(str(test_result))

                log.log(gettime() + " >>>【保存CH3@VCI波形CSV文件】")
                path = f"E:\\test1\\ICOff_VCI.csv"
                com = Component("interface_data_caul")
                com.instrName = instrName
                com.ch = "CH3"
                com.save_path = path
                log.log(gettime() + http_service.post_message(com))

                log.log(gettime() + " >>>【获取CH3@VCI下降沿的两个点位：（90%|10%）】")
                com = Component("interface_get_FallEdge")
                com.save_path = path
                com.min_per = 0.2
                com.max_per = 0.8
                ICOff_VCI = http_service.post_message(com)  # ICOff_VCI[0]: VCI90% | ICOff_VCI[1]: VCI10%

                log.log(gettime() + " >>>【进行【tof2】光标卡时间测试中】")
                com = Component("tof2")
                com.instrName = instrName
                com.time_a = ICOff_VCI[1]
                com.time_b = ICOff_VDDR[0]
                ICOff2 = http_service.post_message(com)
                test_result["tof2"] = ICOff2["delta"]

                log.log(gettime() + " >>>【保存Shutdown--->tof2信号】")
                file_name = pic_path + "Shutdown_1@VDDI_2@VDDR_3@VCI_4@LCDRST_tof2" + '.png'
                com = Component_SIPTiming("interface_save_screen")
                com.instrName = instrName
                com.file_name = file_name
                result33 = http_service.post_message(com)
                test_result['PngPaths'].append(result33['filename'])
                log.log(str(test_result))

                log.log(gettime() + " >>>【获取CH4@LCDRST第一个下降沿点位】")
                com = Component("interface_ICoff_LCDRST")
                com.instrName = instrName
                com.ch = "CH4"
                ICOff_LCDRST = http_service.post_message(com)  # ICOff_LCDRST["position_a"]: LCDRST First-Fall

                log.log(gettime() + " >>>【进行【t12】光标卡时间测试中】")
                com = Component("t12")
                com.instrName = instrName
                com.time_a = ICOff_LCDRST["position_a"]
                com.time_b = ICOff_VCI[0]
                ICOff3 = http_service.post_message(com)
                test_result["t12"] = ICOff3["delta"]

                log.log(gettime() + " >>>【保存Shutdown--->t12信号】")
                file_name = pic_path + "Shutdown_1@VDDI_2@VDDR_3@VCI_4@LCDRST_t12" + '.png'
                com = Component_SIPTiming("interface_save_screen")
                com.instrName = instrName
                com.file_name = file_name
                result34 = http_service.post_message(com)
                test_result['PngPaths'].append(result34['filename'])
                log.log(str(test_result))

                flag = message_box.askyesno('任务确认', '是否继续执行波形2Shutdown1@VCI--->4@MIPI测试，请确认各通道探针接触点位？')
                if flag:
                    log.log(gettime() + " >>>【执行波形2：Shutdown1@VCI_2@VDDR_3@LCDRST_4@MIPI测试任务：】")
                    com = Component("interface_set_Factory")
                    com.instrName = instrName
                    devices1 = http_service.post_message(com)

                    log.log(gettime() + " >>>【示波器参数设置：】")
                    com = Component("interface_set_DriveIC_DCDC")
                    com.instrName = instrName
                    com.OLEDTest = OLEDTest
                    com.CH_ARR = CH_ARR
                    com.ch_label = CH_LABEL_D
                    devices2 = http_service.post_message(com)

                    flag = message_box.askyesno('波形确认', '确认各路通道波形是否正常触发！')
                    if flag:
                        log.log(gettime() + " >>>【保存波形Shutdown1@VCI_2@VDDR_3@LCDRST_4@MIPI信号】")
                        file_name = pic_path + "Shutdown1@VCI_2@VDDR_3@LCDRST_4@MIPI" + '.png'
                        com = Component_SIPTiming("interface_save_screen")
                        com.instrName = instrName
                        com.file_name = file_name
                        result35 = http_service.post_message(com)
                        test_result['PngPaths'].append(result35['filename'])
                        log.log(str(test_result))

                        log.log(gettime() + " >>>【获取CH3@LCDRST第一个下降沿点位】")
                        com = Component("interface_ICoff_LCDRST")
                        com.instrName = instrName
                        com.ch = "CH3"
                        ICOff_LCDRST = http_service.post_message(com)  # ICOff_LCDRST["position_a"]: LCDRST First-Fall

                        log.log(gettime() + " >>>【保存CH4@MIPI波形CSV文件】")
                        path = f"E:\\test1\\ICOff_MIPI.csv"
                        com = Component("interface_data_caul")
                        com.instrName = instrName
                        com.ch = "CH4"
                        com.save_path = path
                        log.log(gettime() + http_service.post_message(com))

                        log.log(gettime() + " >>>【获取CH4@MIPI下降沿的两个点位：（95%|10%）】")
                        com = Component("interface_get_FallEdge")
                        com.save_path = path
                        com.min_per = 0.1
                        com.max_per = 0.95
                        ICOff_MIPI_a = http_service.post_message(com)  # ICOff_VDDR[0]: VDDR95% | ICOff_VDDR[1]: VDDR10%

                        log.log(gettime() + " >>>【获取CH4@MIPI最后第二个下降沿点位】")
                        com = Component("interface_ICoff_MIPI")
                        com.instrName = instrName
                        com.ch = "CH4"
                        ICOff_MIPI_b = http_service.post_message(com)  # ICOff_MIPI_b["position_a"]: MIPI Last-Second-Fall

                        log.log(gettime() + " >>>【进行【t13】光标卡时间测试中】")
                        com = Component("t13")
                        com.instrName = instrName
                        com.time_a = ICOff_MIPI_a[0]
                        com.time_b = ICOff_LCDRST["position_a"]
                        ICOff5 = http_service.post_message(com)
                        test_result["t13"] = ICOff5["delta"]

                        log.log(gettime() + " >>>【保存Shutdown--->t13信号】")
                        file_name = pic_path + "Shutdown _1@VCI_2@VDDR_3@LCDRST_4@MIPI_t13" + '.png'
                        com = Component_SIPTiming("interface_save_screen")
                        com.instrName = instrName
                        com.file_name = file_name
                        result36 = http_service.post_message(com)
                        test_result['PngPaths'].append(result36['filename'])
                        log.log(str(test_result))

                        log.log(gettime() + " >>>【进行【t14】光标卡时间测试中】")
                        com = Component("t14")
                        com.instrName = instrName
                        com.time_a = ICOff_MIPI_b["position_a"]
                        com.time_b = ICOff_MIPI_a[0]
                        ICOff6 = http_service.post_message(com)
                        test_result["t14"] = ICOff6["delta"]

                        log.log(gettime() + " >>>【保存Shutdown_1VDDI--->t14信号】")
                        file_name = pic_path + "Shutdown _1@VCI_2@VDDR_3@LCDRST_4@MIPI_t14" + '.png'
                        com = Component_SIPTiming("interface_save_screen")
                        com.instrName = instrName
                        com.file_name = file_name
                        result37 = http_service.post_message(com)
                        test_result['PngPaths'].append(result37['filename'])
                        log.log(str(test_result))

        elif OLEDTest == "DCDC上电":
            log.log(gettime() + " >>>【执行波形1：ScreenOn_1@AS_2@ES_3@ELVDD_4@ELVSS测试任务：】")
            com = Component("interface_set_Factory")
            com.instrName = instrName
            devices1 = http_service.post_message(com)

            log.log(gettime() + " >>>【示波器参数设置：】")
            com = Component("interface_set_DriveIC_DCDC")
            com.instrName = instrName
            com.OLEDTest = OLEDTest
            com.CH_ARR = CH_ARR
            com.ch_label = CH_LABEL_E
            devices2 = http_service.post_message(com)

            flag = message_box.askyesno('波形确认', '确认各路通道波形是否正常触发！')
            if flag:

                log.log(gettime() + " >>>【保存波形ScreenOn_1@AS_2@ES_3@ELVDD_4@ELVSS信号】")
                file_name = pic_path + "ScreenOn_1@AS_2@ES_3@ELVDD_4@ELVSS" + '.png'
                com = Component_SIPTiming("interface_save_screen")
                com.instrName = instrName
                com.file_name = file_name
                result41 = http_service.post_message(com)
                test_result['PngPaths'].append(result41['filename'])
                log.log(str(test_result))

                log.log(gettime() + " >>>【获取CH2@ES所需的各个点位：】")
                com = Component("interface_DCDCon_ES")
                com.instrName = instrName
                com.ch = "CH2"
                DCDCOn_ES = http_service.post_message(com)
                # DCDCOn_ES["ES_First_Rise"]: ES-First-Rise | DCDCOn_ES["ES_Last_Rise"]: ES-Last-Rise | DCDCOn_ES["ES_persist_a"]: 持续高电平a |
                # DCDCOn_ES["ES_persist_b"]: 持续高电平b | DCDCOn_ES["ES_persist_c"]: 持续高电平c

                log.log(gettime() + " >>>【保存CH3@ELVDD波形CSV文件】")
                path = f"E:\\test1\\DCDCOn_ELVDD.csv"
                com = Component("interface_data_caul")
                com.instrName = instrName
                com.ch = "CH3"
                com.save_path = path
                log.log(gettime() + http_service.post_message(com))

                log.log(gettime() + " >>>【获取CH3@ELVDD上升沿的两个点位：（10%|90%）】")
                com = Component("interface_get_RiseEdge")
                com.save_path = path
                com.min_per = 0.1
                com.max_per = 0.9
                DCDCOn_ELVDD = http_service.post_message(com)  # DCDCOn_ELVDD[0]: ELVDD10% | DCDCOn_ELVDD[1]: ELVDD90%

                log.log(gettime() + " >>>【进行【tINT】光标卡时间测试中】")
                com = Component("tINT")
                com.instrName = instrName
                com.time_a = DCDCOn_ES["ES_First_Rise"]
                com.time_b = DCDCOn_ELVDD[0]
                ScreenOn1 = http_service.post_message(com)
                test_result["tINT"] = ScreenOn1["delta"]

                log.log(gettime() + " >>>【保存ScreenOn--->tINT信号】")
                file_name = pic_path + "ScreenOn_1@AS_2@ES_3@ELVDD_4@ELVSS_tINT" + '.png'
                com = Component_SIPTiming("interface_save_screen")
                com.instrName = instrName
                com.file_name = file_name
                result42 = http_service.post_message(com)
                test_result['PngPaths'].append(result42['filename'])
                log.log(str(test_result))

                log.log(gettime() + " >>>【进行【tSS1】光标卡时间测试中】")
                com = Component("tSS1")
                com.instrName = instrName
                com.time_a = DCDCOn_ELVDD[0]
                com.time_b = DCDCOn_ELVDD[1]
                ScreenOn2 = http_service.post_message(com)
                test_result["tSS1"] = ScreenOn2["delta"]

                log.log(gettime() + " >>>【保存ScreenOn--->tSS1信号】")
                file_name = pic_path + "ScreenOn_1@AS_2@ES_3@ELVDD_4@ELVSS_tSS1" + '.png'
                com = Component_SIPTiming("interface_save_screen")
                com.instrName = instrName
                com.file_name = file_name
                result43 = http_service.post_message(com)
                test_result['PngPaths'].append(result43['filename'])
                log.log(str(test_result))

                log.log(gettime() + " >>>【保存CH4@ELVSS波形CSV文件】")
                path = f"E:\\test1\\ICOff_ELVSS.csv"
                com = Component("interface_data_caul")
                com.instrName = instrName
                com.ch = "CH4"
                com.save_path = path
                log.log(gettime() + http_service.post_message(com))

                log.log(gettime() + " >>>【获取CH1@ELVSS下降沿的两个点位：（90%|10%）】")
                com = Component("interface_get_FallEdge")
                com.save_path = path
                com.min_per = 0.1
                com.max_per = 0.8
                DCDCOn_ELVSS = http_service.post_message(com)  # ICOff_ELVSS[0]: ELVSS90% | ICOff_ELVSS[1]: ELVSS10%

                log.log(gettime() + " >>>【进行【tDELAY】光标卡时间测试中】")
                com = Component("tDELAY")
                com.instrName = instrName
                com.time_a = DCDCOn_ELVDD[1]
                com.time_b = DCDCOn_ELVSS[0]
                ScreenOn3 = http_service.post_message(com)
                test_result["tDELAY"] = ScreenOn3["delta"]

                log.log(gettime() + " >>>【保存ScreenOn--->tDELAY信号】")
                file_name = pic_path + "ScreenOn_1@AS_2@ES_3@ELVDD_4@ELVSS_tDELAY" + '.png'
                com = Component_SIPTiming("interface_save_screen")
                com.instrName = instrName
                com.file_name = file_name
                result44 = http_service.post_message(com)
                test_result['PngPaths'].append(result44['filename'])
                log.log(str(test_result))

                log.log(gettime() + " >>>【进行【tSS2】光标卡时间测试中】")
                com = Component("tSS2")
                com.instrName = instrName
                com.time_a = DCDCOn_ELVSS[0]
                com.time_b = DCDCOn_ELVSS[1]
                ScreenOn4 = http_service.post_message(com)
                test_result["tSS2"] = ScreenOn4["delta"]

                log.log(gettime() + " >>>【保存ScreenOn--->tSS2信号】")
                file_name = pic_path + "ScreenOn_1@AS_2@ES_3@ELVDD_4@ELVSS_tSS2" + '.png'
                com = Component_SIPTiming("interface_save_screen")
                com.instrName = instrName
                com.file_name = file_name
                result45 = http_service.post_message(com)
                test_result['PngPaths'].append(result45['filename'])
                log.log(str(test_result))

                log.log(gettime() + " >>>【进行【tHIGH】光标卡时间测试中】")
                com = Component("tHIGH")
                com.instrName = instrName
                com.time_a = DCDCOn_ES["ES_persist_a"]
                com.time_b = DCDCOn_ES["ES_persist_b"]
                ScreenOn5 = http_service.post_message(com)
                test_result["tHIGH"] = ScreenOn5["delta"]

                log.log(gettime() + " >>>【保存ScreenOn--->tHIGH信号】")
                file_name = pic_path + "ScreenOn_1@AS_2@ES_3@ELVDD_4@ELVSS_tHIGH" + '.png'
                com = Component_SIPTiming("interface_save_screen")
                com.instrName = instrName
                com.file_name = file_name
                result46 = http_service.post_message(com)
                test_result['PngPaths'].append(result46['filename'])
                log.log(str(test_result))

                log.log(gettime() + " >>>【进行【tLOW】光标卡时间测试中】")
                com = Component("tLOW")
                com.instrName = instrName
                com.time_a = DCDCOn_ES["ES_persist_b"]
                com.time_b = DCDCOn_ES["ES_persist_c"]
                ScreenOn6 = http_service.post_message(com)
                test_result["tLOW"] = ScreenOn5["delta"]

                log.log(gettime() + " >>>【保存ScreenOn--->tLOW信号】")
                file_name = pic_path + "ScreenOn_1@AS_2@ES_3@ELVDD_4@ELVSS_tLOW" + '.png'
                com = Component_SIPTiming("interface_save_screen")
                com.instrName = instrName
                com.file_name = file_name
                result47 = http_service.post_message(com)
                test_result['PngPaths'].append(result47['filename'])
                log.log(str(test_result))

                log.log(gettime() + " >>>【获取【ELVSS】上升沿0%位置】")
                path = f"E:\\test1\\ICOff_ELVSS.csv"
                com = Component("interface_DCDCon_ELVSS")
                com.save_path = path
                DCDCOn_ELVSS = http_service.post_message(com)

                log.log(gettime() + " >>>【进行【tSTORE】时间测试中】")
                com = Component("tSTORE")
                com.instrName = instrName
                com.time_a = DCDCOn_ES["ES_Last_Rise"]
                com.time_b = DCDCOn_ELVSS
                ScreenOn7 = http_service.post_message(com)
                test_result["tSTORE"] = ScreenOn7["delta"]

                log.log(gettime() + " >>>【保存ScreenOn--->tSTORE信号】")
                file_name = pic_path + "ScreenOn_1@AS_2@ES_3@ELVDD_4@ELVSS_tSTORE" + '.png'
                com = Component_SIPTiming("interface_save_screen")
                com.instrName = instrName
                com.file_name = file_name
                result48 = http_service.post_message(com)
                test_result['PngPaths'].append(result48['filename'])
                log.log(str(test_result))

        elif OLEDTest == "DCDC下电":
            log.log(gettime() + " >>>【执行波形1：ScreenOff_1@AS_2@ES_3@ELVDD_4@ELVSS测试任务：】")
            com = Component("interface_set_Factory")
            com.instrName = instrName
            devices1 = http_service.post_message(com)

            log.log(gettime() + " >>>【示波器参数设置：】")
            com = Component("interface_set_DriveIC_DCDC")
            com.instrName = instrName
            com.OLEDTest = OLEDTest
            com.CH_ARR = CH_ARR
            com.ch_label = CH_LABEL_E
            devices2 = http_service.post_message(com)

            flag = message_box.askyesno('波形确认', '确认各路通道波形是否正常触发！')
            if flag:
                log.log(gettime() + " >>>【保存波形ScreenOff_1@AS_2@ES_3@ELVDD_4@ELVSS信号】")
                file_name = pic_path + "ScreenOff_1@AS_2@ES_3@ELVDD_4@ELVSS" + '.png'
                com = Component_SIPTiming("interface_save_screen")
                com.instrName = instrName
                com.file_name = file_name
                result51 = http_service.post_message(com)
                test_result['PngPaths'].append(result51['filename'])
                log.log(str(test_result))

                log.log(gettime() + " >>>【获取CH2@ES波形所需的位置】")
                com = Component("interface_DCDCoff_ES")
                com.instrName = instrName
                com.ch = "CH2"
                DCDCOff_ES = http_service.post_message(com)  # DCDCOff_ES["position_a"]:ES-First-Rise

                log.log(gettime() + " >>>【保存CH3@ELVDD波形CSV文件】")
                path = f"E:\\test1\\DCDCOff_ELVDD.csv"
                com = Component("interface_data_caul")
                com.instrName = instrName
                com.ch = "CH3"
                com.save_path = path
                log.log(gettime() + http_service.post_message(com))

                path = f"E:\\test1\\DCDCOff_ELVDD.csv"
                log.log(gettime() + " >>>【获取CH3@ELVDD下降沿的两个点位：（95%|10%）】")
                com = Component("interface_get_FallEdge")
                com.save_path = path
                com.min_per = 0.1
                com.max_per = 0.95
                DCDCOff_ELVDD = http_service.post_message(com)  # DCDCOff_ELVDD[0]: ELVDD95% | DCDCOff_ELVDD[1]: ELVDD5%

                log.log(gettime() + " >>>【进行【tOFF】光标卡时间测试中】")
                com = Component("tOFF")
                com.instrName = instrName
                com.time_a = DCDCOff_ES["position_a"]
                com.time_b = DCDCOff_ELVDD[0]
                ScreenOff1 = http_service.post_message(com)
                test_result["tOFF"] = ScreenOff1["delta"]

                log.log(gettime() + " >>>【保存ScreenOff--->tOff信号】")
                file_name = pic_path + "ScreenOn_1@AS_2@ES_3@ELVDD_4@ELVSS_tOff" + '.png'
                com = Component_SIPTiming("interface_save_screen")
                com.instrName = instrName
                com.file_name = file_name
                result52 = http_service.post_message(com)
                test_result['PngPaths'].append(result52['filename'])
                log.log(str(test_result))

                log.log(gettime() + " >>>【进行【tDISCHG】光标卡时间测试中】")
                com = Component("tDISCHG")
                com.instrName = instrName
                com.time_a = DCDCOff_ELVDD[0]
                com.time_b = DCDCOff_ELVDD[1]
                ScreenOff2 = http_service.post_message(com)
                test_result["tDISCHG"] = ScreenOff2["delta"]

                log.log(gettime() + " >>>【保存ScreenOff--->tDISCHG信号】")
                file_name = pic_path + "ScreenOn_1@AS_2@ES_3@ELVDD_4@ELVSS_tDISCHG" + '.png'
                com = Component_SIPTiming("interface_save_screen")
                com.instrName = instrName
                com.file_name = file_name
                result53 = http_service.post_message(com)
                test_result['PngPaths'].append(result53['filename'])
                log.log(str(test_result))

    except Exception as err:
        log.exception(str(err))








