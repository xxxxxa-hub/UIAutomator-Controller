# coding=utf-8
import time

from pack_phoneself.Base.util import Log


class EngineerAuto(object):

    def __init__(self, db, parent=None):
        self.swipe_list = ("Telephony", "Connectivity", "Hardware Testing", "Location", "Log and Debugging", "Others")
        self.tab_list = ("产线测试项", "设备调试", "Camera", "媒体调试", "WCN", "通信调试", "其他")
        self.current_item = None
        self.db = db
        self.action = parent

    @classmethod
    def build(cls, device):
        cls(device)

    def get_sql_data(self, value, mode=None):
        """
        描述：拨号键盘输入
        :param mode: 工程模式类型，*#808#  或  *#36446337#
        :param value: 正常输入
        :return: search_list,包含字典的数组
        """
        search_list = []
        if mode:
            comm = 'SELECT * FROM {} WHERE {}="{}" and code="{}";'
        else:
            comm = 'SELECT * FROM {} WHERE {}="{}";'
        for i in range(65, 76):
            if i + 1 >= 76:
                break
            sql = comm.format(self.action.hardware, chr(i), value, mode)
            search_list = search_list + self.db.select_all(sql, params=None)
        return search_list

    def go_in_test(self, item_name, mode):
        """
        对外功能，调用此函数才能自动进入待测页面
        :param item_name:  待测页面的名称，即点击后才能进入待测页面的那个名称
        :param mode: 指定进入*#36446337#还是*#808#的测试
        """

        curr_path = self.get_current_page_path()
        Log.log_print(Log.Type.OTHER, '当前处于：', curr_path)
        date_sql = self.get_sql_data(item_name, mode)
        if not date_sql:
            Log.log_print(Log.Type.ERROR, '%s的 %s 模式不包含 %s' % (self.action.hardware, mode, item_name))
            return False
        des_path = self.get_dict_from_list(date_sql, [item_name, ])
        Log.log_print(Log.Type.OTHER, '预设页面：', des_path)
        if not curr_path or curr_path.get('code')[0] != mode:
            self.action.set_dial_pan_to_default()
            self.action.dial_number(mode)
            same_mode = False
        else:
            self.action.MTK = 1 if mode == '*#36446337#' else 0
            same_mode = True
        _, des_mode = curr_path.pop('code') if curr_path else None, des_path.pop('code')[0]
        des_list = list(map(lambda x: des_path.get(x)[0], des_path))
        if same_mode:
            curr_list = list(map(lambda x: curr_path.get(x)[0], curr_path))
            self.had_in_engineer(curr_list, des_list, item_name)
        else:
            self.into_engineer_from_desktop(des_list, item_name)
        return True

    def had_in_engineer(self, curr_list, des_list, item_name):
        """
        针对当前页已经在工程模式下，需要判断待测页面与当前页面所需返回次数
        :param curr_list: 数组，当前页面的所有路径信息
        :param des_list: 数组， 进入待测页面的所有路径信息
        :param item_name: 待测页面的名称，即点击后才能进入待测页面的那个名称
        """
        temp_des = des_list + [item_name]
        if temp_des == curr_list and len(temp_des) == len(curr_list):
            return
        back_target = None
        mode_list = self.swipe_list if self.action.MTK else self.tab_list
        for curr, temp in zip(curr_list, temp_des):
            if curr == temp:
                des_list.remove(curr)
            else:
                if curr in mode_list and temp in mode_list:
                    back_target = curr
                    break
        if back_target:
            curr_dict = self.action.replace_element_info('EngineerMode', back_target)
        else:
            temp_value = curr_list[0] if curr_list else None
            curr_dict = self.action.replace_element_info('click_label', temp_value)
        for i in range(len(curr_list)):
            if len(self.action.find_elements(curr_dict, 2)):
                break
            else:
                self.action.adb_comm_execute('adb shell input keyevent 4')
        self.into_engineer_from_desktop(des_list, item_name)

    def into_engineer_from_desktop(self, des_list, item_name):
        """
        从手机桌面进入工程模式的待测页面
        :param des_list: 数组，包含从桌面进入待测页面的元素信息，form 数据库
        :param item_name: 测试项名称
        """
        for des in des_list:
            if not self.action.MTK:
                if des in self.tab_list:
                    self.select_tab_by_click(des)
            else:
                if des in self.swipe_list:
                    self.select_tab_by_swipe(des)
                elif des in self.tab_list:
                    self.action.click_horizon_label(des)
                else:
                    self.action.click_label(des)
        self.action.click_label(item_name)

    def select_tab_by_swipe(self, tab):
        """
        主要针对*#36446337#的工程模式， 根据self.swipe_list的顺序，判断向左或向右滑动，滑动到待测标题下
        :param tab: 页面标题头
        :return: 返回 True  or False
        """
        if tab not in self.swipe_list:
            return False
        x = 5
        while x:
            dst_index = self.swipe_list.index(tab)
            elements = self.action.find_elements('white_page_titles', 4)
            if not elements:
                x = x - 1
                continue
            if len(elements) == 2 and elements[0].text == self.swipe_list[0]:
                elements = [elements[0], ] + elements
            curr_index = self.swipe_list.index(elements[1].text)
            for i in range(abs(dst_index - curr_index)):
                if dst_index > curr_index:
                    self.action.white_mode(tab, "左")
                elif dst_index < curr_index:
                    self.action.white_mode(tab, "右")
            if curr_index != dst_index:
                x = x - 1
            else:
                break

    def select_tab_by_click(self, tab):
        """
        主要针对*#808#，自动拼接路径 产线测试项-设备调试-Camera，只要测试项在*#808#中，就无需再重新调用键盘进行输入
        :param tab: 页面标题头
        :return: 返回 True  or False
        """
        if tab not in self.tab_list:
            return False
        time.sleep(1)
        elements = self.action.find_elements('工程模式')
        if self.current_item:
            cur_tab = self.current_item
        else:
            cur_tab = elements[0].text
        if cur_tab in self.tab_list:
            cur_index = self.tab_list.index(cur_tab)
        else:
            new_tabList = [x.lower() for x in self.tab_list]
            cur_index = new_tabList.index(cur_tab.lower())
        dst_index = self.tab_list.index(tab)
        begin, end = (cur_index, dst_index) if cur_index < dst_index else (dst_index, cur_index)
        tab_step = list(self.tab_list[begin:end + 1])
        if cur_index > dst_index:
            tab_step.reverse()
        self.action.black_mode(tab_step)
        return True

    def get_current_page_path(self):
        """
        获取当前页面所有text属性不为空的元素，传入get_dict_from_list进行处理
        return:{'code': '*#808#', 'A': 'Telephony', 'B': 'CFU'}
        思路：数据库中查找带有*#808#，*#36446337#的所有数据，数据多方被选
        """
        pL = self.action.driver.app_current()
        if pL.get('package') == 'com.android.launcher':
            return None
        date_sql3644 = []
        date_sql808 = []
        elements = self.action.find_elements('所有非空元素')
        current_ele_list = []
        for element in elements:
            if element.center()[1] > self.action.rec.get('height') * 0.078:
                current_ele_list.append(element.text)
                date_sql808 += self.get_sql_data(element.text, '*#808#')
                date_sql3644 += self.get_sql_data(element.text, '*#36446337#')
        search_list = date_sql3644 if len(date_sql3644) > len(date_sql808) else date_sql808
        result = self.get_dict_from_list(search_list, current_ele_list)
        return result

    def get_dict_from_list(self, values: list, text_list: list):
        """
        将从数据库中传来的数据进行整合判断当前或者预设的测试项
        :param values: 数据库中读取的数据
        :param text_list: 当前页面的所有测试项的文字
        return:{'code': '*#808#', 'A': 'Telephony', 'B': 'CFU'}
        思路：从values计算出出现次数最多的key,通过key多少来进行判断截取的长度
        """
        temp_dict, key_list = {}, []
        x, tag = 0, ''
        for value in values:
            for key, item in value.items():
                if item in text_list and item is not None:
                    key_list.append(key)
                    break
        for key in key_list:
            if key_list.count(key) > x:
                x = key_list.count(key)
                tag = key
        for value in values:
            for key, item in value.items():
                if key in temp_dict.keys():
                    if item not in temp_dict.get(key) and key == tag:
                        temp_dict[key].append(item)
                else:
                    if item is not None:
                        temp_dict[key] = [item, ]
                if item in text_list:
                    break
        if not temp_dict: return temp_dict
        if tag == "": return temp_dict
        for i in range(ord(tag), 76):
            if chr(i) in temp_dict.keys():
                temp_dict.pop(chr(i))
            else:
                break
        return temp_dict


if __name__ == "__main__":
    auto = EngineerAuto('192.168.1.77')
    # auto.get_current_page_path()
    # auto.go_in_test('wifi SAR测试', '*#808#')
    # auto.go_in_test('Audio', '*#36446337#')
    # print(auto.action.driver.dump_hierarchy())
    print(auto.action.driver.xpath().info)
    auto.action.driver(resourceId="com.nextdoordeveloper.miperf.miperf:id/swStart").click()
    time.sleep(2)
    print(auto.action.driver(resourceId="com.nextdoordeveloper.miperf.miperf:id/swStart").info)
