import os
from http_service import HttpService, MessageToCSharpType


# module:功能块，如示波器，此参数不能省
# moduleType:功能块类型，如示波器MDO3054，此参数不能省
# interface:功能块已经实现的接口，此参数不能省
# 其余参数按照实际需求进行传递
class Component(object):
    def __init__(self, interface):
        self.pack = "pack_phoneself"
        self.module = "module_phone_run"
        self.interface = interface


log = MessageToCSharpType("")
http_service = HttpService()

# 调试脚本
if __name__ == '__main__':
    log.log("在工程师模式下设置亮度")
    com = Component("interface_ripple_load_phone_pre_process")
    com.frequency = 90
    com.brightness_rate = 50
    com.pic = "fruit"
    result1 = http_service.post_message(com)
