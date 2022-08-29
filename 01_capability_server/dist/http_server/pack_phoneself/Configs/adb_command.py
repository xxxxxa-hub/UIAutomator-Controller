# coding=utf-8
commands = {
    "设置音量": "adb shell service call audio 10 i32 %s i32 %s i32 1",
    "设置查找": "adb shell settings list system |find '%s'",
    "解锁屏幕": "adb shell input keyevent 82",
    "锁定屏幕": "shell input keyevent 26",
    "进入Home": "adb shell input keyevent KEYCODE_HOME",
    "物理返回": "adb shell input keyevent 4",
    # ------------------------------
    "飞行模式": "adb shell settings put global airplane_mode_on 1",
    "广播": "adb shell am broadcast -a android.intent.action.AIRPLANE_MODE --ez state true",
    # ------------------------------
    "清除缓存": "adb shell pm clear %s",
    "拨打电话": "adb shell am start -a android.intent.action.CALL -d tel:10086",
    "接听电话": "adb shell input keyevent 5",
    "查CPU型号": "adb shell cat /proc/cpuinfo|find 'Hardware'",
    "关闭亮度自动调节": "adb shell settings put system screen_brightness_mode 0",
    "设置当前屏幕亮度": "adb shell settings put system screen_brightness {} light = int((rate/100)*8200)",
    "屏幕长亮": "adb shell svc power stayon true",
    "打开蓝牙": "adb shell service call bluetooth_manager 6",
    "关闭蓝牙": "adb shell service call bluetooth_manager 9",
    # ------------------------------
    "进入WIFI设置": "adb shell am start -a android.intent.action.MAIN -n com.android.settings/.wifi.WifiSettings",
    "打开wifi": "adb shell svc wifi enable",
    "关闭wifi": "adb shell svc wifi disable",
    # ------------------------------
    "强制停止": 'adb shell am force-stop %s',
    "NFC开关": 'adb shell svc nfc %s',
    "获取当前使用WIFI名": 'adb shell dumpsys connectivity | findstr "state: CONNECTED/CONNECTED"',
    # ------------------------------
    "短信内容": 'adb shell am start -a android.intent.action.SENDTO -d sms:10086 --es sms_body  hello',
    '聚焦发送': 'adb shell input keyevent 22',
    '回车发送': 'adb shell input keyevent 66 ',
    '获取手机名称': 'adb shell getprop ro.product.model',
    '获取手机版本': 'adb shell getprop ro.build.version.release',
    '获取手机厂商': 'adb shell getprop ro.product.brand',
    '获取系统属性名': 'adb shell getprop | grep product',
    '获取到电话状态': 'adb shell dumpsys telephony.registry'

}


class ADB(object):
    _comm = None

    def __init__(self, comm):
        self.comm = comm

    def execute(self, *args):
        command = self._comm.replace('%s', '{}')
        comm = command.format(*args)
        if 'findstr' in comm:
            comm = comm.replace('findstr', 'grep')
        if 'shell' in comm:
            result = comm.split('shell')[-1]
        else:
            result = None
        return result

    @property
    def comm(self):
        return self._comm

    @comm.setter
    def comm(self, value):
        self._comm = commands.get(value)


class ADB2(object):

    def __init__(self, comm):
        self.comm = comm

    def execute2(self, *args):
        new_comm = commands.get(self.comm).replace('%s', '{}')
        comm = new_comm.format(*args)
        return comm


print(ADB2("设置音量").execute2(1, 2))
