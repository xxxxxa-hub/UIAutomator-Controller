# coding=utf-8
import os
import time
from pack_oscilloscope.base.common_TekMDO3054 import TekMDO3054
from pack_oscilloscope.base import spi_signal_quality
from pack_phoneself.Base import mobile_base
from pack_oscilloscope.base.scene_library import GoScene
import pandas
import pack_oscilloscope.base.spi_signal_quality as OpCsv

"""
    电源质量测试后端方法 --- 常一杰
"""


def interfaces_run_test_scene(scene_name, *args):
    """
    执行对应的测试场景
    :param scene_name: 需要执行的测试场景名称
    """
    try:
        run_scene = GoScene()
        return eval(f"run_scene.{scene_name}")(args)
    except Exception as e:
        return str(e)


def get_scene(item, scene):
    """
    获取场景
    :param item: 场景类别，提示信息或程序执行（artificial 或 procedure；）
    :param scene: 场景
    :return: 场景信息
    """
    try:
        go_scene = GoScene()
        return go_scene.switch_test_item(item, scene)
    except Exception as err:
        return str(err)


def interface_initial(instrName):
    """
    初始化接口
    :return:
    """
    try:
        tek = TekMDO3054(instrName)
        tek.set_visa_timeout(100)
        tek.set_date_time()
        return instrName
    except Exception as err:
        return str(err)


def interface_open_ch(instrName):
    """
    开启指定通道
    :param instrName: 示波器ID
    :return:示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        tek.open_ch("CH1")      # 打开示波器1通道
        return instrName
    except Exception as err:
        return str(err)


def interface_close_ch(instrName):
    """
    关闭指定通道
    :param instrName: 示波器ID
    :return:示波器ID
    """
    close_list = ["CH2", "CH3", "CH4"]     # 需要关闭的通道列表
    try:
        tek = TekMDO3054(instrName)
        for i in close_list:
            tek.close_ch(i)
        return instrName
    except Exception as err:
        return str(err)


def interface_set_bandwidth(instrName, bandwidth):
    """
    设置示波器带宽
    @param instrName:示波器ID
    @param bandwidth:设置带宽值
    @return:示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        tek.set_bandwidth("CH1", bandwidth)     # 设置1通道示波器带宽(指定数值或FULL)
        return instrName
    except Exception as err:
        return str(err)


def interface_set_coupling(instrName, ch_coupling):
    """
    设置通道耦合模式
    @param instrName: 示波器ID
    @param ch_coupling:耦合方式
    @return:示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        tek.set_coupling("CH1", ch_coupling)    # 设置示波器1通道耦合模式
        return instrName
    except Exception as err:
        return str(err)


def interface_set_channel_label(instrName, name):
    """
    设置示波器通道标签名称
    @param instrName: 示波器ID
    @return: 示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        tek.set_channel_label("CH1", name)     # 设置1通道的标签名称为VDD
        return instrName
    except Exception as err:
        return str(err)


def interface_set_offset(instrName, offset):
    """
    设置示波器偏置值
    @param instrName:示波器ID
    @param offset:需要设置的偏置值
    @return:示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        tek.set_offset("CH1", offset)       # 设置示波器1通道的偏置值
        return instrName
    except Exception as err:
        return str(err)


def interface_set_scale(instrName, Voltage):
    """
    设置示波器垂直比例（垂直刻度）, 垂直位置值
    @param instrName: 示波器ID
    @param Voltage: 电压值
    @return: 返回列表[str(垂直刻度)， str(垂直位置)]
    """
    try:
        tek = TekMDO3054(instrName)
        req = tek.compute_set_scale("CH1", float(Voltage))   # 设置示波器1通道的垂直比例（垂直刻度）
        return req
    except Exception as err:
        return str(err)


def interface_par_set_scale(instrName, vertical_scale):
    """
    根据参数设置垂直刻度
    @param instrName: 示波器ID
    @param vertical_scale: 需要设置的比例（刻度）值
    @return: 示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        req = tek.set_scale("CH1", vertical_scale)   # 设置示波器1通道的垂直比例（垂直刻度）
        return req
    except Exception as err:
        return str(err)


def interface_set_position(instrName, vertical_position):
    """
    设置示波器垂直位置
    @param instrName:示波器ID
    @param vertical_position:需要设置的垂直位置
    @return:示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        tek.set_position("CH1", vertical_position)      # 设置示波器1通道的垂直位置
        return instrName
    except Exception as err:
        return str(err)


def interface_set_horizontal_scale(instrName, scale_horizontal):
    """
    设置示波器水平时基
    @param instrName:示波器ID
    @param scale_horizontal:需要设置的水平时基参数
    @return:示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        tek.set_horizontal_scale(scale_horizontal)
        return instrName
    except Exception as err:
        return str(err)


