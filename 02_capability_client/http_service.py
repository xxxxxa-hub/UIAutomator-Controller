import requests
import json
import tkinter
import tkinter.messagebox


# 消息打印类
class MessageBox:
    def __init__(self):
        top = tkinter.Tk()  # *********
        top.wm_attributes('-topmost', 1)
        top.withdraw()  # ****实现主窗口隐藏
        top.update()  # *********需要update一下
        # top.destroy()

    @staticmethod
    def askyesno(title, message):
        result = tkinter.messagebox.askyesno(title, message)
        return result

    @staticmethod
    def askokcancel(title, message):
        result = tkinter.messagebox.askokcancel(title, message)
        return result

    @staticmethod
    def showerror(title, message):
        result = tkinter.messagebox.showerror(title, message)
        return result

    @staticmethod
    def showinfo(title, message):
        result = tkinter.messagebox.showinfo(title, message)
        return result

    @staticmethod
    def showwarning(title, message):
        result = tkinter.messagebox.showwarning(title, message)
        return result


# 消息类别 如下类禁止改动，否则影响示波器平台的调度
class MessageToCSharpType:
    def __init__(self, result_info):
        self.LOG = 0  # 正常输出log
        self.SUCCESS = 1  # 成功输出信息
        self.FAIL = 2  # 失败输出信息
        self.EXCEPTION = 3  # 异常输出信息
        self.result_info = result_info

    # 打印消息主要接口
    @staticmethod
    def print_msg(msg_title, message):
        typeinfo = "ToCSharp" + str(msg_title) + ":"
        msg_info = str(message)
        if msg_info is not None:
            print(typeinfo + msg_info)

    # 成功输出信息
    def success(self, success_msg):
        self.print_msg(self.SUCCESS, success_msg)

    # 正常输出调试信息
    def log(self, log_msg):
        self.print_msg(self.LOG, log_msg)

    # 错误输出信息
    def fail(self, error_msg):
        self.print_msg(self.FAIL, error_msg)

    # 异常输出信息
    def exception(self, exception_msg):
        print("=====异常======", exception_msg)
        self.print_msg(self.EXCEPTION, exception_msg)

    # 如下为测试样例
    def test_for_communication(self):
        try:
            print("Test中收到的CSharpToPythonTest为：", self.result_info)
            self.success(self.result_info)
            self.log(self.result_info)
            self.fail(self.result_info)
            self.exception(self.result_info)
            print("所有的元素是:" + str(self.result_info.keys()))
            return self.result_info
        except Exception as err:
            self.exception(err)
            return str(err)


class HttpService:
    def __init__(self):
        self.defaultUrl = 'http://127.0.0.1:8802'
        self.getUrl = "http://127.0.0.1:8802/request_handle"
        self.postUrl = "http://127.0.0.1:8802/instrument_handle"
        return

    # default get
    def get_default(self):
        r = requests.get(self.defaultUrl)  # 默认消息
        print("缺省获取" + r.text)

    # get消息示例
    def get_message(self, component):
        """
        :param component: 需要调用的接口及接口参数
        :return:
        """
        replay = requests.get(self.getUrl, params=component.__dict__)
        try:
            replyList = json.loads(replay.text)
            if replyList["result"] == "OK":
                print("get执行成功！\r\n" + replyList["message"])
            else:
                print("get执行错误！\r\n" + replyList["message"])
        except Exception as e:
            print("get异常" + str(e))

    # post消息
    def post_message(self, component):
        """
        :param component: 需要调用的接口及接口参数
        :return:
        """
        replay = requests.post(self.postUrl,  json=component.__dict__)
        try:
            replyList = json.loads(replay.text)
            if replyList["result"] == "OK":
                return replyList["message"]
            else:
                # 使用异常的错误信息字符串作为参数
                ex = Exception(replyList["message"])
                raise ex
        except Exception as e:
            raise e
