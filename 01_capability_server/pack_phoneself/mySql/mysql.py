# coding=utf-8
# @Time    : 2022/01/05 15:33
# @Author  : FU
# @File    : mysql.py
import datetime
import pymysql
import hashlib


class dbHelper(object):

    def __init__(self):
        self.host = '172.16.207.46'
        self.user = 'root'
        self.password = '1234qwer'
        self.port = 3306
        self.database = 'audiotest'
        self.settings = ''
        self.title_date = ''
        self.title_case = ''
        self.connect()

    def connect(self):
        self.conn = pymysql.connect(host=self.host, user=self.user, password=self.password, port=self.port,
                                    database=self.database)
        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)

    # 关闭
    def close(self):
        self.cursor.close()
        self.conn.close()

    def select_all(self, sql, params=None):
        self.cursor.execute(sql, params)
        datas = self.cursor.fetchall()
        return datas

    def select_one(self, sql, params=None):
        self.cursor.execute(sql, params)
        data = self.cursor.fetchone()
        return data

    # 封装增删改
    def oper(self, sql, params=None):
        row = 0
        try:
            row = self.cursor.execute(sql, params)
            self.conn.commit()
        except Exception as e:
            print(e)
        return row

    def insert(self, *params):
        if not self.find_one():
            args = (self.title_date, self.title_case, self.settings)
            sql = "INSERT INTO result set {}, {}, {};".format(*args)
            status = self.oper(sql, params)
        else:
            status = self.update()
        return status

    def delete(self, sql, params: []):
        return self.oper(sql, params)

    def update(self, *params):
        args = (self.settings, self.title_date, self.title_case)
        sql = "UPDATE result SET {} WHERE {} AND {};".format(*args)
        return self.oper(sql, params)

    def find_one(self, *params):
        args = (self.title_date, self.title_case)
        sql = "SELECT * FROM result WHERE {} AND {}".format(*args)
        try:
            self.cursor.execute(sql, params)
            data = self.cursor.fetchone()
        except Exception as e:
            data = None
            print(e)
        return data

    def find_all(self, *params):
        if self.title_date and self.title_case:
            args = (self.title_date, self.title_case)
            sql = "SELECT * FROM result WHERE {} AND {}".format(*args)
        else:
            if self.title_case or self.title_date:
                where = self.title_date if self.title_date else self.title_case
                sql = "SELECT * FROM result WHERE {}".format(where)
            else:
                sql = "SELECT * FROM result"
        # try:
        self.cursor.execute(sql, params)
        datas = self.cursor.fetchall()
        # except Exception as e:
        #     print(e)
        return datas

    def secret_sha256(self, password):
        sha256 = hashlib.sha256()
        sha256.update(password.encode('utf-8'))
        password = sha256.hexdigest()
        return password


def send_data_to_sql(result: dict):
    """
    向数据库输入测试结果，集成了 insert与update
    result_date：
     {'下行，解决': {'value': '0.244226', 'threshold': '0.08', 'note': 'THD', 'status': 'Fail'},}
    """
    db = dbHelper()
    date = datetime.datetime.today().strftime('%Y%m%d')
    for item in result.keys():
        temp = ''
        for key, value in result.get(item).items():
            temp = temp + "%s = '%s'," % (key, value)
        db.settings = temp[:-1]
        db.title_date = "date = '{}'".format(date)
        db.title_case = "caseName = '{}'".format(item)
        db.insert()
    db.close()


def get_data_from_sql(caseName: list, date=None):
    """
    获取某个时间的，指定case集群的数据
    返回类型为list
    """
    db = dbHelper()
    if date is None:
        date = datetime.datetime.today().strftime('%Y%m%d')
    request_date = []
    for item in caseName:
        db.title_date = "date = '{}'".format(date)
        db.title_case = "caseName = '{}'".format(item)
        request_date.append(db.find_one())
    db.close()
    return request_date


def get_all_from_sql(caseName: list = None, date=None):
    """
    caseName不空，则返回一个字大点，如{'上行':[{}, {},]}
    caseName 空，返回list
    """
    db = dbHelper()
    db.title_date = "date = '{}'".format(date) if date else None
    result_list = []
    if caseName is None:
        caseName = []
    for case in caseName:
        db.title_case = "caseName = '{}'".format(case)
        result = db.find_all()
        result_list = result_list + list(result)
    if caseName and result_list:
        db.close()
        return result_list
    result_list = db.find_all()
    db.close()
    return result_list


if __name__ == '__main__':
    data = {
        '下行，音频客观指标，测试THD，音量15级': {'value': '0.2442263939614077', 'threshold': '0.08', 'note': 'THD', 'status': 'Fail'},
        '下行，音频客观指标，testingGap': {'status': 'Pass', 'value': '0.2442263939614077', 'threshold': '0.08', 'note': 'THD'},
        '下行，音频客观指标，Pink测试': {'status': 'Pass', 'value': '0.2442263939614077', 'threshold': '0.08', 'note': 'THD'},
        '下行，音频客观指标，Dukou测试': {'status': 'Pass', 'value': '0.2442263939614077', 'threshold': '0.08', 'note': 'THD'},
        '下行，音频客观指标，播放混合信号，覆盖到最大到最小15级音量': {'status': 'Pass', 'value': '', 'threshold': '', 'note': ''},
        '下行，音频功能 连续慢/快速，点击“上一曲”、“下一曲”': {'status': 'Pass333', 'value': '', 'threshold': '', 'note': ''},
        '下行，音频功能 连续慢/快速，点击“播放”、“暂停”': {'status': 'Pass222', 'value': '', 'threshold': '', 'note': ''},
        '下行，视频功能 连续慢速、快速点击“播放”、“暂停”': {'status': 'Pass111', 'value': '', 'threshold': '', 'note': ''},
        '下行，开始第四次尝试新增ITEM': {'status': 'pass333', 'value': '', 'threshold': '', 'note': ''}}
    # send_data_to_sql(data)
    send_data_to_sql(data)
