# coding=utf-8

import time

from pack_phoneself.Base.mobile_base import MobileBase


class QuickSet(MobileBase):

    def return_class_name(self):
        return __class__

    def enter_quick_settings(self):
        for i in range(3):
            self.driver.open_quick_settings()
            if self.find_elements('WLAN', 2):
                break
            else:
                time.sleep(2)

    def search_wlan_switch_off(self):
        self.enter_quick_settings()
        self.driver.implicitly_wait(3)
        self.wait_key_word_exist('WLAN', 5)
        elements = self.find_elements('WLAN')
        if elements[0].text == "开启":
            elements[0].click()
        self.go_back_home()
        return True

    def fly_mode_settings(self, switch='on'):
        self.enter_quick_settings()
        self.driver.implicitly_wait(3)
        self.wait_key_word_exist('飞行模式', 5)
        elements = self.find_elements('飞行模式')
        if switch == 'on':
            if elements[0].text != "开启":
                elements[0].click()
        else:
            if elements[0].text != "关闭":
                elements[0].click()
        self.go_back_home()
        return True

    def search_gps_switch_on(self):
        """
        进入快捷设置，开启gps,然后回到首页
        :return:
        """
        for i in range(3):
            self.go_back_home()
            time.sleep(2)
            self.driver.open_quick_settings()
            if self.find_elements('关闭', 2):
                break
            else:
                time.sleep(2)
        self.driver.implicitly_wait(3)
        self.wait_key_word_exist('定位服务', 5)
        elements = self.find_elements('位置报告')
        if elements:
            element = elements[0]
        else:
            # element = self.swipe_and_find_element('定位服务', 0.9, 0.1, 0.5, 0.5)
            element = self.swipe_and_find_element('定位服务', "左")
        if element.text == "关闭":
            element.click()
        self.go_back_home()
        return True

    def page_source(self):
        print(self.driver.dump_hierarchy())


if __name__ == '__main__':
    quick = QuickSet()
    quick.fly_mode_settings('on')
    # quick.page_source()
