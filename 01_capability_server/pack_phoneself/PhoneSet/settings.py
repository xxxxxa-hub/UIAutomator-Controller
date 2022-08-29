# coding=utf-8
import time

from pack_phoneself.Base.mobile_base import MobileBase
import re


class Settings(MobileBase):

    def return_class_name(self):
        return __class__

    def into_settings(self):
        """
        进入手机的设置页
        :return:
        """
        self.stop_app('com.android.settings')
        self.go_back_home()
        self.start_app('com.android.settings')

    def connect_wlan(self):
        self.click_element(self.replace_element_info('WLAN名称', 'WLAN'))
        self.wait_key_word_exist('oppo')
        self.click_element(self.replace_element_info('WLAN名称', 'oppo'))

    def search(self, value):
        """
        搜索框中输入搜索项
        :param value: 搜索项名称
        :return:
        """
        self.into_settings()
        self.wait_key_word_exist("设置")
        # self.driver(scrollable=True).scroll.toBeginning()
        self.input_send_keys('搜索设置项', value)
        return self

    def select_search_result(self, result):
        self.click_element(self.replace_element_info('选择搜索结果', result))
        self.driver.implicitly_wait(1.5)
        return self

    def goto_select_ring(self, audioName, play_type="录音"):
        if self.find_elements(self.replace_element_info('音乐.录音', play_type), 2):
            self.adb_comm_execute('adb shell input keyevent 4')
        else:
            self.search('电话铃声').wait_key_word_exist("声音与振动")
            self.select_search_result('电话铃声')
            self.click_element(self.replace_element_info('选择搜索结果', '电话铃声'))
            self.wait_key_word_exist('从文件中选择')
        self.click_element(self.replace_element_info('选择搜索结果', '从文件中选择'))
        self.wait_key_word_exist('音乐')
        self.click_element(self.replace_element_info('音乐.录音', play_type))
        # -------------选择铃声----------------
        element_dict = self.replace_element_info('音频名称', audioName)
        self.click_element_with_swipe(element_dict, '上', scroll_times=20)

    def power_time_off(self):
        """
        关机
        :return:
        """
        self.adb_comm_execute('adb shell reboot -p')

    def power_on_time(self, time_duration=2):
        """
        进入设置，搜索定时开关机，选择启动时间后，关机
        :param time_duration: 几分钟后开机
        :return:
        """
        self.search("定时开关机")
        self.wait_key_word_exist('其他设置')
        self.click_element('定时开关机')
        self.wait_key_word_exist('每天', 10)
        elements = self.find_elements('定时开始开关')
        if elements[0].text == '关闭':
            elements[0].click()
        on_time = self.set_power_on_time(time_duration)
        self.power_time_off()
        return on_time

    def set_power_on_time(self, minute_duration=2):
        """
        计算开机时间，滑动时间轮盘，选择开机时间
        :param minute_duration: 时长，几分钟后开机
        :return:
        """
        # Tue Sep 28 16:31:53 CST 2021   09:01
        minute_duration = int(minute_duration)
        if minute_duration > 59:
            return ''
        msystem_time = self.adb_comm_execute('adb shell "date"')
        ms_time = re.findall(r"(\d{1,2}:\d{1,2})", msystem_time)[0]
        ms_hour, ms_minutes = int(ms_time[:2]), int(ms_time[-2:])
        if ms_minutes + minute_duration >= 60:
            on_hour, on_minutes = ms_hour + 1, ms_minutes + minute_duration - 60
        else:
            on_hour, on_minutes = ms_hour, ms_minutes + minute_duration
        if on_hour - 24 >= 0:
            on_hour = on_hour - 24
        p_show = self.find_element('开机时间').get_text()
        p_hour, p_minutes = int(p_show[:2]), int(p_show[-2:])
        self.click_element('开机时间')
        self.wait_element_exist('时间轮盘')
        element = self.find_element('时间轮盘')
        top_x, top_y, left_x, left_y = element.bounds()
        unit_duration = (left_y - top_y) / 5
        dict_3 = {'center': element.center(), 'current': p_hour, 'settings': on_hour, 'type': 'hour'}
        self.scroll_time_picker(dict_3, unit_duration)
        dict_3 = {'center': element.center(), 'current': p_minutes, 'settings': on_minutes, 'type': 'minutes'}
        self.scroll_time_picker(dict_3, unit_duration)
        self.click_element('保存选择')
        time.sleep(0.5)
        p_show = self.find_element('开机时间').get_text()
        p_hour, p_minutes = int(p_show[:2]), int(p_show[-2:])
        if p_hour == on_hour and p_minutes == on_minutes:
            return p_show
        else:
            self.set_power_on_time(minute_duration)

    def scroll_time_picker(self, center: dict, duration):
        """
        计算当前选择时间，与预设时间需要滑动的次数
        :param center: 时间轮盘的中心点，参数类型字典
        :param duration: 两个时间的最小单位距离，浮点型参数
        :return:
        """
        center_x, center_y = center.get('center')
        cur_hour = center.get('current')
        set_hour = center.get('settings')
        set_type = center.get('type')
        biv, vic = (24, 0.5) if set_type == 'hour' else (60, 1.3)
        if cur_hour > set_hour:
            if biv - (cur_hour - set_hour) * 2 <= 0:
                steps, direction = biv - (cur_hour - set_hour), 'up'
            else:
                steps, direction = cur_hour - set_hour, 'down'
        else:
            if biv - (set_hour - cur_hour) * 2 <= 0:
                steps, direction = biv - (set_hour - cur_hour), 'down'
            else:
                steps, direction = set_hour - cur_hour, 'up'
        if direction == 'up':
            bx, ex, by, ey = [center_x * vic, center_x * vic, center_y, center_y - duration * 1.25]
        else:
            bx, ex, by, ey = [center_x * vic, center_x * vic, center_y - duration * 1.25, center_y]
        for i in range(steps):
            self.drag_in_element(bx, ex, by, ey, 0.2)

    def touch_pay(self, pay_type):
        # 触碰付款
        element_dict = self.replace_element_info('默认付款应用', pay_type)
        self.search("触碰付款")
        for i in range(2):
            self.wait_element_exist('触碰付款')
            self.click_element('触碰付款')
        self.wait_element_exist(element_dict)
        self.click_element(element_dict)

    def set_hot_point(self, account, password):
        self.search('个人热点')
        time.sleep(1)
        self.click_element('个人热点设置')
        time.sleep(0.5)
        self.click_element('个人热点设置')
        self.wait_key_word_exist('名称')
        element = self.find_element(self.replace_element_info('名称密码', '名称'))
        if element.get_text() != account:
            element.click()
            time.sleep(0.3)
            self.click_element(self.replace_element_info('删除', '名称'))
            self.input_send_keys(self.replace_element_info('名称密码', '名称'), account)
        element = self.find_element(self.replace_element_info('名称密码', '密码'))
        if element.get_text() != password:
            element.click()
            time.sleep(0.3)
            self.click_element(self.replace_element_info('删除', '密码'))
            self.input_send_keys(self.replace_element_info('名称密码', '密码'), password)
            self.click_element('收起安全键盘')
            self.click_element(self.replace_element_info('名称密码', '名称'))

    def page_source(self):
        print(self.driver.app_current())
        print(self.driver.dump_hierarchy())


if __name__ == "__main__":
    settings = Settings()
    # settings.page_source()
    settings.search('附加费积分')
