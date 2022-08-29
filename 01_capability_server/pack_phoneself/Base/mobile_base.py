# coding=utf-8
import copy
from threading import Thread, Event

from pack_phoneself.Base.connect import Connect
from pack_phoneself.Base.util import *
from pack_phoneself.Base.submit_record import submit_record


def power_on_u2(self):
    self.adb_comm_execute('adb shell pm clear com.github.uiautomator')
    subprocess_Popen(f'adb -s {self.device_id} forward tcp:7912 tcp:7912')
    subprocess_Popen('curl 127.0.0.1:7912/dump/hierarchy')
    subprocess_Popen('curl -X POST 127.0.0.1:7912/uiautomator')

    device_id = self.device_id.split(':')[0] if ':' in self.device_id else self.device_id
    self.alert_exist = False
    self.connect.device = device_id
    self.driver = self.connect.device


class MobileBase(object):
    MTK = 0
    black_list = {"USB 用于": "传输文件", "无法连接到移动网络": "知道了"}
    move_rec = {'上': (0.5, 0.5, 0.8, 0.2), '下': (0.5, 0.5, 0.2, 0.8),
                '左': (0.85, 0.01, 0.5, 0.5), '右': (0.15, 0.99, 0.5, 0.5)}
    direction_dict = {"上": "up", "下": "down", "左": "left", "右": "right"}

    def __init__(self, device_id=None):
        self.connect = Connect(device_id)
        self.alert_exist, self.patrol = False, True
        self.driver, self.client = self.connect.device, self.connect.adbClient
        self.device_id = self.connect.device.serial
        self.hardware = self.get_phone_hardware()
        self.all_xpath = self.read_yaml()
        self.b_box = self.black_dict()
        ProcessAlert(self).start()
        self.rec = {'left': 0, 'top': 0, 'width': self.driver.window_size()[0], 'height': self.driver.window_size()[1]}
        self.screen_light_unlock()

    def read_yaml(self):
        class_name = re.findall(r"\.(.*?)'>", str(self.return_class_name()))[0].split('.')[-1]
        obj_yaml = YamlDate()
        yaml_dates = obj_yaml.read(class_name)
        yaml_dates.update(obj_yaml.read(__class__.__name__))
        return yaml_dates

    def return_class_name(self):
        # 获取class name，包括子类
        return __class__

    def black_dict(self):
        # 获取子类的异常弹窗信息
        if '黑名单' in self.all_xpath.keys():
            return self.all_xpath.get('黑名单')
        return {}

    def start_app(self, package_name, activity=None, stop=True):
        """
        启动apk，通过包名启动，最好带上activity
        """
        Log.log_print(Log.Type.START_APP, package_name)
        for i in range(10):
            result = self.driver.app_current()
            if package_name != result.get('package'):
                self.driver.app_start(package_name, activity, stop)
                self.driver.app_wait(package_name, 10)
            else:
                break
        Log.log_print(Log.Type.APP_STARTED, package_name)
        return self

    def stop_app(self, package_name):
        """通过包名关闭apk"""
        try:
            Log.log_print(Log.Type.STOP_APP, package_name)
            self.driver.app_stop(package_name)
        except:
            pass

    def screen_light_unlock(self):
        # 点亮解锁屏幕
        if self.driver.info.get('screenOn') is False:
            Log.log_print(Log.Type.SCREEN_ON, self.device_id)
            self.driver.screen_on()
            time.sleep(0.5)


        if os.popen('adb -s %s shell dumpsys window policy |find "mIsShowing"' %(self.device_id)).readline().strip('\n').split('=')[-1] == 'true':
            self.adb_comm_execute('adb -s %s shell input keyevent 82' %(self.device_id))
            time.sleep(0.5)
            self.adb_comm_execute('adb -s %s shell input keyevent KEYCODE_HOME' %(self.device_id))

        if self.driver.info.get('screenOn') is False:
            Log.log_print(Log.Type.SCREEN_ON, self.device_id)
            result = self.adb_comm_execute('adb shell dumpsys window displays | findstr mAwake')
            if 'mAwake=false mScreenOnEarly=false mScreenOnFully=false' in result:
                self.adb_comm_execute('adb shell input keyevent KEYCODE_POWER')

        if os.popen('adb shell dumpsys window policy |find "mIsShowing"').readline().strip('\n').split('=')[-1] == 'true':
            self.adb_comm_execute('adb shell input keyevent 82')
            status_bar = self.adb_comm_execute('adb shell dumpsys window policy |find "isStatusBarKeyguard"')
            lock_screen = self.adb_comm_execute('adb shell dumpsys window policy |find "mShowingLockscreen"')
            if not status_bar and not lock_screen:
                self.adb_comm_execute('adb shell input keyevent KEYCODE_MENU')

    def go_back_home(self):
        # 返回主桌面
        if not self.driver(resourceId="com.android.launcher:id/workspace").exists:
            self.adb_comm_execute('adb -s {} shell input keyevent KEYCODE_HOME')  # 返回主桌面

    def get_phone_hardware(self):
        """获取硬件信息"""
        result = self.adb_comm_execute('adb shell grep "Hardware" /proc/cpuinfo')
        if result == '':
            temp = self.adb_comm_execute('adb shell ls -h /proc/mtk*')
            hardware = 'Qualcomm' if 'No such file or directory' in temp else 'MTK'
        else:
            hardware = 'MTK' if 'mt' in result.lower() else 'Qualcomm'
        return hardware

    def replace_element_info(self, element_key, *args):
        """
        获取Yaml文件对应函数的元素定位，并填充对应参数（包含%s或{}）
        """
        xpath_dict = {}
        if type(element_key) is dict:
            pass
        else:
            element_dict = self.all_xpath.get(element_key)
            if self.hardware in element_dict.keys():
                info = element_dict.get('info')
                ele_dict = element_dict.get(self.hardware)
                ele_dict.update({'info': info})
                element_dict = ele_dict
            info, by_type, type_value = element_dict.get('info'), element_dict.get('type'), element_dict.get(
                'typeValue')
            if '%s' in type_value:
                type_value = type_value.replace('%s', '{}')
            if not info:
                info = element_key + "-> {}" if len(args) else element_key
            else:
                info = info.replace('%s', '{}') if "%s" in info else info + '-> {}' if len(args) else info
            xpath_dict['info'] = info.format(args[0]) if len(args) else info
            xpath_dict['type'] = by_type
            if len(args) < type_value.count('{}'):
                args = args * type_value.count('{}')
            xpath_dict['typeValue'] = type_value.format(*args)
        return xpath_dict

    def get_element_dict(self, element):
        element_dict = {}
        if type(element) is str:
            temp = self.all_xpath.get(element)
            if self.hardware in temp.keys():
                info = temp.get('info')
                ele_dict = temp.get(self.hardware)
                ele_dict.update({'info': info})
                temp = ele_dict
            if not temp.get('info'):
                temp.update({'info': element})
            element_dict = temp
        elif type(element) is dict:
            element_dict = element
        return element_dict

    def find_element(self, element_key, time_out=0.1):
        """
        描述：查找元素
        :param time_out:查抄超时时间
        :param element_key:字符串，与yaml文件一一对应
        :return: 返回元素
        """
        xpath_dict, element = self.get_element_dict(element_key), None
        find_by, type_value = xpath_dict.get('type'), xpath_dict.get('typeValue')
        self.black_list.update(self.b_box)
        for i in range(len(self.black_list)):
            if find_by == 'xpath':
                if self.driver.xpath(type_value).exists:
                    element = self.driver.xpath(type_value)
            else:
                if self.driver(**{find_by: type_value}).exists:
                    element = self.driver(**{find_by: type_value})
            if element:
                Log.log_print(Log.Type.ELEMENT_FINDED, xpath_dict.get('info'))
                return element
            else:
                self.wait_kill_alert()
        Log.log_print(Log.Type.FIND_ERROR, xpath_dict.get('info'))
        self.patrol = False
        raise AssertionError('当前页面未包含【%s】' % element_key)

    def find_elements(self, element_key, sec=10):
        """
        查找元素集合
        :param element_key: 字符串，与yaml文件一一对应
        :param sec: 超时时间
        :return: 元素集
        """
        xpath_dict = self.get_element_dict(element_key)
        find_by, type_value = xpath_dict.get('type'), xpath_dict.get('typeValue')
        for i in range(sec):
            try:
                if find_by != 'xpath':
                    # if self.driver(**{find_by: type_value}).exists:
                    elements = [self.driver(**{find_by: type_value})]
                else:
                    elements = self.driver.xpath(type_value).all()
                if elements:
                    Log.log_print(Log.Type.ELEMENTS_FINDED, xpath_dict.get('info'))
                    return elements
                else:
                    self.wait_kill_alert()
            except:
                power_on_u2(self)
                continue
        Log.log_print(Log.Type.FIND_ERROR, xpath_dict.get('info'))
        return []

    def wait_kill_alert(self):
        while self.alert_exist:
            time.sleep(2)

    def click_element(self, element_key):
        """
        点击元素
        :param element_key: 字符串，与yaml文件一一对应
        :return:
        """
        xpath_dict = self.get_element_dict(element_key)
        self.find_element(element_key).click()
        Log.log_print(Log.Type.CLICK, xpath_dict.get('info'))

    def input_send_keys(self, element_key, value):
        """
        输入框输入
        :param element_key: 字符串，与yaml文件一一对应
        :param value:
        :return:
        """
        xpath_dict = self.get_element_dict(element_key)
        self.driver.set_fastinput_ime(True)
        element = self.find_element(element_key)
        element.set_text(value)
        # element.send_keys(value)
        Log.log_print(Log.Type.INPUT, xpath_dict.get('info'), value)

    def click_element_with_swipe(self, element_key, direction=None, duration=0.5, scroll_times=5):
        """
        滑动查找元素
        :param duration:
        :param element_key: 字符串，与yaml文件一一对应
        :param direction: 滑动方向，value：上下左右
        :param scroll_times: 滑动次数
        :return:
        """
        if direction:
            self.swipe_and_find_element(element_key, direction, duration, scroll_times)
            time.sleep(1)
            self.click_element(element_key)

    def back_top(self):
        """回到顶部"""
        try:
            self.driver(scrollable=True).scroll.toBeginning()
        except:
            pass

    def swipe_and_find_element(self, element, direction="上", duration=0.5, scroll_times=5):
        """
        描述：滑动页面查找元素
        :param duration: 滑动间隔
        :param direction: 方向
        :param element:字符串，与yaml文件一一对应
        :param scroll_times:滑动次数
        :return:返回元素
        """
        for i in range(scroll_times):
            elements = self.find_elements(element, 2)
            if elements:
                return elements[0]
            x1, x2, y1, y2 = self.move_rec.get(direction)
            w, h = self.rec.get('width'), self.rec.get('height')
            self.driver.swipe(x1 * w, y1 * h, x2 * w, y2 * h, duration)
            if i > 0:
                time.sleep(1)
                continue
            Log.log_print(Log.Type.SWIPE, str(i + 1))
        self.patrol = False
        raise Exception('经过%s次滑动，未找到【%s】' % (scroll_times, element))

    def drag_in_element(self, begin_x, end_x, begin_y, end_y, duration=0.5):
        """
        根据坐标进行滑动，精细操作
        :param begin_x: 起点x坐标
        :param end_x: 终点x坐标
        :param begin_y: 起点y坐标
        :param end_y: 终点y坐标
        :param duration: 起点到终点用时
        :return:
        """
        self.driver.drag(begin_x, begin_y, end_x, end_y, duration)

    def adb_comm_execute(self, command, *args):
        """
        执行adb命令
        :param command: 命令行
        :param args: 参数
        :return:
        """
        device = self.client.device(self.device_id)
        command = command.replace('%s', '{}')
        withS = re.findall(r'adb -s (.*?) ', command)
        if withS and withS[0] == '{}':
            comm = command.format(self.device_id, *args)
        else:
            comm = command.format(*args)
        Log.log_print(Log.Type.ADB, comm)
        if 'findstr' in comm:
            comm = comm.replace('findstr', 'grep')
        if 'shell' in comm:
            exe_comm = comm.split('shell')[-1]
            temp = device.shell(exe_comm)
            result = re.sub(r'\n|\t|\r', '', temp)
        else:
            result = None
            Log.log_print(Log.Type.ERROR, '暂时仅支持adb shell')
        Log.log_print(Log.Type.HAD_ADB, "ADB 命令执行结束")
        return result

    def tap(self, x, y):
        """
        adb点击
        :param x: x坐标,宽度的百分比
        :param y: y坐标，高度的百分比
        :return:
        """
        x = self.rec.get('width') * x
        y = self.rec.get('height') * y
        # command = 'adb -s {} shell input tap {} {}'
        # self.adb_comm_execute(command, x, y)
        self.driver.click(x, y)

    def wait_element_exist(self, element_dict, sec=10):
        """
        等待元素存在
        :param element_dict: 字符串
        :param sec:
        :return:
        """
        for i in range(sec):
            elements = self.find_elements(element_dict, 2)
            if elements:
                return elements[0]
            else:
                time.sleep(0.5)
        return None

    def wait_element_disappear(self, element_key, sec=10):
        """
        等待元素消失
        :param element_key:字符串，与yaml文件一一对应
        :param sec:超时时间
        :return:
        """
        for i in range(sec):
            if not self.find_elements(element_key, 4):
                Log.log_print(Log.Type.OTHER, '%s 已消失' % element_key)
                return True
            else:
                time.sleep(0.5)
        Log.log_print(Log.Type.ERROR, '%s 未消失' % element_key)
        return False

    def wait_key_word_exist(self, txt, wait_times=10):
        """
        等待关键字存在，页面文字
        :param txt: 页面必然存在的文字
        :param wait_times: 超时时间
        :return:
        """
        for i in range(wait_times):
            page_source = self.driver.dump_hierarchy()
            self.driver.implicitly_wait(3)
            if txt in page_source:
                break
            else:
                time.sleep(0.5)
        return self

    def wait_key_word_not_exist(self, txt, wait_times=10):
        """
        等待关键字消失，页面文字
        :param txt: 页面必然存在的文字
        :param wait_times: 超时时间
        :return:
        """
        for i in range(wait_times):
            page_source = self.driver.dump_hierarchy()
            self.driver.implicitly_wait(3)
            if txt not in page_source:
                break
            else:
                time.sleep(0.5)
        return self

    def swipe_element_to_middle(self, element_key, direction="左"):
        """
        描述：先左滑查找到元素，然后判断元素是否在title的中间，不在则向左或向右滑动
        :param element_key: 字符串，与yaml文件一一对应
        :param direction: 上下左右
        :return:
        """
        #
        self.driver.implicitly_wait(10)
        x_round = self.rec.get('width') / 3
        for i in range(3):
            elements = self.find_elements(element_key, 2)
            if elements:
                if elements[0].bounds[0] - x_round * 2 > 0:
                    self.driver.swipe_ext("left")
                elif elements[0].bounds[0] - x_round < 0:
                    self.driver.swipe_ext("right")
                else:
                    return elements[0]
            else:
                self.swipe_and_find_element(element_key, direction, duration=0.2, scroll_times=10)
        return self

    def push_file(self, pc_path=None, audio_name=None, name=None):
        """
        导入指定文件到手机的sdcard
        :param name: 存入手机后的音频文件名
        :param pc_path:PC端的音源路径
        :param audio_name:Pc端的音频名
        :return:
        """
        push_result = False
        name = audio_name if not name else name
        abs_path = pc_path
        if not os.path.isabs(pc_path):
            abs_path = os.path.abspath(pc_path)
        if abs_path[-2:] != '\\':
            audio_file = abs_path + '\\' + audio_name
        else:
            audio_file = abs_path + audio_name
        for i in range(3):
            if not self.adb_comm_execute('adb shell ls /sdcard | grep "%s"' % name):
                self.driver.push(audio_file, "/sdcard/%s" % name)
            else:
                push_result = True
                break
        if not push_result:
            Log.log_print(Log.Type.ERROR, "adb push %s 到 sdcard 失败！！" % audio_name)

    def move_file(self, file_name, des_path, name=None):
        """
        从sdcard目录下移动到手机中的指定路径下
        :param file_name:被移动的文件名
        :param des_path: 指定目录，格式：/Music/Recordings/
        :param name:移动到指定文件夹后的存储名，为None时与file_name一致
        eg:'mv /sdcard/Call.txt /sdcard/Music/Recordings/Standard\ Recordings/Css.txt'
        """
        mv = False
        name = file_name if not name else name
        comm = 'adb shell mv '
        sdcard = '/sdcard/' + file_name + ' '
        des_full = '/sdcard' + des_path + name
        for i in range(3):
            if self.adb_comm_execute('adb shell ls ' + '/sdcard' + des_path + ' | grep "%s"' % name):
                mv = True
                break
            else:
                self.adb_comm_execute(comm + sdcard + des_full)
        if not mv:
            Log.log_print(Log.Type.ERROR, "mv %s 到 %s 失败！！" % (file_name, '/sdcard' + des_path))

    def pull_file(self, sd_path, audio_name, pc_path=None):
        """
        从手机sdcard导出音频文件到指定文档
        :param sd_path: 手机sdcard路径
        :param audio_name: 音频文件名称
        :param pc_path: PC端存储路径
        :return:
        """
        abs_path = pc_path
        if not os.path.isabs(pc_path):
            abs_path = os.path.abspath(pc_path)
        if abs_path[-2:] != '\\':
            audio_file = abs_path + '\\' + audio_name
        else:
            audio_file = abs_path + audio_name
        if not os.path.isabs(sd_path):
            sd_path = os.path.abspath(sd_path)
        sd_name = sd_path + audio_name
        self.driver.pull(sd_name, audio_file)

    def long_click(self, element_key, time_out: float = 5):
        """
        长按按钮
        :param element_key: 元素信息
        :param time_out: 按压时间
        :return:
        """
        x, y = self.find_element(element_key).center()
        self.driver.long_click(x, y, time_out)

    def dial_number(self, value, input_type='adb', dialOut=False):
        """
        描述：拨号键盘输入
        :param dialOut:拨号呼出开关
        :param input_type: adb:adb 输入；dial: 拨号输入
        :param value: 正常输入
        :return: self
        """
        if not value:
            return self
        self.MTK = 1 if value == '*#36446337#' else 0
        pan_dict = self.all_xpath.get('pan_dict')
        Log.log_print(Log.Type.OTHER, '拨号键盘输入：%s' % value)
        self.wait_key_word_exist('star')
        if input_type == 'adb':
            self.adb_comm_execute('adb shell service call phone 1 s16 "{}"'.format(value[:-1].replace('#', '%23')))
            self.click_element(self.replace_element_info('dial_key', pan_dict['#']))
        else:
            for char in value:
                self.click_element(self.replace_element_info('dial_key', pan_dict[char]))
            self.driver.implicitly_wait(1)
        if dialOut:
            ret = re.match(r"^1[35678]\d{9}$", value)
            if '*#' not in value and value.isdigit() and ret and len(value) == 11:
                self.click_element(self.replace_element_info('dial_key', pan_dict['dial']))
        return self