def interface_set_record_length(instrName):
    """
    设置示波器的记录长度
    @param instrName: 示波器ID
    @return: 示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        tek.set_record_length(5.0E6)    # 设置示波器的记录长度（科学计数法表示5000000.0）
        return instrName
    except Exception as err:
        return str(err)


def interface_change_time_set(instrName, change_type, source_num=0):
    """
    设置示波器，添加测量项
    @param instrName: 示波器ID
    @param change_type: 需要添加设置的测量项，高：HIGH / 低：LOW / 上升：RISe / 下降：FALL
    @return: 示波器ID
    """
    # change_time_new 示波器显示上升/下降沿上下电测量时间,返回测量值
    try:
        tek = TekMDO3054(instrName)
        tek.change_time_set(change_type, "CH1", source_num)
        return instrName
    except Exception as err:
        return str(err)


def interface_set_trigger(instrName, trigger_type, trigger_level, trigger_delay):
    """
    设置示波器的触发方式（触发类型、触发电平、触发位置）
    @param instrName: 示波器ID
    @param trigger_type: 上升沿触发或下降沿触发，FALL/RISE二者选一
    @param trigger_level: 触发电平
    @param trigger_delay: 触发位置
    @return: 示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        tek.set_trigger(trigger_type, "CH1", trigger_level, trigger_delay)
        return instrName
    except Exception as err:
        return str(err)


def interface_set_trigger_mode(instrName, acquire_type):
    """
    设置触发模式
    @param instrName: 示波器ID
    @param acquire_type: 触发模式（设置单次触发acquire_type=SEQUENCE，正常运行是acquire_type=RUNSTOP）
    @return:示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        if int(tek.query_acquire_mode()) == 0:
            tek.set_acquisitions_start()
            tek.set_trigger_mode(acquire_type)
        else:
            tek.set_trigger_mode(acquire_type)
        return instrName
    except Exception as err:
        return str(err)


def interface_set_acquisitions_stop(instrName):
    """
    停止示波器采集
    :param instrName: 示波器ID
    :return: 示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        tek.set_acquisitions_stop()
        return instrName
    except Exception as e:
        return str(e)


def interface_data_caul(instrName, save_path, low_v=None, high_v=None):
    """
    获取1通道的波形数据；
    :param low_v: 低电平位置
    :param high_v: 高电平位置
    :param instrName: 示波器ID
    :param save_path: 波形文件保存路径
    :return: 示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        req = tek.data_caul("CH1")  # 抓取数据耗时39秒
        tek.save_data_list(req, save_path, low_v, high_v)      # 耗时10秒左右
        return req
    except Exception as err:
        return str(err)


def interface_get_MEASUrement_data(instrName, MEASUrement_type: list):
    """
    获取测量项的测量结果值
    :return: 示波器ID
    """
    # MEASUrement_type = ["HIGH", "LOW"]
    try:
        tek = TekMDO3054(instrName)
        res = tek.get_MEASUrement_data(MEASUrement_type)
        return res
    except Exception as err:
        return str(err)


def interface_phone_reboot():
    """
    重启手机
    :return: 错误：ERROR 或返回设备名称
    """
    order = os.popen("ADB devices")
    res = order.read()
    if len(res.splitlines()) == 2:
        return "ERROR"
    elif len(res.splitlines()) > 2:
        devicesName = res.splitlines()[1].split('\t')[0]    # 截取获取手机设备名称
        os.system("ADB reboot")     # 发送重启指令
        return devicesName


def interface_check_phone_connect():
    """
    检查手机连接，50秒内如果没有检测到，将报错ERROR
    :return: 设备ID
    """
    for x in range(50):
        order = os.popen("ADB devices")
        req = order.read()
        if len(req.splitlines()) > 2:
            devicesName = req.splitlines()[1].split('\t')[0]
            return devicesName
        elif len(req.splitlines()) == 2:
            time.sleep(1)
        elif x == 50:
            return "ERROR"


def interface_check_back(csv_path, base, top):
    """
    判断回勾
    :param csv_path: 文件路径
    :param base: 低电平位置
    :param top: 高电平位置
    :return: 返回回勾数据
    """
    check_res = spi_signal_quality.SpiSignalQuality()
    res = check_res.check_back(csv_path, base, top)  # 传进获取的高、低电平值
    return res


def interface_set_afterglow_mode(instrName, mode):
    """
    设置示波器余晖模式
    :param instrName: 示波器ID
    :param mode: 余晖模式
    :return: 示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        tek.set_afterglow_mode(mode)
    except Exception as e:
        return str(e)


