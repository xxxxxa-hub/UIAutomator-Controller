import os
from http_service import HttpService, MessageToCSharpType, MessageBox
import datetime
import time
import sys
import ast
import pandas as pd

# pack:功能块，如示波器，此参数不能省
# module:功能块类型，如示波器MDO3054，此参数不能省
# interface:功能块已经实现的接口，此参数不能省
# 其余参数按照实际需求进行传递


class Component(object):
    def __init__(self, interface):
        self.pack = "pack_oscilloscope"
        self.module = "module_TEKMDO3054_PowerTiming"
        self.interface = interface


log = MessageToCSharpType("")
messageBox = MessageBox()
http_service = HttpService()

# 调试脚本
if __name__ == '__main__':
    try:
        # instrName = "TCPIP::" + "169.254.8.103" + "::INSTR"
        # # 标签 和 示波器通道依次对应
        # ch_label = "VX022,VAUX18,VCORE,VS2"
        # # 需要测量的时序对
        # timing_to_meas = "VX022-VAUX18,VAUX18-VCORE,VCORE-VS2"
        # # timing_flag = "POWER OFF"
        # # save_path = "E:/test2"
        # timing_flag = "POWER ON"
        # save_path = "E:/test1"
        # record_length = 1.0E6
        # scale_horizontal = 0.04
        # scale_vertical = "1,1,1,1"
        # trigger_level = 0.5
        # trigger_delay = 0
        # trigger_chn = "CH1"

        # 1,(CH1 rise trigger 0.5v level)/(20ms horizontal)/(1v,1v,1v,1v Vertical)
        # 2,(CH1 rise trigger 0.5v level)/(2ms horizontal)/(0.5v,0.5v,1v,0.5v Vertical)
        # 3,(CH1 rise trigger 0.5v level)/(2ms horizontal)/(0.5v,0.5v,0.5v,0.5v Vertical)
        # 4,(CH1 rise trigger 0.5v level)/(2ms horizontal)/(1v,0.5v,1v,0.5v Vertical)
        # 5,(CH3 rise trigger 0.5v level)/(4ms horizontal)/(0.5v,1v,0.5v,0.5v Vertical)
        # 6,(CH4 rise trigger 0.5v level)/(4ms horizontal)/(0.5v,0.5v,0.5v,0.5v Vertical)
        # 7,(CH2 rise trigger 0.5v level)/(4ms horizontal)/(0.5v,0.5v,0.5v,0.5v Vertical)
        # 8,(CH3 rise trigger 0.5v level)/(4ms horizontal)/(0.5v,0.5v,0.5v,1v Vertical)
        # 9,(CH1 rise trigger 0.5v level)/(100ms horizontal)/(0.5v,0.5v,0.5v,1v Vertical)
        # PowerON_List = [{'VXO22,VAUX18,VCORE,VS2': 'VXO22-VAUX18,VAUX18-VCORE,VCORE-VS2'},
        #                 {'VCORE,EXT_PMIC_EN2,VPU,VA09': 'VCORE-EXT_PMIC_EN2,EXT_PMIC_EN2-VPU,VPU-VA09'},
        #                 {'VA09,VRF12,VA12,VUFS': 'VA09-VRF12,VRF12-VA12,VA12-VUFS'},
        #                 {'VS1,VIO18,VM18,VUFS': 'VS1-VUFS,VUFS-VIO18,VIO18-VM18'},
        #                 {'VPROC1,VEMC,VM18,VRFCK': 'VM18-VPROC1,VPROC1-VEMC,VEMC-VRFCK'},
        #                 {'VBBCK,VSRAM_MD,VSRAM_PROC2,VRFCK': 'VRFCK-VBBCK,VBBCK-VSRAM_PROC2,VSRAM_PROC2-VSRAM_MD'},
        #                 {'VPROC2,VSRAM_MD,VSRAM_Others,VSRAM_PROC1':
        #                 'VSRAM_MD-VPROC2,VPROC2-VSRAM_PROC1,VSRAM_PROC1-VSRAM_Others'},
        #                 {'VGPU,VAUD18,VSRAM_Others,VUSB': 'VSRAM_Others-VGPU,VGPU-VAUD18,VAUD18-VUSB'},
        #                 {'VRF12,VS1,RESETB,VUSB': 'VRF12-VS1,VUSB-RESETB,NONE'},
        #                 ]

        # 1,(CH1 fall trigger 0.5v level)/(20ms horizontal)/(1v,0.5v,1v,1v Vertical)
        # 2,(CH3 fall trigger 0.5v level)/(2ms horizontal)/(0.5v,0.5v,1v,0.5v Vertical)
        # 3,(CH1 fall trigger 0.5v level)/(2ms horizontal)/(1v,0.5v,0.5v,0.5v Vertical)
        # 4,(CH4 fall trigger 0.5v level)/(10ms horizontal)/(0.5,0.5v,1v,0.5v Vertical)
        # 5,(CH2 fall trigger 0.5v level)/(4ms horizontal)/(0.5v,0.5v,0.5v,0.5v Vertical)
        # 6,(CH3 fall trigger 0.5v level)/(4ms horizontal)/(0.5v,0.5v,0.5v,0.5v Vertical)
        # 7,(CH4 fall trigger 0.5v level)/(4ms horizontal)/(0.5v,0.5v,0.5v,0.5v Vertical)
        # 8,(CH4 fall trigger 0.5v level)/(100ms horizontal)/(0.5v,0.5v,0.5v,1v Vertical)
        # PowerOFF_List = [{'VXO22,VPU,VCORE,VS2': 'VXO22-VCORE,VCORE-VS2,VS2-VPU'},
        #                  {'VRF12,VS1,VPU,VA09': 'VPU-VA09,VA09-VRF12,VRF12-VS1'},
        #                  {'VS1,VRF12,VA12,VUFS': 'VRF12-VA12,VA12-VS1,VUFS-VS1'},
        #                  {'VPROC1,VIO18,VM18,VUFS': 'VUFS-VIO18,VIO18-VM18,VM18-VPROC1'},
        #                  {'VBBCK,VEMC,VSRAM_PROC2,VRFCK': 'VEMC-VRFCK,VBBCK-VSRAM_PROC2,NONE'},
        #                  {'VPROC2,VSRAM_MD,VSRAM_PROC2,VSRAM_PROC1':
        #                  'VSRAM_PROC2-VSRAM_MD,VSRAM_PROC2-VPROC2,VPROC2-VSRAM_PROC1'},
        #                  {'VGPU,VAUD18,VSRAM_Others,VSRAM_PROC1': 'VSRAM_PROC1-VGPU,VSRAM_Others-VGPU,VGPU-VAUD18'},
        #                  {'VAUX18,VAUD18,RESETB,VUSB': 'VAUX18-VUSB,VUSB-RESETB,NONE'},
        #                  ]

        # # 开机测量点序列
        # PowerON_PointsList = [['VXO22', 'VAUX18', 'VCORE', 'VS2'], ['VCORE', 'EXT_PMIC_EN2', 'VPU', 'VA09'],
        #                       ['VA09', 'VRF12', 'VA12', 'VUFS'], ['VS1', 'VIO18', 'VM18', 'VUFS'],
        #                       ['VPROC1', 'VEMC', 'VM18', 'VRFCK'], ['VBBCK', 'VSRAM_MD', 'VSRAM_PROC2', 'VRFCK'],
        #                       ['VPROC2', 'VSRAM_MD', 'VSRAM_Others', 'VSRAM_PROC1'],
        #                       ['VGPU', 'VAUD18', 'VSRAM_Others', 'VUSB'], ['VRF12', 'VS1', 'RESETB', 'VUSB']]
        #
        # # 需要测量的时序序列
        # PowerON_TimingList = [['VXO22-VAUX18', 'VAUX18-VCORE', 'VCORE-VS2'], ['VCORE-EXT_PMIC_EN2', 'EXT_PMIC_EN2-VPU', 'VPU-VA09'],
        #                       ['VA09-VRF12', 'VRF12-VA12', 'VA12-VUFS'], ['VS1-VUFS', 'VUFS-VIO18', 'VIO18-VM18'],
        #                       ['VM18-VPROC1', 'VPROC1-VEMC', 'VEMC-VRFCK'], ['VRFCK-VBBCK', 'VBBCK-VSRAM_PROC2', 'VSRAM_PROC2-VSRAM_MD'],
        #                       ['VSRAM_MD-VPROC2', 'VPROC2-VSRAM_PROC1', 'VSRAM_PROC1-VSRAM_Others'],
        #                       ['VSRAM_Others-VGPU', 'VGPU-VAUD18', 'VAUD18-VUSB'], ['VRF12-VS1', 'VUSB-RESETB', 'NONE']]
        #
        # PowerOFF_PointsList = [['VXO22', 'VPU', 'VCORE', 'VS2'], ['VRF12', 'VS1', 'VPU', 'VA09'],
        #                        ['VS1', 'VRF12', 'VA12', 'VUFS'], ['VPROC1', 'VIO18', 'VM18', 'VUFS'],
        #                        ['VBBCK', 'VEMC', 'VSRAM_PROC2', 'VRFCK'],
        #                        ['VPROC2', 'VSRAM_MD', 'VSRAM_PROC2', 'VSRAM_PROC1'],
        #                        ['VGPU', 'VAUD18', 'VSRAM_Others', 'VSRAM_PROC1'],
        #                        ['VAUX18', 'VAUD18', 'RESETB', 'VUSB']]
        #
        # PowerOFF_TimingList = [['VXO22-VCORE', 'VCORE-VS2', 'VS2-VPU'], ['VPU-VA09', 'VA09-VRF12', 'VRF12-VS1'],
        #                        ['VRF12-VA12', 'VA12-VS1', 'VUFS-VS1'], ['VUFS-VIO18', 'VIO18-VM18', 'VM18-VPROC1'],
        #                        ['VEMC-VRFCK', 'VBBCK-VSRAM_PROC2', 'NONE'],
        #                        ['VSRAM_PROC2-VSRAM_MD', 'VSRAM_PROC2-VPROC2', 'VPROC2-VSRAM_PROC1'],
        #                        ['VSRAM_PROC1-VGPU', 'VSRAM_Others-VGPU', 'VGPU-VAUD18'],
        #                        ['VAUX18-VUSB', 'VUSB-RESETB', 'NONE']]

        # PowerON_List = [{'Label': ['VXO22', 'VAUX18', 'VCORE', 'VS2'],
        #                  'TimingPair': ['VXO22-VAUX18', 'VAUX18-VCORE', 'VCORE-VS2'],
        #                  'NeedMeasure': [True, True, True]},
        #                 {'Label': ['VCORE', 'EXT_PMIC_EN2', 'VPU', 'VA09'],
        #                  'TimingPair': ['VCORE-EXT_PMIC_EN2', 'EXT_PMIC_EN2-VPU', 'VPU-VA09'],
        #                  'NeedMeasure': [True, True, True]},
        #                 {'Label': ['VA09', 'VRF12', 'VA12', 'VUFS'],
        #                  'TimingPair': ['VA09-VRF12', 'VRF12-VA12', 'VA12-VUFS'],
        #                  'NeedMeasure': [True, True, True]},
        #                 {'Label': ['VS1', 'VIO18', 'VM18', 'VUFS'],
        #                  'TimingPair': ['VS1-VUFS', 'VUFS-VIO18', 'VIO18-VM18'],
        #                  'NeedMeasure': [True, True, True]},
        #                 {'Label': ['VPROC1', 'VEMC', 'VM18', 'VRFCK'],
        #                  'TimingPair': ['VM18-VPROC1', 'VPROC1-VEMC', 'VEMC-VRFCK'],
        #                  'NeedMeasure': [True, True, True]},
        #                 {'Label': ['VBBCK', 'VSRAM_MD', 'VSRAM_PROC2', 'VRFCK'],
        #                  'TimingPair': ['VRFCK-VBBCK', 'VBBCK-VSRAM_PROC2', 'VSRAM_PROC2-VSRAM_MD'],
        #                  'NeedMeasure': [True, True, True]},
        #                 {'Label': ['VPROC2', 'VSRAM_MD', 'VSRAM_Others', 'VSRAM_PROC1'],
        #                  'TimingPair': ['VSRAM_MD-VPROC2', 'VPROC2-VSRAM_PROC1', 'VSRAM_PROC1-VSRAM_Others'],
        #                  'NeedMeasure': [True, True, True]},
        #                 {'Label': ['VGPU', 'VAUD18', 'VSRAM_Others', 'VUSB'],
        #                  'TimingPair': ['VSRAM_Others-VGPU', 'VGPU-VAUD18', 'VAUD18-VUSB'],
        #                  'NeedMeasure': [True, True, True]},
        #                 {'Label': ['VRF12', 'VS1', 'RESETB', 'VUSB'],
        #                  'TimingPair': ['VRF12-VS1', 'VUSB-RESETB', 'NONE'],
        #                  'NeedMeasure': [True, True, True]}]
        #
        # PowerOFF_List = [{'Label': ['VXO22', 'VPU', 'VCORE', 'VS2'],
        #                   'TimingPair': ['VXO22-VCORE', 'VCORE-VS2', 'VS2-VPU'],
        #                   'NeedMeasure': [True, True, True]},
        #                  {'Label': ['VRF12', 'VS1', 'VPU', 'VA09'],
        #                   'TimingPair': ['VPU-VA09', 'VA09-VRF12', 'VRF12-VS1'],
        #                   'NeedMeasure': [True, True, True]},
        #                  {'Label': ['VS1', 'VRF12', 'VA12', 'VUFS'],
        #                   'TimingPair': ['VRF12-VA12', 'VA12-VS1', 'VUFS-VS1'],
        #                   'NeedMeasure': [True, True, True]},
        #                  {'Label': ['VPROC1', 'VIO18', 'VM18', 'VUFS'],
        #                   'TimingPair': ['VUFS-VIO18', 'VIO18-VM18', 'VM18-VPROC1'],
        #                   'NeedMeasure': [True, True, True]},
        #                  {'Label': ['VBBCK', 'VEMC', 'VSRAM_PROC2', 'VRFCK'],
        #                   'TimingPair': ['VEMC-VRFCK', 'VBBCK-VSRAM_PROC2', 'NONE'],
        #                   'NeedMeasure': [False, True, True]},
        #                  {'Label': ['VPROC2', 'VSRAM_MD', 'VSRAM_PROC2', 'VSRAM_PROC1'],
        #                   'TimingPair': ['VSRAM_PROC2-VSRAM_MD', 'VSRAM_PROC2-VPROC2', 'VPROC2-VSRAM_PROC1'],
        #                   'NeedMeasure':[False, True, True]},
        #                  {'Label': ['VGPU', 'VAUD18', 'VSRAM_Others', 'VSRAM_PROC1'],
        #                   'TimingPair': ['VSRAM_PROC1-VGPU', 'VSRAM_Others-VGPU', 'VGPU-VAUD18'],
        #                   'NeedMeasure':[True, True, False]},
        #                  {'Label': ['VAUX18', 'VAUD18', 'RESETB', 'VUSB'],
        #                   'TimingPair': ['VAUX18-VUSB', 'VUSB-RESETB', 'NONE'],
        #                   'NeedMeasure':[True, True, True]}]

        # parameterList = {
        #     'clockchn': '',
        #     'datachn': '',
        #     'oscillographName': 'A019583',
        #     'instrName': 'TCPIP::169.254.7.181::INSTR',
        #     'instrModel': 'Tektronix MDO3000 Series',
        #     'prjname': '21841',
        #     'prjver': 'Ver.A',
        #     'signaltyp': '',
        #     'LoopTimes': '1',
        #     'datasignal': '',
        #     'clksignal': '',
        #     'expectAddress': '',
        #     'autoTrig': 'False',
        #     'needInitScope': 'False',
        #     'TestCaseName': 'SM8475_下电_VREG_S2C_S3C,VREG_L1H,VREG_S2H,VREG_S6C_S7C_S8C',
        #     'TestUnit': '电源',
        #     'rechipname': 'SM8475',
        #     'rechipnum': 'U001',
        #     'trchipname': 'MT6365',
        #     'trchipnum': 'U001',
        #     'prjdescr': '',
        #     'useClkChannel': 'True',
        #     'useDataChannel': 'True',
        #     'testSceneName': '',
        #     'DataSignalName': 'NA',
        #     'ClkSignalName': 'NA',
        #     'ChipAddress': '',
        #     'loop_index': '1',
        #     'CH4 Vertical': '0.5',
        #     'Power Action': 'POWER OFF',
        #     '1st Timing Pair': 'VREG_S2C_S3C-VREG_L1H',
        #     'Trigger Level': '0.5',
        #     'Scale Horizontal': '10',
        #     'CH3 Vertical': '0.5',
        #     '3rd Timing Pair': 'VREG_S2H-VREG_S6C_S7C_S8C',
        #     '2nd Timing Pair': 'VREG_L1H-VREG_S2H',
        #     'Trigger Channel': 'CH2',
        #     'CH2 Vertical': '0.5',
        #     'All Channel Display': 'yes',
        #     'Manual Test': 'yes',
        #     'CH1 Vertical': '0.5',
        #     'Python_File_Name': 'Py_TEKMDO3054_PowerTiming.py',
        #     'screenshotPath': 'E:\\brandonyuan\\20220704\\Debug\\Testresult\\21841\\Ver.A'}

        # parameterList = {
        #     'clockchn': '',
        #     'datachn': '',
        #     'oscillographName': 'A019583',
        #     'instrName': 'TCPIP::169.254.7.181::INSTR',
        #     'instrModel': 'Tektronix MDO3000 Series',
        #     'prjname': '21841',
        #     'prjver': 'Ver.A',
        #     'signaltyp': '',
        #     'LoopTimes': '1',
        #     'datasignal': '',
        #     'clksignal': '',
        #     'expectAddress': '',
        #     'autoTrig': 'False',
        #     'needInitScope': 'False',
        #     'TestCaseName': 'SM8475_上电_VREG_S1C,VREG_BOB,VREG_S11B,VREG_S12B',
        #     'TestUnit': '电源',
        #     'rechipname': 'SM8475',
        #     'rechipnum': 'U001',
        #     'trchipname': 'MT6365',
        #     'trchipnum': 'U001',
        #     'prjdescr': '',
        #     'useClkChannel': 'True',
        #     'useDataChannel': 'True',
        #     'testSceneName': '',
        #     'DataSignalName': 'NA',
        #     'ClkSignalName': 'NA',
        #     'ChipAddress': '',
        #     'loop_index': '1',
        #     'Scale Horizontal': '100',
        #     'All Channel Display': 'yes',
        #     'CH2 Vertical': '1',
        #     'CH4 Vertical': '1',
        #     'Power Action': 'POWER ON',
        #     'Trigger Level': '0.5',
        #     '1st Timing Pair': 'VREG_S1C-VREG_BOB',
        #     'Trigger Channel': 'CH1',
        #     '3rd Timing Pair': 'VREG_S11B-VREG_S12B',
        #     'CH3 Vertical': '0.5',
        #     '2nd Timing Pair': 'VREG_BOB-VREG_S11B',
        #     'CH1 Vertical': '1',
        #     'Manual Test': 'yes',
        #     'Python_File_Name': 'Py_TEKMDO3054_PowerTiming.py',
        #     'screenshotPath': 'E:\\brandonyuan\\20220704\\Debug\\Testresult\\21841\\Ver.A'}

        strReceive = sys.argv[1]
        parameterList = ast.literal_eval(strReceive)
        log.log("INFO >>> 案例参数: {}{}{}".format("=" * 215, parameterList, "=" * 230))

        instrName = parameterList['instrName']
        save_path = parameterList['screenshotPath']

        all_channel_display_flag = parameterList['All Channel Display']
        manual_test_flag = parameterList['Manual Test']
        timing_flag = parameterList['Power Action']
        first_timing_pair = parameterList['1st Timing Pair']
        second_timing_pair = parameterList['2nd Timing Pair']
        third_timing_pair = parameterList['3rd Timing Pair']
        scale_horizontal = float(parameterList['Scale Horizontal']) / 1000  # ms
        vertical_ch1 = parameterList['CH1 Vertical']
        vertical_ch2 = parameterList['CH2 Vertical']
        vertical_ch3 = parameterList['CH3 Vertical']
        vertical_ch4 = parameterList['CH4 Vertical']
        trigger_chn = parameterList['Trigger Channel']
        trigger_level = float(parameterList['Trigger Level'])

        trigger_delay = 0
        record_length = 1.0E6

        first_timing_lbl = first_timing_pair.split('-')
        second_timing_lbl = second_timing_pair.split('-')
        third_timing_lbl = third_timing_pair.split('-')

        if first_timing_lbl[0] == first_timing_lbl[1] \
                or second_timing_lbl[0] == second_timing_lbl[1] \
                or third_timing_lbl[0] == third_timing_lbl[1]:
            raise Exception("不允许时序对名称相同！")

        if first_timing_lbl[1] != second_timing_lbl[0] or second_timing_lbl[1] != third_timing_lbl[0]:
            raise Exception("待测时序对必须符合A-B, B-C, C-D的输入规则！A,B,C,D依次被接入示波器CH1-CH4，请检查！")

        TIMING_Dict = {'Label': [first_timing_lbl[0], second_timing_lbl[0], third_timing_lbl[0], third_timing_lbl[1]],
                       'TimingPair': [first_timing_pair, second_timing_pair, third_timing_pair],
                       'NeedMeasure': [True, True, True]}

        # 通道和label之间的对应关系
        # 待测信号之间与相应通道的对应关系
        if timing_flag.upper() == 'POWER ON':
            ch_label_list = TIMING_Dict['Label']    # ch_label.split(",")
            measure_list = TIMING_Dict['TimingPair']  # timing_to_meas.split(",")
            need_meas_list = TIMING_Dict['NeedMeasure']
        elif timing_flag.upper() == 'POWER OFF':
            ch_label_list = TIMING_Dict['Label']
            measure_list = TIMING_Dict['TimingPair']
            need_meas_list = TIMING_Dict['NeedMeasure']
        else:
            raise Exception("Only 'POWER ON' or 'POWER OFF' is Permitted!")

        log.log(f"当前测试序列：CH1-CH4 : {ch_label_list[0]}, {ch_label_list[1]}, {ch_label_list[2]}, {ch_label_list[3]}")

        # 仅人工测试时弹框提醒
        if manual_test_flag.upper() == 'YES':
            messageBox.showinfo("Remind", f"当前测试序列：CH1-CH4 : {ch_label_list[0]}, {ch_label_list[1]}, "
                                          f"{ch_label_list[2]}, {ch_label_list[3]}。请确认接线正确！")

        # 各通道之间的纵向坐标刻度
        ch_scale_vertical_list = [float(vertical_ch1), float(vertical_ch2), float(vertical_ch3), float(vertical_ch4)]

        # 待测时序对信息
        measure_info_list = []
        for item in measure_list:
            if item != "NONE":
                meas_lbl = item.split("-")
                measure_info = {'title': item,  # 待测时序对名称
                                'chn_a_index': ch_label_list.index(meas_lbl[0]),    # 通道序号a
                                'chn_b_index': ch_label_list.index(meas_lbl[1]),    # 通道序号b
                                'chn_a_string': 'CH{0}'.format(ch_label_list.index(meas_lbl[0]) + 1),   # 对应的示波器通道号
                                'chn_b_string': 'CH{0}'.format(ch_label_list.index(meas_lbl[1]) + 1),   # 对应的示波器通道号
                                'need_measure': need_meas_list[measure_list.index(item)]}   # 此时序对是否需要光标卡时序
                measure_info_list.append(measure_info)

        #################################################################
        #################################################################
        # 重要数据结构
        # measure_info_list包含所有待测量时序对所有信息
        # chn_info_list 示波器各通道测量到的信息
        #################################################################
        #################################################################

        # --------------------step 1 init---------------------
        log.log("初始化示波器")
        com = Component("interface_initial")
        com.instrName = instrName
        device = http_service.post_message(com)

        # --------------------step 2 record length---------------------
        log.log("示波器恢复默认设置并设置记录长度")
        com = Component("interface_set_oscilloscope")
        com.instrName = instrName
        com.record_length = record_length
        result1 = http_service.post_message(com)

        # --------------------step 3 channel setup---------------------
        log.log("设置通道标签、位置、通道垂直刻度等")
        com = Component("interface_ch_set1")
        com.instrName = instrName
        com.ch_label = ch_label_list
        com.ch_vertical = ch_scale_vertical_list
        result2 = http_service.post_message(com)

        # --------------------step 4 horizontal setup---------------------
        log.log("设置水平时基刻度")
        com = Component("interface_set_horizontal_scale")
        com.instrName = instrName
        com.scale_horizontal = scale_horizontal
        result3 = http_service.post_message(com)

        # --------------------step 5 trigger setup---------------------
        log.log("设置触发类型")
        com = Component("interface_set_trigger")
        com.instrName = instrName
        com.trigger_ch = trigger_chn
        if timing_flag.upper() == "POWER ON":
            com.trigger_type = "RISE"
        else:
            com.trigger_type = "FALL"
        com.trigger_level = trigger_level
        com.trigger_delay = trigger_delay
        result4 = http_service.post_message(com)

        # --------------------step 6 acquisitions---------------------
        log.log("示波器开始采集数据")
        com = Component("interface_start_acquisitions")
        com.instrName = instrName
        result5 = http_service.post_message(com)

        # --------------------step 7 start single trigger---------------------
        log.log("设置触发模式")
        com = Component("interface_set_trigger_mode")
        com.instrName = instrName
        com.acquire_type = "SEQUENCE"
        result6 = http_service.post_message(com)

        # 等待波形触发
        if timing_flag.upper() == "POWER ON":
            if manual_test_flag.upper() == 'YES':
                messageBox.showinfo("Remind", "请开机，并等待波形触发")
        else:
            if manual_test_flag.upper() == 'YES':
                messageBox.showinfo("Remind", "请关机，并等待波形触发")

        # --------------------waiting for triggered---------------------
        count = 0
        while True:
            count += 1
            log.log('time running: {0}s'.format(count))
            time.sleep(1)
            com = Component("interface_query_acquire_mode")
            com.instrName = instrName
            acquire_mode = http_service.post_message(com)
            if acquire_mode == '0\n':
                break
            if count >= 20:
                log.fail("在20s之内未能捕捉到正确的波形，请重新测试")
                sys.exit()

        # # --------------------acquire triggered data---------------------
        # 将示波器四个通道的数据暂存在列表中
        log.log("获取示波器数据并导出...")
        chn_info_list = []
        for ch_index in range(1, 5):
            chn_info = {}
            if ch_label_list[ch_index - 1].upper() != 'NONE':   # 当前示波器通道无波形
                log.log("正在处理示波器通道 {0} 数据...".format(ch_index))
                chn_csv_path = save_path + "/CH{0}-{1}.csv".format(ch_index, ch_label_list[ch_index - 1])
                com = Component("interface_data_caul")
                com.instrName = instrName
                com.ch = 'CH' + str(ch_index)
                com.save_path = chn_csv_path
                chn_data = http_service.post_message(com)

                chn_info['chn_number'] = 'CH' + str(ch_index)   # 通道号
                chn_info['chn_label'] = ch_label_list[ch_index - 1]     # 通道标签
                chn_info['csv_path'] = chn_csv_path     # csv路径

                com = Component("interface_measure_high_low_level")
                com.instrName = instrName
                com.channel = f'CH{ch_index}'
                high_low_level = http_service.post_message(com)

                chn_info["HIGH"] = high_low_level["HIGH"]
                chn_info["LOW"] = high_low_level["LOW"]
            else:
                chn_info['chn_number'] = 'NONE'
                chn_info['chn_label'] = 'NONE'
                chn_info['csv_path'] = 'NONE'
                chn_info["HIGH"] = "NONE"
                chn_info["LOW"] = "NONE"

            chn_info_list.append(chn_info)

        # --------------------search for rise/fall point(time,voltage)---------------------'''
        # 需要考虑增加无跳变沿的情形
        if timing_flag.upper() == "POWER ON":
            log.log("获取波形上升沿位置")
            for item in chn_info_list:
                if item['chn_number'] != 'NONE':
                    try:
                        com = Component("interface_pick_rise_point")
                        com.instrName = instrName
                        com.path = item['csv_path']
                        com.level_high = item['HIGH']
                        com.level_low = item['LOW']
                        rise_fall_point = http_service.post_message(com)
                        if type(rise_fall_point) is str:
                            raise Exception("No Edge!")
                        item['rf_point'] = rise_fall_point
                        item['rf_exist'] = True
                    except Exception as err:
                        if str(err) == 'No Edge!':
                            item['rf_point'] = "NONE"
                            item['rf_exist'] = False
                        else:
                            raise err
                else:
                    item['rf_point'] = "NONE"
                    item['rf_exist'] = "NONE"
        else:
            log.log("获取波形下降沿位置")
            for item in chn_info_list:
                if item['chn_number'] != 'NONE':
                    try:
                        com = Component("interface_pick_fall_point")
                        com.instrName = instrName
                        com.path = item['csv_path']
                        com.level_high = item['HIGH']
                        com.level_low = item['LOW']
                        rise_fall_point = http_service.post_message(com)
                        if type(rise_fall_point) is str:
                            raise Exception("No Edge!")
                        item['rf_point'] = rise_fall_point
                        item['rf_exist'] = True
                    except Exception as err:
                        if str(err) == 'No Edge!':
                            item['rf_point'] = "NONE"
                            item['rf_exist'] = False
                        else:
                            raise err
                else:
                    item['rf_point'] = "NONE"
                    item['rf_exist'] = "NONE"

        # --------------------get result--------------------'''
        test_result = {}
        pic_result = []
        for item in measure_info_list:
            if timing_flag == "POWER ON":
                str_meas_title = item['title'] + "(RISE)"
            else:
                str_meas_title = item['title'] + "(FALL)"

            ch_a = item['chn_a_string']
            ch_b = item['chn_b_string']

            if item['need_measure']:
                if (chn_info_list[item['chn_a_index']]['rf_exist'] is not True) or\
                        (chn_info_list[item['chn_b_index']]['rf_exist'] is not True):
                    test_result[str_meas_title] = 888888.8
                    continue

            # 只显示正在测量的通道波形 or 显示所有通道波形
            if all_channel_display_flag.upper() != 'YES':
                log.log("仅显现待测量通道波形...")
                # 关闭所有通道
                for ch_index in range(1, 5):
                    com = Component("interface_close_ch")
                    com.instrName = instrName
                    com.ch = f'CH{ch_index}'
                    result = http_service.post_message(com)

                com = Component("interface_open_ch")
                com.instrName = instrName
                com.ch = ch_a
                result = http_service.post_message(com)

                com = Component("interface_open_ch")
                com.instrName = instrName
                com.ch = ch_b
                result = http_service.post_message(com)

            cursor_a = chn_info_list[item['chn_a_index']]['rf_point']['time']
            cursor_b = chn_info_list[item['chn_b_index']]['rf_point']['time']

            log.log("测试结果处理:{0}...".format(item['title']))
            com = Component("interface_adjust_scale")
            com.instrName = instrName
            com.pos_a = cursor_a
            com.pos_b = cursor_b
            zoom_result = http_service.post_message(com)

            com = Component("interface_set_cursor_wave")
            com.instrName = instrName
            com.cursor_source = ch_a
            com.position1 = cursor_a
            com.position2 = cursor_b
            cursor_ret = http_service.post_message(com)

            if cursor_b < cursor_a:
                test_result[str_meas_title] = 0 - cursor_ret['delta'] * 1000    # ms单位
            else:
                test_result[str_meas_title] = cursor_ret['delta'] * 1000    # ms单位

            log.log("保存截图:{0}".format(str_meas_title))
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            com = Component("interface_save_screen")
            com.instrName = instrName
            if timing_flag == "POWER ON":
                com.file_name = save_path + "\\" + str_meas_title + '.png'
            else:
                com.file_name = save_path + "\\" + str_meas_title + '.png'
            save_pic_ret = http_service.post_message(com)

            pic_result.append(save_pic_ret['filename'])

        test_result['PngPaths'] = pic_result
        log.success(test_result)

        # test_result={'VREG_S1C-VREG_BOB(RISE)': 0.5, 'VREG_BOB-VREG_S11B(RISE)': 4.5, 'VREG_S11B-VREG_S12B(RISE)': -0.4,
        #  'PngPaths': ['E:\\brandonyuan\\20220704\\Debug\\Testresult\\21841\\Ver.A\\VREG_S1C-VREG_BOB-RISE.png',
        #               'E:\\brandonyuan\\20220704\\Debug\\Testresult\\21841\\Ver.A\\VREG_BOB-VREG_S11B-RISE.png',
        #               'E:\\brandonyuan\\20220704\\Debug\\Testresult\\21841\\Ver.A\\VREG_S11B-VREG_S12B-RISE.png']}
        # log.success(test_result)

    except Exception as err:
        log.exception(str(err))