class ProcessAlert(Thread):

    def __init__(self, parent):
        Thread.__init__(self, daemon=True)
        self.base = parent

    def run(self):
        xpath = '//*[contains(@text, "{0}") or contains(@content-desc, "{0}") or contains(@resource-id, "{0}")]'
        self.base.black_list.update(self.base.b_box)
        temp_dict = copy.deepcopy(self.base.black_list)
        while self.base.patrol:
            for key, value in temp_dict.items():
                values = []
                try:
                    if value == "无相关撤销动作":
                        if self.base.driver.xpath(xpath.format(key)).all():
                            self.base.tap(0.5, 0.8)  # 点击屏幕某处取消弹窗
                    if self.base.driver.xpath(xpath.format(key)).all():
                        self.base.alert_exist = True
                        if type(value) is not list:
                            values.append(value)
                        else:
                            values = values + value
                        for txt in values:
                            if self.__deal_alert(txt):
                                Log.log_print(Log.Type.BLACKBOX, key)
                                break
                    else:
                        self.base.alert_exist = False
                except Exception as e:
                    Log.log_print(Log.Type.ERROR, f"出现异常：{str(e)}")
                    self.base.alert_exist = True
                    power_on_u2(self.base)
                    break

    def __deal_alert(self, value):
        xpath, x = '//*[@text="{0}" or @content-desc="{0}" or @resource-id="{0}"]', 2
        while x:
            elements, alert_txt = self.base.driver.xpath(xpath.format(value)).all(), None
            for element in elements:
                if abs(len(element.text) - len(value)) <= 3:
                    alert_txt = element.text
                    element.click()
            if alert_txt:
                if not self.base.driver.xpath(xpath.format(alert_txt)).exists:
                    return True
            else:
                x = x - 1
                time.sleep(0.5)
        return False


if __name__ == "__main__":
    # nfc = Connect('99U4Z9K7M749PZUG')
    # print(nfc)
    pass
