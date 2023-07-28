# -*- coding:utf-8-*-
# Author：Jack Ferrous
# 测试数据记录
# Version 2.1.2

import pymysql
from platformkey import platform_key

password_ = ''


class MysqlObject(object):
    def __init__(self, ip="172.16.216.117", port=3308, username="autotest", password=password_, database="auto_test"):
        self.db = pymysql.connect(ip, username, platform_key(password), database, port, autocommit=True,
                                  charset='utf8mb4')

    def commit__(self, sql):
        cursor = self.db.cursor()
        try:
            print('打印sql', sql)
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            self.db.commit()
        except Exception as e:
            print(e)
            # 如果发生错误则回滚
            self.db.rollback()

    def select__(self, sql):
        try:
            print('开始打印sql:', sql)
            cursor = self.db.cursor()
            cursor.execute(sql)
            data = cursor.fetchone()
            if data is None:
                data = []
        except Exception:
            data = []

    def close__(self):
        self.db.close()


if __name__ == '__main__':
    aa = MysqlObject()
    print(aa.select__('select 1 from dual'))
    aa.close__()
