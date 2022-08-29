import time
from http_service import HttpService, MessageToCSharpType, MessageBox
import ast
import sys
# pack:功能块，如示波器，此参数不能省
# module:功能块类型，如示波器MDO3054，此参数不能省
# interface:功能块已经实现的接口，此参数不能省
# 其余参数按照实际需求进行传递


class Component(object):
    def __init__(self, interface):
        self.pack = "pack_oscilloscope"
        self.module = "module_TEKMDO3054_PowerQuality"
        self.interface = interface


log = MessageToCSharpType("")
http_service = HttpService()


# 调试脚本 【电源质量测试 -- 常一杰】
if __name__ == '__main__':
    start_time = time.time()
    BOX = MessageBox()

    # 获取时间，提供日志、图片、文件使用；
    def get_time():
        return str(time.strftime("%Y-%m-%d %H:%M:%S  ", time.localtime(time.time())))

    # 配置平台参数列表入参
    strReceive = sys.argv[1]
    # strReceive = r"{'clockchn': '', 'datachn': '', 'oscillographName': 'A019990033', 'instrName': 'TCPIP::169.254.5.85::INSTR', 'instrModel': 'Tektronix MDO3000 Series', 'prjname': '21143', 'priplat': 'MTK', 'prjver': 'Ver.A', 'signaltyp': '', 'LoopTimes': '1', 'datasignal': '', 'clksignal': '', 'expectAddress': '', 'autoTrig': 'False', 'needInitScope': 'False', 'Voltage': '1.2', 'scale_horizontal': '10E-06', 'TestCaseName': 'GSL6159N2(U321)<--GSL6159N2(U321)--ripple_wave', 'TestUnit': '侧边指纹', 'rechipname': 'GSL6159N2', 'rechipnum': 'U321', 'trchipname': 'GSL6159N2', 'trchipnum': 'U321', 'prjdescr': 'ripple_wave', 'useClkChannel': 'True', 'useDataChannel': 'True', 'testSceneName': 'WIFI/BT/GPS电源-wifi', 'DataSignalName': 'NA', 'ClkSignalName': 'NA', 'ChipAddress': '', 'loop_index': '1', 'trigger_mode': 'AUTO', 'trigger_type': 'RISE', 'vertical_scale': '10.0E-3', 'vertical_position': '-3', 'trigger_level': '3', 'acquire_type': 'RUN', 'trigger_delay': '0', 'bandwidth': '20E6', 'offset': '3', 'FALL_time': '0', 'RISE_time': '0', 'meter_list': 'MAXimum,MINImum,RMS,PK2Pk', 'test_name': 'PowerQuality（ripple）', 'Python_File_Name': 'Py_TEKMDO3054_PowerQuality.py', 'screenshotPath': 'D:\\changyijie\\STS\\sts\\01_Code\\STS\\Debug\\Testresult\\21143\\Ver.A'}"
    # strReceive = r"{'clockchn': '', 'datachn': '', 'oscillographName': 'A019990033', 'instrName': 'TCPIP::169.254.5.85::INSTR'," \
    #              r"'instrModel': 'Tektronix MDO3000 Series','prjname': '21143','priplat': 'MTK','prjver': 'Ver.A','signaltyp': ''," \
    #              r"'LoopTimes': '1','datasignal': '','clksignal': '','expectAddress': '','autoTrig': 'False'," \
    #              r"'needInitScope': 'False','scale_horizontal': '500.0E-06','Voltage': '1.8'," \
    #              r"'TestCaseName': '数字MIC电源下电|GSL6159N2|VIDD_ON--power_off','TestUnit': '侧边指纹','rechipname': " \
    #              r"'GSL6159N2','rechipnum': 'VIDD_ON','trchipname': 'GSL6159N2','trchipnum': 'VIDD_ON','prjdescr': 'power_off'," \
    #              r"'useClkChannel': 'True','useDataChannel': 'True','testSceneName': '数字MIC电源','DataSignalName': 'NA'," \
    #              r"'ClkSignalName': 'NA','ChipAddress': '','loop_index': '1','test_name': 'PowerQuality（FallPower）'," \
    #              r"'trigger_level': '0.9','trigger_mode': 'NORMal','vertical_scale': '-100','vertical_position': '-100'," \
    #              r"'meter_list': 'HIGH,LOW,FALL','bandwidth': 'FULL','FALL_time': '0','RISE_time': '0'," \
    #              r"'acquire_type': 'SEQUENCE','trigger_delay': '0','offset': '0','trigger_type': 'FALL'," \
    #              r"'Python_File_Name': 'Py_TEKMDO3054_PowerQuality.py','screenshotPath': 'D:\\changyijie\\STS\\sts\\01_Code\\STS\\Debug\\Testresult\\21143\\Ver.A'} "
    parameterList = ast.literal_eval(strReceive)
    log.log("INFO >>> 案例参数: {}{}{}".format("="*215, parameterList, "="*215))
    res_success = {}      # 输出结果保存字典(包含输出参数与图片)
    test_name = parameterList["test_name"]   # 'tv(MISO)'
    instrName = parameterList["instrName"]      # 从平台传入的示波器ID

    # instrName = "TCPIP::" + "169.254.5.85" + "::INSTR"  # 示波器ID
    # 上电波形
    # test_name = "test"
    # bandwidth = "FULL"  # 示波器的带宽值，指定数值或FULL
    # ch_coupling = "DC"  # 设置示波器的耦合方式，可以写死DC
    # offset = 0  # 设置示波器的偏置值
    # Voltage = 3     # 设置电压
    # scale_horizontal = 100.0E-06  # 设置示波器的水平时基
    # meter_list = ["HIGH", "LOW", "RISe"]  # 需要添加的测量项
    # vertical_position = None      # 垂直位置【使用算法计算】
    # vertical_scale = None         # 垂直刻度【使用算法计算】
    # trigger_type = "RISE"   # 设置示波器上升/下降沿类型
    # RISE_time = 0
    # FALL_time = 0
    # trigger_level = 0.9     # 设置触发电平
    # trigger_delay = 0       # 设置触发位置
    # trigger_mode = "NORMal"     # 余晖模式
    # acquire_type = "SEQUENCE"  # 触发模式
    # filePath = f"E:\\POST\\Data.csv"
    # imagePath = "E:\\POST\\image\\{}{}.png".format(test_name, get_time()[:-2].replace(":", "-"))

    # 下电波形 【还相差下电时间处理】
    # bandwidth = "FULL"  # 示波器的带宽值，指定数值或FULL
    # ch_coupling = "DC"  # 设置示波器的耦合方式，可以写死DC
    # offset = 0  # 设置示波器的偏置值
    # Voltage = 3     # 设置电压
    # scale_horizontal = 500.0E-06  # 设置示波器的水平时基
    # meter_list = ["HIGH", "LOW", "FALL"]  # 需要添加的测量项
    # vertical_position = None      # 垂直位置【使用算法计算】
    # vertical_scale = None         # 垂直刻度【使用算法计算】
    # trigger_type = "FALL"   # 设置示波器上升/下降沿类型
    # trigger_level = 0.9     # 设置触发电平
    # trigger_delay = 0       # 设置触发位置
    # RISE_time = 0
    # FALL_time = 0
    # trigger_mode = "NORMal"     # 余晖模式
    # acquire_type = "SEQUENCE"  # 触发模式
    # filePath = f"E:\\POST\\Data.csv"
    # imagePath = "E:\\POST\\image\\{}{}.png".format(test_name, str(time.time()).split(".")[0])

    # 纹波
    # bandwidth = 250E6  # 示波器的带宽值，指定数值或FULL（1.8V使用20.0E6）
    # ch_coupling = "DC"  # 设置示波器的耦合方式，可以写死DC
    # offset = 3  # 设置示波器的偏置值【偏执获取电压值】
    # # 需要开放调用垂直刻度、垂直位置设置
    # Voltage = 3     # 设置电压
    # scale_horizontal = 100E-09  # 设置示波器的水平时基  100ns
    # meter_list = ["MAXimum", "MINImum", "RMS", "PK2Pk"]  # 需要添加的测量项
    # vertical_position = -3       # 垂直位置 【使用算法根据电压自动计算】
    # vertical_scale = 10.0E-5    # 垂直刻度 【使用算法根据电压自动计算】
    # # 可不需要触发类参数
    # trigger_type = "RISE"   # 设置示波器上升/下降沿类型
    # trigger_level = 3     # 设置触发电平
    # trigger_delay = 0       # 设置触发位置
    # RISE_time = 0
    # FALL_time = 0
    # trigger_mode = "AUTO"
    # acquire_type = "RUN"  # 触发模式
    # filePath = f"E:\\POST\\Data.csv"
    # imagePath = "E:\\POST\\image\\{}{}.png".format(test_name, str(time.time()).split(".")[0])

    # 噪声
    # bandwidth = "FULL"  # 示波器的带宽值，指定数值或FULL
    # ch_coupling = "DC"  # 设置示波器的耦合方式，可以写死DC
    # offset = 3  # 设置示波器的偏置值
    # Voltage = 3     # 设置电压
    # scale_horizontal = 20.0E-3  # 设置示波器的水平时基（已设置好）
    # meter_list = ["HIGH", "LOW", "RMS", "PK2Pk"]  # 需要添加的测量项
    # vertical_position = -3        # 垂直位置
    # vertical_scale = 10.0E-5        # 垂直刻度
    # trigger_type = "RISE"   # 设置示波器上升/下降沿类型
    # trigger_level = 3     # 设置触发电平
    # trigger_delay = 0       # 设置触发位置
    # RISE_time = 0
    # FALL_time = 0
    # trigger_mode = "AUTO"       # 余晖模式
    # acquire_type = "RUN"  # 触发模式
    # filePath = f"E:\\POST\\Data.csv"
    # imagePath = "E:\\POST\\image\\{}{}.png".format(test_name, str(time.time()).split(".")[0])

    # """从平台端传入参数"""
    bandwidth = parameterList["bandwidth"]      # 示波器的带宽值，指定数值或FULL
    offset = float(parameterList["offset"])  # 设置示波器的偏置值
    ch_coupling = "DC"  # 设置示波器的耦合方式，可以写死DC
    Voltage = float(parameterList["Voltage"])    # 设置电压
    scale_horizontal = float(parameterList["scale_horizontal"])   # 设置示波器的水平时基（已设置好）
    meter_list = parameterList["meter_list"].split(",")  # 需要添加的测量项
    vertical_position = float(parameterList["vertical_position"])       # 垂直位置
    vertical_scale = float(parameterList["vertical_scale"])      # 垂直刻度
    trigger_type = parameterList["trigger_type"]   # 设置示波器上升/下降沿类型
    trigger_level = float(parameterList["trigger_level"])     # 设置触发电平
    trigger_delay = float(parameterList["trigger_delay"])       # 设置触发位置
    # 需要补充上下电时间要求；
    RISE_time = float(parameterList["RISE_time"])
    FALL_time = float(parameterList["FALL_time"])
    trigger_mode = parameterList["trigger_mode"]       # 余晖模式
    acquire_type = parameterList["acquire_type"]  # 触发模式
    filePath = parameterList['screenshotPath'] + "\\{}{}Data.csv".format(test_name, get_time()[:-2].replace(":", "-"))
    testSceneName = parameterList['testSceneName']
    # imagePath = parameterList['screenshotPath'] + "\\{}{}.png".format(test_name, get_time()[:-2].replace(":", "-"))
    res_success["PngPaths"] = []
    try:
        # log.log(strReceive)  平台传参
        log.log("========================================================")
        log.log(get_time() + f"INFO >>> 获取到测试场景 ： {testSceneName}")
        log.log("========================================================")

        log.log(get_time() + "INFO >>> 请将被测手机接入测试环境WIFI，并使用USB连接电脑；")

        log.log(get_time() + "INFO >>> 配置示波器波形强度显示为：100%；")
        com = Component("interface_set_display_intensity")
        com.instrName = instrName
        com.intensity = 100
        intensity = http_service.post_message(com)

        # 清除示波器历史光标信息：
        log.log(get_time() + "INFO >>> 清除示波器光标展示；")
        com = Component("interface_off_cursors")
        com.instrName = instrName
        off_cursors = http_service.post_message(com)
        log.log(get_time() + "INFO >>> 已清除示波器光标信息；")

        log.log(get_time() + "INFO >>> 初始化示波器")
        com = Component("interface_initial")
        com.instrName = instrName
        device = http_service.post_message(com)

        # 打开示波器1通道
        log.log(get_time() + "INFO >>> 正在打开示波器1通道；")
        com = Component("interface_open_ch")
        com.instrName = instrName
        result = http_service.post_message(com)
        log.log(get_time() + "INFO >>> 示波器1通道已开启；")

        # 关闭示波器其他通道
        log.log(get_time() + "INFO >>> 正在关闭2、3、4通道；")
        com = Component("interface_close_ch")
        com.instrName = instrName
        result1 = http_service.post_message(com)
        log.log(get_time() + "INFO >>> 示波器2、3、4通道已关闭；")

        # 设置示波器全带宽
        log.log(get_time() + f"INFO >>> 正在设置示波器带宽为：{bandwidth}；")
        com = Component("interface_set_bandwidth")
        com.instrName = instrName
        com.bandwidth = bandwidth
        result2 = http_service.post_message(com)
        log.log(get_time() + f"INFO >>> 示波器带宽已设置为：{bandwidth}；")

        # 设置示波器记录长度
        log.log(get_time() + f"INFO >>> 正在设置示波器长度为：{'5M'}；")
        com = Component("interface_set_record_length")
        com.instrName = instrName
        result3 = http_service.post_message(com)
        log.log(get_time() + f"INFO >>> 示波器长度已设置为：{'5M'}；")

        # 设置示波器耦合方式
        log.log(get_time() + f"INFO >>> 正在设置示波器耦合方式为：{ch_coupling}；")
        com = Component("interface_set_coupling")
        com.instrName = instrName
        com.ch_coupling = ch_coupling
        result4 = http_service.post_message(com)
        log.log(get_time() + f"INFO >>> 示波器耦合方式已设置为：{ch_coupling}；")

        # 设置示波器通道标签名
        log.log(get_time() + "INFO >>> 正在设置示波器通道名称为：VDD；")
        com = Component("interface_set_channel_label")
        com.instrName = instrName
        com.name = parameterList["rechipnum"]
        result5 = http_service.post_message(com)
        log.log(get_time() + "INFO >>> 示波器通道名称已设置为：VDD；")

        # 设置示波器偏置==================================================================================================
        log.log(get_time() + "INFO >>> 正在设置示波器的偏置值；")
        com = Component("interface_set_offset")
        com.instrName = instrName
        com.offset = 0
        if trigger_mode == "NORMal":
            com.offset = 0
        elif trigger_mode == "AUTO":
            com.offset = Voltage
        result6 = http_service.post_message(com)
        log.log(get_time() + f"INFO >>> 示波器的偏置值已设置为：{str(com.offset)}；")

        # 适配示波器垂直刻度（使用算法计算）
        if trigger_mode == "NORMal":
            log.log(get_time() + "INFO >>> 正在自动适配示波器垂直刻度、垂直位置；")
            com = Component("interface_set_scale")
            com.instrName = instrName
            com.Voltage = Voltage
            result7 = http_service.post_message(com)
            log.log(get_time() + f"INFO >>> 示波器的垂直刻度已设置为：{result7[0]}，垂直位置已设置为：{result7[1]}；")

        # 设置示波器水平时基===============================================================================================
        log.log(get_time() + f"INFO >>> 正在设置示波器的水平时基为：{scale_horizontal}；")
        com = Component("interface_set_horizontal_scale")
        com.instrName = instrName
        com.scale_horizontal = scale_horizontal
        result9 = http_service.post_message(com)
        log.log(get_time() + f"INFO >>> 示波器的水平时基已设置为：{scale_horizontal}；")

        # 清除测量项
        log.log(get_time() + "INFO >>> 正在清除历史测量项信息；")
        com = Component("interface_clear_Measure_type")
        com.instrName = instrName
        clear = http_service.post_message(com)
        log.log(get_time() + "INFO >>> 历史测量项信息已清除；")

        # 添加测量项
        com = Component("interface_change_time_set")
        for i in range(len(meter_list)):
            com.instrName = instrName
            log.log(get_time() + f"INFO >>> 正在设置添加测量项：{meter_list[i]}；")
            com.change_type = meter_list[i]
            com.source_num = i+1
            result10 = http_service.post_message(com)
            log.log(get_time() + f"INFO >>> 已完成测量项{meter_list[i]}的添加；")
        log.log(get_time() + "INFO >>> 添加测量项已完成！")

        # 依据是否进行余晖进行判断（AUTO为余晖模式，NORMal为正常模式）
        if trigger_mode == "AUTO":
            log.log(get_time() + "INFO >>> 正在开启余晖模式：AUTO；")
            com = Component('interface_set_afterglow_mode')
            com.instrName = instrName
            com.mode = "AUTO"
            result14 = http_service.post_message(com)
            log.log(get_time() + "INFO >>> 触发模式已强制自动切换到RUNSTOP模式；")
            acquire_type = "RUNSTOP"        # 如果是需要开启余晖，强制把采集模式设置成RUNSTOP；

            # 设置偏执
            log.log(get_time() + f"INFO >>> 正在设置偏执为：{Voltage}；")
            com = Component("interface_set_offset")
            com.instrName = instrName
            com.offset = Voltage
            result15 = http_service.post_message(com)
            log.log(get_time() + f"INFO >>> 偏执已设置为：{Voltage}")

            # 设置垂直刻度
            log.log(get_time() + f"INFO >>> 正在设置初始垂直刻度；")
            com = Component("interface_par_set_scale")
            com.instrName = instrName
            com.vertical_scale = 500E-3
            result16 = http_service.post_message(com)
            log.log(get_time() + f"INFO >>> 初始垂直刻度已设置为：500E-3；")

            # 参数设置垂直位置
            log.log(get_time() + f"INFO >>> 正在调整垂直位置：{0-(Voltage/2)}；")
            com = Component("interface_set_position")
            com.instrName = instrName
            com.vertical_position = (0-(Voltage/2))
            result17 = http_service.post_message(com)
            log.log(get_time() + f"INFO >>> 示波器垂直位置已设置为：{0-(Voltage/2)}；")

        elif trigger_mode == "NORMal":
            log.log(get_time() + "INFO >>> 正在开启余晖模式：NORMal（正常）；")
            com = Component('interface_set_afterglow_mode')
            com.instrName = instrName
            com.mode = "NORMal"
            result14 = http_service.post_message(com)
            log.log(get_time() + "INFO >>> 已开启余晖模式：NORMal（正常）；")

            # 设置示波器触发类型
            log.log(get_time() + "INFO >>> 正在设置示波器触发类型；")
            com = Component("interface_set_trigger")
            com.instrName = instrName
            com.trigger_type = trigger_type
            com.trigger_level = trigger_level
            com.trigger_delay = trigger_delay
            result11 = http_service.post_message(com)
            log.log(get_time() + f"INFO >>> 示波器的触发边沿为：{trigger_type}，触发电平为：{trigger_level}，触发位置为：{trigger_delay}；")

        # 设置示波器的触发模式
        log.log(get_time() + f"INFO >>> 正在设置示波器触发模式为：{acquire_type}；")
        com = Component("interface_set_trigger_mode")
        com.instrName = instrName
        com.acquire_type = acquire_type
        result12 = http_service.post_message(com)
        log.log(get_time() + f"INFO >>> 示波器的触发模式被设置为：{acquire_type}；")

        # =======================================场景控制========================================================
        # com = Component("get_scene")  # 操作场景（人为配合部分）
        # com.item = "artificial"
        # com.scene = str(testSceneName)
        # res_reboot = http_service.post_message(com)
        # if res_reboot != '未查询到对应的测试场景！':
        #     BOX.showinfo("系统提示", f"{res_reboot} 后确认执行")
        # elif res_reboot == "未查询到对应的测试场景！":
        #     log.log(get_time() + "WARNING >>> 人为配合部分：未查询到对应的测试场景！")

        # com = Component("get_scene")  # 操作场景（程序控制部分）
        # com.item = "procedure"
        # com.scene = str(testSceneName)
        # res_reboot = http_service.post_message(com)
        # log.log(get_time() + f"INFO >>> 需要执行场景对象名称：{res_reboot}")
        # if res_reboot != '未查询到对应的测试场景！':
        #     run_test = Component("interfaces_run_test_scene")  # 执行测试
        #     run_test.scene_name = res_reboot
        #     log.log(get_time() + f"INFO >>> 开始执行场景{res_reboot}，将对手机进行控制，在提示出现之前，请不要操作手机！")
        #     log.log(get_time() + "INFO >>> 正在执行控制手机，因手机控制框架原因，过程可能较慢，请耐心等待！")
        #     run_scene = http_service.post_message(run_test)
        #     if run_scene is not None and "请" in run_scene:
        #         BOX.showinfo("系统提示", f"开发过程缺少调试机型，该场景暂未开发。 暂时{run_scene}后点击“确定”，并与开发人员反馈！")
        # elif res_reboot == "未查询到对应的测试场景！":
        #     log.log(get_time() + "WARNING >>> 程序控制部分：未查询到对应的测试场景！")
        #     # BOX.showinfo("系统提示", f"{res_reboot}")
        # log.log(get_time() + "INFO >>> 程序控制执行完成！")
        # log.log(get_time() + f"INFO >>> 场景控制操作完成；")

        # 提示手动操作到测试场景
        BOX.showinfo("系统提示", f"请手动操作手机到对应的测试场景“{testSceneName}”后，点击确定！")
        # =======================================场景控制========================================================

        if trigger_mode == "NORMal":
            log.log(get_time() + "INFO >>> 开始进入测试场景（部分场景需要人工配合，请注意提示信息）；")
            # 检查手机连接状态(原方案不断检测手机连接状态，效率过慢；  只要设备上电、示波器采集到数据便判定生效)
            log.log(get_time() + "INFO >>> 正在检测波形触发，请保持接触笔勿动！")
            com = Component("interface_query_acquire_mode")
            com.instrName = instrName
            check_acquire_mode = http_service.post_message(com)
            if check_acquire_mode == 0:
                log.log(get_time() + "INFO >>> 已采取到波形数据，探头可以移开！")
            elif check_acquire_mode == "ERROR":
                log.exception(get_time() + "ERROR >>> 在50秒内未采集到波形数据，请检查连接正确！")

        # 如果是余晖模式，采集5S停止（变更需求，停止权限开放）；
        if trigger_mode == "AUTO":
            log.log(get_time() + "INFO >>> 当前处于波形积累检查模式，将持续采集波形！")
            time.sleep(5)
            com = Component("interface_set_acquisitions_stop")     # 停止示波器采集
            com.instrName = instrName
            stop = http_service.post_message(com)
            # stop_acquisitions = BOX.askokcancel("系统提示", "首次抓取纹波/噪声数据，非正式数据，合适位置按下确认；")
            # if stop_acquisitions is True:
            #     com = Component("interface_set_acquisitions_stop")     # 停止示波器采集
            #     com.instrName = instrName
            #     stop = http_service.post_message(com)

