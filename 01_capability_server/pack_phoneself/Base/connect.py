# coding=utf-8

import re

import uiautomator2 as u2
from ppadb.client import Client

from pack_phoneself.Base.util import Log, subprocess_Popen


def get_adb_port():
    result = subprocess_Popen('set android_adb_server_port')
    code = str(result) if type(result) is bytes else result
    a_list = re.findall(r"[\d]+", code)
    port = 5037 if not len(a_list) else a_list[0]
    return int(port)


class Singleton(object):
    """A python style singleton"""
    Drivers = {}
    client = Client(port=get_adb_port())

    @property
    def adbClient(self):
        return self.client

    def get_id(self) -> str:
        pass

    def connect_device(self):
        device_id = self.get_id()
        device = self.Drivers.get(device_id)
        if device and device.healthcheck:
            return device
        for i in range(3):
            try:
                d = u2.connect(device_id)
                d.set_fastinput_ime(True)
                self.Drivers[device_id] = d
                Log.log_print(Log.Type.OTHER, '请求控制设备ID：%s' % device_id)
                return d
            except Exception as e:
                if 'java.lang.NullPointerException' in str(e) and '-32001' in str(e):
                    subprocess_Popen(f'adb -s {device_id} forward tcp:7912 tcp:7912')
                    result = subprocess_Popen('curl 127.0.0.1:7912/dump/hierarchy')
                    print(result)
                    subprocess_Popen('curl -X POST 127.0.0.1:7912/uiautomator')
                    continue
                Log.log_print(Log.Type.ERROR, str(e))


class Connect(Singleton):
    """
    与手机设备创建连接，与adb接口连接
    """

    def get_id(self):
        return self.device_id

    @property
    def device(self):
        device_driver = self.connect_device()
        return device_driver

    def __init__(self, device=None):
        """
        实例化
        :param device: Phone的IP 如192.168.1.18，Phone的ID，如EHGJUG8768JG
        """
        self.device = device

    @device.setter
    def device(self, device_id):
        """设置deviceID供外部设置参数"""
        devices = self.client.devices()
        if not devices:
            raise AssertionError('无设备在线，请连接设备')
        all_devices = list(map(lambda x: x.serial, devices))
        if device_id is None:
            self.device_id = all_devices[0]
        else:
            devices = [x for x in all_devices if device_id in x]
            if not devices:
                raise AssertionError('设备【%s】未连接至PC' % device_id)
            self.device_id = devices[0]
