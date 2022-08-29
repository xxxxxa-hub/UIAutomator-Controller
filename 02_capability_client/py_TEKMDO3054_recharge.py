import time
import xlwt
import pandas as pd
from http_service import HttpService, MessageToCSharpType, MessageBox
import xlrd
from xlutils.copy import copy
from openpyxl.utils import get_column_letter, column_index_from_string


# pack:功能块，如示波器，此参数不能省
# module:功能块类型，如示波器MDO3054，此参数不能省
# interface:功能块已经实现的接口，此参数不能省
# 其余参数按照实际需求进行传递


class Component(object):
    def __init__(self, interface):
        self.pack = "pack_oscilloscope"
        self.module = "module_TEKMDO3054_recharge"
        self.interface = interface


log = MessageToCSharpType("")
http_service = HttpService()

# 调试脚本 【电源质量测试 -- 常一杰】
if __name__ == '__main__':
    BOX = MessageBox()
    instrName = "TCPIP::" + "169.254.5.85" + "::INSTR"  # 示波器ID
    native = "有线普充插入-无线普充"

    # 获取时间，提供日志、图片、文件使用；
    def get_time():
        return str(time.strftime("%Y-%m-%d %H:%M:%S  ", time.localtime(time.time())))

    # 获取真值表真值标准（为结果校验使用，如无bug，请勿乱动）
    def get_check_standard(scene):
        """
        获取检查标准
        :param scene: 场景
        :return: {truth_table: [], signal_list: []} 真值表列表及信号列表
        """
        insert_param = scene.split("-")  # 测试场景=insert_param[0], 状态=insert_param[1]
        return_tup = {}
        # 操作Excel，读写真值表
        log.log(get_time() + "INFO >>> 开始调取”测试标准模板“方法，获取测试标准信息")
        excel_data = xlrd.open_workbook(r"D:\testImg\result.xls", formatting_info=True)  # 文件路径需要传参实现
        tab_sheet = excel_data.sheet_by_name("测试标准模板")  # 打开sheet页签
        log.log(get_time() + "INFO >>> 已成功打开”测试标准模板“sheet页签")

        # 获取Excel第一列内容
        cols = tab_sheet.col_values(0)  # 获取第一列内容（场景）
        start_index_init = cols.index(insert_param[0])  # 场景起始位置（1）
        cols.reverse()  # 列表暂时反转，取场景结束位置
        end_index_init = len(cols) - 1 - cols.index(insert_param[0])  # 获取场景结束位置下标（8）
        log.log(get_time() + "INFO >>> 读取”测试标准模板“第一列“场景”完成")

        # 获取Excel第二列内容
        start_index, end_index = start_index_init, end_index_init
        if len(insert_param) > 1:
            cols = tab_sheet.col_values(1)[start_index_init: end_index_init + 1]  # 获取第二列内容（场景）
            start_index = cols.index(insert_param[1]) + start_index_init  # 场景起始位置
            cols.reverse()  # 列表暂时反转，取场景结束位置
            end_index = len(cols) - 1 - cols.index(insert_param[1]) + start_index_init  # 获取场景结束位置下标
            log.log(get_time() + "INFO >>> 读取”测试标准模板“第二列“状态”完成")

        # 获取Excel第三列内容
        cols = tab_sheet.col_values(2)[start_index: end_index + 1]
        item_tup, d = {}, start_index
        for t in cols:
            item_tup[t] = d
            d += 1
        log.log(get_time() + f"INFO >>> 读取”测试标准模板“中“场景-状态”对应操作有：{item_tup.keys()}{item_tup.values()}")

        # 获取横向列名
        log.log(get_time() + "INFO >>> 开始获取列名（信号名）")
        rows = []
        for b in tab_sheet.row(0):
            rows.append(b.value)
        log.log(get_time() + f"INFO >>> 获取列名（信号名）为{rows[rows.index('触发') + 1: len(rows)]}")
        log.log(get_time() + f"INFO >>> 信号名index排列从{rows.index('触发') + 1}至{len(rows) - 1}")
        # 返回值信号列表
        return_tup["signal_list"] = rows[rows.index("触发") + 1: len(rows)]

        # 获取数据
        for x, y in item_tup.items():
            return_tup[x] = []  # 返回值：触发前真值序列，触发后真值序列
            for z in tab_sheet.row_values(y, rows.index('触发') + 1, len(rows) - 1):
                if z is "":  # 如果值出现中断，中断后续的值将不纳入
                    break
                return_tup[x].append(str(int(z)))
        return return_tup

    try:
        # log.log(strReceive)  平台传参
        # 获取场景信息
        test_case = get_check_standard(native)
        signal_list = test_case["signal_list"]  # 信号列表
        trigger_start = test_case["触发前"]  # 触发前检验标准
        trigger_end = test_case["触发后"]  # 触发后检验标准
        test_signal_list = [signal_list[s:s + 4] for s in range(0, len(signal_list), 4)]  # 需要测试的信号分组(4个一组)
        log.log(get_time() + "INFO >>> 请将被测手机接入测试环境WIFI，并使用USB连接电脑；")
        channel_list = ["CH1", "CH2", "CH3", "CH4"]
        native = native.split("-")

        # 操作Excel，读写真值表
        log.log(get_time() + "INFO >>> 开始操作Excel表格，记录真值表信息")
        excel_data = xlrd.open_workbook(r"D:\testImg\result.xls", formatting_info=True)
        tab_sheet = excel_data.sheet_by_name("测试结果")  # 打开sheet页签
        log.log(get_time() + "INFO >>> 已成功打开Excel表sheet页")
        # nrows = tab_sheet.nrows

        # 获取Excel第一列内容
        cols = tab_sheet.col_values(0)  # 获取第一列内容（场景）
        start_index_init = cols.index(native[0])  # 场景起始位置
        cols.reverse()  # 列表暂时反转，取场景结束位置
        temp_reverse = cols
        end_index_init = len(cols) - 1 - cols.index(native[0])  # 获取场景结束位置下标
        log.log(get_time() + "INFO >>> 读取Excel第一列“场景”完成")

        # 获取Excel第二列内容
        start_index, end_index = start_index_init, end_index_init
        if len(native) > 1:
            cols = tab_sheet.col_values(1)[start_index_init: end_index_init + 1]  # 获取第二列内容（场景）
            start_index = cols.index(native[1]) + start_index_init  # 场景起始位置
            cols.reverse()  # 列表暂时反转，取场景结束位置
            temp_reverse1 = cols
            end_index = len(cols) - 1 - cols.index(native[1]) + start_index_init  # 获取场景结束位置下标
            log.log(get_time() + "INFO >>> 读取Excel第二列“状态”完成")

        # 获取Excel第三列内容
        cols = tab_sheet.col_values(2)[start_index: end_index + 1]
        item_tup, k = {}, start_index
        for i in cols:
            item_tup[i] = k
            k += 1
        log.log(get_time() + f"INFO >>> 读取Excel“场景-状态”对应操作有：{item_tup.keys()}")

        # 初始化单元格
        log.log(get_time() + "INFO >>> 开始准备写入Excel操作")
        excel_file_copy = copy(excel_data)
        log.log(get_time() + "INFO >>> 正在设置单元格格式")
        write_sheet = excel_file_copy.get_sheet(0)

        # 设置单元格格式(居中)
        set_style = xlwt.XFStyle()  # 设置单元格居中格式
        al = xlwt.Alignment()
        al.horz = 0x02  # 设置水平居中
        al.vert = 0x01  # 设置垂直居中
        set_style.alignment = al

        # 设置单元格边框（实线）
        borders = xlwt.Borders()
        borders.left, borders.right, borders.top, borders.bottom = \
            xlwt.Borders.THIN, xlwt.Borders.THIN, xlwt.Borders.THIN, xlwt.Borders.THIN
        set_style.borders = borders

        # 初始化写入范围单元格
        log.log(get_time() + "INFO >>> 对需要写入的范围进行初始化")
        for key, value in item_tup.items():
            for i in (3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15):
                write_sheet.write(value, i, "——", set_style)  # 初始化表格，将被测对象表格全部填写“——”
        log.log(get_time() + "INFO >>> 范围初始化写入完成")
        excel_file_copy.save(r"D:\testImg\result.xls")

        check_result = "未检查"        # 初始默认检查结果信息
        for test_run in test_signal_list:
            label_tup = {}
            for range_num in range(0, len(test_run)):
                label_tup[test_run[range_num]] = channel_list[range_num]
            print(label_tup)

            # label_tup = {"VBUS": "CH1", "VIDT_OUT": "CH2", "WLS_CHG_IN": "CH3"}  # 标签名列表
            aisle_list = ["CH1", "CH2", "CH3", "CH4"]

            # 初始化充电板
            log.log(get_time() + "INFI >>> 正在初始化充电板")
            com = Component("interface_charging_panel_control")
            com.sequence = {"pc": 0, "svooc": 0, "pd": 0, "qc": 0, "otg": 0}
            resq = http_service.post_message(com)
            log.log(get_time() + f"INFO >>> 充电板所有端口已关闭，发送控制板指令如下：{resq}")

            # 清除zoom放大
            log.log(get_time() + "INFO >>> 正在关闭ZOOM缩放放大")
            com = Component("interface_close_zoom")
            com.instrName = instrName
            close_zoom = http_service.post_message(com)
            log.log(get_time() + "INFO >>> ZOOM缩放已关闭")

            # 打开示波器通道
            log.log(get_time() + "INFO >>> 打开示波器所有通道")
            com = Component("interface_select_ch")
            for i in range(len(label_tup)):
                com.instrName = instrName
                com.CH = aisle_list[i]
                log.log(get_time() + f"INFO >>> 正在开启示波器{aisle_list[i]}通道")
                aisle = http_service.post_message(com)
            log.log(get_time() + "INFO >>> 示波器所有通道已开启成功")

            # 设置1、2、3、4通道全带宽
            log.log(get_time() + "INFO >>> 正在开启示波器通道带宽")
            com = Component("interface_set_bandwidth")
            for i in range(len(label_tup)):
                com.instrName = instrName
                com.CH = aisle_list[i]
                com.bandwidth = "FULL"
                log.log(get_time() + f"INFO >>> 正在设置{aisle_list[i]}通道带宽为“FULL”")
                bandwidth = http_service.post_message(com)
            log.log(get_time() + "INFO >>> 示波器通道带宽设置完成")

            # 设置1、2、3、4通道耦合方式
            log.log(get_time() + "INFO >>> 正在设置示波器通道耦合方式")
            com = Component("interface_set_coupling")
            for i in range(len(label_tup)):
                com.instrName = instrName
                com.CH = aisle_list[i]
                com.ch_coupling = "DC"
                log.log(get_time() + f"INFO >>> 正在设置示波器{aisle_list[i]}通道耦合方式为”DC“")
                coupling = http_service.post_message(com)
            log.log(get_time() + "INFO >>> 示波器通道耦合方式设置完成")

            # 设置1、2、3、4通道标签名称【依据信号标签名称循环执行次数】
            flag_tup = {}  # 定义字典，供后续根据电压设置垂直刻度使用
            log.log(get_time() + "INFO >>> 正在设置示波器通道标签名称")
            com = Component("interface_set_channel_label")
            for key, value in label_tup.items():
                com.instrName = instrName
                com.CH = value
                com.label = key
                log.log(get_time() + f"INFO >>> 正在设置{value}通道名称为{key}")
                label_name = http_service.post_message(com)
                flag_tup[key] = value
            log.log(get_time() + "INFO >>> 示波器通道名称设置完成")

            # 设置1、2、3、4通道偏置值
            log.log(get_time() + "INFO >>> 正在设置示波器通道偏置值")
            com = Component("interface_set_offset")
            for i in range(len(label_tup)):
                com.instrName = instrName
                com.CH = aisle_list[i]
                com.offset = 0
                log.log(get_time() + f"INFO >>> 正在设置{aisle_list[i]}通道的偏置值为0")
                set_offset_value = http_service.post_message(com)
            log.log(get_time() + "INFO >>> 示波器通道偏置值已设置完成")

            # 设置1、2、3、4通道垂直刻度
            voltage_tup = {"WRX_OVP-OFF": 5, "WRX_EN": 5, "Boost_EN": 5, "VBAT_EN": 4, "EXT2_OTG_EN": 5,
                           "EXT1_OTG_EN": 5, "CP_EN": 4, "VIDT_OUT": 5, "VIDT_Vrect": 4, "Wireless_CHARGE_IN": 4,
                           "Vbus_CHARGE_IN": 5, "VBUS": 4, "WLS_CHG_IN": 5}
            # "VBUS": 5, "VIDT_OUT": 5, "WLS_CHG_IN": 5
            log.log(get_time() + "INFO >>> 正在根据信号电压设置对应通道的垂直刻度")
            # test = {}
            com = Component("interface_compute_only_set_scale")
            for key, value in flag_tup.items():  # value是通道号
                com.instrName = instrName
                com.CH = value
                com.Voltage = voltage_tup.get(key)  # 电压值
                set_scale = http_service.post_message(com)
                log.log(get_time() + f"INFO >>> 已设置通道{value}的垂直刻度为{set_scale}")
            log.log(get_time() + "INFO >>> 示波器通道垂直刻度已设置完成")

            # 设置示波器通道的垂直位置
            log.log(get_time() + "INFO >>> 正在设置示波器通道垂直位置")
            position_tup = {"CH1": 1, "CH2": 0, "CH3": -2, "CH4": -3}
            com = Component("interface_set_position")
            for key, value in position_tup.items():
                com.instrName = instrName
                com.CH = key
                com.vertical_position = value
                log.log(get_time() + f"INFO >>> 正在设置{key}通道的垂直位置为{value}")
                set_position = http_service.post_message(com)
            log.log(get_time() + "INFO >>> 示波器通道垂直位置已设置完成")
            """
            （2）通道1：带宽选择全带宽，耦合方式选择DC耦合，标签名设置为信号1名称，偏置设为0mV，垂直刻度根据电压幅值设置（信号占2格位置），垂直位置设为1格；
            （3）通道2：带宽选择全带宽，耦合方式选择DC耦合，标签名设置为信号2名称，偏置设为0mV，垂直刻度根据电压幅值设置，垂直位置设为0格；
            （4）通道3：带宽选择全带宽，耦合方式选择DC耦合，标签名设置为信号3名称，偏置设为0mV，垂直刻度根据电压幅值设置，垂直位置设为-2格；
            （5）通道4：带宽选择全带宽，耦合方式选择DC耦合，标签名设置为信号4名称，偏置设为0mV，垂直刻度根据电压幅值设置，垂直位置设为-3格；
            """

            # 设置示波器的水平时基
            log.log(get_time() + "INFO >>> 正在设置示波器的水平时基")
            com = Component("interface_set_horizontal_scale")
            com.instrName = instrName
            com.scale_horizontal = 0.9
            set_scale_horizontal = http_service.post_message(com)
            log.log(get_time() + f"INFO >>> 示波器水平时基已设置为{0.9 * 1000}ms")

            # 设置示波器记录长度
            log.log(get_time() + "INFO >>> 正在设置示波器记录长度")
            com = Component("interface_set_record_length")
            com.instrName = instrName
            com.length = 5.0E6
            set_length = http_service.post_message(com)
            log.log(get_time() + f"INFO >>> 示波器记录长度已设置为{5.0E6 / 1000000}M")

            # 开启快充==================================================
            log.log(get_time() + "INFO >>> 正在开启无线充")
            com = Component("interface_charging_panel_control")
            com.sequence = {"pc": 1, "pd": 1}
            resp_list = http_service.post_message(com)

            # 设置示波器滚动模式
            log.log(get_time() + "INFO >>> 正在设置示波器为滚动模式")
            com = Component("interface_set_trigger_mode")
            com.instrName = instrName
            com.acquire_type = "RUNSTOP"  # 余晖滚动模式
            set_mode = http_service.post_message(com)
            log.log(get_time() + f"INFO >>> 已将示波器设置为{'SEQUENCE'}滚动模式")

            # 设置示波器显示亮度
            log.log(get_time() + "INFO >>> 正在配置示波器波形强度显示为100%")
            com = Component("interface_set_display_intensity")
            com.instrName = instrName
            com.intensity = 100
            intensity = http_service.post_message(com)
            log.log(get_time() + "INFO >>> 已将示波器波形强度显示设置为100%")
            time.sleep(3)
            """
            （6）水平时基初始值设为400ms/div，记录长度设为5M，采用滚动模式，亮度设置为100%；
            """

            # 触发
            log.log(get_time() + "INFI >>> 正在开启快充")
            com = Component("interface_charging_panel_control")
            com.sequence = {"pc": 1, "svooc": 1, "pd": 1}
            resq = http_service.post_message(com)
            log.log(get_time() + f"INFO >>> 快充已开启，发送控制板指令如下：{resq}")

            # 停止采集
            log.log(get_time() + "INFO >>> 开始停止采集")
            com = Component("interface_set_acquisitions_stop")
            com.instrName = instrName
            req = http_service.post_message(com)
            log.log(get_time() + "INFO >>> 已停止采集")

            # 保存截图
            log.log(get_time() + "INFO >>> 开始保存屏幕截图")
            time.sleep(2)
            com = Component("interface_save_screen")
            com.instrName = instrName
            temp_name = ""  # 触发事件_手机当前状态_
            flag = 1
            for key in flag_tup.keys():
                temp_name = temp_name + f"{flag}@{key}"
                flag += 1
            com.fileName = f"D:\\testImg\\{temp_name}_{get_time()[:-2].replace(':', '-')}.png"
            save_screen = http_service.post_message(com)
            log.log(get_time() + f"INFO >>> 图片保存成功，保存路径为：{save_screen}")

            # VBUS / VIDD_OUT上升或下降，对波形进行放大（放大到20ms毫秒）； 之后再保存一张图

            # 判断通道上升或下降沿，并记录成列表
            log.log(get_time() + r"INFO >>> 开始计算通道上升\下降沿")  # 耗时90秒
            com = Component("interface_data_caul")
            com.instrName = instrName
            result_tup = {}  # 存放处理结果
            cc = time.time()
            for key, value in flag_tup.items():
                com.CH = value
                data_dic = http_service.post_message(com)
                df = pd.DataFrame(list(data_dic.items()), columns=["Time", "Voltage"])
                end_voltage = df["Voltage"].values[-1]  # 获取最终电压
                flag_tup = {}
                temp_data = df[
                    (df.Voltage > (end_voltage + (5 / 2))) | (df.Voltage < (end_voltage - (5 / 2)))]  # 获取上升/下降中间点
                temp_index = temp_data.index.max()  # 获取中间点的index
                if str(temp_index) == "nan":
                    log.log("在此判断0，0和1，1 ")
                if str(temp_index) != "nan":
                    start_v = df.iloc[temp_index - 250000]  # 中间点向前推半格位置
                    end_v = df.iloc[temp_index + 250000]  # 中间点向后推半格位置
                    if start_v.Voltage > end_v.Voltage + 0.2:
                        result_tup[key] = [1, 0]
                    elif start_v.Voltage < end_v.Voltage - 0.2:
                        result_tup[key] = [0, 1]
                    else:  # 除了判断00，还要判断11
                        result_tup[key] = [0, 0]

            # 开始写入波形变化数据
            log.log(get_time() + "INFO >>> 开始写入波形变化数据")
            # 根据result_tup元组key值查询Excel列ID
            key_data = xlrd.open_workbook(r"D:\testImg\result.xls", formatting_info=True)  # 结论表格
            insert_key_copy = copy(key_data)
            key_sheet_copy = insert_key_copy.get_sheet(0)

            rows = []
            for i in tab_sheet.row(0):
                rows.append(i.value)
            for key, value in result_tup.items():  # 循环查找到信号对应的index
                # 需要增加判断依据，
                key_sheet_copy.write(item_tup["触发前"], rows.index(key), value[0], set_style)
                key_sheet_copy.write(item_tup["触发后"], rows.index(key), value[1], set_style)
            insert_key_copy.save(r"D:\testImg\result.xls")
            log.log(get_time() + "INFO >>> 真值表信息写入完成")

            # 判断结果是否通过
            if len(trigger_start) > 0 and len(trigger_end) > 0:
                for res_check in range(len(result_tup)):    # 0,1,2,3
                    check_flag = list(result_tup.values())[res_check]
                    if res_check == len(trigger_start)-1:
                        break
                    if trigger_start[res_check] == str(check_flag[0]) and trigger_end[res_check] == str(check_flag[1]) and \
                            (check_result == "未检查" or check_result == "通过"):
                        check_result = "通过"
                    elif trigger_start[res_check] != str(check_flag[0]) or trigger_end[res_check] != str(check_flag[1]):
                        check_result = "不通过"
                for pop_list in range(len(result_tup)):  # 对比完数据之后，删除已比对过的信息，避免下一轮循环重复比对；
                    if len(trigger_start) > 0 and len(trigger_end) > 0:
                        trigger_start.pop(0)
                        trigger_end.pop(0)

            excel_file_copy.save(r"D:\testImg\result.xls")
            log.log(get_time() + r"文件保存完成，文件路径为：D:\testImg\result.xls")

            # 如果VBUS / VIDT_OUT发生变化，则放大波形再截图
            log.log(get_time() + "INFO >>> 开始判断VBUS / VIDT_OUT波形变化，是否进行波形放大")
            for temp_flag in ["VBUS", "VIDT_OUT"]:
                if temp_flag in result_tup.keys():
                    if result_tup[temp_flag][0] != result_tup[temp_flag][1]:
                        log.log(get_time() + f"INFO >>> 检查到{temp_flag}波形有变化，将对波形进行放大")
                        time_scaling = Component("interface_time_scaling")
                        time_scaling.instrName = instrName
                        time_scaling.zoom_point = float(df.iloc[temp_index]["Time"])
                        time_scaling.zoom_scale = 0.02
                        call_time_scaling = http_service.post_message(time_scaling)
                        log.log(get_time() + "INFO >>> 波形放大完成")

                        # 对放大后的波形进行截图
                        log.log(get_time() + "INFO >>> 对放大后的波形进行截图")
                        com = Component("interface_save_screen")
                        com.instrName = instrName
                        com.fileName = f"D:\\testImg\\{temp_name}_{get_time()[:-2].replace(':', '-')}.png"
                        save_screen = http_service.post_message(com)
                        log.log(get_time() + f"INFO >>> 图片保存成功，保存路径为：{save_screen}")
                        break
            print(check_result)

        # 填入测试结论
        rows = []
        # for b in tab_sheet.row(0):
        #     rows.append(b.value)
        # log.log(get_time() + f"INFO >>> 已经获取到测试结果的横向index为{rows.index('测试结果')}")    # 获取到结果需要填入的列
        # open_insert_conclusion = xlrd.open_workbook(r"D:\testImg\result.xls", formatting_info=True)     # 结论表格
        # insert_conclusion = copy(open_insert_conclusion)
        # insert_table = insert_conclusion.get_sheet(0)
        # # insert_col_num = get_column_letter(rows.index('测试结果') + 1)  # 获取列名
        # insert_rows_num = []
        # for rows_num in item_tup.values():
        #     insert_rows_num.append(rows_num)
        # # 设置单元格背景颜色
        # pattern = xlwt.Pattern()
        # pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        # if check_result == "通过":
        #     pattern.pattern_fore_colour = 11  # 颜色设置(绿色)
        # if check_result == "不通过":
        #     pattern.pattern_fore_colour = 10  # 颜色设置（红色）
        # if check_result == "未检查":
        #     pattern.pattern_fore_colour = 13  # 颜色设置（黄色）
        # set_style.pattern = pattern
        # insert_table.write_merge(insert_rows_num[0], insert_rows_num[1], rows.index('测试结果'), rows.index('测试结果'),
        #                          check_result, set_style)
        # insert_conclusion.save(r"D:\testImg\result.xls")

    except Exception as err:
        raise err
