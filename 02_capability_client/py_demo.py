import os
from http_service import HttpService


# pack:功能块，如示波器，此参数不能省
# module:功能块类型，如示波器MDO3054，此参数不能省
# interface:功能块已经实现的接口，此参数不能省
class Component(object):
    def __init__(self, interface):
        self.pack = "pack_demo"
        self.module = "module_demo"
        self.interface = interface


http_service = HttpService()

# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    http_service.get_default()

    com = Component("interface_initial")
    com.parameter1 = "1"
    com.parameter2 = "2"
    com.parameter3 = "3"
    device = http_service.post_message(com)
    print(device)
    print(device)

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
