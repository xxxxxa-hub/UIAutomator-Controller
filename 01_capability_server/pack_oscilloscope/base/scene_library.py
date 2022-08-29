from pack_oscilloscope.base import WIFI_control_phone
from pack_phoneself.Base import mobile_base
from pack_phoneself.Demand import singleaction
from pack_oscilloscope.base import USB_circuit_board
import os
import inspect
import time
import datetime
import threading
from uiautomator2.exceptions import XPathElementNotFoundError



def find_file(file_dir):
    file_list = []
    for i in os.walk(file_dir):
        for j in i[2]:
            if "kernel" in j:
                file_list.append(i[0]+"\\"+j)
                #file_list.append("/mnt/"+(i[0].replace("\\","/")+"/"+j).split(":")[0].lower()+(i[0].replace("\\","/")+"/"+j).split(":")[1])
    if len(file_list) == 1:
        return file_list[0]
    else:
        raise Exception("Found more than one files.")


class GoScene(object):
    def __init__(self, device):
        self.control_phone = WIFI_control_phone.ControlPhone()  # 连接控制手机方法
        self.device = device
        self.serialno = os.popen("adb -s %s shell getprop ro.serialno" %(self.device)).readline().strip('\n')

    @staticmethod
    def switch_test_item(item, scene):
        """
        场景库，需要长期增量维护不同的场景；
            1. artificial是人为控制场景，将返回对应的value值，建议在前端使用弹框提示处理；
            2. procedure是程序控制场景，返回对应的value方法函数名；
        :param item: 类别，artificial 或 procedure；
        :param scene: 类别下的对应场景；
        :return: value
        """
        switcher = {
            "artificial": {"SIM卡电源测试-1.8V": "请插入1.8V电压的SIM卡！",  # #  人为配合控制操作(返回对应提示信息，建议使用弹框提示处理)
                           "SIM卡电源测试-3V": "请插入3V电压的SIM卡！",  # #
                           "T卡电源": "请插入T卡，并播放T卡上的电影！",  # #
                           "NFC电源-刷卡": "请刷NFC卡！",   # #
                           "NFC电源-读卡器": "请刷NFC读卡器！",    # NFC电源-读卡器
                           "耳机接口电源-高通平台": "请插入耳机！", #
                           "耳机接口电源-MTK平台": "请插入耳机！", #
                           "WIFI/BT/GPS电源-蓝牙": "请连接蓝牙耳机！"
                           },
            "procedure": {"耳机接口电源-高通平台": "headset_qualcomm",  # 程序控制部分(返回对应的函数方法名，函数体自己根据场景编写代码)
                          "耳机接口电源-MTK平台": "headset_mtk", #
                          "模拟MIC电源": "simulation_mic",  # #
                          "数字MIC电源": "number_mic",  # #
                          "普通功放/智能功放电源-高通平台": "power_amplifier_qualcomm",   #
                          "普通功放/智能功放电源-MTK平台": "power_amplifier_mtk",   #
                          "CODEC电源-高通平台": "codec_qualcomm", #
                          "CODEC电源-MTK平台": "codec_mtk",  #
                          "前置摄像头电源": "front_camera",    # #
                          "后置主摄像头电源": "main_cameras",   # #
                          "后置广角摄像头电源": "wide_angle_camera", # #
                          "后置长焦摄像头电源": "telephoto_camera",  # #
                          "通用传感器电源-GSensor": "sensor_g_sensor", # #
                          "通用传感器电源-MSensor": "sensor_m_sensor",
                          "通用传感器电源-接近": "sensor_approach",
                          "通用传感器电源-光感": "sensor_light_sensor",
                          "指纹识别信号电源": "fingerprint_identifier", # #
                          "WIFI/BT/GPS电源-wifi": "short_distance_wifi",  # #
                          "WIFI/BT/GPS电源-蓝牙": "short_distance_bt",  # #
                          "主芯片供电电源": "main_chip",   # #
                          "射频PA供电电源-lte7-16db": "rf_pa_lte7_16db",  # #
                          "射频PA供电电源-lte3-16db": "rf_pa_lte3_16db",  # #
                          "射频PA供电电源-lte7-23db": "rf_pa_lte7_23db",  # #
                          "射频PA供电电源-lte3-23db": "rf_pa_lte3_23db",  # #
                          "USB接口相关电源": "usb_interface", # #
                          "EMMC相关电源": "emmc",   # #
                          "亮灭屏": "poweron_off",
                          "AOD": "AOD_on",
                          "黑屏手势": "BlankScreen_on"
                          }
        }
        return switcher.get(item, "未查询到对应的测试场景！").get(scene, "未查询到对应的测试场景！")

    # temp = switch_test_item(item)
    # if temp != "未查询到对应的测试场景！":
    #     box_info(temp)  # 弹窗提示配合，需要获取前端传入参数
    # if temp == "未查询到对应的测试场景！":
    #     log.exception(temp)

    def headset_qualcomm(self, *args):      # 耳机接口电源-高通平台
        self.control_phone.set_airplane_mode("off")     # 关闭飞行模式
        self.control_phone.self_go_in_test("RF测试工具", "*#808#")      # 进入到RF测试工具页面
        self.control_phone.self_click_element("PA_play")    # 点击PA打功率
        self.control_phone.self_click_element("GSM")    # 选择GSM单选按钮
        self.control_phone.self_click_element("TX_ON")  # 点击TX ON按钮
        self.control_phone.self_click_element("GET")    # 点击GET按钮
        self.control_phone.self_adb_comm_execute("adb shell input keyevent 3")  # 模拟按键HOME，返回主界面；
        try:
            self.control_phone.self_start_app("com.coloros.soundrecorder")  # 启动录音机(OPPO录音机)
            self.control_phone.self_click_element("start_record")  # 点击开始录音
        except:
            self.control_phone.self_start_app("com.oneplus.soundrecorder")  # 一加录音机
            self.control_phone.self_click_element("oneplus_start_record")     # 一加录音机开始录音

    def headset_mtk(self, *args):  # 耳机接口电源_MTK平台
        self.control_phone.set_airplane_mode("off")     # 关闭飞行模式
        self.control_phone.self_go_in_test("RF De-sense Test", "*#36446337#")  # 进入工模自动寻路；
        self.control_phone.self_click_element("TX_Test")  # TX Test元素不能使用自动寻路，需要自己根据xpath点击；
        self.control_phone.self_click_element("GSM_checkbox")  # 勾选GSM复选框；
        self.control_phone.self_input_send_keys("Test_Count", "100")  # 在Test Count输入框输入100；
        self.control_phone.self_click_element("START")  # 点击START按钮；
        self.control_phone.self_adb_comm_execute("adb shell input keyevent 3")  # 模拟按键HOME，返回主界面；
        try:
            self.control_phone.self_start_app("com.coloros.soundrecorder")  # 启动录音机(OPPO录音机)
            self.control_phone.self_click_element("start_record")  # 点击开始录音
        except:
            self.control_phone.self_start_app("com.oneplus.soundrecorder")  # 一加录音机
            self.control_phone.self_click_element("oneplus_start_record")     # 一加录音机开始录音

    def simulation_mic(self, *args):  # 模拟MIC电源
        self.control_phone.set_airplane_mode("off")     # 关闭飞行模式
        self.control_phone.self_adb_comm_execute("adb shell input keyevent 3")  # 模拟按键HOME，返回主界面；
        try:
            self.control_phone.self_start_app("com.coloros.soundrecorder")  # 启动录音机(OPPO录音机)
            self.control_phone.self_click_element("start_record")  # 点击开始录音
        except:
            self.control_phone.self_start_app("com.oneplus.soundrecorder")  # 一加录音机
            self.control_phone.self_click_element("oneplus_start_record")     # 一加录音机开始录音

    def number_mic(self, *args):  # 数字MIC电源
        # 设置——Breeno——Breeno 语音  开启语音唤醒功能(未找到);   使用小布助手;
        self.control_phone.set_airplane_mode("off")     # 关闭飞行模式
        self.control_phone.self_start_app("com.heytap.speechassist")    # 启动小布助手
        try:
            try:
                self.control_phone.self_click_element("jurisdiction_allow")     # 处理允许按钮
            except: pass
            self.control_phone.self_click_element("phone_move_protocol")    # 处理用户须知弹框
        except: pass
        try:
            self.control_phone.self_click_element("dialog_cancel")  # 点击体验取消按钮
        except: pass
        self.control_phone.self_click_element("config")     # 点击设置按钮
        self.control_phone.self_click_element("awaken")     # 点击语音唤醒
        self.control_phone.self_click_element("continue")       # 点击继续按钮

    def power_amplifier_qualcomm(self, *args):  # 普通功放/智能功放电源-高通平台
        self.control_phone.set_airplane_mode("off")     # 关闭飞行模式
        self.control_phone.self_go_in_test("RF测试工具", "*#808#")      # 进入到RF测试工具页面
        self.control_phone.self_click_element("PA_play")    # 点击PA打功率
        self.control_phone.self_click_element("GSM")    # 选择GSM单选按钮
        self.control_phone.self_click_element("TX_ON")  # 点击TX ON按钮
        self.control_phone.self_click_element("GET")    # 点击GET按钮
        self.control_phone.self_adb_comm_execute("adb shell input keyevent 3")  # 模拟按键HOME，返回主界面；
        # 拷贝白噪声音乐文件进入手机，打开手机播放
        file_path = inspect.getfile(inspect.currentframe()).replace("scene_library.py", '')     # 获取音乐绝对文件路径[路径最好不要包含中文]
        os.popen(fr"adb push {file_path}0db_white_noise.wav /sdcard/Music/Record/SoundRecord").read()     # 拷贝文件进入手机
        self.control_phone.self_start_app("com.google.android.apps.youtube.music")  # 打开谷歌音乐
        self.control_phone.self_click_element("devices_file")   # 点击仅设备文件
        self.control_phone.self_click_element("play_music")     # 点击歌曲列表
        for i in range(20):     # 模拟音量按键，调整最大音量
            self.control_phone.self_adb_comm_execute("adb shell input keyevent 24")
        self.control_phone.self_click_element("white_noise")    # 点击播放白噪声音乐

    def power_amplifier_mtk(self, *args):  # 普通功放/智能功放电源-MTK平台
        self.control_phone.set_airplane_mode("off")     # 关闭飞行模式
        self.control_phone.self_go_in_test("RF De-sense Test", "*#36446337#")  # 进入工模自动寻路；
        self.control_phone.self_click_element("TX_Test")  # TX Test元素不能使用自动寻路，需要自己根据xpath点击；
        self.control_phone.self_click_element("GSM_checkbox")  # 勾选GSM复选框；
        self.control_phone.self_input_send_keys("Test_Count", "100")  # 在Test Count输入框输入100；
        self.control_phone.self_click_element("START")  # 点击START按钮；
        self.control_phone.self_adb_comm_execute("adb shell input keyevent 3")  # 模拟按键HOME，返回主界面；
        # =====================================================播放指定音源（0db白噪，最大音量）=============================
        file_path = inspect.getfile(inspect.currentframe()).replace("scene_library.py", '')  # 获取音乐绝对文件路径[路径最好不要包含中文]
        os.popen(fr"adb push {file_path}0db_white_noise.wav /sdcard/Music/song").read()     # 拷贝文件进入手机
        for i in range(20):     # 模拟音量按键，调整最大音量
            self.control_phone.self_adb_comm_execute("adb shell input keyevent 24")
        self.control_phone.self_start_app("com.heytap.music")       # 启动音乐
        try:
            self.control_phone.self_click_element("music_protocol")  # 处理用户须知弹框
        except:
            pass
        self.control_phone.self_click_element("local_music")  # 点击音乐本地
        try:
            self.control_phone.self_click_element("immediately_play")  # 点击立即播放
        except:
            tap = mobile_base.MobileBase()
            tap.tap(0.5, 0.3)  # 根据坐标点击
        # =============================================无法确认歌曲名称====================================================

    def codec_qualcomm(self, *args):    # CODEC电源_高通平台
        self.control_phone.set_airplane_mode("off")     # 关闭飞行模式
        self.control_phone.self_go_in_test("RF测试工具", "*#808#")      # 进入到RF测试工具页面
        self.control_phone.self_click_element("PA_play")    # 点击PA打功率
        self.control_phone.self_click_element("GSM")    # 选择GSM单选按钮
        self.control_phone.self_click_element("TX_ON")  # 点击TX ON按钮
        self.control_phone.self_click_element("GET")    # 点击GET按钮
        self.control_phone.self_adb_comm_execute("adb shell input keyevent 3")  # 模拟按键HOME，返回主界面；
        try:
            self.control_phone.self_start_app("com.coloros.soundrecorder")  # 启动录音机(OPPO录音机)
            self.control_phone.self_click_element("start_record")  # 点击开始录音
        except:
            self.control_phone.self_start_app("com.oneplus.soundrecorder")  # 一加录音机
            self.control_phone.self_click_element("oneplus_start_record")     # 一加录音机开始录音

    def codec_mtk(self, *args):  # CODEC电源_MTK平台
        self.control_phone.set_airplane_mode("off")     # 关闭飞行模式
        # 设置——关于本机——版本信息——点击7次版本号让手机进入开发者模式
        self.control_phone.self_go_in_test("RF De-sense Test", "*#36446337#")  # 进入工模自动寻路；
        self.control_phone.self_click_element("TX_Test")  # TX Test元素不能使用自动寻路，需要自己根据xpath点击；
        self.control_phone.self_click_element("GSM_checkbox")  # 勾选GSM复选框；
        self.control_phone.self_input_send_keys("Test_Count", "100")  # 在Test Count输入框输入100；
        self.control_phone.self_click_element("START")  # 点击START按钮；
        self.control_phone.self_adb_comm_execute("adb shell input keyevent 3")  # 模拟按键HOME，返回主界面；
        self.control_phone.self_start_app("com.coloros.soundrecorder")  # 启动录音机
        self.control_phone.self_click_element("start_record")  # 点击开始录音

    def front_camera(self, *args):          # 打开前置摄像头
        self.control_phone.set_airplane_mode("off")     # 关闭飞行模式
        self.control_phone.self_start_app("com.oplus.camera")   # 启动相机
        try:
            self.control_phone.self_click_element("phone_move_protocol")    # 处理用户须知弹框_同意并使用
        except: pass
        try:
            self.control_phone.self_click_element("camera_location")    # 处理应用需要使用位置信息权限弹框
        except: pass
        try:
            self.control_phone.self_find_element("camera_preposition")      # 前置摄像头未出现，则点击后置摄像头切换按钮；
        except AssertionError:
            self.control_phone.self_click_element("camera_main")

    def main_cameras(self, *args):  # 打开后置主摄像头
        self.control_phone.set_airplane_mode("off")     # 关闭飞行模式
        self.control_phone.self_start_app("com.oplus.camera")   # 启动相机
        try:
            self.control_phone.self_click_element("phone_move_protocol")    # 处理用户须知弹框_同意并使用
        except: pass
        try:
            self.control_phone.self_click_element("camera_location")    # 处理应用需要使用位置信息权限弹框
        except: pass
        try:
            self.control_phone.self_find_element("camera_main")      # 主摄像头未出现，则点击前置摄像头切换按钮；
        except AssertionError:
            self.control_phone.self_click_element("camera_preposition")

    def wide_angle_camera(self, *args):
        # 打开广角摄像头（超广镜头）
        self.control_phone.set_airplane_mode("off")     # 关闭飞行模式
        self.main_cameras()     # 打开后置摄像头
        self.control_phone.self_click_element("camera_wide_angle")  # 点开调整转盘
        try:
            self.control_phone.self_click_element("x_wide_angle")   # 选择0.6X倍广角
        except:
            self.control_phone.self_click_element("camera_wide_angle")  # 点开调整转盘
            self.control_phone.self_click_element("x_wide_angle")  # 选择0.6X倍广角

    def telephoto_camera(self, *args):
        self.control_phone.set_airplane_mode("off")     # 关闭飞行模式
        # ================================================打开长焦摄像头【QQ糖项目没有长焦摄像头】=============================
        return "请手动打开长焦摄像头！"
        # self.main_cameras()  # 打开后置摄像头

    def sensor_g_sensor(self):  # GSensor
        self.control_phone.self_go_in_test("GSensor", "*#808#")  # 进入GSensor页面
        self.control_phone.self_click_element("GSensor")  # 点击进入GSensor页面

    def sensor_m_sensor(self):      # MSensor
        self.control_phone.self_go_in_test("MSensor", "*#808#")     # 进入MSensor页面

    def sensor_approach(self):      # 接近
        self.control_phone.self_go_in_test("接近传感测试", "*#808#")
        self.control_phone.self_click_element("approach")  # 接近功能测试

    def sensor_light_sensor(self):      # 光感
        self.control_phone.self_go_in_test("LightSensor", "*#808#")     # 点击进入光感测试页面
        self.control_phone.self_click_element("sensitization_sensor")   # 点击进入感光sensor测试页面

    def fingerprint_identifier(self, *args):    # 指纹识别信号电源
        # self.control_phone.self_go_in_test("指纹测试", "*#808#")
        return "请手动操作手机至测试场景！"
        # =================================================没有屏下指纹==============================================

    def short_distance_wifi(self):    # 短距离WIFI/BT蓝牙场景
        """
        # 1、WIFI上行传输 手机搬家（DUT作为上行机器）
        # 2、BT上行传输 蓝牙耳机播放歌曲（加州旅馆）
        """
        self.control_phone.self_start_app("com.coloros.backuprestore")      # 启动手机搬家APP
        try:
            self.control_phone.self_click_element("phone_move_protocol")    # 处理关闭协议“同意并使用”
        except: pass
        try:
            self.control_phone.self_click_element("jurisdiction_allow")     # 处理权限弹框_允许
        except: pass
        self.control_phone.self_click_element("this_old")   # 点击“这是旧设备”
        try:
            self.control_phone.self_click_element("jurisdiction_allow")     # 处理权限弹框_允许
        except: pass
        try:
            self.control_phone.self_click_element("camera_location")    # 相机权限
            self.control_phone.self_click_element("camera_location")    # 手机搬家位置权限
            self.control_phone.self_click_element("jurisdiction_allow")     # 已安装应用信息
        except: pass
        return "请扫码连接！"
        # ==================================================提示用户扫码========================================

    def short_distance_bt(self):
        """
        短距离——蓝牙
        """
        # 连接蓝牙耳机
        file_path = inspect.getfile(inspect.currentframe()).replace("scene_library.py",
                                                                    '')  # 获取音乐绝对文件路径[路径最好不要包含中文]
        test = os.popen(fr"adb push {file_path}CalifoniaHotel.flac /sdcard/Music/song").read()  # 拷贝文件进入手机
        print(test)
        self.control_phone.self_start_app("com.heytap.music")  # 启动音乐
        try:
            self.control_phone.self_click_element("music_protocol")  # 处理用户须知弹框
        except:
            pass
        self.control_phone.self_click_element("local_music")  # 点击音乐本地
        try:
            self.control_phone.self_click_element("scan")   # 点击扫描
        except: pass
        self.control_phone.self_click_element("back")   # 点击返回
        try:
            self.control_phone.self_click_element("immediately_play")  # 点击立即播放
        except:
            tap = mobile_base.MobileBase()
            tap.tap(0.5, 0.3)   # 根据坐标点击

    def main_chip(self, *args):    # 主芯片供电电源
        # 连接WiFi，优酷在线播放视频
        self.control_phone.self_start_app("com.youku.phone")    # 启动优酷视频
        try:
            self.control_phone.self_click_element("youku_protocol")     # 处理启动优酷温馨提示信息
        except: pass
        try:
            self.control_phone.self_click_element("youku_know")        # 处理权限申请_我知道了
        except: pass
        try:
            self.control_phone.self_click_element("jurisdiction_allow")     # 电话权限申请_允许
        except: pass
        try:
            self.control_phone.self_click_element("youku_know")       # 青少年模式_我知道了
        except: pass
        try:
            self.control_phone.self_click_element("youku_update")       # 更新弹框提示_稍后
        except: pass
        self.control_phone.self_click_element("youku_play")     # 优酷播放_猜你再追

    def rf_pa_lte3_23db(self):
        # 工模射频PA打功率，LTE7或者LTE3  23db 和16db，测试两个纹波波形
        self.control_phone.self_go_in_test("RF测试工具", "*#808#")
        self.control_phone.self_click_element("pa_play")    # 点击进入PA打功率
        self.control_phone.self_click_element("lte")    # 选择LTE
        self.control_phone.self_click_element("band_select_box")
        self.control_phone.self_click_element("lte_b3")
        self.control_phone.self_input_send_keys("edit_power", 23)  # 输入测试功率值
        self.control_phone.self_click_element("TX_ON")

    def rf_pa_lte7_23db(self):
        # 工模射频PA打功率，LTE7或者LTE3  23db 和16db，测试两个纹波波形
        self.control_phone.self_go_in_test("RF测试工具", "*#808#")
        self.control_phone.self_click_element("pa_play")    # 点击进入PA打功率
        self.control_phone.self_click_element("lte")    # 选择LTE
        self.control_phone.self_click_element("band_select_box")
        self.control_phone.self_click_element("lte_b7")
        self.control_phone.self_input_send_keys("edit_power", 23)  # 输入测试功率值
        self.control_phone.self_click_element("TX_ON")

    def rf_pa_lte3_16db(self):
        # 工模射频PA打功率，LTE7或者LTE3  23db 和16db，测试两个纹波波形
        self.control_phone.self_go_in_test("RF测试工具", "*#808#")
        self.control_phone.self_click_element("pa_play")  # 点击进入PA打功率
        self.control_phone.self_click_element("lte")  # 选择LTE
        self.control_phone.self_click_element("band_select_box")
        self.control_phone.self_click_element("lte_b3")
        self.control_phone.self_input_send_keys("edit_power", 16)  # 输入测试功率值
        self.control_phone.self_click_element("TX_ON")

    def rf_pa_lte7_16db(self):
        # 工模射频PA打功率，LTE7或者LTE3  23db 和16db，测试两个纹波波形
        self.control_phone.self_go_in_test("RF测试工具", "*#808#")
        self.control_phone.self_click_element("pa_play")  # 点击进入PA打功率
        self.control_phone.self_click_element("lte")  # 选择LTE
        self.control_phone.self_click_element("band_select_box")
        self.control_phone.self_click_element("lte_b7")
        self.control_phone.self_input_send_keys("edit_power", 16)  # 输入测试功率值
        self.control_phone.self_click_element("back")
        self.control_phone.self_click_element("TX_ON")

    def usb_interface(self, *args):    # 开启连接USB
        usb = USB_circuit_board.SerialPort()
        usb.pc_on()     # 通过USB开关切换板打开USB功能

    def emmc(self, *args):
        # 电影片段从T卡拷贝到手机内存，拷贝过程中测试纹波电压
        return "请手动从T卡拷贝电影片段到手机内存！"

    def poweron_off(self):
        self.control_phone.self_adb_comm_execute("adb shell input keyevent 26")
        time.sleep(2)
        self.control_phone.self_adb_comm_execute("adb shell input keyevent 26")

    def user_get_log(self, item):
        self.control_phone.self_go_in_feedback(item,"*#800#")

        self.control_phone.self_click_element("更多")
        self.control_phone.self_click_element("设置")
        self.control_phone.self_click_element("用户模式")
        self.control_phone.self_adb_comm_execute("adb shell input keyevent BACK")

        self.control_phone.self_click_element(item)
        self.control_phone.self_click_element(item)

        self.control_phone.self_input_send_keys("问题描述", item + "测试（仅测试使用）")
        self.control_phone.self_adb_comm_execute("adb shell input keyevent BACK")
        self.control_phone.self_click_element("抓取日志")
        self.control_phone.self_click_element("开始抓取")
        self.control_phone.self_click_element("留在当前界面")
        time.sleep(5)
        self.control_phone.self_click_element("完成抓取")
        self.control_phone.self_input_send_keys("联系方式", "13917933260")
        self.control_phone.self_click_element("最近故障时间")
        self.control_phone.self_click_element("确定")
        self.control_phone.self_click_element("故障出现频率")
        self.control_phone.self_click_element("仅本次出现")
        self.control_phone.self_click_element("提交")

    def developer_get_log(self, item):
        self.control_phone.self_go_in_feedback("*#800#", self.device)
        try:
            time.sleep(5)
            self.control_phone.self_click_element("更多", self.device)
            time.sleep(5)
            self.control_phone.self_click_element("设置", self.device)
            time.sleep(10)
            self.control_phone.self_click_element("开发者模式", self.device)
        except AssertionError:
            pass
        except XPathElementNotFoundError:
            pass

        self.control_phone.self_adb_comm_execute("adb shell input keyevent BACK", self.device)
        time.sleep(5)
        self.control_phone.self_click_element(item, self.device)
        time.sleep(5)
        self.control_phone.self_click_element(item, self.device)
        time.sleep(5)
        self.control_phone.self_click_element("开始抓取", self.device)
        self.control_phone.self_click_element("继续抓取", self.device)
        time.sleep(10)
        self.control_phone.self_click_element("完成抓取", self.device)

    def get_latest_log(self):
        log_list = os.popen("adb -s %s shell ls /storage/emulated/0/Android/data/com.oplus.logkit/files/Log" %(self.device)).readlines()
        os.popen("adb -s %s pull /storage/emulated/0/Android/data/com.oplus.logkit/files/Log/" %(self.device)+max(log_list).strip('\n')+" D:\\Users")

        if "zip" in max(log_list):
            command = 'wsl unzip /mnt/d/Users/'+max(log_list).strip('\n')+' -d /mnt/d/Users/'
            time.sleep(60)
            os.system(command)
            path = find_file("D:\\Users\\"+"log@stop@"+max(log_list).split('@')[0])
            ff = open(path+"2", 'w')
            with open(path, 'r', encoding='utf-8') as f:
                line = f.readlines()
                for line_list in line:
                    line_new = line_list.replace('\n', '') # 将换行符替换为空('')
                    line_new = line_new + r'device: ' + self.device + " " + self.serialno + '\n'  # 行末尾加上"|",同时加上"\n"换行符
                    ff.write(line_new)  # 写入一个新文件中

            return "/mnt/"+(path+"2").replace("\\","/").split(":")[0].lower()+(path+"2").replace("\\","/").split(":")[1]

        else:
            time.sleep(180)
            path = find_file("D:\\Users\\"+max(log_list).strip('\n'))

            ff = open(path.split('.')[0]+"2."+path.split('.')[1], 'w')
            with open(path, 'r') as f:
                line = f.readlines()  # 读取文件中的每一行，放入line列表中
                for line_list in line:
                    line_new = line_list.replace('\n', '') # 将换行符替换为空('')
                    line_new = line_new + r'device: ' + self.device + " " + self.serialno + '\n'  # 行末尾加上"|",同时加上"\n"换行符
                    ff.write(line_new)  # 写入一个新文件中

            return "/mnt/d/Users/"+path[9:].replace('\\','/').split('.')[0]+"2."+path[9:].split('.')[1]

    def send_file(self, password, from_path, server, to_path):
        os.popen("wsl sshpass -p \"%s\" scp -P 1992 \"%s\" root@%s:%s" % (password, from_path, server, to_path))

    def get_state(self):
        states = os.popen("adb -s %s shell dumpsys battery" %(self.device)).readlines()
        time = datetime.datetime.now()
        f = open("D:\\Users\\"+str(time).replace(":","_")+".txt",'w')
        for state in states:
            f.write(state.strip('\n')+"device: " + self.device + " " + self.serialno + '\n')

        return "/mnt/d/Users/"+str(time).replace(":","_")+".txt"


