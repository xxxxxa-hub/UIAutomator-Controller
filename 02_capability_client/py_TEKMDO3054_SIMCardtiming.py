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

# 定义三个class (SIMCard本身 | SIPTiming接口应用 | jpg保存接口)
class Component(object):
    def __init__(self, interface):
        self.pack = "pack_oscilloscope"
        self.module = "module_TEKMDO3054_SIMCardtiming"
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


log = MessageToCSharpType("")
http_service = HttpService()


#  log中显示时间
def gettime():
    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return t

# 调试脚本
if __name__ == '__main__':
    try:
        strReceive = r'{"clockchn": "", "datachn": "", "oscillographName": "A019990201","instrName": ' \
                     r'"TCPIP::169.254.8.23::INSTR","instrModel": "Tektronix MDO3000 Series", "prjname": "21841", ' \
                     r'"priplat": "高通", "prjver": "Ver.A","signaltyp": "", "LoopTimes": "1", "datasignal": "", ' \
                     r'"clksignal": "", "expectAddress": "","autoTrig": "False","needInitScope": "False", ' \
                     r'"TestCaseName": "SIMCard(U)\u003c--SIMCard(U)", "TestUnit": "SIM卡","rechipname": "SIMCard", ' \
                     r'"rechipnum": "U", "trchipname": "SIMCard", "trchipnum": "U","prjdescr": "","useClkChannel": ' \
                     r'"True", "useDataChannel": "True", "testSceneName": "", "DataSignalName": "NA","ClkSignalName": ' \
                     r'"NA", "ChipAddress": "", "loop_index": "1", "SIMCardTest": "时钟停止","t_clock": "0.0000026",' \
                     r'"SIMCardVol": "3", "Python_File_Name": "Py_TEKMDO3054_SIMCardtiming.py","screenshotPath": ' \
                     r'"D:\\OPPO\\Mr_Wang\\sts\\01_Code\\STS\\Debug\\Testresult\\21841\\Ver.A"} '

        # strReceive = sys.argv[1]
        # log.log(strReceive)
        parameterList = ast.literal_eval(strReceive)
        log.log(parameterList)

        SIMCardTest = parameterList['SIMCardTest']
        SIMCardVol = parameterList['SIMCardVol']
        t_clock = float(parameterList['t_clock'])
        instrName = parameterList["instrName"]

        test_name = 'SIMCard'
        record_length = 5E-6
        ch_list = 'CH1,CH2,CH3,CH4'
        label_list = 'VSIM,CLK,RST,IO'
        acquire_type = 'SEQUENCE'
        open_ch = ["CH1", "CH2", "CH3", "CH4"]

        search_ch1 = 'CH1'
        search_type1_R = 'RISE'
        search_level1_R = 1.26
        search_type1_F = 'FALL'
        search_level1_F = 1.26

        search_ch2 = 'CH2'
        search_type2_R = 'RISE'
        search_level2_R = 1.26
        search_type2_F = 'FALL'
        search_level2_F = 1.26

        search_ch3 = 'CH3'
        search_type3_R = 'RISE'
        search_level3_R = 1.26
        search_type3_F = 'FALL'
        search_level3_F = 1.26

        search_ch4 = 'CH4'
        search_type4_R = 'RISE'
        search_level4_R = 1.26
        search_type4_F = 'FALL'
        search_level4_F = 1.26

        close_ch1 = "CH1"
        close_ch2 = "CH2"
        close_ch3 = "CH3"
        close_ch4 = "CH4"

        message_box = MessageBox()  # 弹出框判断选择

        pic_path = r'E:\test1' + "\\"
        # pic_path = parameterList['screenshotPath'] + "\\"
        # pic_path = pic_patha.replace('/', '\\')
        # file_name = test_name + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + '.png'

        #  约定为这个变量名称，存储返回结果的字典
        test_result = {'PngPaths': []}
        # --------------------------------------示波器公共操作方法---------------------------------------------------

        log.log(gettime() + " >>>【初始化示波器设置参数】")
        com = Component("interface_Set_Common")
        com.instrName = instrName
        com.open_ch = open_ch
        com.ch_list = ch_list
        com.label_list = label_list
        device_set1 = http_service.post_message(com)


        # -------------------------------------------------------------激活时序-------------------------------------------------------------------
        """1.设置示波器 ———— 2.获取各通道波形 ———— 3.将通道波形连接为str给server ———— 4.获取光标水平位置 ———— 5.显示光标位置获取tb和tg间隔 ———— 6.截图保存波形"""
        if SIMCardTest == "激活时序":

            if SIMCardVol == '1.8':
                trigger_level = 0.9
            if SIMCardVol == '3':
                trigger_level = 2

            position_horizontal1 = 2.26
            position_horizontal2 = 1.26
            cursor_source = "CH2"

            log.log(gettime() + " >>>【设置[激活时序]测试项示波器参数】")
            com = Component("interface_Set_Activate_Timing")
            com.instrName = instrName
            com.trigger_level =trigger_level
            device_set2 = http_service.post_message(com)

            flag = message_box.askyesno('波形确认', '请先触发波形并确认激活时序波形正确，再点击确认！')
            if flag:
                log.log(gettime() + " >>>【调整示波器亮度为100】")
                com = Component("set_DisplayIntensity")
                com.instrName = instrName
                com.intensity = 100
                device = http_service.post_message(com)

                log.log(gettime() + " >>>【设置 CLK 通道的搜索条件，并返回搜索值】")
                com = Component_SIPTiming("interface_set_search")
                com.instrName = instrName
                com.search_ch = search_ch2
                com.search_type = search_type2_R
                com.search_level = search_level2_R
                mark_position2 = http_service.post_message(com)
                if mark_position2['query'][:4] == 'NONE':
                    log.fail("CLK 通道的搜索返回值为空")
                    sys.exit()

                log.log(gettime() + " >>>【设置 RST 通道的搜索条件，并返回搜索值】")
                com = Component_SIPTiming("interface_set_search")
                com.instrName = instrName
                com.search_ch = search_ch3
                com.search_type = search_type3_R
                com.search_level = search_level3_R
                mark_position3 = http_service.post_message(com)
                if mark_position3['query'][:4] == 'NONE':
                    log.fail("RST 通道的搜索返回值为空")
                    sys.exit()

                log.log(gettime() + " >>>【设置 IO 通道的搜索条件，并返回搜索值】")
                com = Component_SIPTiming("interface_set_search")
                com.instrName = instrName
                com.search_ch = search_ch4
                com.search_type = search_type4_F
                com.search_level = search_level4_F
                mark_position4 = http_service.post_message(com)
                if mark_position4['query'][:4] == 'NONE':
                    log.fail("IO 搜索通道的搜索返回值为空")
                    sys.exit()

                # 截取各个通道的第一个触发数据
                if ";" in mark_position2['query']:
                    mark_position2['query'] = (mark_position2['query'][:mark_position2['query'].index(';')])
                if ";" in mark_position3['query']:
                    mark_position3['query'] = (mark_position3['query'][:mark_position3['query'].index(';')])
                if ";" in mark_position4['query']:
                    mark_position4['query'] = (mark_position4['query'][:mark_position4['query'].index(';')])

                log.log(gettime() + " >>>【计算光标的位置坐标】")
                mark_position_str = mark_position2['query'] + ';' + mark_position3['query'] + ';' + mark_position4[
                    'query'] + ';'
                com = Component("interface_position_client")
                com.instrName = instrName
                com.position_str = mark_position_str
                position_return = http_service.post_message(com)

                horizontal_position_a = float(position_return['position_a'])  # CLK光标垂直位置
                horizontal_position_b = float(position_return['position_b'])  # RST光标垂直位置
                horizontal_position_c = float(position_return['position_c'])  # IO光标垂直位置

                log.log(gettime() + " >>>【获取tb时间并判断是否满足协议】")
                com = Component("interface_set_simcursor")
                com.instrName = instrName
                com.cursor_source = "CH4"
                com.position_horizontal1 = 0
                com.position_horizontal2 = 0
                com.position1 = horizontal_position_a
                com.position2 = horizontal_position_b
                cursor_return = http_service.post_message(com)

                tb = float(cursor_return['delta'])
                result = bool(tb >= 400 * t_clock)
                if result:
                    test_result['HasJudged'] = True
                    TestResult = "SIM激活时序Tc测试结果：Pass,Tb为:" + str(cursor_return['delta']) + "s"
                    log.log(gettime() + " >>>【" + TestResult + "】")
                else:
                    test_result['HasJudged'] = False
                    TestResult = "SIM激活时序Tc测试结果：Fail,Tb为:" + str(cursor_return['delta']) + "s"
                    log.log(gettime() + " >>>【" + TestResult + "】")
                test_result['Tb'] = tb

                log.log(gettime() + " >>>【保存激活时序Tb时间图片】")
                # 约定PngPaths键名，存储图像列表
                file_name = pic_path + test_name + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + 'Tb.png'
                # 约定PngPaths键名，存储图像列表
                com = Component_SIPTiming("interface_save_screen")
                com.instrName = instrName
                com.file_name = file_name
                # 结果返回图像路径，此路径包必须含在参数parameterList["screenshotPath"]目录下
                result15 = http_service.post_message(com)
                #  结果图像路径追加到字典中的键为PngPaths的列表
                test_result['PngPaths'].append(result15['filename'])
                log.log(str(test_result))

                log.log(gettime() + " >>>【放大Tb时间图片】")
                com = Component("interface_adjust_Picture")
                com.instrName = instrName
                com.cursor_source = "CH4"
                com.position_horizontal1 = horizontal_position_a
                com.position_horizontal2 = horizontal_position_b
                Zoom_picture1 = http_service.post_message(com)

                log.log(gettime() + " >>>【保存激活时序Tb时间放大后图片】")
                # 约定PngPaths键名，存储图像列表
                file_name = pic_path + test_name + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + 'Tb.png'
                # 约定PngPaths键名，存储图像列表
                com = Component_SIPTiming("interface_save_screen")
                com.instrName = instrName
                com.file_name = file_name
                # 结果返回图像路径，此路径包必须含在参数parameterList["screenshotPath"]目录下
                result15 = http_service.post_message(com)
                #  结果图像路径追加到字典中的键为PngPaths的列表
                test_result['PngPaths'].append(result15['filename'])
                log.log(str(test_result))

                log.log("获取tc时间并判断是否满足协议")
                if SIMCardVol == "3":
                    log.log("开启zoom放大波形")
                    com = Component("interface_adjust_scale")
                    com.instrName = instrName
                    com.pos_a = horizontal_position_b
                    com.pos_b = horizontal_position_c
                    com.siterate = False
                    res = http_service.post_message(com)

                com = Component("interface_set_simcursor")
                com.instrName = instrName
                com.cursor_source = "CH2"
                com.position_horizontal1 = 0
                com.position_horizontal2 = 0
                com.position1 = horizontal_position_b
                com.position2 = horizontal_position_c
                cursor_return = http_service.post_message(com)
                tc = float(cursor_return['delta'])
                t_clock = float(t_clock)
                result = bool(tc >= 400 * t_clock and tc <= 40000 * t_clock)
                if result:
                    test_result['HasJudged'] = True
                    TestResult = "SIM激活时序Tc测试结果：Pass,Tc为:" + str(cursor_return['delta']) + "s"
                else:
                    test_result['HasJudged'] = False
                    TestResult = "SIM激活时序Tc测试结果：Pass,Tc为:" + str(cursor_return['delta']) + "s"
                test_result['Tc'] = tc

                # 约定PngPaths键名，存储图像列表
                file_name = pic_path + test_name + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + '.png'
                # 约定PngPaths键名，存储图像列表
                com = Component_SIPTiming("interface_save_screen")
                com.instrName = instrName
                com.file_name = file_name
                # 结果返回图像路径，此路径包必须含在参数parameterList["screenshotPath"]目录下
                result15 = http_service.post_message(com)
                # pic_path = pic_patha + result15['filename']
                #  结果图像路径追加到字典中的键为PngPaths的列表
                test_result['PngPaths'].append(result15['filename'])

                log.log(gettime() + " >>>【放大Tc时间图片】")
                com = Component("interface_adjust_Picture")
                com.instrName = instrName
                com.cursor_source = "CH1"
                com.position_horizontal1 = horizontal_position_b
                com.position_horizontal2 = horizontal_position_c
                Zoom_picture2 = http_service.post_message(com)

                log.log(gettime() + " >>>【保存激活时序Tc时间放大后图片】")
                # 约定PngPaths键名，存储图像列表
                file_name = pic_path + test_name + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + 'Tb.png'
                # 约定PngPaths键名，存储图像列表
                com = Component_SIPTiming("interface_save_screen")
                com.instrName = instrName
                com.file_name = file_name
                # 结果返回图像路径，此路径包必须含在参数parameterList["screenshotPath"]目录下
                result15 = http_service.post_message(com)
                #  结果图像路径追加到字典中的键为PngPaths的列表
                test_result['PngPaths'].append(result15['filename'])
                log.log(str(test_result))

            else:
                pass

        # -----------------------------------------------------------时钟停止时序-----------------------------------------------------------------
        """1.设置示波器 ———— 2.获取各通道波形 ———— 3.将通道波形连接为str给server ———— 4.获取光标水平位置 ———— 5.显示光标位置获取tb和tg间隔 ———— 6.截图保存波形"""
        if SIMCardTest == "时钟停止":
            # if SIMCardVol == "1.8":
            #     trigger_delay = 20E-3
            #     scale_horizontal = 10E-3  # 时基参数
            # elif SIMCardVol == "3":
            trigger_delay = 20E-3
            scale_horizontal = 10E-3  # 时基参数
            trigger_type = 'RISE'
            trigger_ch = 'CH2'
            trigger_level = 0.9
            position_horizontal1 = 2.26
            position_horizontal2 = 1.26

            log.log("关闭 VSIM 通道")
            com = Component_SIPTiming("interface_close_ch")
            com.instrName = instrName
            com.ch = close_ch1
            result1 = http_service.post_message(com)

            log.log("关闭 RST 通道")
            com = Component_SIPTiming("interface_close_ch")
            com.instrName = instrName
            com.ch = close_ch3
            result2 = http_service.post_message(com)

            log.log("设置时基")
            com = Component_SIPTiming("interface_set_horizontal_scale")
            com.instrName = instrName
            com.scale_horizontal = scale_horizontal
            result3 = http_service.post_message(com)

            log.log("设置触发类型")
            com = Component_SIPTiming("interface_set_trigger")
            com.instrName = instrName
            com.trigger_type = trigger_type
            com.trigger_ch = trigger_ch
            com.trigger_level = trigger_level
            com.trigger_delay = trigger_delay
            result4 = http_service.post_message(com)

            log.log("设置触发模式")
            com = Component_SIPTiming("interface_set_trigger_mode")
            com.instrName = instrName
            com.acquire_type = acquire_type
            result5 = http_service.post_message(com)

            log.log("示波器开始采集数据")
            com = Component_SIPTiming("interface_start_acquisitions")
            com.instrName = instrName
            result6 = http_service.post_message(com)

            log.log("等待波形触发")
            time.sleep(20)

            flag = message_box.askyesno('波形确认', '请确认时钟停止时序波形是否正确？')
            if flag:

                log.log("设置 CLK 通道的搜索条件(上升沿数据)，并返回搜索值")
                com = Component_SIPTiming("interface_set_search")
                com.instrName = instrName
                com.search_ch = search_ch2
                com.search_type = search_type2_R
                com.search_level = search_level2_R
                mark_position1 = http_service.post_message(com)
                if mark_position1['query'][:4] == 'NONE':
                    log.fail("RST 通道的搜索返回值为空")
                    sys.exit()

                log.log("设置 IO 通道的搜索条件（下降沿数据），并返回搜索值")
                com = Component_SIPTiming("interface_set_search")
                com.instrName = instrName
                com.search_ch = search_ch4
                com.search_type = search_type4_F
                com.search_level = search_level4_F
                mark_position2 = http_service.post_message(com)
                if mark_position2['query'][:4] == 'NONE':
                    log.fail("IO 搜索通道的搜索返回值为空")
                    sys.exit()

                log.log("设置 IO 通道的搜索条件（上升沿数据），并返回搜索值")
                com = Component_SIPTiming("interface_set_search")
                com.instrName = instrName
                com.search_ch = search_ch4
                com.search_type = search_type4_R
                com.search_level = search_level4_R
                mark_position3 = http_service.post_message(com)
                if mark_position3['query'][:4] == 'NONE':
                    log.fail("IO 搜索通道的搜索返回值为空")
                    sys.exit()

                log.log("设置 CLK 通道的搜索条件（下降沿数据），并返回搜索值")
                path = "E:/test1/test.csv"
                com = Component("interface_data_caul")
                com.instrName = instrName
                com.ch = search_ch2
                com.save_path = path
                Path_result = http_service.post_message(com)

                # 截取各个通道的第一个触发数据
                if ";" in mark_position1['query']:
                    mark_position1['query'] = (mark_position1['query'][:mark_position1['query'].index(';')])
                if ";" in mark_position2['query']:
                    mark_position2['query'] = (mark_position2['query'][:mark_position2['query'].index(';')])
                if ";" in mark_position3['query']:
                    com = Component("interface_laststr")
                    com.str1 = mark_position3['query']
                    mark_position3['query'] = http_service.post_message(com)

                log.log("计算光标的位置坐标")
                mark_position_str = mark_position1['query'] + ';' + mark_position2['query'] + ';' + mark_position3[
                    'query'] + ';'
                com = Component("interface_position_client")
                com.instrName = instrName
                com.position_str = mark_position_str
                position_return = http_service.post_message(com)

                horizontal_position_a = float(position_return['position_a'])  # CLK光标垂直位置
                horizontal_position_b = float(position_return['position_b'])  # RST光标垂直位置
                horizontal_position_c = float(position_return['position_c'])  # IO光标垂直位置
                com = Component("interface_latepoint")
                com.save_path = path
                horizontal_position_d = http_service.post_message(com)

                log.log("获取tg时间并判断是否满足协议")
                com = Component("interface_set_simcursor")
                com.instrName = instrName
                com.cursor_source = "CH4"
                com.position_horizontal1 = 0
                com.position_horizontal2 = 0
                com.position1 = horizontal_position_a
                com.position2 = horizontal_position_b
                cursor_return1 = http_service.post_message(com)

                tg = float(cursor_return1['delta'])
                result = bool(tg >= 1860 * t_clock)
                if result:
                    test_result['relust_Tg'] = True
                    TestResult = "时钟停止时序Tg测试结果：Pass,Tg为:" + str(cursor_return1['delta']) + "s"
                    log.log(TestResult)
                else:
                    test_result['relust_Tg'] = False
                    TestResult = "时钟停止时序Tg测试结果：Pass,Tg为:" + str(cursor_return1['delta']) + "s"
                    log.log(TestResult)
                test_result['Tg'] = tg

                file_name = pic_path + test_name + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + '.png'
                com = Component_SIPTiming("interface_save_screen")
                com.instrName = instrName
                com.file_name = file_name
                result14 = http_service.post_message(com)
                test_result['PngPaths'].append(result14['filename'])
                log.log(str(test_result))

                log.log(gettime() + " >>>【放大Tg时间图片】")
                com = Component("interface_adjust_Picture")
                com.instrName = instrName
                com.cursor_source = "CH4"
                com.position_horizontal1 = horizontal_position_a
                com.position_horizontal2 = horizontal_position_b
                com.trigger_delay = trigger_delay
                Zoom_picture1 = http_service.post_message(com)

                log.log(gettime() + " >>>【保存激活时序Tg时间放大后图片】")
                # 约定PngPaths键名，存储图像列表
                file_name = pic_path + test_name + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + 'Tg.png'
                # 约定PngPaths键名，存储图像列表
                com = Component_SIPTiming("interface_save_screen")
                com.instrName = instrName
                com.file_name = file_name
                # 结果返回图像路径，此路径包必须含在参数parameterList["screenshotPath"]目录下
                result15 = http_service.post_message(com)
                #  结果图像路径追加到字典中的键为PngPaths的列表
                test_result['PngPaths'].append(result15['filename'])
                log.log(str(test_result))

                log.log("获取th时间并判断是否满足协议")
                com = Component("interface_set_simcursor")
                com.instrName = instrName
                com.cursor_source = "CH4"
                com.position_horizontal1 = 0
                com.position_horizontal2 = 0
                com.position1 = horizontal_position_c
                com.position2 = horizontal_position_d
                cursor_return2 = http_service.post_message(com)

                th = float(cursor_return2['delta'])
                result = bool(th >= 700 * t_clock)
                if result:
                    test_result['relust_Th'] = True
                    TestResult = "时钟停止时序Th测试结果：Pass,Th为:" + str(cursor_return2['delta']) + "s"
                    log.log(TestResult)
                else:
                    test_result['relust_Th'] = False
                    TestResult = "时钟停止时序Th测试结果：Fail,Th为:" + str(cursor_return2['delta']) + "s"
                    log.log(TestResult)
                test_result['Th'] = th

                file_name = pic_path + test_name + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + '.png'
                # 约定PngPaths键名，存储图像列表
                com = Component_SIPTiming("interface_save_screen")
                com.instrName = instrName
                com.file_name = file_name
                # 结果返回图像路径，此路径包必须含在参数parameterList["screenshotPath"]目录下
                result15 = http_service.post_message(com)
                # pic_path = pic_patha + result15['filename']
                #  结果图像路径追加到字典中的键为PngPaths的列表
                test_result['PngPaths'].append(result15['filename'])

                log.log(gettime() + " >>>【放大Th时间图片】")
                com = Component("interface_adjust_Picture")
                com.instrName = instrName
                com.cursor_source = "CH4"
                com.position_horizontal1 = horizontal_position_c
                com.position_horizontal2 = horizontal_position_d
                com.trigger_delay = trigger_delay
                Zoom_picture1 = http_service.post_message(com)

                log.log(gettime() + " >>>【保存激活时序Th时间放大后图片】")
                # 约定PngPaths键名，存储图像列表
                file_name = pic_path + test_name + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + 'Th.png'
                # 约定PngPaths键名，存储图像列表
                com = Component_SIPTiming("interface_save_screen")
                com.instrName = instrName
                com.file_name = file_name
                # 结果返回图像路径，此路径包必须含在参数parameterList["screenshotPath"]目录下
                result15 = http_service.post_message(com)
                #  结果图像路径追加到字典中的键为PngPaths的列表
                test_result['PngPaths'].append(result15['filename'])
                log.log(str(test_result))
            else:
                pass

        # ------------------------------------------------------------上电时序-------------------------------------------------------------------
        """1.设置示波器 ———— 2.获取各通道波形 ———— 3.将通道波形连接为str给server ———— 4.获取光标水平位置 ———— 5.对比各光标水平位置值大小判断结果 ———— 6.截图保存波形"""
        if SIMCardTest == "上电时序":
            trigger_type = 'RISE'
            trigger_ch = 'CH1'
            trigger_level = 0.9
            trigger_delay = 150E-6
            position_horizontal1 = 2.26
            position_horizontal2 = 1.26
            screen_position = 20  # 屏幕位置
            scale_horizontal = 10E-3  # 时基参数

            log.log("设置时基")
            com = Component_SIPTiming("interface_set_horizontal_scale")
            com.instrName = instrName
            com.scale_horizontal = scale_horizontal
            result1 = http_service.post_message(com)

            log.log("设置触发类型")
            com = Component_SIPTiming("interface_set_trigger")
            com.instrName = instrName
            com.trigger_type = trigger_type
            com.trigger_ch = trigger_ch
            com.trigger_level = trigger_level
            com.trigger_delay = trigger_delay
            result2 = http_service.post_message(com)

            log.log("关闭水平延迟功能")
            com = Component_SIPTiming("interface_horizontal_delay_state")
            com.instrName = instrName
            com.state = "OFF"
            result3 = http_service.post_message(com)

            log.log("设置触发位置")
            com = Component_SIPTiming("interface_set_horizontal_position")
            com.instrName = instrName
            com.position_horizontal = screen_position
            result4 = http_service.post_message(com)

            log.log("设置触发模式")
            com = Component_SIPTiming("interface_set_trigger_mode")
            com.instrName = instrName
            com.acquire_type = acquire_type
            result5 = http_service.post_message(com)

            log.log("示波器开始采集数据")
            com = Component_SIPTiming("interface_start_acquisitions")
            com.instrName = instrName
            result6 = http_service.post_message(com)

            log.log("等待波形触发")
            time.sleep(20)

            flag = message_box.askyesno('波形确认', '请确认上电时序波形是否正确？')
            if flag:
                log.log("设置 VSIM 通道的搜索条件(上升沿数据)，并返回搜索值")
                com = Component_SIPTiming("interface_set_search")
                com.instrName = instrName
                com.search_ch = search_ch1
                com.search_type = search_type1_R
                com.search_level = search_level1_R
                mark_position1 = http_service.post_message(com)
                if mark_position1['query'][:4] == 'NONE':
                    log.fail("VSIM 通道的搜索返回值为空")
                    sys.exit()

                log.log("设置 CLK 通道的搜索条件(上升沿数据)，并返回搜索值")
                com = Component_SIPTiming("interface_set_search")
                com.instrName = instrName
                com.search_ch = search_ch2
                com.search_type = search_type2_R
                com.search_level = search_level2_R
                mark_position2 = http_service.post_message(com)
                if mark_position2['query'][:4] == 'NONE':
                    log.fail("CLK 通道的搜索返回值为空")
                    sys.exit()

                log.log("设置 RST 通道的搜索条件(上升沿数据)，并返回搜索值")
                com = Component_SIPTiming("interface_set_search")
                com.instrName = instrName
                com.search_ch = search_ch3
                com.search_type = search_type3_R
                com.search_level = search_level3_R
                mark_position3 = http_service.post_message(com)
                if mark_position3['query'][:4] == 'NONE':
                    log.fail("RST 通道的搜索返回值为空")
                    sys.exit()

                log.log("设置 IO 通道的搜索条件(上升沿数据)，并返回搜索值")
                com = Component_SIPTiming("interface_set_search")
                com.instrName = instrName
                com.search_ch = search_ch4
                com.search_type = search_type4_R
                com.search_level = search_level4_R
                mark_position4 = http_service.post_message(com)
                if mark_position4['query'][:4] == 'NONE':
                    log.fail("IO 通道的搜索返回值为空")
                    sys.exit()

                # 截取各个通道的第一个触发数据
                if ";" in mark_position1['query']:
                    mark_position1['query'] = (mark_position1['query'][:mark_position1['query'].index(';')])
                if ";" in mark_position2['query']:
                    mark_position2['query'] = (mark_position2['query'][:mark_position2['query'].index(';')])
                if ";" in mark_position3['query']:
                    mark_position3['query'] = (mark_position3['query'][:mark_position3['query'].index(';')])
                if ";" in mark_position4['query']:
                    mark_position4['query'] = (mark_position4['query'][:mark_position4['query'].index(';')])

                log.log("计算光标的位置坐标")
                mark_position_str = mark_position1['query'] + ';' + mark_position2['query'] + ';' + mark_position3[
                    'query'] + ';' + mark_position4[
                                        'query'] + ';'
                com = Component("interface_position_client")
                com.instrName = instrName
                com.position_str = mark_position_str
                position_return = http_service.post_message(com)

                horizontal_position_a = float(position_return['position_a'])  # SIM光标垂直位置
                horizontal_position_b = float(position_return['position_b'])  # CLK光标垂直位置
                horizontal_position_c = float(position_return['position_c'])  # RST光标垂直位置
                horizontal_position_d = float(position_return['position_d'])  # IO光标垂直位置

                test_result['上电时序VSIM位置：'] = horizontal_position_a
                test_result['上电时序CLK位置'] = horizontal_position_b
                test_result['上电时序RST位置'] = horizontal_position_c
                test_result['上电时序IO位置'] = horizontal_position_d

                if horizontal_position_a < horizontal_position_d < horizontal_position_b < horizontal_position_c:
                    test_result["Power_on"] = True
                    TestResult = "上电时序测试结果：Pass"
                    log.log(TestResult)
                else:
                    test_result["Power_on"] = False
                    TestResult = "上电时序测试结果：Fail"
                    log.log(TestResult)

                flag = message_box.askyesno('示波器截图', '请确认是否保存当前波形图片？')
                if flag:
                    # 约定PngPaths键名，存储图像列表
                    file_name = pic_path + test_name + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + '.png'
                    com = Component_SIPTiming("interface_save_screen")
                    com.instrName = instrName
                    com.file_name = file_name
                    result14 = http_service.post_message(com)
                    test_result['PngPaths'].append(result14['filename'])
                    log.log(str(test_result))
            else:
                exit()

        # ------------------------------------------------------------下电时序-------------------------------------------------------------------
        """1.设置示波器 ———— 2.获取各通道波形 ———— 3.将通道波形连接为str给server ———— 4.获取光标水平位置 ———— 5.对比各光标水平位置值大小判断结果 ———— 6.截图保存波形"""
        if SIMCardTest == "下电时序":
            trigger_type = 'FALL'
            trigger_ch = 'CH1'
            trigger_level = 0.9
            trigger_delay = 150E-6
            position_horizontal1 = 2.26
            position_horizontal2 = 1.26
            screen_position = 60  # 屏幕位置
            scale_horizontal = 200E-6  # 时基参数

            log.log("设置时基")
            com = Component_SIPTiming("interface_set_horizontal_scale")
            com.instrName = instrName
            com.scale_horizontal = scale_horizontal
            result1 = http_service.post_message(com)

            log.log("设置触发类型")
            com = Component_SIPTiming("interface_set_trigger")
            com.instrName = instrName
            com.trigger_type = trigger_type
            com.trigger_ch = trigger_ch
            com.trigger_level = trigger_level
            com.trigger_delay = trigger_delay
            result2 = http_service.post_message(com)

            log.log("关闭水平延迟功能")
            com = Component_SIPTiming("interface_horizontal_delay_state")
            com.instrName = instrName
            com.state = "OFF"
            result3 = http_service.post_message(com)

            log.log("设置触发位置")
            com = Component_SIPTiming("interface_set_horizontal_position")
            com.instrName = instrName
            com.position_horizontal = screen_position
            result4 = http_service.post_message(com)

            log.log("设置触发模式")
            com = Component_SIPTiming("interface_set_trigger_mode")
            com.instrName = instrName
            com.acquire_type = acquire_type
            result5 = http_service.post_message(com)

            log.log("示波器开始采集数据")
            com = Component_SIPTiming("interface_start_acquisitions")
            com.instrName = instrName
            result6 = http_service.post_message(com)

            log.log("等待波形触发")
            time.sleep(20)

            flag = message_box.askyesno('波形确认', '请确认下电时序波形是否正确？')
            if flag:
                log.log("设置 VSIM 通道的搜索条件(下降沿数据)，并返回搜索值")
                com = Component_SIPTiming("interface_set_search")
                com.instrName = instrName
                com.search_ch = search_ch1
                com.search_type = search_type1_F
                com.search_level = search_level1_F
                mark_position1 = http_service.post_message(com)
                if mark_position1['query'][:4] == 'NONE':
                    log.fail("VSIM 通道的搜索返回值为空")
                    sys.exit()

                log.log("设置 CLK 通道的搜索条件（触发沿数据），并返回搜索值")
                path = f"E:\\test1\\test2.csv"
                com = Component("interface_data_caul")
                com.instrName = instrName
                com.ch = search_ch2
                com.save_path = path
                Path_result = http_service.post_message(com)

                log.log("设置 RST 通道的搜索条件，并返回搜索值")
                com = Component_SIPTiming("interface_set_search")
                com.instrName = instrName
                com.search_ch = search_ch3
                com.search_type = search_type3_F
                com.search_level = search_level3_F
                mark_position3 = http_service.post_message(com)
                if mark_position3['query'][:4] == 'NONE':
                    log.fail("RST 通道的搜索返回值为空")
                    sys.exit()

                log.log("设置 IO 通道的搜索条件，并返回搜索值")
                com = Component_SIPTiming("interface_set_search")
                com.instrName = instrName
                com.search_ch = search_ch4
                com.search_type = search_type4_F
                com.search_level = search_level4_F
                mark_position4 = http_service.post_message(com)
                if mark_position4['query'][:4] == 'NONE':
                    log.fail("IO 通道的搜索返回值为空")
                    sys.exit()

                # 截取各个通道的第一个触发数据
                if ";" in mark_position1['query']:
                    mark_position1['query'] = (mark_position1['query'][:mark_position1['query'].index(';')])
                if ";" in mark_position3['query']:
                    mark_position3['query'] = (mark_position3['query'][:mark_position3['query'].index(';')])
                if ";" in mark_position4['query']:
                    mark_position4['query'] = (mark_position4['query'][:mark_position4['query'].index(';')])

                    com = Component("interface_secondpoint")
                    com.querylist = mark_position1['query']
                    mark_position_b = http_service.post_message(com)

                log.log("计算光标的位置坐标")
                mark_position_str = mark_position1['query'] + ';' + mark_position3['query'] + ';' + mark_position4[
                    'query'] + ';'
                com = Component("interface_position_client")
                com.instrName = instrName
                com.position_str = mark_position_str
                position_return = http_service.post_message(com)

                horizontal_position_a = float(position_return['position_a'])  # SIM光标垂直位置
                com = Component("interface_latepoint")
                com.save_path = path
                horizontal_position_b = http_service.post_message(com)  # CLK光标垂直位置
                horizontal_position_c = float(position_return['position_b'])  # RST光标垂直位置
                horizontal_position_d = float(position_return['position_c'])  # IO光标垂直位置

                test_result['下电时序VSIM位置：'] = horizontal_position_a
                test_result['下电时序CLK位置'] = horizontal_position_b
                test_result['下电时序RST位置'] = horizontal_position_c
                test_result['下电时序IO位置'] = horizontal_position_d

                if horizontal_position_c < horizontal_position_b < horizontal_position_d < horizontal_position_a:
                    test_result["Power_Down"] = True
                    TestResult = "下电时序测试结果：Pass"
                    log.log(TestResult)
                else:
                    test_result["Power_Down"] = False
                    TestResult = "下电时序测试结果：Fail"
                    log.log(TestResult)

                flag = message_box.askyesno('示波器截图', '请确认是否保存当前波形图片？')
                if flag:
                    # 约定PngPaths键名，存储图像列表
                    file_name = pic_path + test_name + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + '.png'
                    com = Component_SIPTiming("interface_save_screen")
                    com.instrName = instrName
                    com.file_name = file_name
                    result14 = http_service.post_message(com)
                    test_result['PngPaths'].append(result14['filename'])
                    log.log(str(test_result))
            else:
                pass

        # ------------------------------------------------------SIM卡class检测延时时序-------------------------------------------------------------
        """1.设置示波器 ———— 2.获取各通道波形 ———— 3.将通道波形连接为str给server ———— 4.显示光标水平位置获取延实间隔 ———— 5.判断间隔大小 ———— 6.截图保存波形"""
        if SIMCardTest == "class检测延时":
            trigger_type = 'RISE'
            trigger_ch = 'CH1'
            trigger_level = 1.5
            trigger_delay = 0.1
            position_horizontal1 = 2.26
            position_horizontal2 = 1.26

            screen_position = 20  # 屏幕位置
            scale_horizontal = 400E-3  # 时基参数

            log.log("设置时基")
            com = Component_SIPTiming("interface_set_horizontal_scale")
            com.instrName = instrName
            com.scale_horizontal = scale_horizontal
            result1 = http_service.post_message(com)

            log.log("设置触发类型")
            com = Component_SIPTiming("interface_set_trigger")
            com.instrName = instrName
            com.trigger_type = trigger_type
            com.trigger_ch = trigger_ch
            com.trigger_level = trigger_level
            com.trigger_delay = trigger_delay
            result2 = http_service.post_message(com)

            log.log("关闭水平延迟功能")
            com = Component_SIPTiming("interface_horizontal_delay_state")
            com.instrName = instrName
            com.state = "OFF"
            result3 = http_service.post_message(com)

            log.log("设置触发位置")
            com = Component_SIPTiming("interface_set_horizontal_position")
            com.instrName = instrName
            com.position_horizontal = screen_position
            result4 = http_service.post_message(com)

            log.log("设置触发类型")
            com = Component_SIPTiming("interface_set_trigger")
            com.instrName = instrName
            com.trigger_type = trigger_type
            com.trigger_ch = trigger_ch
            com.trigger_level = trigger_level
            com.trigger_delay = trigger_delay
            result6 = http_service.post_message(com)

            log.log("设置触发模式")
            com = Component_SIPTiming("interface_set_trigger_mode")
            com.instrName = instrName
            com.acquire_type = acquire_type
            result7 = http_service.post_message(com)

            log.log("示波器开始采集数据")
            com = Component_SIPTiming("interface_start_acquisitions")
            com.instrName = instrName
            result8 = http_service.post_message(com)

            log.log("等待波形触发")
            time.sleep(20)

            flag = message_box.askyesno('波形确认', '请确认class延时时序波形是否正确？')
            if flag:
                log.log("设置 VSIM 通道的搜索条件，并返回搜索值")
                com = Component_SIPTiming("interface_set_search")
                com.instrName = instrName
                com.search_ch = search_ch1
                com.search_type = search_type1_F
                com.search_level = search_level1_F
                mark_position1 = http_service.post_message(com)
                if mark_position1['query'][:4] == 'NONE':
                    log.fail("CLK 通道的搜索返回值为空")
                    sys.exit()

                log.log("设置 RST 通道的搜索条件，并返回搜索值")
                com = Component_SIPTiming("interface_set_search")
                com.instrName = instrName
                com.search_ch = search_ch1
                com.search_type = search_type1_R
                com.search_level = search_level1_R
                mark_position2 = http_service.post_message(com)
                if mark_position2['query'][:4] == 'NONE':
                    log.fail("RST 通道的搜索返回值为空")
                    sys.exit()

                # 截取各个通道的第一个触发数据
                if ";" in mark_position1['query']:
                    mark_position1['query'] = (mark_position1['query'][:mark_position1['query'].index(';')])
                if ";" in mark_position2['query']:
                    com = Component("interface_secondpoint")
                    com.querylist = mark_position2['query']
                    mark_position2['query'] = http_service.post_message(com)

                log.log("计算光标的位置坐标")
                mark_position_str = mark_position1['query'] + ';' + mark_position2['query'] + ';'
                com = Component("interface_position_client")
                com.instrName = instrName
                com.position_str = mark_position_str
                position_return = http_service.post_message(com)

                horizontal_position_a = float(position_return['position_a'])  # CLK第一个下降沿光标垂直位置
                horizontal_position_b = float(position_return['position_b'])  # CLK第二个上升沿光标垂直位置

                log.log("获取class延时间隔并判断是否满足协议")

                log.log("开启zoom放大波形")
                com = Component("interface_adjust_scale")
                com.instrName = instrName
                com.pos_a = horizontal_position_a
                com.pos_b = horizontal_position_b
                com.siterate = True
                res = http_service.post_message(com)

                com = Component("interface_set_simcursor")
                com.instrName = instrName
                com.cursor_source = "CH3"
                com.position_horizontal1 = 0
                com.position_horizontal2 = 0
                com.position1 = horizontal_position_a
                com.position2 = horizontal_position_b
                cursor_return = http_service.post_message(com)

                delta = float(cursor_return['delta'])
                result = bool(delta > 0.01)
                if result:
                    test_result["ClassDaley"] = True
                    TestResult = "测试结果：Pass，class时延间隔：" + str(cursor_return['delta']) + "s"
                    log.log(TestResult)
                else:
                    test_result["ClassDaley"] = False
                    TestResult = "测试结果：Fail，class时延间隔：" + str(cursor_return['delta']) + "s"
                    log.log(TestResult)

                flag = message_box.askyesno('示波器截图', '请确认是否保存当前波形图片？')
                if flag:
                    # 约定PngPaths键名，存储图像列表
                    file_name = pic_path + test_name + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + '.png'
                    com = Component_SIPTiming("interface_save_screen")
                    com.instrName = instrName
                    com.file_name = file_name
                    result14 = http_service.post_message(com)
                    test_result['PngPaths'].append(result14['filename'])
                    log.log(str(test_result))
            else:
                pass

        # ------------------------------------------------------待机状态下SIM卡查询时序-------------------------------------------------------------
        """1.设置示波器 ———— 2.获取各通道波形 ———— 3.将通道波形连接为str给server ———— 4.显示光标水平位置获取SIM卡查询间隔 ———— 5.截图保存波形"""
        if SIMCardTest == "SIM卡查询时序":
            trigger_type = 'RISE'
            trigger_ch = 'CH2'
            trigger_level = 0.9
            trigger_delay = 10E-3
            position_horizontal1 = 2.26
            position_horizontal2 = 1.26

            screen_position = 15  # 屏幕位置
            scale_horizontal = 4  # 时基参数

            log.log("设置时基")
            com = Component_SIPTiming("interface_set_horizontal_scale")
            com.instrName = instrName
            com.scale_horizontal = scale_horizontal
            result1 = http_service.post_message(com)

            log.log("设置触发类型")
            com = Component_SIPTiming("interface_set_trigger")
            com.instrName = instrName
            com.trigger_type = trigger_type
            com.trigger_ch = trigger_ch
            com.trigger_level = trigger_level
            com.trigger_delay = trigger_delay
            result2 = http_service.post_message(com)

            log.log("关闭水平延迟功能")
            com = Component_SIPTiming("interface_horizontal_delay_state")
            com.instrName = instrName
            com.state = "OFF"
            result3 = http_service.post_message(com)

            log.log("设置触发位置")
            com = Component_SIPTiming("interface_set_horizontal_position")
            com.instrName = instrName
            com.position_horizontal = screen_position
            result4 = http_service.post_message(com)

            log.log("设置触发类型")
            com = Component_SIPTiming("interface_set_trigger")
            com.instrName = instrName
            com.trigger_type = trigger_type
            com.trigger_ch = trigger_ch
            com.trigger_level = trigger_level
            com.trigger_delay = trigger_delay
            result6 = http_service.post_message(com)

            log.log("设置触发模式")
            com = Component_SIPTiming("interface_set_trigger_mode")
            com.instrName = instrName
            com.acquire_type = acquire_type
            result7 = http_service.post_message(com)

            log.log("示波器开始采集数据")
            com = Component_SIPTiming("interface_start_acquisitions")
            com.instrName = instrName
            result8 = http_service.post_message(com)

            log.log("等待波形触发")
            time.sleep(20)

            flag = message_box.askyesno('波形确认', '请确认SIM卡查询时序波形是否正确？')
            if flag:

                log.log("获取CLK通道的数据并存储在 test.csv ")
                path = "E:/test1/test.csv"
                com = Component("interface_data_caul")
                com.instrName = instrName
                com.ch = search_ch2
                com.save_path = path
                result9 = http_service.post_message(com)
                log.log(result9)

                log.log("CLK进行数据分析获取a、b光标的位置")
                com = Component("adjoin_twopoint")
                com.csv_path = path
                mark_position = http_service.post_message(com)

                horizontal_position_a = mark_position[0]  # CLK--a光标位置
                horizontal_position_b = mark_position[1]  # CLK--b光标位置

                log.log("获取class延时间隔并判断是否满足协议")
                com = Component("interface_set_simcursor")
                com.instrName = instrName
                com.cursor_source = "CH3"
                com.position_horizontal1 = 0
                com.position_horizontal2 = 0
                com.position1 = horizontal_position_a
                com.position2 = horizontal_position_b
                cursor_return = http_service.post_message(com)

                delta = float(cursor_return['delta'])
                TestResult = "待机状态下class时延间隔：" + str(cursor_return['delta']) + "s"
                log.log(TestResult)
                test_result['SIM_query'] = delta

                flag = message_box.askyesno('示波器截图', '请确认是否保存当前波形图片？')
                if flag:
                    # 约定PngPaths键名，存储图像列表
                    file_name = pic_path + test_name + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + '.png'
                    com = Component_SIPTiming("interface_save_screen")
                    com.instrName = instrName
                    com.file_name = file_name
                    result14 = http_service.post_message(com)
                    test_result['PngPaths'].append(result14['filename'])
                    log.log(str(test_result))

            else:
                pass

        # ----------------------------------------------------------热插拔上电时序-----------------------------------------------------------------
        """1.设置示波器 ———— 2.获取各通道波形 ———— 3.将通道波形连接为str给server ———— 4.获取光标水平位置 ———— 5.对比光标水平位置值大小判断结果 ———— 6.截图保存波形"""
        if SIMCardTest == "热插拔上电时序":
            ch_list = 'CH1,CH2,CH3,CH4'
            label_list = 'VSIM,INT,RST,IO'

            trigger_type = 'RISE'
            trigger_ch = 'CH1'
            trigger_level = 0.9
            trigger_delay = 10E-3
            position_horizontal1 = 2.26
            position_horizontal2 = 1.26
            screen_position = 70  # 屏幕位置
            scale_horizontal = 20E-3  # 时基参数

            log.log("设置通道标签和位置等")
            com = Component("interface_ch_SIMCardset")
            com.instrName = instrName
            com.ch_list = ch_list
            com.label_list = label_list
            result1 = http_service.post_message(com)

            log.log("关闭 RST 通道")
            com = Component_SIPTiming("interface_close_ch")
            com.instrName = instrName
            com.ch = close_ch3
            result2 = http_service.post_message(com)

            log.log("关闭 IO 通道")
            com = Component_SIPTiming("interface_close_ch")
            com.instrName = instrName
            com.ch = close_ch4
            result3 = http_service.post_message(com)

            log.log("设置时基")
            com = Component_SIPTiming("interface_set_horizontal_scale")
            com.instrName = instrName
            com.scale_horizontal = scale_horizontal
            result4 = http_service.post_message(com)

            log.log("设置触发类型")
            com = Component_SIPTiming("interface_set_trigger")
            com.instrName = instrName
            com.trigger_type = trigger_type
            com.trigger_ch = trigger_ch
            com.trigger_level = trigger_level
            com.trigger_delay = trigger_delay
            result5 = http_service.post_message(com)

            log.log("关闭水平延迟功能")
            com = Component_SIPTiming("interface_horizontal_delay_state")
            com.instrName = instrName
            com.state = "OFF"
            result6 = http_service.post_message(com)

            log.log("设置触发位置")
            com = Component_SIPTiming("interface_set_horizontal_position")
            com.instrName = instrName
            com.position_horizontal = screen_position
            result7 = http_service.post_message(com)

            log.log("设置触发类型")
            com = Component_SIPTiming("interface_set_trigger")
            com.instrName = instrName
            com.trigger_type = trigger_type
            com.trigger_ch = trigger_ch
            com.trigger_level = trigger_level
            com.trigger_delay = trigger_delay
            result8 = http_service.post_message(com)

            log.log("设置触发模式")
            com = Component_SIPTiming("interface_set_trigger_mode")
            com.instrName = instrName
            com.acquire_type = acquire_type
            result9 = http_service.post_message(com)

            log.log("示波器开始采集数据")
            com = Component_SIPTiming("interface_start_acquisitions")
            com.instrName = instrName
            result10 = http_service.post_message(com)

            log.log("等待波形触发")
            time.sleep(20)

            flag = message_box.askyesno('波形确认', '请确认热插拔上电时序波形是否正确？')
            if flag:
                log.log("设置 VSIM 通道的搜索条件(上升沿数据)，并返回搜索值")
                com = Component_SIPTiming("interface_set_search")
                com.instrName = instrName
                com.search_ch = search_ch1
                com.search_type = search_type1_R
                com.search_level = search_level1_R
                mark_position1 = http_service.post_message(com)
                if mark_position1['query'][:4] == 'NONE':
                    log.fail("VSIM 通道的搜索返回值为空")
                    sys.exit()

                log.log("设置 INT 通道的搜索条件(上升沿数据)，并返回搜索值")
                com = Component_SIPTiming("interface_set_search")
                com.instrName = instrName
                com.search_ch = search_ch2
                com.search_type = search_type2_R
                com.search_level = search_level2_R
                mark_position2 = http_service.post_message(com)
                if mark_position2['query'][:4] == 'NONE':
                    log.fail("INT 通道的搜索返回值为空")
                    sys.exit()

                # 截取各个通道的第一个触发数据
                if ";" in mark_position1['query']:
                    mark_position1['query'] = (mark_position1['query'][:mark_position1['query'].index(';')])
                if ";" in mark_position2['query']:
                    mark_position2['query'] = (mark_position2['query'][:mark_position2['query'].index(';')])

                log.log("计算光标的位置坐标")
                mark_position_str = mark_position1['query'] + ';' + mark_position2['query'] + ';'
                com = Component("interface_position_client")
                com.instrName = instrName
                com.position_str = mark_position_str
                position_return = http_service.post_message(com)

                horizontal_position_a = float(position_return['position_a'])  # SIM光标垂直位置
                horizontal_position_b = float(position_return['position_b'])  # INT光标垂直位置

                log.log("光标显示通道触发位置获取时间")
                com = Component("interface_set_simcursor")
                com.instrName = instrName
                com.cursor_source = "CH2"
                com.position_horizontal1 = 0
                com.position_horizontal2 = 0
                com.position1 = horizontal_position_a
                com.position2 = horizontal_position_b
                cursor_return1 = http_service.post_message(com)

                if horizontal_position_a > horizontal_position_b:
                    test_result['Hot_Power_On'] = True
                    TestResult = "热插拔下电时序判定结果：Pass,T_vsim：" + str(horizontal_position_a) + "s,T_int:" + str(
                        horizontal_position_b) + "s"
                    log.log(TestResult)
                else:
                    test_result['Hot_Power_On'] = False
                    TestResult = "热插拔下电时序判定结果：Fail,T_vsim：" + str(horizontal_position_a) + "s,T_int:" + str(
                        horizontal_position_b) + "s"
                    log.log(TestResult)

                flag = message_box.askyesno('示波器截图', '请确认是否保存当前波形图片？')
                if flag:
                    # 约定PngPaths键名，存储图像列表
                    file_name = pic_path + test_name + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + '.png'
                    com = Component_SIPTiming("interface_save_screen")
                    com.instrName = instrName
                    com.file_name = file_name
                    result14 = http_service.post_message(com)
                    test_result['PngPaths'].append(result14['filename'])
                    log.log(str(test_result))
            else:
                pass

        # ----------------------------------------------------------热插拔下电时序-----------------------------------------------------------------
        """1.设置示波器 ———— 2.获取各通道波形 ———— 3.将通道波形连接为str给server ———— 4.获取光标水平位置 ———— 5.对比光标水平位置值大小判断结果 ———— 6.截图保存波形"""
        if SIMCardTest == "热插拔下电时序":
            ch_list = 'CH1,CH2,CH3,CH4'
            label_list = 'VSIM,INT,RST,IO'

            trigger_type = 'FALL'
            trigger_ch = 'CH1'
            trigger_level = 0.9
            trigger_delay = 10E-3
            position_horizontal1 = 2.26
            position_horizontal2 = 1.26
            screen_position = 70  # 屏幕位置
            scale_horizontal = 20E-3  # 时基参数

            log.log("设置通道标签和位置等")
            com = Component("interface_ch_SIMCardset")
            com.instrName = instrName
            com.ch_list = ch_list
            com.label_list = label_list
            result1 = http_service.post_message(com)

            log.log("关闭 RST 通道")
            com = Component_SIPTiming("interface_close_ch")
            com.instrName = instrName
            com.ch = close_ch3
            result2 = http_service.post_message(com)

            log.log("关闭 IO 通道")
            com = Component_SIPTiming("interface_close_ch")
            com.instrName = instrName
            com.ch = close_ch4
            result3 = http_service.post_message(com)

            log.log("设置时基")
            com = Component_SIPTiming("interface_set_horizontal_scale")
            com.instrName = instrName
            com.scale_horizontal = scale_horizontal
            result4 = http_service.post_message(com)

            log.log("设置触发类型")
            com = Component_SIPTiming("interface_set_trigger")
            com.instrName = instrName
            com.trigger_type = trigger_type
            com.trigger_ch = trigger_ch
            com.trigger_level = trigger_level
            com.trigger_delay = trigger_delay
            result5 = http_service.post_message(com)

            log.log("关闭水平延迟功能")
            com = Component_SIPTiming("interface_horizontal_delay_state")
            com.instrName = instrName
            com.state = "OFF"
            result6 = http_service.post_message(com)

            log.log("设置触发位置")
            com = Component_SIPTiming("interface_set_horizontal_position")
            com.instrName = instrName
            com.position_horizontal = screen_position
            result7 = http_service.post_message(com)

            log.log("设置触发类型")
            com = Component_SIPTiming("interface_set_trigger")
            com.instrName = instrName
            com.trigger_type = trigger_type
            com.trigger_ch = trigger_ch
            com.trigger_level = trigger_level
            com.trigger_delay = trigger_delay
            result8 = http_service.post_message(com)

            log.log("设置触发模式")
            com = Component_SIPTiming("interface_set_trigger_mode")
            com.instrName = instrName
            com.acquire_type = acquire_type
            result9 = http_service.post_message(com)

            log.log("示波器开始采集数据")
            com = Component_SIPTiming("interface_start_acquisitions")
            com.instrName = instrName
            result10 = http_service.post_message(com)

            log.log("等待波形触发")
            time.sleep(20)

            flag = message_box.askyesno('波形确认', '请确认热插拔下电时序波形是否正确？')
            if flag:
                log.log("设置 VSIM 通道的搜索条件(下降沿数据)，并返回搜索值")
                com = Component_SIPTiming("interface_set_search")
                com.instrName = instrName
                com.search_ch = search_ch1
                com.search_type = search_type1_F
                com.search_level = search_level1_F
                mark_position1 = http_service.post_message(com)
                if mark_position1['query'][:4] == 'NONE':
                    log.fail("VSIM 通道的搜索返回值为空")
                    sys.exit()

                log.log("设置 INT 通道的搜索条件，并返回搜索值")
                com = Component_SIPTiming("interface_set_search")
                com.instrName = instrName
                com.search_ch = search_ch2
                com.search_type = search_type2_F
                com.search_level = search_level2_F
                mark_position2 = http_service.post_message(com)
                if mark_position2['query'][:4] == 'NONE':
                    log.fail("INT 通道的搜索返回值为空")
                    sys.exit()

                # 截取各个通道的第一个触发数据
                if ";" in mark_position1['query']:
                    mark_position1['query'] = (mark_position1['query'][:mark_position1['query'].index(';')])
                if ";" in mark_position2['query']:
                    mark_position2['query'] = (mark_position2['query'][:mark_position2['query'].index(';')])

                log.log("计算光标的位置坐标")
                mark_position_str = mark_position1['query'] + ';' + mark_position2['query'] + ';'
                com = Component("interface_position_client")
                com.instrName = instrName
                com.position_str = mark_position_str
                position_return = http_service.post_message(com)

                horizontal_position_a = float(position_return['position_a'])  # SIM光标垂直位置
                horizontal_position_b = float(position_return['position_b'])  # INT光标垂直位置

                log.log("光标显示通道触发位置获取时间")
                com = Component("interface_set_simcursor")
                com.instrName = instrName
                com.cursor_source = "CH2"
                com.position_horizontal1 = 0
                com.position_horizontal2 = 0
                com.position1 = horizontal_position_a
                com.position2 = horizontal_position_b
                cursor_return1 = http_service.post_message(com)

                if horizontal_position_a > horizontal_position_b:
                    test_result['Hot_Power_Down'] = True
                    TestResult = "热插拔下电时序判定结果：Pass,T_vsim：" + str(horizontal_position_a) + "s,T_int:" + str(
                        horizontal_position_b) + "s"
                    log.log(TestResult)
                else:
                    test_result['Hot_Power_Down'] = False
                    TestResult = "热插拔下电时序判定结果：Fail,T_vsim：" + str(horizontal_position_a) + "s,T_int:" + str(
                        horizontal_position_b) + "s"
                    log.log(TestResult)

                flag = message_box.askyesno('示波器截图', '请确认是否保存当前波形图片？')
                if flag:
                    # 约定PngPaths键名，存储图像列表
                    file_name = pic_path + test_name + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + '.png'
                    com = Component_SIPTiming("interface_save_screen")
                    com.instrName = instrName
                    com.file_name = file_name
                    result14 = http_service.post_message(com)
                    test_result['PngPaths'].append(result14['filename'])
                    log.log(str(test_result))
            else:
                log.fail("波形异常")
                exit()

        #  成功输出结果给到平台
        log.success(test_result)


    except Exception as err:
        log.exception(str(err))








