# coding=utf-8
import datetime
import time
import pandas
from charset_normalizer import detect
import pack_oscilloscope.base.spi_signal_quality as OpCsv
import pack_oscilloscope.module_TEKMDO3054_SPItiming as MTS
from pack_oscilloscope.base.common_TekMDO3054 import TekMDO3054

def interface_ch_SIMCardset(instrName, ch_list, label_list):
    """
    设置示波器各个通道的标签和位置等
    :param instrName: 示波器ID
    :param ch_list: 通道号列表
    :param label_list: 标签列表
    :return:示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        tek.ch_SIMCardset(ch_list, label_list)
        return instrName
    except Exception as err:
        return str(err)


def interface_ch_piontlist(mark_allstr):
    """
    将接收到的字符串转化为列表 按 ";" 分隔截取，加入到list：position_list
    :param instrName:示波器的ID
    :param mark_allstr:所需通道的数据汇总字符串 string
    :return:position_list：字符串截取合成的列表 list
    """
    try:
        str_a = ';'
        if str_a in mark_allstr:
            m = mark_allstr.count(str_a)
            A = -1
            a = [-1]
            for i in range(m):
                A = mark_allstr.find(str_a, A + 1, len(mark_allstr))
                a.append(A)
        position_list = []
        for i in range(len(a) - 1):
            position_list.append(mark_allstr[a[i] + 1:a[i + 1]])
        return position_list
    except Exception as err:
        return str(err)


def interface_position_client(instrName, position_str):
    """
    找出满足时序要求的光标位置（两个通道的第一个上升沿）
    :param instrName:示波器的ID
    :param position_list_all:所需通道的上升沿数据汇总列表 list
    :return:cursor_position：光标的垂直位置集 dict
    """
    try:
        tek = TekMDO3054(instrName)
        position_list_all = interface_ch_piontlist(position_str)
        cursor_simposition = tek.SIMCardtiming_positionAll(position_list_all)
        cursor_position = {}
        cursor_position['instrName'] = instrName
        if len(position_list_all) == 1:
            cursor_position['position_a'] = cursor_simposition[0]
        elif len(position_list_all) == 2:
            cursor_position['position_a'] = cursor_simposition[0]
            cursor_position['position_b'] = cursor_simposition[1]
        elif len(position_list_all) == 3:
            cursor_position['position_a'] = cursor_simposition[0]
            cursor_position['position_b'] = cursor_simposition[1]
            cursor_position['position_c'] = cursor_simposition[2]
        elif len(position_list_all) == 4:
            cursor_position['position_a'] = cursor_simposition[0]
            cursor_position['position_b'] = cursor_simposition[1]
            cursor_position['position_c'] = cursor_simposition[2]
            cursor_position['position_d'] = cursor_simposition[3]
        return cursor_position
    except Exception as err:
        return str(err)


def interface_position_server(instrName, position_list_all):
    """
    找出满足时序要求的光标位置（两个通道的第一个上升沿）
    :param instrName:示波器的ID
    :param position_list_all:所需通道的上升沿数据汇总列表 list
    :return:cursor_position：光标的垂直位置集 dict
    """
    try:
        tek = TekMDO3054(instrName)
        cursor_simposition = tek.SIMCardtiming_positionAll(position_list_all)
        cursor_position = {}
        cursor_position['instrName'] = instrName
        if len(position_list_all) == 1:
            cursor_position['position_a'] = cursor_simposition[0]
        elif len(position_list_all) == 2:
            cursor_position['position_a'] = cursor_simposition[0]
            cursor_position['position_b'] = cursor_simposition[1]
        elif len(position_list_all) == 3:
            cursor_position['position_a'] = cursor_simposition[0]
            cursor_position['position_b'] = cursor_simposition[1]
            cursor_position['position_c'] = cursor_simposition[2]
        elif len(position_list_all) == 4:
            cursor_position['position_a'] = cursor_simposition[0]
            cursor_position['position_b'] = cursor_simposition[1]
            cursor_position['position_c'] = cursor_simposition[2]
            cursor_position['position_d'] = cursor_simposition[3]
        return cursor_position
    except Exception as err:
        return str(err)


def interface_set_simcursor(instrName, cursor_source, position_horizontal1, position_horizontal2, position1, position2):
    """
    设置示波器光标的水平和垂直位置
    :param instrName: 示波器的ID
    :param cursor_source: 光标的源(如，CH1)
    :param position_horizontal1: 光标a的水平位置
    :param position_horizontal2: 光标b的水平位置
    :param position1: 光标a的垂直位置
    :param position2: 光标b的垂直位置
    :return:cursor_value:示波器ID和垂直光标的时间差值
    """
    try:
        tek = TekMDO3054(instrName)
        delta_timing = tek.set_cursor(cursor_source, position_horizontal1, position_horizontal2, position1, position2)
        cursor_value = {}
        cursor_value['instrName'] = instrName
        cursor_value['delta'] = delta_timing
        return cursor_value
    except Exception as err:
        return str(err)


def interface_ClockStoptiming_position1(instrName, position_list_all):
    """
    找出满足时序要求的光标位置（两个通道的第一个上升沿）
    :param instrName:示波器的ID
    :param position_list1:第一个通道的位置坐标列表
    :param position_list2:第二个通道的位置坐标列表
    :return:cursor_position：垂直光标差值(min),光标a的垂直位置,光标b的垂直位置
    """
    try:
        tek = TekMDO3054(instrName)
        cursor_simposition = tek.SIMCardtiming_positionAll(position_list_all)
        cursor_position = {}
        cursor_position['instrName'] = instrName
        cursor_position['position_a'] = cursor_simposition[0]
        cursor_position['position_b'] = cursor_simposition[1]
        cursor_position['position_c'] = cursor_simposition[2]
        return cursor_position
    except Exception as err:
        return str(err)


def interface_laststr(str1):
    """
    找出满足要求的最后一个边缘数据
    :param str1:所有字符集
    :return:Laststr：搜索通道的最后一个边缘数据
    """
    label_a = ';'
    m = str1.count(label_a)
    A = -1
    a = []
    for i in range(m):
        A = str1.find(label_a, A + 1, len(str1))
        a.append(A)
    Lastsrt = str1[a[-1] + 1:-1]
    return Lastsrt


def interface_data_caul(instrName, ch, save_path):
    """
    获取1个通道的波形数据保存为CSV文件；
    :param instrName: 示波器ID
    :param save_path: 波形文件保存路径
    :return: 提示语：保存CSV文件是否成功： res
    """
    print("开始获取波纹数据！")
    try:
        tek = TekMDO3054(instrName)
        res = tek.data_caul(ch)
        rel = tek.save_data_list(res, save_path)
        return rel
    except Exception as err:
        return str(err)


def interface_latepoint(save_path):
    """
    通过的CSV文件获取通道最后一个点的 time；
    :param save_path: 波形文件保存路径
    :return: 水平位置 time ：x
    """
    df = OpCsv.read_data(save_path)
    df.columns = ["Time", "Vel"]
    data = df.apply(pandas.to_numeric, errors='coerce')  # 将所有字符串转为数字
    data = data[(data.Vel > 0.63)]
    df_a = data.values.tolist()
    x = df_a[-1][0]
    x = float(x)
    return x


def interface_fristpoint(save_path):
    """
    获取1通道的波形数据；
    :param save_path: 波形文件保存路径
    :return: 示波器ID
    """
    df = pandas.read_csv(save_path, nrows = 50000)
    df.columns = ["Time", "Vel"]
    data_max = max(df['Vel'])
    data = df.apply(pandas.to_numeric, errors='coerce')  # 将所有字符串转为数字
    data = data.drop_duplicates(subset=['Vel'])
    data = data[(data['Vel'] < 0.9*data_max)]
    firstpoint = data.iloc[0, [0,1]]
    knee_position = firstpoint['Time']
    print("Time:",knee_position)
    return knee_position


def interface_secondpoint(querylist):
    """
    获取通道的第二个触发沿数据；
    :param querylist: 波形query字符串
    :return: 第二个触发沿数据： string
    """
    A = []
    i, m = 0, 0
    for a in querylist:
        m = m + 1
        if a == ";":
            i = i + 1
            A.append(m)
        if i == 2:
            break
    secondpoint = querylist[A[0]:A[1] - 1]
    return secondpoint


def interface_adjust_scale(instrName, pos_a, pos_b, siterate):
    """
    根据计算出的光标要卡的位置对波形进行缩放
    :param instrName:
    :param pos_a:计算出的a光标放置的位置
    :param pos_b:计算出的b光标放置的位置
    :return:
    """
    try:
        pos_a = float(pos_a)
        pos_b = float(pos_b)
        tek = TekMDO3054(instrName)
        zoom_point = float((pos_a+pos_b)/2)     #  缩放的位置
        delta = float(abs(pos_a - pos_b))       #  缩放的比例
        old_scale = tek.query_horsacle()
        if delta < float(old_scale):            #  判读当前屏幕是否需要缩放
            zoom_scale = float(delta)
        if siterate:
            tek.set_SIM_PositionRateZoom(zoom_point, zoom_scale)
        else:
            tek.set_SIM_zoom(zoom_point, zoom_scale)
    except Exception as err:
        return str(err)


def set_DisplayIntensity(instrName,intensity):


    tek = TekMDO3054(instrName)
    tek.set_display_intensity(intensity)


def adjoin_twopoint(csv_path):
    """
    读取波形csv，返回波形中相邻间隔最大的两个point的time
    :param csv_path:
    :return: horizontal_position_a，horizontal_position_b
    """
    with open(csv_path, 'rb+') as fp:
        content = fp.read()
        encoding = detect(content)['encoding']
        # df = pandas.read_csv(csv_path, encoding=encoding)
        content = content.decode(encoding).encode('utf8')
        fp.seek(0)
        fp.write(content)
        # yield from asyncio.sleep(1)

    data = pandas.read_csv(csv_path, encoding='utf8', low_memory=False)

    # 获取子表'坐标'和‘测试结果’列的数
    data.columns = ['time', 'voltage']  # 设置纵坐标
    data = data.apply(pandas.to_numeric, errors='coerce')  # 将所有字符串转为数字
    lower = data["voltage"].values.min() + 1
    topper = data["voltage"].values.max()
    data = data[(data.voltage > lower) & (data.voltage < topper)]    # 获取voltage在(lower,topper)之间的所有数据
    data_a = data["time"].diff()                                     # data["time"]列相邻上下两行做差
    data_max = data_a.max()
    data["Time_diff"] = data_a                                       # 将做差后的列加到原数据中
    data.index = range(len(data))                                    # 重置data的索引
    horizontal_position_b = data["time"][data["Time_diff"].values == data_max].values        # 时间间隔最大的 上time值（b光标）
    time_min_index = data["time"][data["Time_diff"].values == data_max].index-1              # 时间间隔最大的 下time索引值
    horizontal_position_a = data.loc[time_min_index].time                                    # 时间间隔最大的 下time值（a光标）
    print(horizontal_position_a)
    print(horizontal_position_b)

    horizontal_position_a = float(horizontal_position_a)
    horizontal_position_b = float(horizontal_position_b)
    return (horizontal_position_a,horizontal_position_b)

def interface_adjust_Picture(instrName, cursor_source, position_horizontal1, position_horizontal2, trigger_delay = 0):
    pos_a = position_horizontal1 - trigger_delay
    pos_b = position_horizontal2 - trigger_delay
    MTS.interface_adjust_scale(instrName, pos_a, pos_b, siterate=False)
    MTS.interface_set_simcursor(instrName, cursor_source, position_horizontal1, position_horizontal2)


def interface_Set_Common(instrName, open_ch, ch_list, label_list):

    MTS.interface_set_Factory(instrName)
    MTS.interface_initial(instrName)
    for i in range(4):
        MTS.interface_open_ch(instrName,open_ch[i])
    MTS.interface_set_record_length(instrName, 5E-6)
    interface_ch_SIMCardset(instrName, ch_list, label_list)

def interface_Set_Activate_Timing(instrName, trigger_level):

    MTS.interface_horizontal_delay_state(instrName, "ON")
    MTS.interface_set_horizontal_scale(instrName, 40E-3)
    MTS.interface_set_trigger(instrName, 'RISE', 'CH1', trigger_level, 0)
    MTS.interface_set_trigger_mode(instrName,'SEQUENCE')
    MTS.interface_start_acquisitions(instrName)


# if __name__ == '__main__':
#     instrName = "TCPIP::" + "169.254.8.23" + "::INSTR"
#     OsDevice = MTS.interface_initial(instrName)
#     MTS.interface_start_acquisitions(instrName)
#     MTS.interface_set_record_length(instrName, 5.0E6)
#     ch_arr = 'CH1,CH2,CH3,CH4'
#     ch_label = 'VSIM,CLK,RST,IO'
#     t_clock = 260 / 1000000000
#     SIM_Vol = '3'
#
#     interface_ch_SIMCardset(instrName, ch_arr, ch_label)
#
#     MTS.interface_open_ch(instrName, "CH1")
#     MTS.interface_open_ch(instrName, "CH2")
#     MTS.interface_open_ch(instrName, "CH3")
#     MTS.interface_open_ch(instrName, "CH4")
#     SIMCardTest = "激活时序"
#     if SIMCardTest == "激活时序":
#         if SIM_Vol == '3':
#             # 设置时基
#             MTS.interface_set_horizontal_scale(instrName, 20E-3)
#             # 调用set_trigger函数设置触发类型
#             MTS.interface_set_trigger(instrName, "RISE", "CH1", 2, 0)
#         if SIM_Vol == '1.8':
#             # 设置时基
#             MTS.interface_set_horizontal_scale(instrName, 9E-3)
#             # 调用set_trigger函数设置触发类型
#             MTS.interface_set_trigger(instrName, "RISE", "CH1", 0.9, 0)
#
#         # 设置为单次触发
#         MTS.interface_set_trigger_mode(instrName, "SEQUENCE")
#         time.sleep(20)
#         a1 = input("(激活时序)波形是否正确：（Y/N）：")
#         if a1 == "Y":
#             print("调整示波器亮度为100" + "--" * 50)
#             set_DisplayIntensity(instrName, 100)
#             print("(激活时序)正在获取各个通道的必要数据中" + "--" * 50)
#             # 搜索通道2标记点的位置坐标(所有上升沿数据)
#             mark_position2 = MTS.interface_set_search(instrName, "CH2", "RISE", 1.26)
#             # 搜索通道3标记点的位置坐标(所有上升沿数据)
#             mark_position3 = MTS.interface_set_search(instrName, "CH3", "RISE", 1.26)
#             # 搜索通道4标记点的位置坐标(所有上升沿数据)
#             mark_position4 = MTS.interface_set_search(instrName, "CH4", "FALL", 1.26)
#             # 截取各个通道的第一个触发数据
#             if ";" in mark_position2['query']:
#                 mark_position2['query'] = (mark_position2['query'][:mark_position2['query'].index(';')])
#             if ";" in mark_position3['query']:
#                 mark_position3['query'] = (mark_position3['query'][:mark_position3['query'].index(';')])
#             if ";" in mark_position4['query']:
#                 mark_position4['query'] = (mark_position4['query'][:mark_position4['query'].index(';')])
#             mark_all = []
#             mark_all.append(mark_position2['query'])
#             mark_all.append(mark_position3['query'])
#             mark_all.append(mark_position4['query'])
#
#             # 调用接口，获取需要卡CLK、RST、IO 信道的光标垂直位置，再进行判断 tb 和 tc
#             print("tb满足协议要求判断中" + "--" * 50)
#             position_return = interface_position_server(instrName, mark_all)
#             horizontal_position_a = float(position_return['position_a'])  # CLK光标垂直位置
#             horizontal_position_b = float(position_return['position_b'])  # RST光标垂直位置
#             horizontal_position_c = float(position_return['position_c'])  # IO光标垂直位置
#             cursor_return = interface_set_simcursor(instrName, "CH2", 2.26, 1.26, horizontal_position_a,
#                                                     horizontal_position_b)
#             tb = float(cursor_return['delta'])
#             result = bool(tb >= 400 * t_clock)
#             if result:
#                 print("SIM激活时序Tb测试结果：Pass,Tb为：", tb)
#             else:
#                 print("SIM激活时序Tb测试结果：Fail,Tb为：", tb)
#
#             a2 = input("是否截图Y/N：")
#             if a2 == "Y":
#                 pic_path = r'E:\test1'
#                 filename = pic_path + "\\" + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + '.png'
#                 filename = MTS.interface_save_screen(instrName, filename)
#             else:
#                 pass
#             print("tc满足协议要求判断中" + "--" * 50)
#
#             if SIM_Vol == '3':
#                 # 放大波形，通过a|b光标距离计算放大倍数和位置
#                 interface_adjust_scale(instrName, horizontal_position_b, horizontal_position_c, siterate= False)
#
#             cursor_return = interface_set_simcursor(instrName, "CH2", 1.26, -1.26, horizontal_position_b,
#                                                     horizontal_position_c)
#             tc = float(cursor_return['delta'])
#             result = bool(tc >= 400 * t_clock and tc <= 40000 * t_clock)
#             if result:
#                 print("SIM激活时序Tc测试结果：Pass,Tc为：", tc)
#             else:
#                 print("SIM激活时序Tc测试结果：Fail,Tc为：", tc)
#             a3 = input("是否截图Y/N：")
#             if a3 == "Y":
#                 pic_path = r'E:\test1'
#                 filename = pic_path + "\\" + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + '.png'
#                 filename = MTS.interface_save_screen(instrName, filename)
#             else:
#                 pass
#     elif SIMCardTest == "时钟停止":
#         OsDevice = MTS.interface_initial(instrName)
#         MTS.interface_start_acquisitions(instrName)
#         MTS.interface_set_record_length(instrName, 5.0E6)
#         # 关闭用不到的通道
#         MTS.interface_close_ch(instrName, "CH1")
#         MTS.interface_close_ch(instrName, "CH3")
#         # 设置时基
#         MTS.interface_set_horizontal_scale(instrName, 4E-3)
#         # 调用set_trigger函数设置触发类型
#         MTS.interface_set_trigger(instrName, "RISE", "CH2", 0.9, 10E-3)
#         # 设置为单次触发
#         MTS.interface_set_trigger_mode(instrName, "SEQUENCE")
#         time.sleep(10)
#         a1 = input("（时钟停止时序）波形是否正确：（Y/N）：")
#         if a1 == "Y":
#             print("(时序)正在获取各个通道的必要数据中" + "--" * 50)
#             # 搜索通道2标记点的位置坐标(所有上升沿数据)
#             mark_position1 = MTS.interface_set_search(instrName, "CH2", "RISE", 1.26)
#             # 搜索通道3标记点的位置坐标(所有下降沿数据)
#             mark_position2 = MTS.interface_set_search(instrName, "CH4", "FALL", 1.26)
#             # 搜索通道4标记点的位置坐标(所有上升沿数据)
#             mark_position3 = MTS.interface_set_search(instrName, "CH4", "RISE", 1.26)
#             # 搜索通道4标记点的位置坐标(所有触发点位,并集成csv文件，存放在path中)
#             path = f"E:\\test1\\test.csv"
#             print(interface_data_caul(instrName,'CH2', path))
#
#             # 截取两个通道的第一个边缘数据和最后一个边缘数据
#             if ";" in mark_position1['query']:
#                 mark_position1['query'] = (mark_position1['query'][:mark_position1['query'].index(';')])
#             if ";" in mark_position2['query']:
#                 mark_position2['query'] = (mark_position2['query'][:mark_position2['query'].index(';')])
#             if ";" in mark_position3['query']:
#                 mark_position3['query'] = interface_laststr(mark_position3['query'])
#
#             mark_all = []
#             mark_all.append(mark_position1['query'])
#             mark_all.append(mark_position2['query'])
#             mark_all.append(mark_position3['query'])
#
#             # 调用接口，获取需要卡CLK、RST、IO 信道的光标垂直位置，再进行判断 tb 和 tc
#             print("tg满足协议要求判断中" + "--" * 50)
#             position_return = interface_ClockStoptiming_position1(instrName, mark_all)
#             horizontal_position_a = float(position_return['position_a'])  # CLK第一个上升沿光标垂直位置
#             horizontal_position_b = float(position_return['position_b'])  # IO第一个下降沿光标垂直位置
#             horizontal_position_c = float(position_return['position_c'])  # IO最后一个上升沿光标垂直位置
#             horizontal_position_d = interface_latepoint(path)  # CLK最后一个下降沿光标垂直位置
#
#             cursor_return = interface_set_simcursor(instrName, "CH2", 1.26, -1.26, horizontal_position_a,
#                                                     horizontal_position_b)
#             tg = float(cursor_return['delta'])
#             result = bool(tg >= 1860 * t_clock)
#             if result:
#                 print("时钟停止时序Tg测试结果：Pass,Tg为：", tg)
#             else:
#                 print("时钟停止时序Tg测试结果：Fail,Tg为：", tg)
#
#             a2 = input("是否截图Y/N：")
#             if a2 == "Y":
#                 pic_path = r'E:\test1'
#                 filename = pic_path + "\\" + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + '.png'
#                 filename = MTS.interface_save_screen(instrName, filename)
#
#             print("th满足协议要求判断中" + "--" * 50)
#             cursor_return = interface_set_simcursor(instrName, "CH2", 1.26, -1.26, horizontal_position_c,
#                                                     horizontal_position_d)
#             th = float(cursor_return['delta'])
#             result = bool(th >= 700 * t_clock)
#             if result:
#                 print("时钟停止时序Th测试结果：Pass,Th为：", th)
#             else:
#                 print("时钟停止时序Th测试结果：Fail,Th为：", th)
#
#             a2 = input("是否截图Y/N：")
#             if a2 == "Y":
#                 pic_path = r'E:\test1'
#                 filename = pic_path + "\\" + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + '.png'
#                 filename = MTS.interface_save_screen(instrName, filename)
#     elif SIMCardTest == "上电":
#         # 设置时基
#         MTS.interface_set_horizontal_scale(instrName, 10E-3)
#         # 调用set_trigger函数设置触发类型
#         MTS.interface_set_trigger(instrName, "RISE", "CH1", 0.9, 150E-6)
#         # 关闭水平延迟功能
#         MTS.interface_horizontal_delay_state(instrName, "OFF")
#         # 设置触发位置
#         MTS.interface_set_horizontal_position(instrName, 20)
#         # 设置为单次触发
#         MTS.interface_set_trigger_mode(instrName, "SEQUENCE")
#         time.sleep(20)
#         a1 = input("上电时序波形是否正确：（Y/N）：")
#         if a1 == "Y":
#             # 搜索通道1标记点的位置坐标(所有上升沿数据)
#             mark_position1 = MTS.interface_set_search(instrName, "CH1", "RISE", 1.62)
#             # 搜索通道2标记点的位置坐标(所有上升沿数据)
#             mark_position2 = MTS.interface_set_search(instrName, "CH2", "RISE", 1.62)
#             # 搜索通道3标记点的位置坐标(所有上升沿数据)
#             mark_position3 = MTS.interface_set_search(instrName, "CH3", "RISE", 1.26)
#             # 搜索通道4标记点的位置坐标(所有上升沿数据)
#             mark_position4 = MTS.interface_set_search(instrName, "CH4", "RISE", 1.26)
#             # 截取通道的第一个边缘数据
#             if ";" in mark_position1['query']:
#                 mark_position1['query'] = (mark_position1['query'][:mark_position1['query'].index(';')])
#             if ";" in mark_position2['query']:
#                 mark_position2['query'] = (mark_position2['query'][:mark_position2['query'].index(';')])
#             if ";" in mark_position3['query']:
#                 mark_position3['query'] = (mark_position3['query'][:mark_position3['query'].index(';')])
#             if ";" in mark_position4['query']:
#                 mark_position4['query'] = (mark_position4['query'][:mark_position4['query'].index(';')])
#
#             mark_all = []
#             mark_all.append(mark_position1['query'])
#             mark_all.append(mark_position2['query'])
#             mark_all.append(mark_position3['query'])
#             mark_all.append(mark_position4['query'])
#             # 调用接口，获取需要卡CLK、RST、IO 信道的光标垂直位置，再进行判断 tb 和 tc
#             print("tb满足协议要求判断中" + "--" * 50)
#             position_return = interface_position_server(instrName, mark_all)
#             horizontal_position_a = float(position_return['position_a'])  # SIM光标垂直位置
#             horizontal_position_b = float(position_return['position_b'])  # CLK:光标垂直位置
#             horizontal_position_c = float(position_return['position_c'])  # RST光标垂直位置
#             horizontal_position_d = float(position_return['position_d'])  # IO光标垂直位置
#             cursor_return = interface_set_simcursor(instrName, "CH2", 2.26, 1.26, horizontal_position_a,
#                                                     horizontal_position_b)
#             a = input("a|b光标卡时序是否正确")
#             if a == "Y":
#                 cursor_return = interface_set_simcursor(instrName, "CH2", 2.26, 1.26, horizontal_position_c,
#                                                     horizontal_position_d)
#             if horizontal_position_a < horizontal_position_d < horizontal_position_b < horizontal_position_c:
#                 print("测试结果：Pass")
#             else:
#                 print("测试结果：Fail")
#             a2 = input("是否截图Y/N：")
#             if a2 == "Y":
#                 pic_path = r'E:\test1'
#                 filename = pic_path + "\\" + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + '.png'
#                 filename = MTS.interface_save_screen(instrName, filename)
#     elif SIMCardTest == "下电":
#         # 设置时基
#         MTS.interface_set_horizontal_scale(instrName, 200E-6)
#         # 调用set_trigger函数设置触发类型
#         MTS.interface_set_trigger(instrName, "FALL", "CH1", 0.9, 150E-6)
#         # 关闭水平延迟功能
#         MTS.interface_horizontal_delay_state(instrName, "OFF")
#         # 设置触发位置
#         MTS.interface_set_horizontal_position(instrName, 60)
#         # 设置为单次触发
#         MTS.interface_set_trigger_mode(instrName, "SEQUENCE")
#         time.sleep(20)
#         a1 = input("下电时序波形是否正确：（Y/N）：")
#         if a1 == "Y":
#             # 搜索通道1标记点的位置坐标(所有下降沿数据)
#             mark_position1 = MTS.interface_set_search(instrName, "CH1", "FALL", 1.62)
#             # 搜索通道2标记点的位置坐标(所有触发点位,并集成csv文件，存放在path中)
#             pathb = f"E:\\test1\\test2.csv"
#             print(interface_data_caul(instrName, 'CH2', pathb))
#             # 搜索通道3标记点的位置坐标(所有下降沿数据)
#             mark_position3 = MTS.interface_set_search(instrName, "CH3", "FALL", 1.26)
#             # 搜索通道4标记点的位置坐标(所有下降沿数据)
#             mark_position4 = MTS.interface_set_search(instrName, "CH4", "FALL", 1.26)
#             # 截取各个通道的最后的触发数据
#             if ";" in mark_position1['query']:
#                 mark_position1['query'] = interface_laststr(mark_position1['query'])
#             if ";" in mark_position3['query']:
#                 mark_position3['query'] = interface_laststr(mark_position3['query'])
#             if ";" in mark_position4['query']:
#                 mark_position4['query'] = interface_laststr(mark_position4['query'])
#
#             mark_all = []
#             mark_all.append(mark_position1['query'])
#             mark_all.append(mark_position3['query'])
#             mark_all.append(mark_position4['query'])
#             # 调用接口，获取需要卡CLK、RST、IO 信道的光标垂直位置，再进行判断 tb 和 tc
#             print("tb满足协议要求判断中" + "--" * 50)
#             position_return = interface_position_server(instrName, mark_all)
#             horizontal_position_a = float(position_return['position_a'])  # SIM光标垂直位置
#             horizontal_position_b = interface_latepoint(pathb)  # CLK光标垂直位置
#             horizontal_position_c = float(position_return['position_b'])  # RST光标垂直位置
#             horizontal_position_d = float(position_return['position_c'])  # IO光标垂直位置
#
#             cursor_return = interface_set_simcursor(instrName, "CH2", 2.26, 1.26, horizontal_position_a,
#                                                         horizontal_position_b)
#             a = input("a|b光标卡时序是否正确")
#             if a == "Y":
#                 cursor_return = interface_set_simcursor(instrName, "CH2", 2.26, 1.26, horizontal_position_c,
#                                                             horizontal_position_d)
#
#             if horizontal_position_c < horizontal_position_b < horizontal_position_d <horizontal_position_a:
#                 print("测试结果：Pass")
#             else:
#                 print("测试结果：Fail")
#             a2 = input("是否截图Y/N：")
#             if a2 == "Y":
#                 pic_path = r'E:\test1'
#                 filename = pic_path + "\\" + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + '.png'
#                 filename = MTS.interface_save_screen(instrName, filename)
#     elif SIMCardTest == "class检测时延":
#         # 设置时基
#         MTS.interface_set_horizontal_scale(instrName, 400E-3)
#         # 关闭水平延迟功能
#         MTS.interface_horizontal_delay_state(instrName, "OFF")
#         # 设置触发位置
#         MTS.interface_set_horizontal_position(instrName, 20)
#         # 调用set_trigger函数设置触发类型
#         MTS.interface_set_trigger(instrName, "RISE", "CH1", 1.5, 0.1)
#         # 设置为单次触发
#         MTS.interface_set_trigger_mode(instrName, "SEQUENCE")
#         time.sleep(20)
#         a1 = input("class检测时延时序波形是否正确：（Y/N）：")
#         if a1 == 'Y':
#
#             # 搜索通道1标记点的位置坐标(所有下降沿数据的第一个下降沿)
#             mark_position1 = MTS.interface_set_search(instrName, "CH1", "FALL", 1.26)
#             if ";" in mark_position1['query']:
#                 mark_position1['query'] = (mark_position1['query'][:mark_position1['query'].index(';')])
#
#             # 搜索通道1标记点的位置坐标(所有上升沿数据的第二个上升沿)
#             mark_position2 = MTS.interface_set_search(instrName, "CH1", "RISE", 1.26)
#             if ";" in mark_position2['query']:
#                 mark_position2 = interface_secondpoint(mark_position2['query'])
#             else:
#                 print("获取波形错误")
#
#             mark_all = []
#             mark_all.append(mark_position1['query'])
#             mark_all.append(mark_position2)
#
#             position_return = interface_position_server(instrName, mark_all)
#
#             horizontal_position_a = float(position_return['position_a'])  # CLK第一个下降沿光标垂直位置
#             horizontal_position_b = float(position_return['position_b'])  # CLK第二个上升沿光标垂直位置
#
#             # 放大波形，通过a|b光标距离计算放大倍数和位置
#             interface_adjust_scale(instrName, horizontal_position_a, horizontal_position_b, siterate=True)
#             cursor_return = interface_set_simcursor(instrName, "CH1", 1.26, -1.26, horizontal_position_a, horizontal_position_b)
#             delta = float(cursor_return['delta'])
#             if delta > 0.01:
#                 print("测试结果：Pass，class时延间隔：", delta, "s")
#             else:
#                 print("测试结果：Fail，class时延间隔：", delta, "s")
#             a2 = input("是否截图Y/N：")
#             if a2 == "Y":
#                 pic_path = r'E:\test1'
#                 filename = pic_path + "\\" + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + '.png'
#                 filename = MTS.interface_save_screen(instrName, filename)
#     elif SIMCardTest == "待机SIM卡间隔":
#         # 设置时基
#         MTS.interface_set_horizontal_scale(instrName, 4)
#         # 关闭水平延迟功能
#         MTS.interface_horizontal_delay_state(instrName, "OFF")
#         # 设置触发位置
#         MTS.interface_set_horizontal_position(instrName, 15)
#         # 调用set_trigger函数设置触发类型
#         MTS.interface_set_trigger(instrName, "RISE", "CH2", 0.9, 10E-3)
#         # 设置为单次触发
#         MTS.interface_set_trigger_mode(instrName, "SEQUENCE")
#         time.sleep(20)
#         a1 = input("待机SIM卡间隔时序波形是否正确：（Y/N）：")
#         if a1 == 'Y':
#             a2 = input("是否截图Y/N：")
#             if a2 == "Y":
#                 pic_path = r'E:\test1'
#                 filename = pic_path + "\\" + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + '.png'
#                 filename = MTS.interface_save_screen(instrName, filename)
#
#             # 搜索通道2标记点的位置坐标(所有触发点位,并集成csv文件，存放在path中)
#             path = f"E:\\test1\\test.csv"
#             print(interface_data_caul(instrName, 'CH2', path))
#
#             point = adjoin_twopoint(path)
#             horizontal_position_a = point[0]
#             horizontal_position_b = point[1]
#
#             cursor_return = interface_set_simcursor(instrName, "CH2", 1.26, -1.26, horizontal_position_a, horizontal_position_b)
#             delta = float(cursor_return['delta'])
#             print("待机状态下class时延间隔：",delta,"s")
#             a2 = input("是否截图Y/N：")
#             if a2 == "Y":
#                 pic_path = r'E:\test1'
#                 filename = pic_path + "\\" + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + '.png'
#                 filename = MTS.interface_save_screen(instrName, filename)
#     elif SIMCardTest == "热插拔上电时序":
#         ch_arr = 'CH1,CH2,CH3,CH4'
#         ch_label = 'VSIM,INT,RST,IO'
#         interface_ch_SIMCardset(instrName, ch_arr, ch_label)
#         MTS.interface_close_ch(instrName, "CH3")
#         MTS.interface_close_ch(instrName, "CH4")
#         # 设置时基
#         MTS.interface_set_horizontal_scale(instrName, 20E-3)
#         # 调用set_trigger函数设置触发类型
#         MTS.interface_set_trigger(instrName, "RISE", "CH2", 0.9, 10E-3)
#         # 关闭水平延迟功能
#         MTS.interface_horizontal_delay_state(instrName, "OFF")
#         # 设置触发位置
#         MTS.interface_set_horizontal_position(instrName, 70)
#         # 设置为单次触发
#         MTS.interface_set_trigger_mode(instrName, "SEQUENCE")
#         time.sleep(20)
#
#         a1 = input("上电时序波形是否正确：（Y/N）：")
#         if a1 == 'Y':
#
#             mark_position1 = MTS.interface_set_search(instrName, "CH1", "RISE", 1.26)
#             mark_position2 = MTS.interface_set_search(instrName, "CH2", "RISE", 1.26)
#
#             if ";" in mark_position1['query']:
#                 mark_position1['query'] = mark_position1['query'][:mark_position1['query'].index(';')]
#             if ";" in mark_position2['query']:
#                 mark_position2['query'] = mark_position2['query'][:mark_position2['query'].index(';')]
#
#             mark_all = []
#             mark_all.append(mark_position1['query'])
#             mark_all.append(mark_position2['query'])
#
#             position_return = interface_position_server(instrName, mark_all)
#             horizontal_position_a = float(position_return['position_a'])  # VSIM第一个上升沿光标垂直位置
#             horizontal_position_b = float(position_return['position_b'])  #  INT第一个上升沿光标垂直位置
#
#             print(horizontal_position_a)
#             print(horizontal_position_b)
#
#             cursor_return = interface_set_simcursor(instrName, "CH2", 1.26, -1.26, horizontal_position_a, horizontal_position_b)
#             if horizontal_position_a > horizontal_position_b:
#                 print("热插拔上电时序判定结果：Pass,T_vsim：", horizontal_position_a,"s,T_int:", horizontal_position_b,"s" )
#             else:
#                 print("热插拔上电时序判定结果：Fail,T_vsim：", horizontal_position_a, "s,T_int:", horizontal_position_b, "s")
#             a2 = input("是否截图Y/N：")
#             if a2 == "Y":
#                 pic_path = r'E:\test1'
#                 filename = pic_path + "\\" + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + '.png'
#                 filename = MTS.interface_save_screen(instrName, filename)
#     elif SIMCardTest == "热插拔下电时序":
#         ch_arr = 'CH1,CH2,CH3,CH4'
#         ch_label = 'VSIM,INT,RST,IO'
#         interface_ch_SIMCardset(instrName, ch_arr, ch_label)
#         MTS.interface_close_ch(instrName, "CH3")
#         MTS.interface_close_ch(instrName, "CH4")
#         # 设置时基
#         MTS.interface_set_horizontal_scale(instrName, 20E-3)
#         # 调用set_trigger函数设置触发类型
#         MTS.interface_set_trigger(instrName, "FALL", "CH2", 0.9, 10E-3)
#         # 关闭水平延迟功能
#         MTS.interface_horizontal_delay_state(instrName, "OFF")
#         # 设置触发位置
#         MTS.interface_set_horizontal_position(instrName, 20)
#         # 设置为单次触发
#         MTS.interface_set_trigger_mode(instrName, "SEQUENCE")
#         time.sleep(20)
#
#         a1 = input("下电时序波形是否正确：（Y/N）：")
#         if a1 == 'Y':
#
#             mark_position1 = MTS.interface_set_search(instrName, "CH1", "FALL", 1.26)
#             mark_position2 = MTS.interface_set_search(instrName, "CH2", "FALL", 1.26)
#
#             if ";" in mark_position1['query']:
#                 mark_position1['query'] = mark_position1['query'][:mark_position1['query'].index(';')]
#             if ";" in mark_position2['query']:
#                 mark_position2['query'] = mark_position2['query'][:mark_position2['query'].index(';')]
#
#             mark_all = []
#             mark_all.append(mark_position1['query'])
#             mark_all.append(mark_position2['query'])
#
#             position_return = interface_position_server(instrName, mark_all)
#             horizontal_position_a = float(position_return['position_a'])  # VSIM第一个上升沿光标垂直位置
#             horizontal_position_b = float(position_return['position_b'])  # INT第一个上升沿光标垂直位置
#
#             cursor_return = interface_set_simcursor(instrName, "CH2", 1.26, -1.26, horizontal_position_a,
#                                                     horizontal_position_b)
#             if horizontal_position_a > horizontal_position_b:
#                 print("热插拔下电时序判定结果：Pass,T_vsim：", horizontal_position_a, "s,T_int:", horizontal_position_b, "s")
#             else:
#                 print("热插拔下电时序判定结果：Fail,T_vsim：", horizontal_position_a, "s,T_int:", horizontal_position_b, "s")
#             a2 = input("是否截图Y/N：")
#             if a2 == "Y":
#                 pic_path = r'E:\test1'
#                 filename = pic_path + "\\" + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + '.png'
#                 filename = MTS.interface_save_screen(instrName, filename)


