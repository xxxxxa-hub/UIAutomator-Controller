# coding=utf-8
import threading
import time
from pack_phoneself.Base.mobile_base import MobileBase, Log
from pack_phoneself.Demand.engineering import EngineerMode
from pack_phoneself.PhoneSet.settings import Settings


class NFC(MobileBase):
    def return_class_name(self):
        return __class__

    def install_app(self, app_path):
        # 准备弃用，手动点击,因为安装过程中有个安装按钮无法找到
        app_path, user_psd = r'D:\NFCApp.apk', 'dbt123!@#'
        threading.Thread(target=self.driver.app_install, args=(app_path,)).start()
        time.sleep(3)
        elements = self.find_elements(self.all_xpath.get('安装'))
        if elements:
            self.driver.send_keys(user_psd)
            time.sleep(2)
            elements[0].click()
        # 图片点击他娘的不靠谱，找不到哇
        self.driver.image.click('test.png')

    def app_start(self):
        # 启动APP
        self.start_app('com.fangka.nfcapp')
        self.driver.implicitly_wait(2)
        self.swipe_and_find_element(self.replace_element_info('栏位名称', '新建标签'))
        # if self.find_elements('初启弹窗'):
        #     self.click_element('初启弹窗')
        return self

    def go_new_tag(self):
        # 进入新建标签页面
        self.wait_key_word_exist('工具箱', 10)
        self.click_element(self.replace_element_info('栏位名称', '新建标签'))
        self.wait_key_word_exist('文本', 10)
        self.click_element(self.replace_element_info('栏位名称', '文本'))
        return self

    def write_txt_tag(self, target):
        # 输入新标签内容
        self.wait_key_word_exist('输入文本信息')
        for i in range(3):
            element = self.find_element('文本信息输入框')
            if element.text != target:
                element.set_text('')
                element.set_text(target)
                time.sleep(1)
            else:
                break
        self.click_element('下一步')

    def store_tag_to_card(self, append=None, wait_time=30):
        # 刷卡，存入卡片新标签，机械手寻找到卡片后，调用此函数，完成数据存入卡片，供下次读取
        temp = None
        if append:
            self.click_element('追加模式')
        for i in range(wait_time):
            temp = self.wait_element_exist('保存结果', 30).text
            if temp:
                return temp
            else:
                time.sleep(1)
        return temp

    def screen_light_on_off(self, switch):
        """
        亮屏，灭屏
        :return:
        """
        try:
            if switch == 'on':
                self.screen_light_unlock()
            else:
                self.driver.screen_off()
            return 'Success'
        except:
            return 'False'

    def screen_always_on(self):
        """
        屏幕常亮
        :return:
        """
        try:
            engineer = EngineerMode(self.device_id)
            engineer.step("调起拨号键盘").step("工模输入", "*#99#")
            return 'Success'
        except:
            return 'False'

    def enable_Embedded_SE(self):
        """
        进入*#808# 中 勾选 Embedded SE
        :return:
        """
        try:
            engineer = EngineerMode(self.device_id)
            engineer.step("调起拨号键盘").step("工模输入", "*#808#").step("测试类型路径", "设备调试-Camera-媒体调试-WCN")
            engineer.step("点击测试类型", "NFC测试").step("点击按钮或文字", "Embedded SE")
            return 'Success'
        except:
            return 'False'

    def get_nfc_tag_value(self):
        """
        机械手移动手机，使用此函数抓取卡片内容，并返回给调用方
        :return:返回字符类型
        """
        # 抓取NFC新标签内容，并返回
        tags_text = []
        self.go_back_home()
        elements = self.find_elements('新标签已收集', 30)
        if elements:
            elements[0].click()
            self.driver.implicitly_wait(3)
            self.wait_element_exist('新标签已收集', 10)
            tag_elements = self.find_elements('所有标签内容', 10)
            for tag in tag_elements:
                tags_text.append(tag.text)
        return tags_text

    def write_new_tag_into_card(self, target_txt, append=None, wait_time=50):
        """
        启动app,新建标签内容，输入内容，存入内容进入卡片
        :param wait_time: 等待写入成功时长
        :param append: 存入标签的模式，是否追加模式
        :param target_txt:标签内容
        :return:返回字符类型
        """
        self.app_start().go_new_tag()
        self.write_txt_tag(target_txt)
        result = self.store_tag_to_card(append, wait_time)
        return result

    def phone_power_on(self, minutes=2):
        """
        进定时开关机，设定好几分钟后开机，执行关机命令
        :param minutes: 单位分钟
        :return: 返回启动时间，如17:30
        """
        try:
            on_time = Settings(self.device_id).power_on_time(minutes)
            return on_time
        except:
            return None

    def switch_nfc_enable(self, switch='enable'):
        """
        开启或关闭NFC
        :param switch: enable or disable
        :return:
        """
        try:
            self.adb_comm_execute('adb shell svc nfc %s' % switch)
            return 'Success'
        except:
            return 'False'

    def touch_pay(self, pay_type):
        """
        选择触碰付款的付款类型，如钱包，支付宝等
        :param pay_type: 付款类型，钱包，支付宝
        :return:
        """
        try:
            Settings(self.device_id).touch_pay(pay_type)
            return 'Success'
        except:
            return 'False'

    def page_source(self):
        # "com.android.systemui:device_id/home"
        print(self.driver.app_current())
        # print(self.driver.dump_hierarchy())


if __name__ == "__main__":
    nfc = NFC()
    nfc.phone_power_on()
