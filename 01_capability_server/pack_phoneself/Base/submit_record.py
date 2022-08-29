import requests
import socket

URL = 'http://10.21.208.110:8089/api/services/app/Tool/SubmitUsingRecord'
HEADERS = {'Content-Type': 'application/json;charset=utf-8'}


def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    with s:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    return ip


def submit_record(using_duration, tool_name, instrument='', ip=None, hostname=None,
                  reserve1='', reserve2='', reserve3='', reserve4=''):
    """
    上传工具使用时长
    :param using_duration: 使用时长 单位:ms
    :param tool_name: 工具名称
    :param instrument: 仪表 建议上传*IDN?指令返回的字符串(去除后面的\n等符号)，多台仪表采用##连接
    :param ip: 本机ip
    :param hostname: 本机用户名
    :param reserve1: 保留字段1
    :param reserve2: 保留字段2
    :param reserve3: 保留字段3
    :param reserve4: 保留字段4
    :return: true或false
    """
    hostname = socket.gethostname() if not hostname else hostname
    ip = get_host_ip() if not ip else ip
    payload = {
        'usingDuration': using_duration,
        'ip': ip,
        'host': hostname,
        'toolName': tool_name,
        'instrument': instrument,
        'reserve1': reserve1,
        'reserve2': reserve2,
        'reserve3': reserve3,
        'reserve4': reserve4
    }
    response = requests.post(URL, headers=HEADERS, json=payload)
    if response.status_code != 200:
        return False
    return response.json().get('success')


if __name__ == '__main__':
    submit_record(1, 'AppControl')
