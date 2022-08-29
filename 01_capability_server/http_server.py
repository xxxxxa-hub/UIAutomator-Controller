# coding=utf-8
import inspect
import json
import numpy as np
from random import choice
from flask import Flask, request, jsonify, render_template
from flask_bootstrap import Bootstrap
import tkinter.messagebox
import pack_demo.module_demo
import pack_oscilloscope.module_baseband_voltage
import pack_phoneself.module_phone_run
import pack_oscilloscope.module_TEKMDO3054_SPItiming
import pack_oscilloscope.module_WAVERUNNER8254_SPIquality
import pack_oscilloscope.module_TEKMDO3054_SIMCardtiming
import pack_oscilloscope.module_TEKMDO3054_PowerQuality
import pack_oscilloscope.module_WAVERUNNER8254_SystemClock
import pack_oscilloscope.module_TEKMDO3054_OLEDtiming

app = Flask(__name__)  # 创建一个服务，赋值给APP
bootstrap = Bootstrap(app)
# 如下定义是用于查询模块功能使用，如果添加新的模块必须在下面数组中增加注册
registered_module_list = ["pack_demo.module_demo",
                          "pack_oscilloscope.module_baseband_voltage",
                          "pack_phoneself.module_phone_run",
                          "pack_oscilloscope.module_TEKMDO3054_SPItiming",          # SPI时序（杨阳）
                          "pack_oscilloscope.module_WAVERUNNER8254_SPIquality",     # SPI质量（胡蓉）
                          "pack_oscilloscope.module_TEKMDO3054_SIMCardtiming",      # SIM时序（王沐鑫）
                          "pack_oscilloscope.module_TEKMDO3054_PowerQuality",       # 电源质量测试（常一杰）
                          "pack_oscilloscope.module_WAVERUNNER8254_SystemClock",    # 系统时钟（胡蓉）
                          "pack_oscilloscope.module_TEKMDO3054_OLEDtiming"          # OLED时序（王沐鑫）
                          ]


class MessageList(object):
    def __init__(self, pack, module, interface, parameters):
        self.pack = pack
        self.module = module
        self.interface = interface
        self.parameters = parameters


@app.route('/CapabilityServerManagement', methods=['post', 'get'])
def result():
    message_list = []
    index = 1
    for registered_module in registered_module_list:
        module = __import__(registered_module, fromlist=True)
        if module is not None:
            list_functions = dir(module)
            for function in list_functions:
                if function.startswith('interface_'):
                    parameters = ''
                    func = getattr(module, function)
                    if func.__doc__:
                        parameters = parameters + func.__doc__
                    else:
                        parameters = parameters + '未定义的内容'
                    if not parameters.isspace():
                        message = {'id': index,
                                   'pack': registered_module.split('.')[0],
                                   'module': registered_module.split('.')[1],
                                   'interface': function,
                                   'parameters': parameters}
                        index += 1
                        message_list.append(message)
    info = request.values
    limit = info.get('limit', len(message_list))  # 每页显示的条数
    offset = info.get('offset', 0)  # 分片数，(页码-1)*limit，它表示一段数据的起点
    return jsonify({'total': len(message_list), 'rows': message_list[int(offset):(int(offset) + int(limit))]})


# 主目录
@app.route('/')
def query():
    return render_template('query.html')


# get消息
@app.route('/request_handle', methods=['get'])
def request_handle():
    try:
        data = request.args.to_dict()
        pack, module, interface = data['pack'], data['module'], data['interface']
        # 反射调用对应的模块，模块类型和接口
        obj = __import__(pack + "." + module, fromlist=True)
        if hasattr(obj, interface):
            func = getattr(obj, interface)
            msg = func(data)
            return jsonify(result="OK", message=msg)
        else:
            msg = '模块：' + pack + ',不存在接口：%s，调用失败！' % interface
            return jsonify(result="Fail", message=msg)
    except Exception as e:
        return jsonify(result="Exception", message=str(e))


# post消息
@app.route('/instrument_handle', methods=['post'])  # 指定接口访问的路径，支持什么请求方式get，post
def instrument_handle():
    try:
        # data = request.values.to_dict()
        data = request.json
        pack, module, interface = data['pack'], data['module'], data['interface']
        data = {key: val for key, val in data.items() if
                (key != 'pack' and key != 'module' and key != 'interface')}
        # 反射调用对应的包，模块和接口
        obj = __import__(pack + "." + module, fromlist=True)
        if hasattr(obj, interface):
            func = getattr(obj, interface)
            msg = func(**data)
            return jsonify(result="OK", message=msg)
        else:
            msg = '模块：' + pack + ',不存在接口：%s，调用失败！' % interface
            return jsonify(result="Fail", message=msg)
    except Exception as e:
        return jsonify(result="Exception", message=str(e))


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)


if __name__ == '__main__':
    app.run(host="localhost", port=8802)
