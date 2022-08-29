# coding=utf-8
import time
from pack_phoneself.Base.mobile_base import MobileBase, Log
from pack_phoneself.Demand.auto_engineer import EngineerAuto
from pack_phoneself.mySql.sqlite import Sqlite


class SingleAction(MobileBase):

    def return_class_name(self):
        return __class__

    # 设置拨号键盘
    def set_dial_pan_to_default(self):
        """
        描述：启动拨号键盘，并使拨号键盘输入为默认[空]
        :return:
        """
        try:
            if not self.driver.beenClick:
                raise AssertionError
        except:
            self.driver.app_stop_all()
            self.adb_comm_execute('adb shell am force-stop com.android.contacts')
            self.adb_comm_execute('adb shell input keyevent KEYCODE_CALL')
        element = self.wait_element_exist(self.replace_element_info('dial_key', 'star'), 2)
        if not element:
            dial_pan = self.wait_element_exist('dial_pan', 1)
            if dial_pan:
                dial_pan.click()
                self.driver.beenClick = True
            else:
                self.find_element('dial_pan')
                self.driver.beenClick = False
            self.set_dial_pan_to_default()
        else:
            self.driver.beenClick = False
            Log.log_print(Log.Type.OTHER, '调起拨号键盘')
            return self

    def go_target_page(self, targetpath):
        """
        描述：根据targetpath提供的路径，进入目标页面
        :param targetpath: 参数中必须包含分隔符-
        :return: self
        """
        self.driver.implicitly_wait(3)
        if not targetpath:
            return self
        if '-' not in targetpath:
            return {'Result': False, 'Reason': '路径中必须包含“-”'}
        if targetpath[-1] == "-":
            targetpath = targetpath[:-1]
        step_list = targetpath.split('-')
        if self.MTK:
            self.white_mode(step_list[-1])
            Log.log_print(Log.Type.OTHER, 'MTK测试类型路径:%s' % targetpath)
        else:
            self.black_mode(step_list)
            Log.log_print(Log.Type.OTHER, '测试类型路径:%s' % targetpath)

    def white_mode(self, target, direction="左"):
        element_dict = self.replace_element_info('setting_engineer_mode', target, target)
        self.swipe_element_to_middle(element_dict, direction)

    def black_mode(self, minlist):
        for xx in minlist:
            temp = self.replace_element_info('black_mode', xx, xx)
            self.wait_key_word_exist(xx)
            self.click_element(temp)
            self.driver.implicitly_wait(3)
        return self

    # 点击指定页面中选择测试项
    def click_label(self, name):
        """
                描述：点击目标页面的label或者按钮
                :param name: label或按钮名称
                :return: Null
                                            """
        if not name:
            return self
        self.driver.implicitly_wait(10)
        element_dict = self.replace_element_info('click_label', name)
        self._swipe_direction(element_dict)
        return self

    def click_horizon_label(self, name):
        element_dict = self.replace_element_info('horizon_label', name, name)
        self.click_element(element_dict)

    # 点击按钮或文字
    def click_text(self, name):
        if not name:
            return self
        self.wait_key_word_exist(name)
        self.driver.implicitly_wait(10)
        element_dict = self.replace_element_info('click_text', name, name)
        self._swipe_direction(element_dict)
        return self

    # 点击同一行文字右侧按钮
    def click_text_right_Bt(self, name):
        if not name:
            return self
        # self.get_page_source()
        self.wait_key_word_exist(name)
        self.driver.implicitly_wait(10)
        element_dict = self.replace_element_info('QC_all_port_key', name)
        self._swipe_direction(element_dict)
        return self

    def get_bt_info(self, name):
        if not name:
            return self
        self.wait_key_word_exist(name)
        self.driver.implicitly_wait(10)
        element_dict = self.replace_element_info('QC_all_port_key', name)
        element = self.find_element(element_dict)
        if element.get_text() == '关闭':
            return False
        else:
            return True

    # 多个选项 类似wifi SAR测试
    def set_multi_option_parameter(self, option_dict):
        """
        描述：页面中有选项供选择，格式比如：测试区域 v  印度
        :param option_dict: 传参字典
        :return: self
        """
        if not option_dict:
            return self
        for lefttag, value in option_dict.items():
            self.wait_key_word_exist(lefttag)
            lefttag_xpath = self.replace_element_info('lefttag', lefttag)
            if type(value) is str:
                if self.find_element(lefttag_xpath).get_text() != value:
                    self.click_element_with_swipe(lefttag_xpath, '上')
                    self.wait_key_word_exist(value)
                    self._swipe_direction(self.replace_element_info('rightvalue', value))
            if type(value) is list:
                elements = self.find_elements(lefttag_xpath)
                for i in range(len(elements)):
                    if not value[i]:
                        return self
                    if elements[i].text == value[i]:
                        continue
                    elements[i].click()
                    self.wait_key_word_exist(value[i])
                    self._swipe_direction(self.replace_element_info('rightvalue', value[i]))
        return self

    def _swipe_direction(self, element_dict):
        if not self.find_elements(element_dict, sec=2):
            self.back_top()
        self.click_element_with_swipe(element_dict, '上', scroll_times=20)

    def input_left_value(self, input_dict):
        for key, value in input_dict.items():
            element_dict = self.replace_element_info('input_left_value', key)
            self.input_send_keys(element_dict, value)

    def input_right_value(self, input_dict):
        for key, value in input_dict.items():
            element_dict = self.replace_element_info('input_right_value', key)
            self.input_send_keys(element_dict, value)

    def check_box_click(self, box_name):
        element_dict = self.replace_element_info('click_text', box_name)
        self.find_element(element_dict).click()

    def alert_click(self, alert_btn):
        element_dict = self.replace_element_info('click_text', alert_btn)
        self.find_element(element_dict).click()

    def alert_input(self, input_txt):
        # self.get_page_source()
        element_dict = self.replace_element_info('alrt_input')
        self.input_send_keys(element_dict, input_txt)

    def get_the_result(self, standup, wait_times=30):
        for i in range(wait_times):
            result = self.driver.dump_hierarchy()
            if standup in result:
                return 'Success'
            else:
                time.sleep(1)
        return 'Fail'

    def get_page_item(self):
        valueDict = {}
        elementKeys = self.find_elements('Charger')
        for element in elementKeys:
            ele_dict = self.replace_element_info('ChargerValue', element.text)
            value_ele = self.find_element(ele_dict)
            valueDict[element.text] = value_ele.get_text()
        return valueDict

    def tap_fix_point(self, tap_times=1):
        # 点击手机屏幕中心点
        for i in range(tap_times):
            self.tap(0.5, 0.5)

    def mtk_tx_test(self):
        element = self.find_element('mtk_tx_test')
        point_x, point_y = element.center()
        self.adb_comm_execute('adb shell am force-stop %s' % 'com.github.uiautomator')
        time.sleep(0.5)
        command = 'adb -s shell input tap {} {}'
        self.adb_comm_execute(command.format(point_x, point_y))
        time.sleep(0.5)
        return True

    def kill_current_app(self):
        packages = self.driver.app_current()
        self.stop_app(packages.get('package'))

    def auto_find(self, item_name, mode):
        db = Sqlite('engineer.db')
        eng = EngineerAuto(db, self)
        eng.go_in_test(item_name, mode)

    def get_page_source(self):
        # print(self.driver.app_current())
        page = self.driver.dump_hierarchy()
        self.driver.info.get('productName')
        print(page)


if __name__ == '__main__':
    # ui = SingleAction('OZFUAIKB99QO9HX4')
    ui = SingleAction()
    ui.get_page_source()

    # ui.set_dial_pan_to_default()
    # ui.dial_number('*#99#')
    # ui.mtk_tx_test()
    # {'package': 'com.google.android.dialer', 'activity': 'com.android.dialer.main.impl.MainActivity', 'pid': 25709}
    # {'package': 'com.google.android.dialer', 'activity': '.extensions.GoogleDialtactsActivity', 'pid': 11996}
    # ui = SingleAction('426e4468')
    # com.google.android.dialer/.extensions.GoogleDialtactsActivity
    # ui.click_label('CW Test')
    # resource-device_id="com.google.android.dialer:device_id/digits"
