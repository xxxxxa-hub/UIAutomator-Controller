# !/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：pythonProject4
@File ：phone_control.py
@Author ：hesiquan
@Date ：2021/12/16 10:52
"""
import pack_phoneself.Demand.engineering as eng
import os
import time


class MyException(Exception):
    """MyException"""


tab_list = ('产线测试项', '设备调试', 'Camera', '媒体调试', 'WCN', '通信调试', '其他')


def select_engineer_mode_tab(tab, em):
    d = em.action.driver
    t = d(resourceId='com.oplus.engineermode:id/pagertitle')
    if len(t) == 0:
        em.step('点亮屏幕').step('调起拨号键盘').step('工模输入', '*#808#')
        cur_tab = tab_list[0]
    else:
        cur_tab = t.child(index=1).info['text']

    cur_index = tab_list.index(cur_tab)
    tab = tab.get('tab') if type(tab) is dict else tab
    dst_index = tab_list.index(tab)
    if dst_index > cur_index:
        tab_step = tab_list[cur_index + 1]
        for i in range(1, dst_index - cur_index):
            tab_step += '-' + tab_list[cur_index + i + 1]
    elif dst_index < cur_index:
        tab_step = tab_list[cur_index - 1]
        for i in range(1, cur_index - dst_index):
            tab_step += '-' + tab_list[cur_index - i - 1]
    else:
        tab_step = cur_tab
    print(tab_step)
    em.step('测试类型路径', tab_step)


def set_screen_refresh_rate(rate, em):
    """
    设置屏幕刷新率
    :param em:
    :param rate: 刷新率
    :return:
    """
    try:
        d = em.action.driver
        d.app_stop('com.android.settings')
        time.sleep(0.5)
        d.shell('am start com.android.settings')

        d(resourceId='com.android.settings:id/animated_hint').click()
        d.send_keys('屏幕刷新')
        d(text='屏幕刷新率').click(offset=(0.5, 0.1))
        time.sleep(0.5)
        items = d(className='android.widget.TextView')
        rate = rate.get('rate') if type(rate) is dict else rate
        rate = str(rate)
        if len(items) == 0:
            raise MyException('没有找到指定刷新率')
        for i in items:
            if rate in i.info['text']:
                i.click()
    except MyException as err:
        raise err
    except Exception as err:
        print(err)
    pass


def set_brightness_in_engineer_mode(rate, em):
    """
    在工程师模式下设置亮度
    :param em:
    :param rate: 亮度值百分比
    :return:
    """
    rate = rate.get('rate') if type(rate) is dict else rate
    if type(rate) is not int:
        rate = int(rate)
    if not 0 <= rate <= 100:
        print(f'输入的参数不对: 0 <= rate <= 100')
        return
    rate = 99 if rate == 100 else rate
    select_engineer_mode_tab('媒体调试', em)
    em.step('点击测试类型', '屏幕亮度调节')
    d = em.action.driver
    skb = d(resourceId='com.oplus.engineermode:id/sb_set_brightness')
    skb.click(offset=(rate / 100, 0.5))
    d(text='确定').click()
    time.sleep(0.5)
    pass


def set_pic_in_engineer_mode(pic, em):
    """
    在工程模式下设置图片
    :param em:
    :param pic: 需要的图片：red, green, blue, white, black, gray, step, color, fruit
    :return:
    """
    dic_pic = ('red', 'green', 'blue', 'white', 'black', 'gray', 'step', 'color', 'fruit')
    pic = pic.get('pic') if type(pic) is dict else pic
    index = dic_pic.index(pic)
    select_engineer_mode_tab('媒体调试', em)
    em.step('点击测试类型', 'LCD测试')
    scr = em.action.driver(className='android.widget.FrameLayout')
    for i in range(0, index):
        scr.click()
        time.sleep(0.2)


def interface_ripple_load_phone_pre_process(frequency, brightness_rate, pic):
    """
    设置轻重载手机模式
    :param frequency:刷新频率
    :param brightness_rate:亮度比例
    :param pic:手机图片
    :return:
    """
    em = eng.EngineerMode()
    set_screen_refresh_rate(frequency, em)
    set_brightness_in_engineer_mode(brightness_rate, em)
    set_pic_in_engineer_mode(pic, em)
    return


def interface_under_display_fingerprint():
    """
    设置屏下指纹：进工模——设备调试——指纹测试——指纹老化测试
    :return: 
    """
    em = eng.EngineerMode()
    em.step('点亮屏幕').step('调起拨号键盘').step('工模输入', '*#808#').step('测试类型路径', '产线测试项-设备调试')
    # em.step('自动寻路', testPage='指纹测试', mode='*#808#')
    em.step("点击测试类型", '指纹测试').step("点击测试类型", "指纹老化测试").step("点击按钮或文字", "开始老化")
    return


def interface_side_fingerprint():
    """
    设置侧边指纹：进工模——设备调试——指纹测试——指纹质量测试——开始录入——录指纹
    :return:
    """
    em = eng.EngineerMode()
    em.step('点亮屏幕').step('调起拨号键盘').step('工模输入', '*#808#').step('测试类型路径', '产线测试项-设备调试')
    # em.step('自动寻路', testPage='指纹测试', mode='*#808#')
    em.step("点击测试类型", '指纹测试').step("点击测试类型", "指纹质量测试").step("点击按钮或文字", "开始录入")
    return


def interface_G_Sensor():
    """
    设置G-sensor测试场景：进工模——设备调试——GSensor——GSensor
    :return:
    """
    em = eng.EngineerMode()
    em.step('点亮屏幕').step('调起拨号键盘').step('工模输入', '*#808#').step('测试类型路径', '产线测试项-设备调试')
    # em.step('自动寻路', testPage='指纹测试', mode='*#808#')
    em.step("点击测试类型", 'GSensor').step("点击测试类型", 'GSensor')
    return


def interface_NFC():
    """
    设置NFC：进工模——其他——CPLC
    :return:
    """
    em = eng.EngineerMode()
    em.step('点亮屏幕').step('调起拨号键盘').step('工模输入', '*#808#').step('测试类型路径', '产线测试项-设备调试-CAMERA-媒体调试-WCN-通信调试-其他')
    em.step("点击测试类型", "CPLC")
    return


def interface_adb_devices():
    """
    adb devices搜索是否有连接手机
    :return:
    有连接手机返回true,否则返回false,无adb环境也返回false
    """
    command = 'adb devices'
    com_ret = os.popen(command).readlines()
    devices = format(com_ret)
    result = '\\tdevice' in devices
    return result


if __name__ == '__main__':
    # xx = eng.EngineerMode()
    # interface_ripple_load_phone_pre_process(60, 90, 'fruit')
    interface_side_fingerprint()
