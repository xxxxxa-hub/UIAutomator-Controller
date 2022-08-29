# coding=utf-8
import time

from pack_phoneself.Base.mobile_base import MobileBase, Log

PACKAGE = 'gpscom.gpsoppo.gpslocation.gnsstools'
TEST_ITEMS = ['GPS L1', 'GPS L5', 'GLO', 'GAL L1', 'GAL E5', 'BDS', 'QZSS']


class SearchStar(MobileBase):

    def return_class_name(self):
        return __class__

    def start_gps_app(self):
        self.start_app(PACKAGE)
        return self

    def stop_gps_app(self):
        self.stop_app(PACKAGE)

    def go_test_page(self):
        self.wait_key_word_exist('OppoGnssTools', 20)
        self.click_element('菜单按钮')
        time.sleep(1)
        self.wait_key_word_exist('GPS信号强度')
        self.click_element('GPS信号强度')
        time.sleep(1)
        self.wait_key_word_exist('开始测试')
        self.click_element('开始测试')
        self.wait_key_word_not_exist('开始测试')
        return self

    def get_all(self):
        items_dict = {}
        self.wait_key_word_exist('Svid', 30)
        for item in TEST_ITEMS:
            element_dict = self.replace_element_info('测试项', item)
            value = self.find_element(element_dict).get_text()
            items_dict[item] = value
        return items_dict

    def get_test_items(self, duration_time):
        count = 0
        self.stop_gps_app()
        self.start_gps_app().go_test_page()
        time.sleep(duration_time)
        items_info = self.get_all()
        for key, value in items_info.items():
            if not value:
                count += 1
        if count == len(TEST_ITEMS):
            self.get_test_items(duration_time)
        self.stop_app(PACKAGE)
        return items_info

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

    def du_women_navigation(self):
        """
        进入百度导航搜索  北京西站-上海火车站-地铁站 路线，然后点击开始导航
        :return:
        """
        self.stop_app('com.baidu.BaiduMap')
        self.driver.implicitly_wait(3)
        self.start_app('com.baidu.BaiduMap')
        self.driver.implicitly_wait(10)
        self.find_element('度娘搜路线').click()
        self.wait_element_exist('度娘输入起点', 10)
        self.find_element('度娘输入起点').set_text('北京西站')
        self.wait_element_exist('丰台区火车站', 10).click()
        self.wait_element_exist('度娘输入终点', 10)
        self.find_element('度娘输入终点').set_text('上海火车站')
        self.wait_element_exist('上海火车站-地铁站', 10).click()
        self.wait_element_exist('度娘开始导航', 30).click()
        if self.find_elements('百度地图导航使用提示'):
            self.click_element('百度地图导航使用提示')
        if len(self.find_elements('退出', 2)) == 0:
            self.du_women_navigation()

    def high_de_navigation(self):
        """
        进入高德地图搜索  北京天安门-上海迪士尼度假区检票口 路线，然后模拟导航
        :return:
        """
        self.stop_app('com.autonavi.minimap')
        self.driver.implicitly_wait(3)
        self.start_app('com.autonavi.minimap', 'com.autonavi.map.activity.NewMapActivity', False)
        self.driver.implicitly_wait(10)
        self.find_element('德子驾车').click()
        self.wait_element_exist('我的位置', 10)
        self.click_element('我的位置')
        elements = self.find_elements('我的位置', 10)
        if elements:
            self.input_send_keys('我的位置', '北京天安门')
        else:
            self.input_send_keys('我的位置绿', '北京天安门')
        self.wait_element_exist('天安门', 10).click()
        self.wait_element_exist('德子输入终点', 10)
        self.find_element('德子输入终点').set_text('上海迪士尼度假区')
        self.wait_element_exist('上海迪士尼度假区检票口', 10).click()
        self.wait_key_word_exist('开始导航', 10)
        self.click_element_with_swipe('模拟导航', '上',duration=0.1)
        # if len(self.find_elements('德子暂停', 2)) == 0:
        #     self.high_de_navigation()

    def start_gnss_app(self):
        self.start_app('com.locationtest.gnsshelper', stop=False)
        elements = self.find_elements('跟踪测试', 5)
        if elements:
            elements[0].click()

    def begin_or_stop_test(self, btn):
        self.start_gnss_app()
        self.wait_key_word_exist('开始测试')
        if btn == "开始测试":
            for i in range(2):
                self.click_element('Gnss开始测试')
                elements = self.find_elements('允许通知开关', 5)
                if elements:
                    if elements[0].text == "关闭":
                        elements[0].click()
                        self.stop_app('com.locationtest.gnsshelper')
                        self.start_gnss_app()
                else:
                    break
        else:
            self.click_element('停止测试')

    def get_current_app_package_name(self):
        # print(self.driver.app_current())
        print(self.driver.dump_hierarchy())
        # self.input_send_keys('我的位置绿', '北京天安门')


if __name__ == "__main__":
    star = SearchStar()
    # star.get_current_app_package_name()
    star.high_de_navigation()
