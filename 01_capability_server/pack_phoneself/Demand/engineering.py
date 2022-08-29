# coding=utf-8
from pack_phoneself.Base.util import subprocess_Popen
from pack_phoneself.PhoneSet.quick_settings import QuickSet
from pack_phoneself.Demand.singleaction import SingleAction


class WLANStop(object):
    def __init__(self, device_id=None):
        self.quick = QuickSet(device_id)

    def stop_wlan(self, **kwargs):
        self.quick.screen_light_unlock()
        self.quick.search_wlan_switch_off()


class EngineerMode(object):
    def __init__(self, device_id=None):
        self.action = SingleAction(device_id)
        subprocess_Popen('adb start-server')

    def step(self, action, *args, **kwargs):
        txt = args[0] if args else ''
        if action == '点亮屏幕':
            self.action.screen_light_unlock()
        elif action == '调起拨号键盘':
            self.action.set_dial_pan_to_default()
        elif action == '工模输入':
            self.action.dial_number(txt)
        elif action == '测试类型路径':
            self.action.go_target_page(txt)
        elif action == '点击测试类型':
            self.action.click_label(txt)
        elif action == '点击按钮或文字':
            self.action.click_text(txt)
        elif action == '点选选项':
            self.action.set_multi_option_parameter(kwargs)
        elif action == '左侧输入框输入':
            self.action.input_left_value(kwargs)
        elif action == '右侧输入框输入':
            self.action.input_right_value(kwargs)
        elif action == '勾选复选框':
            self.action.check_box_click(txt)
        elif action == '勾选单选框':
            self.action.check_box_click(txt)
        elif action == '弹窗按钮':
            self.action.alert_click(txt)
        elif action == '获取结果':
            return self.action.get_the_result(txt)
        elif action == '抓取页面内容':
            return self.action.get_page_item()
        elif action == '点击屏中心':
            self.action.tap_fix_point(txt)
        elif action == 'adb命令行':
            self.action.adb_comm_execute(txt)
        elif action == 'MTK_TX专项':
            self.action.mtk_tx_test()
        elif action == '退出页面':
            self.action.kill_current_app()
        elif action == '自动寻路':
            name, mode = kwargs.get('testPage'), kwargs.get('mode')
            self.action.auto_find(item_name=name, mode=mode)
        else:
            raise Exception('动作：【%s】 输入有误，请重新输入' % action)
        return self


if __name__ == '__main__':
    xx = EngineerMode()

    xx.step('自动寻路', testPage='产线测试 11', mode='*#36446337#')
    xx.step('自动寻路', testPage='蓝牙测试', mode='*#36446337#')
    xx.step('自动寻路', testPage='Wifi Calling', mode='*#36446337#')
    xx.step('自动寻路', testPage='wifi SAR测试', mode='*#808#')

    # xx.step('点选选项', **{'Set preferred network type:': 'NR only', })
    # xx.step('自动寻路', testPage='CFU', mode='*#36446337#').step('自动寻路', testPage='Audio', mode='*#36446337#')
    # xx = EngineerMode('192.168.1.102')  # 数据线连接手机到电脑上，cmd命令 adb devices 查看设备id
    # xx.step('点亮屏幕').step('调起拨号键盘').step('工模输入', '*#818#').step('点击按钮或文字', '自动搜网')

    # xx.step('点亮屏幕').step('调起拨号键盘').step('工模输入', '*#808#').step('测试类型路径', '设备调试-Camera-媒体调试-WCN')
    # xx.step("点击测试类型", 'wifi SAR测试')
    # xx.step("点选选项", **{'测试区域': '欧洲CE', '5G测试信道': '5180(Band1)', 'Sensor状态': '接近'})
    # xx.step('点击按钮或文字', '进入测试模式')

    # WLANStop('KVSKLJPBDY8HMZFI').stop_wlan()
    # xx = EngineerMode('192.168.1.99')
    # xx.step('调起拨号键盘').step('工模输入', '*#36446337#').step('点击测试类型', '工程模式').step('测试类型路径',
    #                                                                                        'Telephony-Connectivity')
    # xx.step('点击测试类型', 'WiFi').step('MTK_TX专项')
    # xx = EngineerMode('KVSKLJPBDY8HMZFI')
    # xx.step('点击按钮或文字', 'WF1')
    # xx.step('点选选项', **{'Tx0 channel': '6 [2437MHz]', })
    # xx.step('右侧输入框输入', **{'Pkt cnt': '2048', })

    # wifi_switch = WLANStop()
    # wifi_switch.stop_wlan()
    # xx = EngineerMode()
    # xx.step('点亮屏幕').step('调起拨号键盘').step('工模输入', '*#36446337#')#.step('点击测试类型', '工程模式')
    # xx.step('测试类型路径', 'Telephony-Connectivity')
    #
    # xx.step('点击测试类型', 'WiFi').step('MTK_TX专项')
    # xx = EngineerMode()
    # xx.step('点击按钮或文字', 'WF1')
    # xx.step('点选选项', **{'Tx0 channel': '6 [2437MHz]', })
    # xx.step('点选选项', **{'Channel Bandwidth': 'BW20', })
    # xx.step('点选选项', **{'Data Bandwidth': 'BW20', })
    # xx.step('点选选项', **{'Primary Ch': '0', })
    # xx.step('点选选项', **{'Mode': 'continuous packet tx', })
    # xx.step('点击按钮或文字', '1')
    # xx.step('右侧输入框输入', **{'Pkt length': '1024', })
    # xx.step('右侧输入框输入', **{'Pkt cnt': '0', })
    # xx.step('点选选项', **{'Preamble': 'CCK', })
    # xx.step('点选选项', **{'Rate': '1M', })
    # xx.step('点选选项', **{'Guard interval': 'normal GI', })
    # xx.step('点选选项', **{'FEC': 'BCC', })
    # xx.step('右侧输入框输入', **{'Tx power (dBm)': '18.0', })
    # xx.step('右侧输入框输入', **{'Inter packet gap [0~255]': '50', })
    # xx.step('点击按钮或文字', 'GO')