# 在此检查波形展示
        result14 = None
        if trigger_mode == "NORMal":    # 上升或者下降触发
            log.log(get_time() + "INFO >>> 正在获取测量项的测量值！")
            com = Component("interface_get_MEASUrement_data")
            com.instrName = instrName
            com.MEASUrement_type = meter_list
            time.sleep(3)  # 等待示波器计算结果
            result14 = http_service.post_message(com)

            set_time_list = [1E-9, 2E-9, 4E-9, 10E-9, 20E-9, 40E-9, 100E-9, 200E-9, 400E-9,     # 纳秒级别
                             1E-6, 2E-6, 4E-6, 10E-6, 20E-6, 40E-6, 100E-6, 200E-6, 400E-6, 800E-6,     # 微秒级别
                             2E-3, 4E-3, 10E-3, 20E-3, 40E-3, 100E-3, 200E-3, 400E-3,       # 毫秒级别
                             1, 2, 4, 10, 20, 40, 100, 200, 400, 1000]      # 秒级别
            time_temp = {"FALL": 'FALL', 'RISe': "RISE"}
            if (result14['LOW']*1000) > (Voltage*1000)*0.02:        # 阈值为工作电压的5%
                log.log(get_time() + f"INFO >>> 检查波形展示不正确，需要重新修正水平时基后重新触发波形！")
                log.log(get_time() + f"INFO >>> 上次设置的水平时基为：{scale_horizontal}；")
                # 重新放大设置水平时基
                log.log(get_time() + "INFO >>> 将展开放大默认水平时基为：40E-3")
                com = Component("interface_set_horizontal_scale")
                com.instrName = instrName
                com.scale_horizontal = 40E-3
                result9 = http_service.post_message(com)
                log.log(get_time() + f"INFO >>> 示波器的水平时基已设置为：40E-3")

                # 再次触发
                log.log(get_time() + f"INFO >>> 正在设置示波器触发模式为：{acquire_type}；")
                com = Component("interface_set_trigger_mode")
                com.instrName = instrName
                com.acquire_type = acquire_type
                result12 = http_service.post_message(com)
                log.log(get_time() + f"INFO >>> 示波器的触发模式被设置为：{acquire_type}；")
                BOX.showinfo("系统提示", "检测到波形展示不正确，请再次操作场景触发波形后，点击确定！")

                # 重新获取测量值
                com = Component("interface_get_MEASUrement_data")
                com.instrName = instrName
                com.MEASUrement_type = meter_list
                time.sleep(3)  # 等待示波器计算结果
                result14 = http_service.post_message(com)
                log.log(get_time() + f"INFO >>> 已获取{meter_list[-1]}时间为：{result14[meter_list[-1]]}")

                # 重新设置水平时基
                set_time_index = 0
                for set_time in set_time_list:
                    if set_time*2 >= result14[meter_list[-1]] <= set_time*3:
                        set_time_index = set_time_list.index(set_time)
                        break
                log.log(get_time() + f"INFO >>> 调整设置水平时基为：{set_time_list[set_time_index]}")
                com = Component("interface_set_horizontal_scale")
                com.instrName = instrName
                com.scale_horizontal = set_time_list[set_time_index]
                result9 = http_service.post_message(com)
                log.log(get_time() + f"INFO >>> 示波器的水平时基已设置为：{set_time_list[set_time_index]}")

            else:
                # 重新获取测量值
                com = Component("interface_get_MEASUrement_data")
                com.instrName = instrName
                com.MEASUrement_type = meter_list
                time.sleep(3)  # 等待示波器计算结果
                result14 = http_service.post_message(com)
                log.log(get_time() + f"INFO >>> 已获取{meter_list[-1]}时间为：{result14[meter_list[-1]]}")

                # 重新设置水平时基
                set_time_index = 0
                for set_time in set_time_list:
                    if set_time * 2 >= result14[meter_list[-1]] <= set_time * 3:
                        set_time_index = set_time_list.index(set_time)
                        break
                log.log(get_time() + f"INFO >>> 调整设置水平时基为：{set_time_list[set_time_index]}")
                com = Component("interface_set_horizontal_scale")
                com.instrName = instrName
                com.scale_horizontal = set_time_list[set_time_index]
                result9 = http_service.post_message(com)
                log.log(get_time() + f"INFO >>> 示波器的水平时基已设置为：{set_time_list[set_time_index]}")

        elif trigger_mode == "AUTO":    # 滚动余晖模式
            log.log(get_time() + "INFO >>> 正在获取测量项的测量值！")
            com = Component("interface_get_MEASUrement_data")
            com.instrName = instrName
            com.MEASUrement_type = meter_list
            # time.sleep(10)  # 等待示波器计算结果
            for i in range(10):
                time.sleep(1)
                i += 1
                result14 = http_service.post_message(com)
                if result14["MAXimum"] != 9.91E+37:
                    break

            # 修正垂直刻度
            log.log(get_time() + f"INFO >>> 正在修正垂直刻度：{vertical_scale}；")
            com = Component("interface_par_set_scale")
            com.instrName = instrName
            com.vertical_scale = vertical_scale
            result16 = http_service.post_message(com)
            log.log(get_time() + f"INFO >>> 已修正垂直刻度：{vertical_scale}；")

            # 修正偏置
            log.log(get_time() + "INFO >>> 正在修正示波器的偏置值；")
            com = Component("interface_set_offset")
            com.instrName = instrName
            com.offset = result14["RMS"]
            result6 = http_service.post_message(com)
            log.log(get_time() + f"INFO >>> 示波器的偏置值已修正为：{str(result14['RMS'])}；")

            # 修改水平位置
            log.log(get_time() + f"INFO >>> 重新修正垂直位置：{str(result14['RMS'])}；")
            com = Component("interface_set_position")
            com.instrName = instrName
            com.vertical_position = result14['RMS']
            result17 = http_service.post_message(com)
            log.log(get_time() + f"INFO >>> 示波器垂直位置已修正为：{str(result14['RMS'])}；")

            # 设置触发模式
            log.log(get_time() + f"INFO >>> 正在设置示波器触发模式为：{acquire_type}；")
            com = Component("interface_set_trigger_mode")
            com.instrName = instrName
            com.acquire_type = acquire_type
            result12 = http_service.post_message(com)
            log.log(get_time() + f"INFO >>> 示波器的触发模式被设置为：{acquire_type}；")

            BOX.showinfo("系统提示", "请再次触发波形后，点击确定！")
            log.log(get_time() + "INFO >>> 当前处于波形积累检查模式，将持续采集波形！")
            stop_acquisitions = BOX.askokcancel("系统提示", "请抓取合适波形后，点击确定；")
            if stop_acquisitions is True:
                com = Component("interface_set_acquisitions_stop")     # 停止示波器采集
                com.instrName = instrName
                stop = http_service.post_message(com)

            # 重新再抓取测量项
            log.log(get_time() + "INFO >>> 重新抓取测量项的测量值！")
            com = Component("interface_get_MEASUrement_data")
            com.instrName = instrName
            com.MEASUrement_type = meter_list
            for i in range(10):
                time.sleep(1)
                i += 1
                result14 = http_service.post_message(com)
                if result14["MAXimum"] != 9.91E+37:
                    break