def update_logs(device):
    i = 0
    while True:
        i += 1
        cc_logs = GoScene(device)
        cc_logs.developer_get_log("充电")
        time.sleep(30)
        path = cc_logs.get_latest_log()
        time.sleep(60)
        cc_logs.send_file("Xxa215&@", path, "10.119.17.154", "/home/xuxiaoan/Downloads/data/logs/"+device+"_"+str(i)+".log")


def update_state(device):
    i = 0
    while True:
        i += 1
        cc_state = GoScene(device)
        path = cc_state.get_state()
        time.sleep(120)
        cc_state.send_file("Xxa215&@", path, "10.119.17.154", "/home/xuxiaoan/Downloads/data/state/"+device+"_"+str(i)+".log")
        # if i == 1:
        #     is_charging_before = is_charging_now = get()
        #
        # is_charging_now = get()
        # if is_charging_before != is_charging_now:
        #     update_logs(device)


if __name__ == '__main__':
    devices = [device.split('\t')[0] for device in os.popen("adb devices").readlines()[1:-1]]
    threads = []
    for device in devices:
        threads.append(threading.Thread(target=update_logs, args=(device,)))
        threads.append(threading.Thread(target=update_state, args=(device,)))

    for thread in threads:
        thread.start()

    # 单设备多线程
    # t1 = threading.Thread(target=update_state, args=("192.168.1.104:43321",))
    # t2 = threading.Thread(target=update_logs, args=("192.168.1.104:43321",))
    # t1.start()
    # t2.start()


    # update_logs("192.168.1.101:42347")
    # update_logs("192.168.1.101:42347")
    # update_state("192.168.1.104:39827")


    #cc.get_all_logs()
    #cc.user_get_log("输入法")
    #cc.rf_pa_lte7_16db()
    #cc.wide_angle_camera()
    # eval("cc." + cc.switch_test_item("procedure", "射频PA供电电源"))("lte 3", '16')
    # eval("cc." + cc.switch_test_item("procedure", "WIFI/BT/GPS电源"))("WIFI")
    # print(c_str)
    # c_str.say()
    # getattr("GoScene", eval(cc.switch_test_item("procedure", "普通功放/智能功放电源-高通平台"))())()

    # cc.headset_mtk()  # 耳机接口电源_MTK
    # cc.simulation_mic()  # 模拟MIC电源
    # cc.number_mic()     # 数字MIC电源   ===[一加手机怎么设置语音唤醒]===
    # cc.power_amplifier_mtk()   # 普通功放/智能功放电源-MTK平台    ===[播放指定音源（0db白噪，最大音量）]===
    # cc.codec_mtk()      # CODEC电源_MTK平台
    # cc.sensor("LightSensor")     # 通用传感器   ===[枚举]===
    # cc.fingerprint_identifier()     # 指纹识别   ===[没有侧边指纹项目]===
    # cc.short_distance("WIFI")     # 短距离WIFI
    # cc.short_distance("BT", True)     # 短距离蓝牙
    # cc.main_chip()    # 主芯片
    # cc.front_camera()     # 前置摄像头
    # cc.main_cameras()     # 主摄像头
    # cc.wide_angle_camera()    #  广角摄像头
    # cc.rf_pa("lte 3", '16')

    # ====================高通平台==========================
    # cc.headset_qualcomm()       # 耳机接口电源_高通平台
    # cc.power_amplifier_qualcomm()       # 普通功放/智能功放电源-高通平台     ===[播放指定音源（0db白噪，最大音量）]===
    # cc.codec_qualcomm()     # CODEC电源_高通平台