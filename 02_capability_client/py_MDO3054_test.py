import os
from http_service import HttpService, MessageToCSharpType


# pack:功能块，如示波器，此参数不能省
# module:功能块类型，如示波器MDO3054，此参数不能省
# interface:功能块已经实现的接口，此参数不能省
# 其余参数按照实际需求进行传递
class Component(object):
    def __init__(self, interface):
        self.pack = "pack_oscilloscope"
        self.module = "module_baseband_voltage"
        self.interface = interface


log = MessageToCSharpType("")
http_service = HttpService()

# 调试脚本
if __name__ == '__main__':
    log.log("初始化示波器")
    instrName = "TCPIP::" + "169.254.35.143" + "::INSTR"
    com = Component("interface_initial")
    com.instrName = instrName
    device = http_service.post_message(com)

    log.log("设置示波器记录长度")
    com = Component("interface_set_record_length")
    com.instrName = instrName
    com.length = 1000000
    result1 = http_service.post_message(com)

    log.log("设置通道名称")
    com = Component("interface_set_channel_name")
    com.instrName = instrName
    com.channelNo = '1'
    com.name = 'TEST2'
    result2 = http_service.post_message(com)

    log.log("设置垂直")
    com = Component("interface_set_horizontal")
    com.scale = 0.1
    com.instrName = instrName
    com.position = 60
    result3 = http_service.post_message(com)

    log.log("设置单条纹波测试项波形参数")
    com = Component("interface_ripple_set")
    com.scale = 0.5
    com.instrName = instrName
    com.channelNo = 1
    result4 = http_service.post_message(com)

    log.log("选择通道")
    com = Component("interface_select_channel")
    com.instrName = instrName
    com.channelNo = 1
    result5 = http_service.post_message(com)

    log.log("获取单条通道纹波数据")
    com = Component("interface_ripple_ch")
    com.instrName = instrName
    com.channelNo = 1
    com.pkpk_max = 0.2
    com.screenshotPath = os.getcwd() + "\\Screenshot\\"
    result6 = http_service.post_message(com)

    log.log("设置带宽为指定数值")
    com = Component("interface_set_bandwidth")
    com.instrName = instrName
    com.channelNo = 1
    result7 = http_service.post_message(com)
    log.success(result6)