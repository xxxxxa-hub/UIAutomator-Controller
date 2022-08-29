import datetime
import time
from pack_oscilloscope.base.os_instructions import *
import pyvisa as visa
import re
import csv
import pandas as pd
import math
import numpy as np


class TekMDO3054(object):
    def __init__(self, instrname):
        # self.device_name = device_name
        self.rm = visa.ResourceManager()

        # 如果不为空则查询
        # if len(device.strip()) > 0:
        self.inst = self.rm.open_resource(instrname)
        self.inst.write(f"HEADer 0")  # 设置示波器查询命令返回不包含头
        return

    # 如果搜索到示波器则返回示波器的序列
    # 否则返回空
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

    def set_visa_timeout(self, num=5):
        """
        :param device:设备名称
        :param self:
        :param num 超时时长,单位为s
        """
        num *= 1000
        self.inst.timeout = num

    # 示波器恢复默认设置
    def default_setup(self):
        self.call_instruction("Factory")

    # 设置示波器的波形强度
    def wave_intensity(self):
        self.call_instruction("WaveIntensity")
        self.inst.write('DISPLAY:PERSISTENCE OFF')

    # 开启指定通道
    def open_ch(self, ch):
        self.call_instruction("OpenCh", ch)

    # 关闭指定通道
    def close_ch(self, ch):
        self.call_instruction("CloseCh", ch)

    # 设置示波器的记录长度
    def set_record_length(self, record_length):
        self.call_instruction("SetRecordLength", record_length)

    # 设置带宽
    def set_bandwidth(self, ch, bandwidth):
        self.call_instruction("SetBandWidth", ch, bandwidth)

    # 设置水平位置及比例
    def set_horizontal(self, scale, position=50):
        self.call_instruction("HorizontalPosition", position)
        self.call_instruction("HorizontalScale", scale)

    # 设置水平位置
    def set_horizontal_position(self, position_horizontal):
        self.call_instruction("HorizontalPosition", position_horizontal)

    # 设置水平时基
    def set_horizontal_scale(self, scale_horizontal):
        self.call_instruction("HorizontalScale", scale_horizontal)

    # 设置通道名称
    def set_channel_label(self, ch, label):
        self.call_instruction("SetChannelLabel", ch, label)

    # 设置通道偏置
    def set_offset(self, ch, offset):
        self.call_instruction("SetOffset", ch, offset)

    # 设置指定通道的垂直比例（垂直刻度）
    def set_scale(self, ch, vertical_scale):
        self.call_instruction("SetScale", ch, vertical_scale)

    # 设置指定通道的垂直位置
    def set_position(self, ch, vertical_position):
        self.call_instruction("SetPosition", ch, vertical_position)

    # 设置通道的耦合方式（直流或交流）
    def set_coupling(self, ch, ch_coupling):
        self.call_instruction("SetChCoupling", ch, ch_coupling)

    # 设置通道的的反向状态:开启(ON)或关闭(OFF)
    def set_invert(self, ch, invert_state):
        self.call_instruction("SetChInvert", ch, invert_state)

    # 设置水平延迟状态（ON或OFF)
    def horizontal_delay_state(self, state):
        self.call_instruction("HorizontalDelay", state)

    # 设置水平延时时间
    def horizontal_delay(self, delay_horizontal):
        self.call_instruction("SetHorizontalDelay", delay_horizontal)

    # 打开延迟开关，设置水平延时时间
    def delay_horizontal(self, delay_horizontal):
        self.call_instruction("HorizontalDelay", "ON")
        self.call_instruction("SetHorizontalDelay", delay_horizontal)

    def set_zoom(self, zoom_point, zoom_scale):
        """
        设置缩放位置和缩放比例
        :param zoom_point: 缩放的位置
        :param zoom_scale: 缩放的水平比例
        :return:
        """
        self.inst.write('HORIZONTAL:SCALE?')
        horizontal_s = self.inst.read()
        scale = float(horizontal_s)
        zoom_position = (scale * 5 + zoom_point)/(scale * 10)*100
        self.call_instruction("OpenZoom")
        self.call_instruction("SetZoomPosition", zoom_position)
        self.call_instruction("SetZoomScale", zoom_scale)

    def set_SIM_zoom(self, zoom_point, zoom_scale):
        """
        设置缩放比例和缩放位置
        :param zoom_point: 缩放的位置;单位（s）
        :param zoom_scale: 缩放的水平比例
        :return:
        """
        self.inst.write('HORIZONTAL:SCALE?')
        horizontal_s = self.inst.read()                      #  获取当前示波器的水平时基;单位（s）
        scale = float(horizontal_s)*10000                    #  计算当前示波器的波形长度;单位（ms）
        zoom_position_section = zoom_point*1000 + scale/2    #  计算左边缘到缩放位置的波形长度;单位（ms）
        zoom_position_rate = zoom_position_section/scale     #  计算左边缘到缩放位置的波形长度/总波长的 比例
        zoom_position = zoom_position_rate * 100             #  换算后使用指令缩放的具体位置
        self.call_instruction("OpenZoom")
        self.call_instruction("SetZoomScale", zoom_scale)
        self.call_instruction("SetZoomPosition", zoom_position)

    def set_SIM_PositionRateZoom(self, zoom_point, zoom_scale):
        """
        设置缩放比例和缩放位置(当关闭水平时基后，设置了触发位置)
        :param zoom_point: 缩放的位置;单位（s）
        :param zoom_scale: 缩放的水平比例
        :return:
        """
        self.inst.write('HORIZONTAL:SCALE?')
        horizontal_s = self.inst.read()             # 获取当前示波器的水平时基;单位（s）
        scale = float(horizontal_s) * 10000         # 计算当前示波器的波形长度;单位（ms）
        self.inst.write('HORizontal:POSition?')
        horizontal = self.inst.read()               # 获取当前示波器的水平位置;单位（%）
        horizontal_rate = float(horizontal)/100     # 获取当前示波器的水平位置;单位（flaot）
        left_scale = -(scale*horizontal_rate)       # 获取当前示波器的最左边的水平刻度;单位（ms）
        zoom_position_section = zoom_point * 1000 - left_scale  # 计算左边缘到缩放位置的波形长度;单位（ms）
        zoom_position_rate = zoom_position_section/scale     #  计算左边缘到缩放位置的波形长度/总波长的 比例
        zoom_position = zoom_position_rate * 100             #  换算后使用指令缩放的具体位置
        self.call_instruction("OpenZoom")
        self.call_instruction("SetZoomScale", zoom_scale)
        self.call_instruction("SetZoomPosition", zoom_position)

    def close_zoom(self):
        """
        关闭zoom放大
        """
        self.call_instruction("CloseZoom")

    def set_cursor(self, cursor_source, position_horizontal_1, position_horizontal_2, position1, position2):
        """
        设置光标的源和光标的位置(光标的类型为屏幕)
        :param cursor_source: 以哪个通道为源
        :param position_horizontal_1: 设置a光标的水平位置
        :param position_horizontal_2: 设置b光标的水平位置
        :param position1:设置a光标的垂直位置
        :param position2:设置b光标的垂直位置
        :return:
        """
        self.call_instruction("SetScreenCursor")
        self.call_instruction("SetCursorSource", cursor_source)
        self.call_instruction("IndependentCursor")
        self.call_instruction("SetCursorUnit", "SECONDS")
        self.call_instruction("SetCursorAHPosition", position_horizontal_1)
        self.call_instruction("SetCursorBHPosition", position_horizontal_2)
        self.call_instruction("SetCursorAVPosition", position1)
        self.call_instruction("SetCursorBVPosition", position2)
        time.sleep(3)
        delta_timing = self.query_instruction("QueryVDELTa")
        delta_timing = float(delta_timing)
        return delta_timing

    def set_cursor_wave(self, cursor_source,  position1, position2):
        """
        设置光标的源和光标的位置(光标的类型为波形)
        :param cursor_source: 以哪个通道为源
        :param position1:设置a光标的垂直位置
        :param position2:设置b光标的垂直位置
        :return:
        """
        self.call_instruction("SetWaveCursor")
        self.call_instruction("SetCursorSource", cursor_source)
        self.call_instruction("IndependentCursor")
        self.call_instruction("SetCursorUnit", "SECONDS")
        self.call_instruction("SetCursorAVPosition", position1)
        self.call_instruction("SetCursorBVPosition", position2)
        time.sleep(1)
        delta_timing = self.query_instruction("QueryVDELTa")
        delta_timing = float(delta_timing)
        return delta_timing

    def set_cursor_horizontal(self, cursor_source, position_horizontal_1, position_horizontal_2):
        """
        设置光标的源和光标的位置(光标的类型为屏幕)
        :param cursor_source: 以哪个通道为源
        :param position_horizontal_1: 设置a光标的水平位置
        :param position_horizontal_2: 设置b光标的水平位置
        :param position1:设置a光标的垂直位置
        :param position2:设置b光标的垂直位置
        :return:
        """
        self.call_instruction("SetScreenCursor")
        self.call_instruction("SetCursorSource", cursor_source)
        self.call_instruction("IndependentCursor")
        self.call_instruction("SetCursorUnit", "SECONDS")
        self.call_instruction("SetCursorAHPosition", position_horizontal_1)
        self.call_instruction("SetCursorBHPosition", position_horizontal_2)
        time.sleep(3)
        delta_timing = self.query_instruction("QueryVDELTa")
        delta_timing = float(delta_timing)
        return delta_timing

    def set_trigger(self, trigger_type, trigger_ch, trigger_level, trigger_delay):
        """
        设置示波器的边沿触发方式(模式：正常)
        :param trigger_type: 上升沿触发或下降沿触发，FALL/RISE二者选一
        :param trigger_ch: 触发源（通道几触发）
        :param trigger_level: 触发电平
        :param trigger_delay: 触发位置
        :return:
        """
        self.call_instruction("SetTriggerASource", trigger_ch)
        self.call_instruction("SetTriggerType", "EDGE")
        self.call_instruction("TriggerACoupling", "DC")
        self.call_instruction("SetTriggerAEdge", trigger_type)
        self.call_instruction("SetTriggerMode", "NORMAL")
        self.call_instruction("SetTriggerALevel", trigger_ch, trigger_level)
        self.call_instruction("SetHorizontalDelay", trigger_delay)

    def set_trigger_pulse(self, pulse_source, pulse_condition, pulse_width, trigger_level):
        """
        设置示波器的触发方式为脉宽(模式：正常)
        :param pulse_source: 触发源（通道几触发）
        :param pulse_condition: 触发条件，LESSthan、MOREthan、EQual、UNEQual、WIThin、OUTside
        :param pulse_width: 脉冲宽度
        :param trigger_level:阈值
        :return:
        """
        self.call_instruction("SetTriggerType", 'PULSE')
        self.call_instruction("PulseClass", 'WIDTH')
        self.call_instruction("PulseSource", pulse_source)
        self.call_instruction("PulsePolarity", 'POSITIVE')
        self.call_instruction("PulseWhen", pulse_condition)
        self.call_instruction("SetTriggerALevel", pulse_source, trigger_level)
        self.call_instruction("SetPulseWidth", pulse_width)
        self.call_instruction("SetTriggerMode", "NORMAL")

    def set_trigger_auto(self, trigger_type, trigger_ch, trigger_level, trigger_delay):
        """
        设置示波器的触发方式(模式：自动（无触发滚动）)
        :param trigger_type: 上升沿触发或下降沿触发，FALL/RISE二者选一
        :param trigger_ch: 触发源（通道几触发）
        :param trigger_level: 触发电平
        :param trigger_delay: 触发位置
        :return:
        """
        self.call_instruction("SetTriggerASource", trigger_ch)
        self.call_instruction("SetTriggerType", "EDGE")
        self.call_instruction("TriggerACoupling", "DC")
        self.call_instruction("SetTriggerAEdge", trigger_type)
        self.call_instruction("SetTriggerMode", "AUTO")
        self.call_instruction("SetTriggerALevel", trigger_ch, trigger_level)
        self.call_instruction("SetHorizontalDelay", trigger_delay)

    # 设置单次触发acquire_type=SEQUENCE，正常运行是acquire_type=RUNSTOP
    def set_trigger_mode(self, acquire_type):
        self.call_instruction("SetAcquireType", acquire_type)

    # 查询示波器的采集状态
    def query_acquire_mode(self):
        trigger_mode = self.query_instruction("QueryAcquireType")
        return trigger_mode

    # 设置示波器开始采集
    def set_acquisitions_start(self):
        self.call_instruction("StartAcquisitions")

    # 设置示波器停止采集
    def set_acquisitions_stop(self):
        self.call_instruction("StopAcquisitions")

    # 设置示波器时间、日期
    def set_date_time(self):
        date = datetime.date.today()
        now_time = time.strftime("%H:%M:%S")
        self.inst.write(f'TIME "{now_time}"')
        self.inst.write(f'DATE "{date}"')

    # UI传入通道参数命名通道
    def name_ch(self, channel, name):
        self.inst.write(f':CH{channel}:LABEL "{name}"')

    # 关闭所有测量项
    def close_measure(self, num=5):
        for i in range(1, num):
            self.inst.write(f':MEASUREMENT:MEAS{i}:STATE 0')

    # 选择指定通道并关闭其他通道
    def select_channel(self, ch):
        """
        :param ch: [1, 2]选择指定通道并关闭其他通道
        """
        all_ch = ["CH1", "CH2", "CH3", "CH4"]
        for i in ch:
            self.inst.write(f':SELECT:{i} 1')
            all_ch.remove(i)
        for j in all_ch:
            self.inst.write(f':SELECT:{j} 0')

    # 示波器显示上升/下降沿上下电测量时间,返回测量值
    def change_time_new(self, ch, change_type):
        """
        :param ch: ch1 - ch4 要测量上电/下电时间的通道
        :param change_type: RISe for 上电, FALL for 下电 上下电类型
        """
        self.inst.write(f':MEASUREMENT:IMMED:SOURCE1 {ch}')
        # 选择上升沿为条件2
        self.inst.write(f':MEASUREMENT:IMMED:TYPE {change_type}')
        # 获取上升沿时间
        origin_data = float(self.inst.query(':MEASUrement:IMMed:VALue?').split()[-1])
        result = round(origin_data, 2)
        result_format = str(round(float(result), 2)) + 'ms'
        return result, result_format, origin_data

    # 在示波器上显示要测量的通道信息及测量值
    def change_time_set(self, change_type, ch, source_num=0):
        """
        :param source_num:
        :param change_type: 要添加测量值的类型,RISE上升时间,FALL下降时间,PWIDTH正脉冲宽度,NWIDTH负脉冲宽度
        :param ch: 要捕捉数据的通道名称,CH1等
        """
        source_num = int(ch[-1]) if source_num == 0 else source_num
        self.inst.write(f':MEASUREMENT:MEAS{source_num}:TYPE {change_type}')
        self.inst.write(f':MEASUREMENT:MEAS{source_num}:SOURCE1 {ch}')
        self.inst.write(f':MEASUREMENT:MEAS{source_num}:STATE 1')

    # 保存当前示波器显示的波形,默认保存到当前工作空间temp\my_image.png
    def save_screen(self, fileName):
        self.inst.write('SAVE:IMAG:FILEF PNG')
        self.inst.write('HARDCOPY START')
        # fileName = pic_path + "\\" + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + '.png'
        raw_data = self.inst.read_raw()
        fid = open(fileName, 'wb')
        fid.write(raw_data)
        fid.close()
        return fileName

    # 若满足要求（delta=cursor_delta），则保存示波器当前显示的波形
    def save_screen_path(self, delta1, delta2, filename):
        delta = round((delta1 * 10 ** 9), 2)
        cursor_delta = round((delta2 * 10 ** 9), 2)
        if abs(delta - cursor_delta) < 1:
            pic_path = r'F:\test1'
            filename = pic_path + "\\" + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + '.png'
            filename = self.save_screen(filename)
        return filename

    # 获取单调通道纹波数据
    def ripple_ch(self, ch, pkpk_max, screenshotPath):
        self.set_offset(ch, 0)
        self.inst.write('ACQUIRE:STOPAFTER RUNSTOP')
        self.inst.write(':TRIGGER:A:MODE AUTO')
        self.inst.write('ACQuire:STATE RUN')
        time.sleep(3)
        self.inst.write(':ACQUIRE:STATE 0')
        ch_rms = self.change_time_new(ch, 'RMS')[2]
        self.set_position(ch, 0)
        self.set_offset(ch, ch_rms)
        self.vertical_ch(ch, pkpk_max / 4)
        self.inst.write('ACQuire:STATE RUN')
        time.sleep(2)
        change_type_arr = ['RMS', 'MAXIMUM', 'MINIMUM', 'PK2PK']
        measure_value = {}
        ch_rms = self.change_time_new(ch, 'RMS')[2]
        self.set_offset(ch, ch_rms)
        time.sleep(2)
        self.inst.write(':ACQUIRE:STATE 0')
        for i in range(4):
            result = self.change_time_new(ch, change_type_arr[i])[2]
            self.change_time_set(change_type_arr[i], ch, i + 1)
            measure_value[change_type_arr[i]] = result
        time.sleep(2)
        # fileName = os.getcwd()+"\\Screenshot\\" + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")+'.png'
        fileName = screenshotPath + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + '.png'
        self.save_screen(fileName)
        measure_value['ScreenPath'] = fileName
        self.close_measure()
        return measure_value

    def call_instruction(self, cmd: object, *args: object) -> object:
        """
        从指令集中获取对应的指令，并赋值执行
        :rtype: object
        :param cmd:指令名称
        :param args: 指定需要的参数
        :return:
        """
        # 通过正则匹配出大括号及其大括号中内容
        instruction = TekMDO3054_instructions.get(cmd)
        regex = re.compile(r'\{.*?\}')
        # 用大括号进行替换
        instruction2 = regex.sub('{}', instruction)
        instruction3 = instruction2.format(*args)
        self.inst.write(instruction3)

    def query_instruction(self, cmd):
        """
        从指令集中获取对应的指令，执行查询功能
        :param cmd:查询指令名称
        :return:
        :query_value:返回搜索值
        """
        instruction = TekMDO3054_instructions.get(cmd)
        query_value = self.inst.query(instruction)
        return query_value

    def set_search(self, search_ch, search_type, search_level):
        """
        设置搜索条件，返回搜索值
        :param search_ch: 搜索通道
        :param search_type: 搜索的类型，上升沿、下降沿等
        :param search_level: 搜索的阈值
        :return:
        """
        self.call_instruction("OpenSearch")
        self.call_instruction("SetSearchSource", search_ch)
        self.call_instruction("SetSearchSlope", search_type)
        self.call_instruction("SetSearchLevel", search_ch, search_level)
        time.sleep(7)
        # 获取每个源通道的所有边沿点数据存储在search_channel
        search_channel0 = self.query_instruction("QuerySearchList")
        return search_channel0

    def search_position(self, search_channel1):
        """
        将搜索返回值转换为列表，并将所有标记点的位置坐标收集到mark_position列表里
        :param search_channel1:搜索返回的值，为字符串
        :return:
        """
        # 添加分割字符串将字符串分割为列表
        '''
                ①先判断是否有点，如为NONE则无点。
                ②将字符串以';'符号分割，判断有几个边沿点
                ③将';'分割后得字符串，再以','进行分割获取第五组数据
        '''
        if search_channel1[:2] == 'CH':
            channel_x = search_channel1.split(';')
            num = int(len(channel_x))
            # for循环，有多少个边沿点循环多少次
            mark_position = []
            for j in range(num):
                search_value = channel_x[j].split(',')
                # 获取坐标位置值
                position_x1 = search_value[4]
                # 将所有标记点的位置坐标收集到mark_position列表里
                mark_position.append(position_x1)
            return mark_position

    def query_position(self, ch, search_type, search_level):
        """
        找出满足要求的位置坐标
        :param ch: 通道号
        :param search_type: 搜索的类型，上升沿、下降沿等
        :param search_level: 搜索的阈值
        :return:
        """
        self.call_instruction("OpenSearch")
        self.call_instruction("SetSearchSource", ch)
        self.call_instruction("SetSearchSlope", search_type)
        self.call_instruction("SetSearchLevel", ch, search_level)
        time.sleep(5)
        # 获取每个源通道的所有边沿点数据存储在search_channel
        search_channel0 = self.query_instruction("QuerySearchList")
        '''
            ①先判断是否有点，如为NONE则无点。
            ②将字符串以';'符号分割，判断有几个边沿点
            ③将';'分割后得字符串，再以','进行分割获取第五组数据
        '''
        if search_channel0[:2] == 'CH':
            channel_x = search_channel0.split(';')
            num = int(len(channel_x))
            # for循环，有多少个边沿点循环多少次
            mark_position = []
            for j in range(num):
                search_value = channel_x[j].split(',')
                # 获取坐标位置值
                position_x1 = search_value[4]
                # 将所有标记点的位置坐标收集到search_position列表里
                mark_position.append(position_x1)
            return mark_position

    def timing_position1(self, search_channel1, search_channel2):
        """
        找出满足时序要求的光标位置（最小值）
        :param search_channel1:第一个通道的搜索返回值
        :param search_channel2:第二个通道的搜索返回值
        :return:
        """
        if search_channel1[:2] == 'CH':
            channel_x1 = search_channel1.split(';')
            num = int(len(channel_x1))
            position_list1 = []
            for j in range(num):
                search_value1 = channel_x1[j].split(',')
                # 获取坐标位置值
                position_x1 = search_value1[4]
                # 将所有标记点的位置坐标收集到position_list1列表里
                position_list1.append(position_x1)
        if search_channel2[:2] == 'CH':
            channel_x2 = search_channel2.split(';')
            num = int(len(channel_x2))
            position_list2 = []
            for j in range(num):
                search_value2 = channel_x2[j].split(',')
                # 获取坐标位置值
                position_x2 = search_value2[4]
                # 将所有标记点的位置坐标收集到position_list2列表里
                position_list2.append(position_x2)
        num1 = len(position_list1)
        num2 = len(position_list2)
        near_mark = []
        for i in range(num1):
            position1 = float(position_list1[i])
            mark = []
            for j in range(num2):
                position2 = float(position_list2[j])
                if position2 > position1:
                    mark.append(position1)
                    mark.append(position2)
                    break
            if len(mark) != 0:
                near_mark.append(mark)
        delta1 = []
        for num3 in range(len(near_mark)):
            min_position1 = near_mark[num3][0]
            min_position2 = near_mark[num3][1]
            delta_value = abs(min_position1 - min_position2)
            delta1.append(delta_value)
        min_delta = min(delta1)
        mark_index = delta1.index(min_delta)
        cursor_position1 = near_mark[mark_index][0]
        cursor_position2 = near_mark[mark_index][1]
        return min_delta, cursor_position1, cursor_position2

    def timing_position2(self, search_channel1, search_channel2, clock_period):
        """
        找出满足要求的光标位置(找到最大值)
        :param search_channel1:第一个通道的位置坐标列表
        :param search_channel2:第二个通道的位置坐标列表
        :param clock_period:时钟周期
        :return:
        """
        clock_period = float(clock_period)
        if search_channel1[:2] == 'CH':
            channel_x1 = search_channel1.split(';')
            num1 = int(len(channel_x1))
            position_list1 = []
            for i in range(num1):
                search_value1 = channel_x1[i].split(',')
                # 获取坐标位置值
                position_x1 = search_value1[4]
                # 将所有标记点的位置坐标收集到position_list2列表里
                position_list1.append(position_x1)
        if search_channel2[:2] == 'CH':
            channel_x2 = search_channel2.split(';')
            num2 = int(len(channel_x2))
            position_list2 = []
            for j in range(num2):
                search_value2 = channel_x2[j].split(',')
                # 获取坐标位置值
                position_x2 = search_value2[4]
                # 将所有标记点的位置坐标收集到position_list2列表里
                position_list2.append(position_x2)
        num_1 = len(position_list1)
        num_2 = len(position_list2)
        near_mark = []
        for i in range(num_1):
            position1 = float(position_list1[i])
            mark = []
            for j in range(num_2):
                position2 = float(position_list2[j])
                if position2 > position1:
                    if (position2-position1) < clock_period:
                        mark.append(position1)
                        mark.append(position2)
                    break
            if len(mark) != 0:
                near_mark.append(mark)
        delta1 = []
        for num3 in range(len(near_mark)):
            min_position1 = near_mark[num3][0]
            min_position2 = near_mark[num3][1]
            delta_value = abs(min_position1 - min_position2)
            delta1.append(delta_value)
        max_delta = max(delta1)
        mark_index = delta1.index(max_delta)
        cursor_position1 = near_mark[mark_index][0]
        cursor_position2 = near_mark[mark_index][1]
        return max_delta, cursor_position1, cursor_position2

    def ch_set(self, ch_list, label_list):
        time.sleep(1)
        ch_list = ch_list.split(',')
        label_list = label_list.split(',')
        for i in range(len(ch_list)):
            self.open_ch(ch_list[i])
            self.set_channel_label(ch_list[i], label_list[i])
            self.set_coupling(ch_list[i], "DC")
            self.set_invert(ch_list[i], "OFF")
            self.set_bandwidth(ch_list[i], "FULL")
            self.set_scale(ch_list[i], 1)
            self.set_offset(ch_list[i], 0)
            if i == 0:
                self.set_position(ch_list[i], 0)
            if i == 1:
                self.set_position(ch_list[i], -3)
            if i == 2:
                self.set_position(ch_list[i], -1)
            if i == 3:
                self.set_position(ch_list[i], 1)

    def ch_SIMCardset(self, ch_list, label_list):
        time.sleep(1)
        ch_list = ch_list.split(',')
        label_list = label_list.split(',')
        for i in range(len(ch_list)):
            self.open_ch(ch_list[i])
            self.set_channel_label(ch_list[i], label_list[i])
            self.set_coupling(ch_list[i], "DC")
            self.set_invert(ch_list[i], "OFF")
            self.set_bandwidth(ch_list[i], "FULL")
            self.set_scale(ch_list[i], 1)
            self.set_offset(ch_list[i], 0)
            if i == 0:
                self.set_position(ch_list[i], 0.48)
            if i == 1:
                self.set_position(ch_list[i], -0.4)
            if i == 2:
                self.set_position(ch_list[i], -1.44)
            if i == 3:
                self.set_position(ch_list[i], -2.54)

    def ch_OLEDdset(self, ch_list, position_list, label_list, scale_list):
        time.sleep(1)
        ch_list = ch_list.split(',')
        self.call_instruction("CloseZoom")
        while label_list:
            label_list = label_list.split(',')
            for i in range(len(ch_list)):
                self.open_ch(ch_list[i])
                self.set_channel_label(ch_list[i], label_list[i])
                self.set_coupling(ch_list[i], "DC")
                self.set_invert(ch_list[i], "OFF")
                self.set_bandwidth(ch_list[i], "FULL")
                self.set_offset(ch_list[i], 0)
                self.set_scale(ch_list[i], scale_list[i])
                self.set_position(ch_list[i], position_list[i])
        else:
            for i in range(len(ch_list)):
                self.set_position(ch_list[i], position_list[i])

    def SIMCardtiming_positionAll(self, search_channel_all):
        """
        找出满足时序要求的光标位置（水平位置）
        :param search_channel1:所有通道搜索值汇总 list
        :return: 光标水平位置集 list
        """
        position_list = []
        for i in range(len(search_channel_all)):
            search_value = search_channel_all[i].split(',')
            # 获取坐标位置值
            position_x = search_value[4]
            # 将标记点的位置坐标收集到position_dict 字典里
            position_list.append(position_x)
        print(position_list)
        return position_list

    def data_caul(self, ch):
        """
        获取指定通道数据，保存到指定位置CSV表
        :param ch: 需要保存的通道号，int类型
        :return: 数据字典列表
        """
        self.inst.write('DATA:SOURCE %s' % ch)
        self.inst.write('DATa:ENCdg ASCIi')
        self.inst.write('WFMOUTPRE:BYT_NR 4')
        self.inst.write('DATA:START 1')
        self.inst.write('DATA:STOP 250e6')
        self.inst.write('WFMOUTPRE?')
        preamble = self.inst.read()
        # ===================================== 获取示波器配置信息，用于数据处理计算 ===========================
        # 垂直位置
        self.inst.write('%s:POSition?' % ch)
        divus_str = self.inst.read()
        divus_float = float(divus_str)
        # 获取ch SCAle(垂直比例)
        self.inst.write('%s:SCAle?' % ch)
        div_str = self.inst.read()
        div_float = float(div_str)
        # =============================================== 数据处理 =====================================================
        data = self.inst.query('CURVE?').split(',')  # 获取数据，并截取成列表；
        YMULT = float(preamble.split(";")[14])  # 获取YMULT，提供解析波点使用
        YZERO = float(preamble.split(";")[16])  # 获取YZERO，提供解析波点使用

        # 使用pandas处理（优化数据处理效率）：
        df = pd.DataFrame(data)
        df.columns = ["source_data"]
        df = df.apply(pd.to_numeric, errors='coerce')
        df = df.reset_index()  # pandas对象数据index可视化
        # 电压值计算公式：数据点 * YMULT - 垂直位置 * 垂直刻度 + YZERO
        voltage_list = df["source_data"].values * YMULT - divus_float * div_float + YZERO
        # 时间轴计算公式： XZEro + XINcr * 数据点
        time_list = float(preamble.split(";")[11]) + float(preamble.split(";")[10]) * df["index"].values
        # 数据压缩打包返回
        data_dic = dict(zip(time_list, voltage_list))
        return data_dic

    def save_data_list(self, data_list, save_path, low=None, high=None):
        """
        储存数据到CSV文件
        :param high: 高电平位置
        :param low: 低电平位置
        :param data_list: 数据源列表
        :param save_path: CSV文件保存路径
        :return: 保存成功或失败
        """
        # ============================================= 储存数据到CSV文件 ==============================================

        try:
            s_time = time.time()
            df = pd.DataFrame(list(data_list.items()), columns=["Time", "Voltage"])
            if low is not None and high is not None:
                data_index = df.loc[(float(high) - 0.2 > abs(df.Voltage)) & (abs(df.Voltage) > (float(low) + 0.2))]  # 获取到满足条件的列表
                if len(data_index) > 1000:  # 如果数据量超过5000，直接取隔点取数
                    index_list = []
                    data_index = data_index.reset_index()
                    data_index.columns = ["INDEX", "Time", "Voltage"]
                    for i in range(0, len(data_index), int(len(data_index) / 5000)):
                        index_list.append(int(data_index.loc[i].INDEX))
                    get_data = df.iloc[index_list]
                    get_data.to_csv(save_path, index=False, header=True)     # 保存文件

            elif low is None and high is None:      # 如果没有指定高低电平位置，则直接全部数据取出；
                df.to_csv(save_path, index=False, header=True)
                # 原始获取数据循环代码块  # for i in data_list:    #     new_data[i] = data_list[i]
            # 原始保存文件代码块
            # with open(save_path, mode='w', encoding='utf-8-sig', newline='') as f:
            #     writer = csv.writer(f)
            #     writer.writerow(rows)
            #     writer.writerows(new_data.items())
            return "success"

        except Exception:
            return "error"

    def get_MEASUrement_data(self, MEASUrement_type: list):
        """
        获取测量项测量结果的值
        :param MEASUrement_type: 需要获取的测量项，列表类型 【注意：获取列表的次序，需要与示波器端添加的测量项次序一致】；
            测量量可以存在的值：AMPlitude|AREa|BURst|CARea|CMEan|CRMs|DELay|FALL|FREQuency|HIGH|HITS|LOW|MAXimum|MEAN|MEDian|MINImum|
            NDUty|NEDGECount|NOVershoot|NPULSECount|NWIdth|PEAKHits|PEDGECount|PDUty|PERIod|PHAse|PK2Pk|POVershoot|PPULSECount|PWIdth|
            RISe|RMS|SIGMA1|SIGMA2|SIGMA3|STDdev|TOVershoot|WAVEFORMS
        :return: 返回获取的值,字典类型；
        """
        res_dec = {}
        for i in range(len(MEASUrement_type)):
            res_dec[MEASUrement_type[i]] = float(self.inst.query("MEASUrement:MEAS%s:VALue?" % (i+1)))
        return res_dec

    # 当有多个沿变信号的时候，不适用
    def knee_point_rise_fall_dichotomy_at_start(self, csv_path, is_dir_rise):
        """
        二分法找出中点数据(电压中间值附近作为查找依据)
        author:brandon.yuan
        :param is_dir_rise:
        :param csv_path:
        :return:
        """
        df = pd.read_csv(csv_path)
        df.columns = ['time', 'voltage']
        volt_min = min(df['voltage'])
        volt_max = max(df['voltage'])
        if volt_max - volt_min < 0.2:
            raise Exception('no edge change signal find')
        volt_mid = (volt_max + volt_min) / 2.0
        cache = df['voltage']
        upper_index = len(cache) - 1
        lower_index = 0
        count = 0
        while True:
            target_index = (upper_index + lower_index) // 2
            count += 1
            if math.fabs(cache[target_index] - volt_mid) < volt_max * 0.05:
                break

            # 所取点位靠近低电平
            if math.fabs(cache[target_index] - volt_max) < math.fabs(cache[target_index] - volt_min):
                upper_index = target_index
            # 所取点位靠近高电平
            else:
                lower_index = target_index

            if count > 20:
                raise Exception('beyond max cycle')

        if is_dir_rise:
            back_point = volt_min
        else:
            back_point = volt_max

        # 再往回找起始点
        while target_index > 0:
            target_index -= 1
            if math.fabs(cache[target_index] - back_point) < 0.2:
                break

        target_pos = df.iloc[target_index]
        return target_index, target_pos['voltage'], target_pos['time']

    def knee_point_rise_fall_at_start(self, csv_path, edge_dir):
        """
        1,分段快速找出区间内是否有沿变信号。2，发现沿变信号后外扩区间，具体查找信号起点位置
        :param csv_path:
        :param edge_dir:
        :return:
        """
        df = pd.read_csv(csv_path)
        df.columns = ['time', 'voltage']
        s_volt = df['voltage']
        max_volt = s_volt.max()
        min_volt = s_volt.min()
        if math.fabs(max_volt - min_volt) < 0.2:
            raise Exception("No Edge Raise occurs!")

        sec_step = 5000
        sec_start_index = 0
        sec_end_index = 0
        total_len = len(s_volt)
        diff = (max_volt - min_volt) * 0.4
        for i in range(0, total_len, sec_step):
            sec_start_index = i
            if total_len - sec_start_index >= sec_step:
                sec_end_index = sec_start_index + sec_step
            else:
                sec_end_index = total_len

            sec_volt = s_volt.iloc[sec_start_index: sec_end_index]
            if math.fabs(max(sec_volt) - min(sec_volt)) > diff:
                break

        if sec_start_index > sec_step:
            sec_start_index -= sec_step
        else:
            sec_start_index = 0

        if total_len - sec_end_index > sec_step:
            sec_end_index += sec_step
        else:
            sec_end_index = total_len

        # 找沿变具体位置
        sec_volt = s_volt.iloc[sec_start_index: sec_end_index]

        if edge_dir == "RISE":
            edge_start_point = min_volt
        else:
            edge_start_point = max_volt

        index = 0
        for item in sec_volt:
            if math.fabs(item - edge_start_point) > math.fabs(max_volt - min_volt) * 0.2:
                break
            index += 1

        target_index = sec_start_index + index
        # 再往回找起始点
        while target_index > 0:
            target_index -= 1
            if math.fabs(s_volt[target_index] - edge_start_point) < 0.2:
                break

        target_pos = df.iloc[target_index]
        return target_index, target_pos['voltage'], target_pos['time']

    @staticmethod
    def avr_of_data_to_mean(data: list):
        data_mean = np.mean(data)
        mean_sum = 0
        for item in data:
            mean_sum += math.fabs(item - data_mean)

        return mean_sum/len(data)

    def knee_point_rise_fall_sequence_xxx(self, csv_path):
        """
        顺序查找电压点，再回溯至起点
        :param csv_path:
        :return:
        """
        df = pd.read_csv(csv_path)
        df.columns = ['time', 'voltage']
        s_volt = df['voltage']
        max_volt = s_volt.max()
        min_volt = s_volt.min()
        diff = math.fabs(max_volt - min_volt)
        step = 200
        threshold = diff * 0.4
        if diff < 0.2:
            raise Exception("No Edge Raise/Fall Occurs!")

        # 判断上升波形还是下降波形
        tmp = s_volt.iloc[20: 80]
        head_mean = tmp.mean()
        if math.fabs(head_mean - max_volt) > math.fabs(head_mean - min_volt):
            edge_dir = "RISE"
        else:
            edge_dir = "FALL"

        sub_volt = s_volt[::step]
        threshold_index = 0
        for val in sub_volt:
            if edge_dir == "RISE":
                if val > threshold:
                    break
            else:
                if val < threshold:
                    break

            threshold_index += step

        # 寻找方差稳定的位置（边沿位置）
        step2 = 400
        index_current = threshold_index
        sec_mean = s_volt[index_current: index_current + step2]
        mean_current = sec_mean.mean()
        mean_last = mean_current - 0.2
        while math.fabs(mean_current - mean_last) > 0.01:
            index_current -= step
            mean_last = mean_current
            if index_current < 0:
                raise Exception("No Stable Level find !")
            sec_mean = s_volt[index_current: index_current + step2]
            mean_current = sec_mean.mean()

        index = index_current + step2
        target_pos = df.iloc[index]
        return index, target_pos['voltage'], target_pos['time']

    def knee_point_rise_fall_sequence(self, csv_path, time_div, record_len):
        """
        顺序查找电压点，再回溯至起点
        :param record_len:
        :param time_div:
        :param csv_path:
        :return:
        """
        df = pd.read_csv(csv_path)
        df.columns = ['time', 'voltage']
        s_volt = df['voltage']
        max_volt = s_volt.max()
        min_volt = s_volt.min()
        diff = math.fabs(max_volt - min_volt)
        step = 200
        threshold = diff * 0.4
        if diff < 0.2:
            raise Exception("No Edge Raise/Fall Occurs!")

        # 判断上升波形还是下降波形
        tmp = s_volt.iloc[20: 80]
        head_mean = tmp.mean()
        if math.fabs(head_mean - max_volt) > math.fabs(head_mean - min_volt):
            edge_dir = "RISE"
        else:
            edge_dir = "FALL"

        sub_volt = s_volt[::step]
        threshold_index = 0
        for val in sub_volt:
            if edge_dir == "RISE":
                if val > threshold:
                    break
            else:
                if val < threshold:
                    break

            threshold_index += step

        # 寻找方差稳定的位置（通过两点之间直线的斜率来判断信号是否水平，横坐标取示波器格栅的十分之一长度）
        index_span = int(record_len / 10 / 40)
        time_span = time_div / 40

        seek_index = threshold_index
        while True:
            if seek_index < index_span:
                raise Exception('No Stable Edge Find !')

            point_head_index = seek_index - index_span
            point_end_index = seek_index + index_span
            point_head_volt = np.mean(s_volt.iloc[point_head_index - 50: point_head_index + 50])
            point_end_volt = np.mean(s_volt.iloc[point_end_index - 50: point_end_index + 50])

            # 计算斜率 单位 (v/s, 任何一点偏差都会导致一个很大的结果，所以单位定位 v/div)
            slope = math.fabs(point_head_volt - point_end_volt) / time_span
            if slope * time_div < 0.1:
                break
            seek_index -= index_span

        stable_volt = point_end_volt
        seek_index = threshold_index
        while True:
            if math.fabs(s_volt[seek_index] - stable_volt) < 0.1:
                break
            seek_index -= 100

        target_pos = df.iloc[seek_index]
        return seek_index, target_pos['voltage'], target_pos['time']

    def knee_point_rise(self, csv_path):
        """
        计算上电波形的拐点
        :param csv_path: 波形数据保存路径
        :return: v_max:幅值的最大值
        :return:knee_position: 波形拐点处的时间坐标值
        """
        df = pd.read_csv(csv_path, nrows=5E5)
        df.columns = ['time', 'voltage']
        value_max = max(df['voltage'])
        print("value_max:", value_max)
        data = pd.read_csv(csv_path)
        data.columns = ['time', 'voltage']
        v_max = max(data['voltage'])
        data = data.apply(pd.to_numeric, errors='coerce')
        data1 = data.drop_duplicates(subset=['voltage'])
        data2 = data1[data1['voltage'] > (value_max+0.02)]
        # data2 = data1[data1['voltage'] >= (0.1 * v_max)]
        data3 = data2.iloc[0, [0, 1]]
        knee_position = data3["time"]
        return v_max, knee_position

    def knee_point_fall(self, csv_path):
        """
        正常下电时，计算下电波形的拐点
        :param csv_path: 波形数据保存路径
        :return: v_max:幅值的最大值
        :return:knee_position: 波形拐点处的时间坐标值
        """
        df = pd.read_csv(csv_path, nrows=5E5)
        df.columns = ['time', 'voltage']
        value_min = min(df['voltage'])
        value_mean = np.mean(df['voltage'])
        data = pd.read_csv(csv_path)
        data.columns = ['time', 'voltage']
        v_max = max(data['voltage'])
        data = data.apply(pd.to_numeric, errors='coerce')
        data1 = data.drop_duplicates(subset=['voltage'])
        data2 = data1[data1['voltage'] < value_min]
        # data2 = data1[data1['voltage'] <= (0.9*value_mean)]
        data3 = data2.iloc[0, [0, 1]]
        knee_position = data3["time"]
        return v_max, knee_position

    def search_num(self, search_ch, search_type, search_level):
        """
        # 设置搜索条件，返回满足搜索要求的边沿个数
        :param search_ch: 搜索通道
        :param search_type: 搜索的类型，上升沿、下降沿等
        :param search_level: 搜索的阈值
        :return: num：边沿个数
        :return: ref_position：最后一个边沿的的位置
        """
        self.call_instruction("OpenSearch")
        self.call_instruction("SetSearchSource", search_ch)
        self.call_instruction("SetSearchSlope", search_type)
        self.call_instruction("SetSearchLevel", search_ch, search_level)
        time.sleep(1)
        num = 0
        # 获取每个源通道的所有边沿点数据存储在search_channel
        search_channel0 = self.query_instruction("QuerySearchList")
        if search_channel0[:2] == 'CH':
            channel_x = search_channel0.split(';')
            num = int(len(channel_x))
        return num

    def search_edge_num(self, search_ch, search_type, search_level):
        """
        # 设置搜索条件，返回满足搜索要求的边沿个数和最后一个边沿的的位置
        :param search_ch: 搜索通道
        :param search_type: 搜索的类型，上升沿、下降沿等
        :param search_level: 搜索的阈值
        :return: num：边沿个数
        :return: ref_position：最后一个边沿的的位置
        """
        self.call_instruction("OpenSearch")
        self.call_instruction("SetSearchSource", search_ch)
        self.call_instruction("SetSearchSlope", search_type)
        self.call_instruction("SetSearchLevel", search_ch, search_level)
        time.sleep(1)
        # 获取每个源通道的所有边沿点数据存储在search_channel
        search_channel0 = self.query_instruction("QuerySearchList")
        if search_channel0[:2] == 'CH':
            channel_x = search_channel0.split(';')
            num = int(len(channel_x))
            # for循环，有多少个边沿点循环多少次
            mark_position = []
            ref_position = 0
            for j in range(num):
                search_value = channel_x[j].split(',')
                # 获取坐标位置值
                position_x1 = search_value[4]
                # 将所有标记点的位置坐标收集到mark_position列表里
                mark_position.append(position_x1)
        if len(mark_position) != 0:
            ref_position = mark_position[-1]
        return num, ref_position

    def fall_knee_point(self, csv_path, num, start_position):
        """
        存在反复上下电时，计算下电波形的拐点
        :param csv_path: 波形数据保存路径
        :param num 搜索出的边沿个数
        :param start_position: 开始计算拐点的数据起点
        :return: v_max:幅值的最大值
        :return:knee_position: 波形拐点处的时间坐标值
        """
        df = pd.read_csv(csv_path, nrows=40000)
        df.columns = ['time', 'voltage']
        value_min = min(df['voltage'])
        data = pd.read_csv(csv_path)
        data.columns = ['time', 'voltage']
        v_max = max(data['voltage'])
        data = data.apply(pd.to_numeric, errors='coerce')
        if num == 0:
            data1 = data.drop_duplicates(subset=['voltage'])
            data2 = data1[data1['voltage'] < value_min]
            data3 = data2.iloc[0, [0, 1]]
            knee_position = data3["time"]
        else:
            data1 = data[data['time'] > start_position]
            data2 = data1.drop_duplicates(subset=['voltage'])
            data3 = data2[data1['voltage'] < value_min]
            data4 = data3.iloc[0, [0, 1]]
            knee_position = data4["time"]
        return v_max, knee_position

    def knee_point_fall1(self, csv_path, search_ch):
        """
        正常下电时，计算下电波形的拐点
        :param csv_path: 波形数据保存路径
        :return: v_max:幅值的最大值
        :return:knee_position: 波形拐点处的时间坐标值
        """
        df = pd.read_csv(csv_path, nrows=50000)
        df.columns = ['time', 'voltage']
        value_min = min(df['voltage'])
        data = pd.read_csv(csv_path)
        data.columns = ['time', 'voltage']
        v_max = max(data['voltage'])
        self.call_instruction("OpenSearch")
        self.call_instruction("SetSearchSource", search_ch)
        self.call_instruction("SetSearchSlope", 'FALL')
        self.call_instruction("SetSearchLevel", search_ch, value_min-0.02)
        # time.sleep(1)
        # 获取每个源通道的所有边沿点数据存储在search_channel
        search_channel0 = self.query_instruction("QuerySearchList")
        if search_channel0[:2] == 'CH':
            channel_x = search_channel0.split(';')
            num = int(len(channel_x))
            # for循环，有多少个边沿点循环多少次
            mark_position = []
            ref_position = 0
            for j in range(num):
                search_value = channel_x[j].split(',')
                # 获取坐标位置值
                position_x1 = search_value[4]
                # 将所有标记点的位置坐标收集到mark_position列表里
                mark_position.append(position_x1)
        return v_max, mark_position[0]

    def find_mean_value(self, csv_path):
        """
        计算波形的最大值
        :param csv_path: 波形数据保存路径
        :return: v_mean:幅值的最大值
        """
        df = pd.read_csv(csv_path, nrows=30000)
        df.columns = ['time', 'voltage']
        v_mean = np.mean(df['voltage'])
        return v_mean

    def query_horsacle(self):
        """
        查询水平时基
        :return: now_scale：返回当前水平时基的值
        """
        now_scale = self.query_instruction("QueryHorScale")
        return now_scale

    # # 根据电压值自动计算垂直刻度、垂直位置；
    def compute_set_scale(self, ch, Voltage:float):
        """
        根据传入的Voltage电压值（单位V），自动计算并设置垂直刻度与垂直位置；
        :param ch: 示波器通道号
        :param Voltage: 电压值，单位V
        :return: 返回列表[垂直刻度， 垂直位置]
        """
        scale = math.ceil(Voltage * 1000 / 8)   # 向上取整
        temp = 0
        # =================================== 计算并设置垂直刻度 ======================================
        scale_list = [10, 20, 50, 100, 200, 300, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000]
        for i in range(len(scale_list)):
            if scale_list[i] < scale < scale_list[i + 1]:
                temp = scale_list[i + 1]
            elif scale == scale_list[i]:
                temp = scale_list[i]
        self.call_instruction("SetScale", ch, temp/1000)
        # print(temp)
        # =================================== 计算并设置垂直位置 ======================================
        # high = temp * 8     # 总高度
        v_high = (Voltage*1000)/2    # 计算垂直位置对称位置
        site = abs(0 - int(v_high/temp))
        site = 0 - site     # 垂直位置为负数
        self.call_instruction("SetPosition", ch, site)
        return [str(temp*1000)+'mV', str(site)]

    def compute_only_set_scale(self, ch, Voltage):
        """
        ***** 注意： 该方法将根据波形电压设置展示在示波器电压幅值2格以内  *****
        ***** 根据传入的Voltage电压值（单位V），自动计算并设置垂直刻度； *****
        :param ch: 示波器通道号
        :param Voltage: 电压值，单位V
        :return: 返回设置垂直刻度
        """
        scale = math.ceil(Voltage * 1000 / 2)   # 向上取整
        temp = 0
        # =================================== 计算并设置垂直刻度 ======================================
        scale_list = [10, 20, 50, 100, 200, 300, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000]
        for i in range(len(scale_list)):
            if scale_list[i] < scale < scale_list[i + 1]:
                temp = scale_list[i + 1]
            elif scale == scale_list[i]:
                temp = scale_list[i]
        self.call_instruction("SetScale", ch, temp/1000)
        return str(temp*1000)+'mV'

    def set_afterglow_mode(self, mode):
        """
        # 设置示波器余晖触发模式
        :param mode: 余晖触发模式， {AUTO|NORMal}
        :return: None
        """
        self.call_instruction("SetTriggerMode", mode)

    def clear_Measure_type(self):
        """
        清除测量项
        :return: None
        """
        button_list = ["MEASurement", "BMENU2", "RMENU5", "CLEARMenu"]
        for i in button_list:
            self.inst.write(f"FPAnel:PRESS %s" % i)
        self.inst.write('CLEARMenu')
        self.inst.write('CLEARMenu')

    def get_observed_value(self, typeID, mold):
        """
        获取指定的测量结果值
        :param typeID: 测量项ID编号
        :param mold: 需要获取的值（平均值MEAN、最小值MINImum、最大值MAXimum、值VALue）
        :return: 获取的值
        """
        value = float(self.inst.query("MEASUrement:MEAS{}:{}?".format(typeID, mold)))
        return value

    def set_display_intensity(self, intensity):
        """
        设置示波器波形显示强度百分比
        :param intensity: 需要设置的显示强度百分比值（值得范围：1-100）
        :return:
        """
        self.inst.write(f"DISPLAY:INTEnsITY:WAVEFORM %d" % int(intensity))

    def off_cursors(self):
        """
        关闭光标
        :return:
        """
        flag = self.inst.query("CURSor:FUNCtion?").replace("\n", "")
        if flag != "OFF":
            self.inst.write("CURSor:FUNCtion OFF")
            return "已关闭光标展示；"
        else:
            return "光标已经处于关闭状态；"

    def set_persistence_status(self, status):
        """
         设置示波器余晖触发模式
        :param mode: 余晖触发模式， {CLEAR|AUTO|INFInite|OFF}
        :return: None
        """
        self.call_instruction("SetPERSistence", status)


if __name__ == '__main__':
    instrName = "TCPIP::" + "169.254.5.85" + "::INSTR"
    rm = visa.ResourceManager()
    inst = rm.open_resource(instrName)

    tek = TekMDO3054(instrName)
    # tek.data_caul('CH1')
    # tek.off_cursors()
    #
    # tek.knee_point_rise_fall_sequence_xxx('E:/test2/datasheet4.csv', 0.04, 1.0E6)

    # # 获取数据
    # data = tek.data_caul("CH1")
    # # 存储数据
    # start = time.time()
    # tek.save_data_list(data, f"E:\\test1\\NewTestData1111.csv")
    # end = time.time()
    # print(end - start)