def interface_check_step(csv_path, base, top, threshold):
    """
    判断台阶
    :param csv_path: 文件路径
    :param base: 低电平位置
    :param top: 高电平位置
    :param threshold: 低于阈值才算台阶
    :return: 台阶数据
    """
    check_step = spi_signal_quality.SpiSignalQuality()
    check_res = check_step.check_step(csv_path, float(base), float(top), threshold)
    # print(check_res)
    return check_res


def interface_clear_Measure_type(instrName):
    """
    清除示波器所有测量项
    :param instrName: 示波器ID
    :return:
    """
    try:
        tek = TekMDO3054(instrName)
        tek.clear_Measure_type()
        return instrName
    except Exception as e:
        return str(e)


def interface_save_screen(instrName, fileName):
    """
    保存示波器屏幕截图
    :param instrName: 示波器ID
    :param fileName: 图片文件保存名称
    :return: 图片保存名称
    """
    try:
        tek = TekMDO3054(instrName)
        save_image = tek.save_screen(fileName)
        return save_image
    except Exception as e:
        return str(e)


def interface_get_observed_value(instrName, typeID, mold):
    """
    获取测量项的测量结果值
    :param instrName: 示波器ID
    :param typeID: 测量项ID编号
    :param mold: 需要获取的值（平均值MEAN、最小值MINImum、最大值MAXimum、值VALue）
    :return: 获取的值
    """
    try:
        tek = TekMDO3054(instrName)
        value = float(tek.get_observed_value(typeID, mold))
        return value
    except Exception as e:
        return str(e)


def interface_set_cursor(instrName, position_horizontal_1, position_horizontal_2, position1, position2):
    """
    设置光标的源和光标的位置(光标的类型为屏幕)
    :param instrName: 示波器ID
    :param position_horizontal_1: 设置a光标的水平位置
    :param position_horizontal_2: 设置b光标的水平位置
    :param position1:设置a光标的垂直位置
    :param position2:设置b光标的垂直位置
    :return: instrName
    """
    try:
        tek = TekMDO3054(instrName)
        tek.set_cursor("CH1", position_horizontal_1, position_horizontal_2, position1, position2)
        return instrName
    except Exception as e:
        return str(e)


def interface_set_display_intensity(instrName, intensity):
    """
    设置示波器的显示波形强度百分比
    :param instrName: 示波器ID
    :param intensity: 需要设置的显示强度百分比值（值得范围：1-100）
    :return: 示波器ID
    """
    try:
        tek = TekMDO3054(instrName)
        tek.set_display_intensity(intensity)
        return instrName
    except Exception as e:
        return str(e)


def interface_query_acquire_mode(instrName):
    """
    在50秒内检测示波器采集状态，如果50秒内没有触发波形，将返回报错
    :return: 状态ID （ 1 为采集状态， 0 为停止状态）
    """
    try:
        acquire_mode = TekMDO3054(instrName)
        for i in range(50):
            time.sleep(1)
            mode_id = int(acquire_mode.query_acquire_mode()[0])
            if mode_id == 0:
                return mode_id
            elif i == 49:
                return "ERROR"
    except Exception as e:
        return str(e)


def interface_off_cursors(instrName):
    """
    关闭示波器光标展示
    :param instrName: 示波器ID
    :return: 关闭结果
    """
    try:
        devices = TekMDO3054(instrName)
        res = devices.off_cursors()
        return res
    except Exception as e:
        return str(e)


def interface_get_RiseEdge(save_path, min_per, max_per):
    """
    通过的CSV文件获取通道中间 10% 和 90% 两个点的time；(使用电源上电测试项)
    :param save_path: 波形文件保存路径
    :param testChName: 通道的标签
    :param low: 高电平*10%
    :param high: 高电平*90%
    :return: 触发沿数据：data_analyse
    """
    df = OpCsv.read_data(save_path)
    df.columns = ["Time", "Vel"]
    data = df.apply(pandas.to_numeric, errors='coerce')  # 将所有字符串转为数字

    max_vel = data["Vel"].max()  # CSV文件Vel最大值
    min_vel = data["Vel"].min()  # CSV文件Vel最小值
    num_long = max_vel - min_vel  # CSV文件Vel最大值 与 最小值之间的距离
    low_point = num_long * min_per + min_vel   # 低电平点位
    high_point = num_long * max_per + min_vel  # 高电平点位

    data_analyse_a = data[(data.Vel < low_point)]
    data_analyse_b = data[(data.Vel > high_point)]

    horizontala = data_analyse_a.iloc[-1]['Time']
    horizontalb = data_analyse_b.iloc[0]['Time']
    return (horizontala, horizontalb)


