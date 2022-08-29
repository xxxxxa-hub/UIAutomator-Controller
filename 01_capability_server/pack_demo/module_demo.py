# coding=utf-8
import json


def interface_initial(parameter1, parameter2, parameter3):
    """
    初始化接口
    :param parameter1:传入参数1
    :param parameter2:传入参数2
    :param parameter3:传入参数3
    :return:接口初始化信息
    """
    return "在Demo模块interface_initial接口中！" + parameter1 + parameter2 + parameter3


def interface_initial2(parameter1, parameter2, parameter3):
    """
    初始化接口
    :param parameter1:传入参数1
    :param parameter2:传入参数2
    :param parameter3:传入参数3
    :return:接口初始化信息
    """
    return "在Demo模块interface_initial接口中！" + parameter1 + parameter2 + parameter3


def interface_test_result(parameter1, parameter2):
    """
    返回测量结果接口
    :param parameter1: 传入参数1
    :param paremeter2: 传入参数2
    :return:
    """
    return parameter2 + parameter1 + ".png"
