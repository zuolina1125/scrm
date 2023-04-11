import MySQLdb

import pytest


class MySqlUtil:

    conn = MySQLdb.connect(  # 获取一个conn
        user='root',
        passwd='aiSmart@70191',
        host='192.168.70.191',
        port=3306,
        db='scrm'
    )

    def get_mysql_data(self):
        query_sql = 'select task_name from task_info where potential_customer_id = 110'
        lst = []
        try:
            cursor = self.conn.cursor()  # 获取一个游标
            cursor.execute(query_sql)  # 游标执行sql语句
            r = cursor.fetchall()
            for x in r:
                lst.append(x)
            return lst
        finally:
            cursor.close()
            self.conn.close()


