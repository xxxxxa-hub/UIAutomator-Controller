# coding=utf-8
import sqlite3

from pack_phoneself.Base.util import get_abs_path


class Sqlite(object):

    def __init__(self, date_base):
        self.sql_connect = date_base

    def select_all(self, sql, params=None):
        format_list = []
        cursor = self.conn.cursor()
        with self.conn:
            obj = cursor.execute(sql)
            dates = cursor.fetchall()
            cursor.close()
            cols = [x[0] for x in obj.description]
            for date in dates:
                temp = {}
                for key, item in zip(cols, date):
                    temp[key] = item
                format_list.append(temp)
        return format_list

    @property
    def sql_connect(self):
        return self.conn

    @sql_connect.setter
    def sql_connect(self, library_name):
        base_path = get_abs_path('Configs\\' + library_name)
        self.conn = sqlite3.connect(base_path)


if __name__ == "__main__":
    sql1 = 'SELECT * FROM MTK WHERE C="SAR测试" and code="*#808#";'
    db = Sqlite('engineer.db')
    print(db.select_all(sql1))
