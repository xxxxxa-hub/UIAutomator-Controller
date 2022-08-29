import json
import time
import requests
import os
from pack_phoneself.Demand import singleaction, engineering
from pack_phoneself.Base import mobile_base
from pack_oscilloscope.base import USB_circuit_board as USB


class ControlPhone(object):
    def __init__(self):
        # usb_on = USB.SerialPort()
        # usb_on.pc_on()  # 打开USB连接
        os.popen("adb start-server")  # 启动ADB连接服务
        # self.connect = os.popen("adb tcpip 5555")
        # os.popen("adb kill-server")     # 关闭ADB连接服务

    def set_airplane_mode(self, mode):
        """
        设置飞行模式
        @param mode: on为开启飞行模式，off为关闭飞行模式
        """
        mobile = mobile_base.MobileBase()
        mobile.drag_in_element(500, 500, 0, 1500, 0.05)
        mobile.drag_in_element(500, 500, 0, 1500, 0.05)
        if mode == "off":
            try:
                self.self_find_element('airplane_mode_off')
            except:
                self.self_click_element("airplane_mode_on")
        elif mode == "on":
            try:
                self.self_find_element('airplane_mode_on')
            except:
                self.self_click_element("airplane_mode_off")
        self.self_adb_comm_execute("adb shell input keyevent 3")  # 返回桌面

    def connect_wifi(self):
        """
        # 连接WIFI后并自动断开USB连接；
        :return:
        """
        os.popen("adb tcpip 5555")
        ip = self.get_ip(self.get_mac())
        com_res = os.popen(f"adb connect {ip}:5555")
        devices_ip = com_res.read()
        # if "already connected to" in devices_ip:
        #     usb_off = USB.SerialPort()
        #     usb_off.pc_off()    # 关闭USB连接板
        return devices_ip.split(" ")[-1].replace("\n", "")

    @staticmethod
    def get_mac():
        """
        # 获取连接设备MAC地址
        :return:
        """
        mobile = singleaction.SingleAction()
        # mobile = mobile_base.MobileBase()
        devices_mac = mobile.adb_comm_execute("adb shell cat /sys/class/net/wlan0/address")
        return devices_mac.replace('\n', "")

    @staticmethod
    def get_ip(phone_mac):
        """
        # 根据phone_mac获取设备IP地址
        :param phone_mac: 设备MAC地址
        :return: 设备IP地址
        """
        wifi_url = 'http://192.168.1.1/'
        # 获取到WIFI路由器登录鉴权stok
        login_data = {"method": "do", "login": {"password": "QpQL48bA3eqVZwK"}}
        login_res = requests.post(url=wifi_url, json=login_data)
        login_res = json.loads(login_res.text)
        # 刷新连接设备列表，并获取IP地址
        ip_data = {"dhcpd": {"table": ["dhcp_clients"]}, "method": "get"}
        ip_res = requests.post(url=f"{wifi_url}stok={login_res['stok']}/ds", json=ip_data)
        ip_res = json.loads(ip_res.text)
        for i in range(len(ip_res["dhcpd"]["dhcp_clients"])):
            temp_mac = ip_res["dhcpd"]["dhcp_clients"][i][f"dhcp_clients_{i}"]["mac"]
            if temp_mac.replace("-", ":").upper() == phone_mac.upper():
                return ip_res["dhcpd"]["dhcp_clients"][i][f"dhcp_clients_{i}"]["ip"]

    @staticmethod
    def self_go_in_test(item_name, mode):
        """
        对外功能，调用此函数才能自动进入待测页面
        :param item_name:  待测页面的名称，即点击后才能进入待测页面的那个名称
        :param mode: 指定进入*#36446337#还是*#808#的测试
        """
        try:
            # 第一种方式，建议使用第一种方式；
            find_item = engineering.EngineerMode()
            find_item.step("自动寻路", testPage=item_name, mode=mode)
            # 第二种方式；
            # new = singleaction.SingleAction()
            # new.auto_find(item_name, mode)
        except Exception as e:
            return str(e)

    @staticmethod
    def self_click_element(element_key,device):
        """
        点击元素
        :param element_key: 字符串，与yaml文件一一对应
        :return:
        """
        click_element = singleaction.SingleAction(device)
        click_element.find_element(element_key).click()

    @staticmethod
    def self_input_send_keys(element_key, value):
        """
        输入框输入
        :param element_key: 字符串，与yaml文件一一对应
        :param value:
        :return:
        """
        # input_key = mobile_base.MobileBase()
        input_key = singleaction.SingleAction()
        input_key.input_send_keys(element_key, value)

    @staticmethod
    def self_adb_comm_execute(command, device, *args):
        """
        执行adb命令
        :param command: 命令行
        :param args: 参数
        :return:
        """
        comm_execute = mobile_base.MobileBase(device)
        comm_execute.adb_comm_execute(command, *args)

    @staticmethod
    def self_start_app(package_name, activity=None, stop=True):
        start_app = mobile_base.MobileBase()
        start_app.start_app(package_name, activity=activity, stop=stop)

    @staticmethod
    def self_find_element(element_key, time_out=0.1):
        """
        描述：查找元素
        :param time_out:查抄超时时间
        :param element_key:字符串，与yaml文件一一对应
        :return: 返回元素
        """
        find_element = mobile_base.MobileBase()
        return find_element.find_element(element_key)

    @staticmethod
    def self_go_in_feedback(mode,device):
        mobile = singleaction.SingleAction(device)
        mobile.set_dial_pan_to_default()
        mobile.dial_number(mode)

        # mobile.click_element(item_name)
        # mobile.click_element(item_name)
        # mobile.input_send_keys("问题描述",item_name+"测试（仅测试使用）")
        # mobile.click_element("back")
        # mobile.click_element("抓取日志")
        # mobile.click_element("开始抓取")
        # mobile.click_element("留在当前界面")
        # time.sleep(5)
        # mobile.click_element("完成抓取")
        # mobile.click_element("最近故障时间")
        # mobile.click_element("确定")
        # mobile.click_element("故障出现频率")
        # mobile.click_element("仅本次出现")
        # mobile.click_element("提交")






if __name__ == '__main__':
    cc = ControlPhone()
    cc.self_go_in_feedback("*#800#")
    # cc.connect_wifi()
    # cc.self_go_in_test('相机测试', '*#808#')
    # # cc = ControlPhone()
    # # cc.get_ip('74:EF:4B:AF:24:BB')
    cc.get_mac()
    # test = cc.self_go_in_test('相机测试', '*#808#')
    # print(cc[0])