# 在此检查波形展示

        if trigger_mode == "NORMal":
            log.log(get_time() + f"INFO >>> 已获取测量项的高电平为：{str(result14['HIGH'])}，低电平为：{str(result14['LOW'])}。")
        elif trigger_mode == "AUTO":    # 如果是纹波/噪声模式，获取测量项为最大、最小；
            log.log(get_time() + f"INFO >>> 已获取测量项的最大值为：{str(result14['MAXimum'])}，最小值为：{str(result14['MINImum'])}。")
        res_success = result14

        # 抓取波纹数据
        if trigger_mode == "NORMal":
            log.log(get_time() + "INFO >>> 开始抓取数据！")
            com = Component("interface_data_caul")
            com.instrName = instrName
            com.save_path = filePath
            com.low_v = str(result14["LOW"])
            com.high_v = str(result14["HIGH"])
            result13 = http_service.post_message(com)
            log.log(get_time() + "INFO >>> 数据抓取完成，请等待分析！")

        if trigger_mode == "NORMal":
            # 获取上升/下降位置；
            log.log(get_time() + "INFO >>> 开始计算波形上升/下降位置！")
            time_request = None
            if trigger_type == "RISE":
                rise_time = Component("interface_get_RiseEdge")
                rise_time.save_path = filePath
                rise_time.min_per = 0.05
                rise_time.max_per = 0.95
                time_request = http_service.post_message(rise_time)
                log.log(get_time() + f"INFO >>> 已获取到上升时间：{time_request}")

            elif trigger_type == "FALL":
                fall_time = Component("interface_get_FallEdge")
                fall_time.save_path = filePath
                fall_time.min_per = 0.05
                fall_time.max_per = 0.95
                time_request = http_service.post_message(fall_time)
                log.log(get_time() + f"INFO >>> 已获取到下降时间：{time_request}")

            # 根据时间进行设置光标
            set_cursors = Component("interface_set_simcursor")
            set_cursors.instrName = instrName
            set_cursors.cursor_source = "CH1"
            set_cursors.position_horizontal1 = time_request[0]
            set_cursors.position_horizontal2 = time_request[1]
            cursors_request = http_service.post_message(set_cursors)

            # 进行截图
            log.log(get_time() + "INFO >>> 开始保存卡光标位置图形；")
            # 保存示波器屏幕图形
            com = Component("interface_save_screen")
            com.instrName = instrName
            com.fileName = parameterList['screenshotPath'] + f"\\{test_name}{get_time()[:-2].replace(':', '-')}.png"
            image = http_service.post_message(com)
            log.log(get_time() + f"INFO >>> 图片保存成功，目标图片对象：{image}；")
            # 运行完成log.SUCCESS
            res_success["PngPaths"] = []
            res_success["PngPaths"].append(image)

            # 开始判断回勾（纹波/噪声不需要判断回勾、台阶）：
            log.log(get_time() + "INFO >>> 开始判断回勾：")
            com = Component("interface_check_back")
            com.csv_path = filePath
            com.base = str(float(result14["LOW"]))
            com.top = str(float(result14["HIGH"]))
            check_back = http_service.post_message(com)
            if len(check_back) == 0:
                log.log(get_time() + "INFO >>> 检查波形不存在回勾！")
            else:
                com = Component("interface_set_cursor")
                com.instrName = instrName
                com.position_horizontal_1 = check_back["x1"]
                com.position1 = check_back["y1"]
                com.position_horizontal_2 = check_back["x2"]
                com.position2 = check_back["y2"]
                set_cursor = http_service.post_message(com)
                res_success["back"] = str(check_back)
                log.exception(get_time() + f"ERROR >>> 判断波形存在回勾：{check_back}；")

                log.log(get_time() + "INFO >>> 开始保存波形回勾标记图形；")
                # 保存示波器屏幕图形
                com = Component("interface_save_screen")
                com.instrName = instrName
                com.fileName = parameterList['screenshotPath'] + f"\\{test_name}{get_time()[:-2].replace(':', '-')}.png"
                image = http_service.post_message(com)
                log.log(get_time() + f"INFO >>> 图片保存成功，目标图片对象：{image}；")
                # 运行完成log.SUCCESS
                res_success["PngPaths"] = []
                res_success["PngPaths"].append(image)

            # 判断台阶：
            log.log(get_time() + "INFO >>> 开始判断台阶：")
            com = Component("interface_check_step")
            com.csv_path = filePath
            com.base = float(result14["LOW"])
            com.top = float(result14["HIGH"])
            com.threshold = 0.01
            check_step = http_service.post_message(com)
            if len(check_step) == 0:
                log.log(get_time() + "INFO >>> 检查波形不存在台阶！")
            else:
                res_success["step"] = str(check_step)
                log.exception(get_time() + f"ERROR >>> 判断波形存在台阶：{check_step}；")

            # 判断上升/下降时间：
            log.log(get_time() + "INFO >>> 开始判断上升/下降时间；")
            if RISE_time > 0 or FALL_time > 0:
                if trigger_type == "RISE":      # 上升
                    if float(result14["RISe"]) <= float(RISE_time):
                        log.log(get_time() + f"INFO >>> 判断上升时间：{float(result14['RISe'])} 符合阈值要求：{RISE_time}；")
                    elif float(result14["RISe"]) > float(RISE_time):
                        log.exception(get_time() + f"ERROR >>> 判断上升时间：{float(result14['RISe'])} 不符合阈值要求：{RISE_time}；")
                elif trigger_type == "FALL":    # 下降
                    log.log(f"下降时间 = {RISE_time}")
                    if float(result14["FALL"]) <= float(FALL_time):
                        log.log(get_time() + f"INFO >>> 判断下降时间：{float(result14['FALL'])} 符合阈值要求：{FALL_time}；")
                    elif float(result14["FALL"]) > float(FALL_time):
                        log.exception(get_time() + f"ERROR >>> 判断下降时间：{float(result14['FALL'])} 不符合阈值要求：{FALL_time}；")
            else:
                log.log(get_time() + "INFO >>> 对上升/下降时间没有要求，不进行检验！")

        elif trigger_mode == "AUTO":
            time.sleep(10)
            log.log(get_time() + "INFO >>> 开始获取测量项峰峰值：")
            com = Component("interface_get_observed_value")
            com.instrName = instrName
            com.typeID = 4
            com.mold = "VALue"
            value = float(http_service.post_message(com))
            # 判断峰峰值 < 工作电压 * 0.05
            if value < (Voltage * 1000) * 0.05:
                log.log(get_time() + f"INFO >>> 获取峰峰值为：{value}，峰峰值小于均方根（工作电压）的5%：{(Voltage * 1000) * 0.05}；")
            else:
                res_success["check_PK2Pk"] = value
                log.exception(get_time() + f"ERROR >>> 获取峰峰值为：{value}，峰峰值大于均方根（工作电压）的5%：{(Voltage * 1000) * 0.05}；")

        log.log(get_time() + "INFO >>> 开始保存波形图片；")
        # 保存示波器屏幕图形
        com = Component("interface_save_screen")
        com.instrName = instrName
        com.fileName = parameterList['screenshotPath'] + f"\\{test_name}{get_time()[:-2].replace(':', '-')}.png"
        image = http_service.post_message(com)
        log.log(get_time() + f"INFO >>> 图片保存成功，目标图片对象：{image}；")
        # 运行完成log.SUCCESS
        res_success["PngPaths"] = []
        res_success["PngPaths"].append(image)

        """
        # 如果波形宽度过高，调低刻度再次保存图片
        # 垂直刻度*8 = 总高度；  高-低 = 电压差；  (总高度/3)-电压差 > 0 : 就放大一格垂直刻度
        # 垂直刻度设置量为2位数起步，  高低电压差计算为个位数，    电压差放大1000倍， 垂直刻度放大10000倍；    之后进行计算；
        """
        vertical_scale = 0 if vertical_scale is None else vertical_scale
        temp_value = float(float(vertical_scale*8)/2*1000)
        if trigger_mode == "AUTO" and temp_value-(float(result14["MAXimum"]*1000)-float(result14["MINImum"]*1000)) <= 0:
            scale_list = [10, 20, 50, 100, 200, 300, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000]
            temp_scale = scale_list[scale_list.index((float(vertical_scale)*100000))+1]
            com = Component("interface_par_set_scale")
            com.instrName = instrName
            com.vertical_scale = temp_scale/1000
            rePNG = http_service.post_message(com)

            # 再次保存截图
            log.log(get_time() + "INFO >>> 检测波形宽度较宽，放大垂直刻度，再次保存示波器屏幕图形；")
            # 保存示波器屏幕图形
            com = Component("interface_save_screen")
            com.instrName = instrName
            com.fileName = parameterList['screenshotPath'] + f"\\{test_name}{get_time()[:-2].replace(':', '-')}.png"
            image1 = http_service.post_message(com)
            log.log(get_time() + f"INFO >>> 图片保存成功，目标图片对象：{image1}；")
            res_success["PngPaths"].append(image1)

        log.success(res_success)
        log.log("INFO >>> 信号功能开发者：常一杰  工号：W9076690， 若有疑问，请及时与开发者沟通，以便充分时间给予解决！")
        end_time = time.time()
        log.log("耗费时间：" + str(float(float(end_time)-float(start_time))/60))

    except Exception as err:
        raise err
