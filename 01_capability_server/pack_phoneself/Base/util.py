# coding=utf-8
import logging
import os
import re
import subprocess
import time
import yaml


class Log(object):
    step = 1

    class Type:
        SCREEN_ON = "【***亮起手机屏幕, Device ID：{}】"
        START_APP = "【***启动APP, package name：{}】"
        APP_STARTED = "【***启动APP成功, package name：{}】"
        STOP_APP = "【***关停APP, package name：{}】"
        FIND_ELEMENT = "【***查找元素：{}】"
        FIND_ERROR = "【***元素：{}未出现】"
        ELEMENT_FINDED = "【***找到元素：{}】"
        FIND_ELEMENTS = "【***查找元素集：{}】"
        ELEMENTS_FINDED = "【***找到元素集：{}】"
        CLICK = "【***点击元素：{}】"
        CLICKED = "【***元素已点击：{}】"
        CLICKFAIL = "【***元素点击失败：{}】"
        INPUT = "【***输入框：{}，预设值：{}】"
        HAD_INPUT = "【***输入框：{}, 当前值：{}】"
        INPUTFAIL = "【元素输入失败：{}】"
        SWIPE = "【***滑动： 第{}次】"
        ADB = "【***执行ADB命令：{}】"
        HAD_ADB = "【***执行ADB完成：{}】"
        OTHER = "【***其他消息：{}】"
        WAITELE = "【***等待元素：{}】"
        BLACKBOX = "【***黑名单出现：{}】"
        ERROR = "【***错误信息：{}】"
        SUCCESS = "【***执行成功：{}】"

    @classmethod
    def log_print(cls, msg_type, *args):
        temp = '{},' * len(args)
        value = temp[:len(temp) - 1]
        if msg_type.count('{}') == len(args):
            out = msg_type
        else:
            out = msg_type.replace('{}', value)
        if '错误信息' in msg_type:
            logging.warning(*args)
        else:
            print(out.format(*args))

    @classmethod
    def cut_step(cls, describe):
        length = int((30 - len(describe)) / 2)
        print('第%d步:%s%s%s' % (cls.step, '<' * length, describe, '>' * length))
        cls.step += 1

    @classmethod
    def cut_case(cls, caseName):
        cls.step = 1
        length = int((40 - len(caseName)) / 2)
        print('caseName:%s%s%s' % ('*' * length, caseName, '*' * length))


class YamlDate(object):

    def __init__(self):
        abspath = get_abs_path("\\Configs\\element_find.yaml")
        with open(abspath, 'r', encoding='utf-8') as f:
            self.paths = yaml.load(f.read(), Loader=yaml.FullLoader)

    def read(self, name):
        date = self.paths.get(name)
        return date

    def write(self, name, date_dict: dict):
        date = self.paths.get(name)
        desired_caps = date.update(date_dict)
        with open("test.yaml", "w", encoding="utf-8") as f:
            yaml.dump(desired_caps, f)


def get_abs_path(suffix):
    suffix = '\\' + suffix if suffix[:1] != '\\' else suffix
    suf_list = suffix.split('\\')
    suf_list.remove('')
    if len(suf_list) == 2:
        suf_dir, suf_file = suf_list[0], suf_list[-1]
        path = from_root_find(suf_dir, suf_file)
        if path: return path
    if len(suf_list) == 1:
        path = from_root_find(suf_list[0])
        if path: return path
    else:
        return None


def from_root_find(suf_dir, suf_file=None):
    temp, path = os.path.dirname(__file__), None
    parent_path = os.path.abspath(os.path.dirname(temp))
    for root, dirs, files in os.walk(parent_path):
        if suf_file:
            if suf_dir in root and suf_file in files:
                path = os.path.join(root, suf_file)
                break
        else:
            if suf_dir in dirs:
                path = os.path.join(root, suf_file)
    return path


def subprocess_Popen(cmd, time_out=10):
    out = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, encoding='gbk')
    begin_time = time.time()
    for i in range(time_out):
        if out.poll() is not None:
            break
        else:
            out.wait()
        second_time = time.time() - begin_time
        if time_out and second_time > time_out:
            out.terminate()
            return False
    stdout, stderr = out.communicate()
    out.terminate()
    if stderr is None:
        if type(stdout) == str:
            result = re.sub(r"\n|\t|\r", '', stdout)
        else:
            result = stdout
        return result
    return stderr


if __name__ == '__main__':
    pass
