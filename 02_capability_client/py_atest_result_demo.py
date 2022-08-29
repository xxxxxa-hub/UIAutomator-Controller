import ast
from http_service import HttpService, MessageToCSharpType
# pack:功能块，如示波器，此参数不能省
# module:功能块类型，如示波器MDO3054，此参数不能省
# interface:功能块已经实现的接口，此参数不能省
# 其余参数按照实际需求进行传递


class Component(object):
    def __init__(self, interface):
        self.pack = "pack_demo"
        self.module = "module_demo"
        self.interface = interface


log = MessageToCSharpType("")
http_service = HttpService()

# 平台与测试脚本的接口demo，主要针对多个图像路径的存储和返回给平台
# 为了能更快更清晰的理解代码，约定结果变量名及参数键值如下：
#  test_result : 字典，存储返回结果
#  PngPaths ：存放结果图像列表的键
if __name__ == '__main__':
    try:
        #  平台下发的参数
        strReceive = r'{"param1":"param1","param2":"param2","param3":"param3",' \
                     r'"prjname":"21121","prjver":"Ver.A",' \
                     r'"Python_File_Name":"Py_WaveRunner8254_SPIQuality.py",' \
                     r'"screenshotPath":"D:\\sts\\01_Code\\STS\\Debug\\Testresult\\21121' \
                     r'\\Ver.A"} '
        log.log(strReceive)
        parameterList = ast.literal_eval(strReceive)
        log.log(parameterList)


        message_box = MessageBox()
        # 返回值是True或者False
        flag = message_box.askyesno('1', '请确认点针是否正确点到位置上？')
        print(flag)
        # 返回值是True或者False
        flag = message_box.askokcancel('2', '请确认点针是否正确点到位置上？')
        print(flag)
        # 返回值是ok
        flag = message_box.showerror('3', '请确认点针是否正确点到位置上？')
        print(flag)
        # 返回值是ok
        flag = message_box.showinfo('4', '请确认点针是否正确点到位置上？')
        print(flag)
        # 返回值是ok
        flag = message_box.showwarning('5', '请确认点针是否正确点到位置上？')
        print(flag)

        #  约定为这个变量名称，存储返回结果的字典
        test_result = {'PngPaths': []}
        # 约定PngPaths键名，存储图像列表
        com = Component("interface_test_result")
        #  根据平台下发的参数关键字取出参数
        com.parameter1 = parameterList['param1']
        com.parameter2 = parameterList["screenshotPath"] + "\\"
        # 结果返回图像路径，此路径包必须含在参数parameterList["screenshotPath"]目录下
        pngPath1 = http_service.post_message(com)
        # 结果图像路径以列表的形式存储到字典中，对应字典的键为PngPaths
        test_result['PngPaths'].append(pngPath1)

        com.parameter1 = parameterList['param2']
        com.parameter2 = parameterList["screenshotPath"] + "\\"
        # 结果返回图像路径，此路径包必须含在参数parameterList["screenshotPath"]目录下
        pngPath2 = http_service.post_message(com)
        #  结果图像路径追加到字典中的键为PngPaths的列表
        test_result['PngPaths'].append(pngPath2)

        log.log(str(test_result))
        #  成功输出结果给到平台
        log.success(test_result)

    except Exception as err:
        log.exception(str(err))

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
