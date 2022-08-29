import os
from http_service import HttpService, MessageToCSharpType
import datetime
import sys
import time
import ast


# pack:功能块，如示波器，此参数不能省
# module:功能块类型，如示波器MDO3054，此参数不能省
# interface:功能块已经实现的接口，此参数不能省
# 其余参数按照实际需求进行传递


class Component(object):
    def __init__(self, interface):
        self.pack = "pack_oscilloscope"
        self.module = "module_TEKMDO3054_SPItiming"
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
        strReceive = sys.argv[1]
        log.log(strReceive)
        parameterList = ast.literal_eval(strReceive)
        log.log(parameterList)

        test_name = parameterList["test_name"]
        instrName = parameterList["instrName"]
        record_length = float(parameterList["record_length"])
        ch_list = parameterList["ch_list"]
        label_list = parameterList["label_list"]
        close_ch1 = parameterList["close_ch1"]
        close_ch2 = parameterList["close_ch2"]
        scale_horizontal = float(parameterList["scale_horizontal"])
        trigger_type = parameterList["trigger_type"]
        trigger_ch = parameterList["trigger_ch"]
        trigger_level = float(parameterList["trigger_level"])
        trigger_delay = float(parameterList["trigger_delay"])
        acquire_type = parameterList["acquire_type"]
        search_ch1 = parameterList["search_ch1"]
        search_type1 = parameterList["search_type1"]
        search_level1 = float(parameterList["search_level1"])
        search_ch2 = parameterList["search_ch2"]
        search_type2 = parameterList["search_type2"]
        search_level2 = float(parameterList["search_level2"])
        calculated_min_value = float(parameterList["calculated_min_value"])
        t_clock = float(parameterList["t_clock"])
        cursor_source = parameterList["cursor_source"]
        position_horizontal1 = float(parameterList["position_horizontal1"])
        position_horizontal2 = float(parameterList["position_horizontal2"])
        pic_path = parameterList["screenshotPath"] + "\\"
        file_name = pic_path + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + '.png'
        TestUnit = parameterList["TestUnit"]
        """
         test_name = 'tv(MISO)'
        instrName = "TCPIP::" + "169.254.4.96" + "::INSTR"
        record_length = 5E6
        ch_list = 'CH1,CH2,CH3,CH4'
        label_list = 'CS,CLK,MISO,MOSI'
        close_ch1 = "CH1"
        close_ch2 = "CH4"
        scale_horizontal = 40E-9
        trigger_type = 'FALL'
        trigger_ch = 'CH3'
        trigger_level = 0.64
        trigger_delay = 250E-9
        acquire_type = 'SEQUENCE'
        search_ch1 = 'CH2'
        search_type1 = 'RISE'
        search_level1 = 1.26
        search_ch2 = 'CH3'
        search_type2 = 'RISE'
        search_level2 = 1.26
        calculated_min_value = 0
        t_clock = 220E-9
        cursor_source = 'CH2'
        position_horizontal1 = 1.26
        position_horizontal2 = 3.26
        pic_path = "E:\\sts\\01_Code\\STS\\Debug\\Testresult\\21312\\Ver.A" + "\\Screenshot\\"
        file_name = pic_path + test_name + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + '.png'
        # test_component = 'side_fingerprint'
        TestUnit = 'side_fingerprint'
        """
        log.log("初始化示波器")
        com = Component("interface_initial")
        com.instrName = instrName
        device = http_service.post_message(com)

        log.log("设置示波器记录长度")
        com = Component("interface_set_record_length")
        com.instrName = instrName
        com.record_length = record_length
        result1 = http_service.post_message(com)

        log.log("设置通道标签和位置等")
        com = Component("interface_ch_set")
        com.instrName = instrName
        com.ch_list = ch_list
        com.label_list = label_list
        result2 = http_service.post_message(com)

        log.log("关闭通道")
        com = Component("interface_close_ch")
        com.instrName = instrName
        com.ch = close_ch1
        result3 = http_service.post_message(com)

        log.log("关闭通道")
        com = Component("interface_close_ch")
        com.instrName = instrName
        com.ch = close_ch2
        result4 = http_service.post_message(com)

        log.log("设置时基")
        com = Component("interface_set_horizontal_scale")
        com.instrName = instrName
        com.scale_horizontal = scale_horizontal
        result5 = http_service.post_message(com)

        log.log("设置触发类型")
        if (TestUnit == "NFC") & (test_name == "tv(MISO)"):
            com = Component("interface_set_trigger_pulse")
            com.instrName = instrName
            com.pulse_source = 'CH3'
            com.pulse_condition = 'LESSTHAN'
            com.pulse_width = 100E-9
            com.trigger_level = 0.5
            result6 = http_service.post_message(com)
        else:
            com = Component("interface_set_trigger")
            com.instrName = instrName
            com.trigger_type = trigger_type
            com.trigger_ch = trigger_ch
            com.trigger_level = trigger_level
            com.trigger_delay = trigger_delay
            result6 = http_service.post_message(com)

        if TestUnit == '屏下指纹':
            log.log("设置屏下指纹")
            com = Component_phone("interface_under_display_fingerprint")
            device = http_service.post_message(com)
        if TestUnit == '侧边指纹':
            log.log("设置侧边指纹")
            com = Component_phone("interface_side_fingerprint")
            device = http_service.post_message(com)
        if TestUnit == "G-sensor":
            log.log("设置G-sensor")
            com = Component_phone("interface_G_Sensor")
            device = http_service.post_message(com)
        if TestUnit == "NFC":
            log.log("设置NFC,请点击CPLC")
            com = Component_phone("interface_NFC")
            device = http_service.post_message(com)

        log.log("示波器开始采集数据")
        com = Component("interface_start_acquisitions")
        com.instrName = instrName
        result1 = http_service.post_message(com)

        log.log("设置触发模式")
        com = Component("interface_set_trigger_mode")
        com.instrName = instrName
        com.acquire_type = acquire_type
        result7 = http_service.post_message(com)

        log.log("设置测试场景")
        # 等待波形触发
        count = 0
        log.log("等待波形触发")
        while True:
            count += 1
            time.sleep(1)
            com = Component("interface_query_acquire_mode")
            com.instrName = instrName
            acquire_mode = http_service.post_message(com)
            if acquire_mode == '0\n':
                break
            if count >= 20:
                log.fail("在20s之内未能捕捉到正确的波形，请重新测试")
                sys.exit()

        log.log("设置第一个搜索通道的搜索条件，并返回搜索值")
        com = Component("interface_set_search")
        com.instrName = instrName
        com.search_ch = search_ch1
        com.search_type = search_type1
        com.search_level = search_level1
        result8 = http_service.post_message(com)
        if result8['query'][:4] == 'NONE':
            log.fail("第一个搜索通道的搜索返回值为空")
            sys.exit()

        log.log("设置第二个搜索通道的搜索条件，并返回搜索值")
        com = Component("interface_set_search")
        com.instrName = instrName
        com.search_ch = search_ch2
        com.search_type = search_type2
        com.search_level = search_level2
        result9 = http_service.post_message(com)
        if result9['query'][:4] == 'NONE':
            log.fail("第二个搜索通道的搜索返回值为空")
            sys.exit()

        log.log("计算光标的位置坐标")
        if calculated_min_value:
            com = Component("interface_timing_position1")
            com.instrName = instrName
            com.position_list1 = result8['query']
            com.position_list2 = result9['query']
        else:
            com = Component("interface_timing_position2")
            com.instrName = instrName
            com.position_list1 = result8['query']
            com.position_list2 = result9['query']
            com.t_clock = t_clock
        result10 = http_service.post_message(com)

        log.log("设置水平延迟")
        com = Component("interface_delay_horizontal")
        com.instrName = instrName
        position_a = float(result10['position_a'])
        position_b = float(result10['position_b'])
        horizontal_position = float((position_a + position_b) / 2)
        com.delay_horizontal = horizontal_position
        result11 = http_service.post_message(com)

        # if calculated_min_value:
        log.log("调整水平时基")
        com = Component("interface_set_horizontal_scale")
        com.instrName = instrName
        scale = float(abs(result10['position_a'] - result10['position_b']))
        if scale >= float(40E-9):
            new_scale = float(abs(result10['position_a'] - result10['position_b']) / 2)
            com.scale_horizontal = new_scale
        else:
            com.scale_horizontal = float(40E-9)
        result12 = http_service.post_message(com)

        log.log("设置光标位置")
        com = Component("interface_set_cursor")
        com.instrName = instrName
        com.cursor_source = cursor_source
        com.position_horizontal1 = position_horizontal1
        com.position_horizontal2 = position_horizontal2
        com.position1 = result10['position_a']
        com.position2 = result10['position_b']
        result13 = http_service.post_message(com)

        log.log("保存示波器当前屏幕波形")
        if not os.path.exists(pic_path):
            os.makedirs(pic_path)
        com = Component("interface_save_screen")
        com.instrName = instrName
        com.file_name = file_name
        result14 = http_service.post_message(com)
        test_result = {}
        test_result['test_name'] = test_name
        test_result['test_value'] = result13['delta']
        test_result['save_path'] = result14['filename']
        log.success(test_result)
    except Exception as err:
        log.exception(str(err))






