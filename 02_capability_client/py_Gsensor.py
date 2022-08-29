import os
from http_service import HttpService, MessageToCSharpType
import datetime
import sys
import ast

# pack:功能块，如示波器，此参数不能省
# module:功能块类型，如示波器MDO3054，此参数不能省
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
    try:
        """
        strReceive = sys.argv[1]
        # log.log(strReceive)
        parameterList = ast.literal_eval(strReceive)
        log.log(parameterList)
        """
        log.log("------------------------------------")
        log.log("G-Sensor测试")
        com = Component("interface_G_Sensor")
        device = http_service.post_message(com)

    except Exception as err:
        log.exception(str(err))