def interface_get_FallEdge(save_path, min_per, max_per):
    """
    通过的CSV文件获取通道中间 10% 和 90% 两个点的time；(使用电源上电测试项)
    :param save_path: 波形文件保存路径
    :param testChName: 通道的标签
    :param low: 高电平*10%
    :param high: 高电平*90%
    :return: 触发沿数据：data_analyse
    """
    df = OpCsv.read_data(save_path)
    df.columns = ["Time", "Vel"]
    data = df.apply(pandas.to_numeric, errors='coerce')  # 将所有字符串转为数字

    max_vel = data["Vel"].max()  # CSV文件Vel最大值
    min_vel = data["Vel"].min()  # CSV文件Vel最小值
    num_long = max_vel - min_vel  # CSV文件Vel最大值 与 最小值之间的距离
    low_point = num_long * min_per + min_vel   # 低电平点位
    high_point = num_long * max_per + min_vel  # 高电平点位

    data_analyse_a = data[(data.Vel > high_point)]
    data_analyse_b = data[(data.Vel < low_point)]

    horizontala = data_analyse_a.iloc[-1]['Time']
    horizontalb = data_analyse_b.iloc[0]['Time']
    return (horizontala, horizontalb)


def interface_set_simcursor(instrName, cursor_source, position_horizontal1, position_horizontal2 ):
    """
    设置示波器光标的水平和垂直位置
    :param instrName: 示波器的ID
    :param cursor_source: 光标的源(如，CH1)
    :param position_horizontal1: 光标a的水平位置
    :param position_horizontal2: 光标b的水平位置
    :return:cursor_value:示波器ID和垂直光标的时间差值
    """
    try:
        tek = TekMDO3054(instrName)
        delta_timing = tek.set_cursor_wave(cursor_source, position_horizontal1, position_horizontal2)
        cursor_value = {'instrName': instrName, 'delta': delta_timing}
        return cursor_value
    except Exception as err:
        return str(err)

if __name__ == '__main__':
    instrName = "TCPIP::" + "169.254.5.85" + "::INSTR"
    interface_set_scale(instrName, 1.8)


    filePath = f"E:\\POST\\Data.csv"
    # filePath = f"D:\\Users\\Downloads\\C1--Trace--clk--00000.csv"
    # filePath = f"E:\\test1\\testData.csv"

    tek = interface_query_acquire_mode(instrName)
    print(tek)
    # # 打开示波器1通道
    # interface_open_ch(instrName)
    # # 关闭示波器其他通道
    # interface_close_ch(instrName)
    #
    # # 示波器通道一设置全带宽
    # interface_set_bandwidth(instrName, "FULL")
    #
    # # 设置示波器的记录长度（全部设置5M）；
    # interface_set_record_length(instrName)
    #
    # # 设置示波器的耦合方式
    # interface_set_coupling(instrName, "DC")
    #
    # # 标签名设置为VDD（自动设置CH1的标签名为VDD）；
    # interface_set_channel_label(instrName)
    #
    # # 设置示波器的偏置为0mV
    # interface_set_offset(instrName, 0)
    #
    # # =====================================================================================================================================
    # print(interface_set_scale(instrName, 3))
    #
    # # 设置示波器水平时基为100us/div
    # interface_set_horizontal_scale(instrName, 100.0E-06)
    #
    # # 添加高、低、上升时间测量项；
    # meter_list = {1: "HIGH", 2: "LOW", 3: "RISe"}
    # for i in meter_list:
    #     interface_change_time_set(instrName, meter_list[i], i)
    #
    # # 设置示波器触发类型
    # interface_set_trigger(instrName, "RISE", 0.9, 0)
    #
    # # 设置示波器触发模式（单次）
    # interface_set_trigger_mode(instrName, "SEQUENCE")
    #
    # # 重启手机
    # devices_reboot = interface_phone_reboot()
    # print(devices_reboot + "设备已重启")
    #
    # # 获取示波器波纹数据
    # res = interface_data_caul(instrName, filePath)      # 返回success表示成功，返回error表示失败
    #
    # # 获取测量项的高、低电平
    # level = interface_get_MEASUrement_data(instrName)
    # print(level)
    # print(float(level["LOW"]), float(level["HIGH"]))

    # 判断波纹数据回勾、台阶、过冲
    # interface_check_back(filePath, float(level["LOW"])-0.3, float(level["HIGH"])+0.3)   # 传进获取的高、低电平值
    # print(type(res))
    # res = interface_check_step(filePath, float(level["LOW"])-0.3, float(level["HIGH"])+0.3, 0.01)
    # print(res)








