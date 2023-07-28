'''
@file : mysql_client.py
@comment:
@date : 2021/02/22 16:20:55
@author : xiu.jiang
@version : 1.0
'''

import pymysql
import time
import traceback



class mysqlClient(object):
    def __init__(self,host,port,user,password,database_name):
        self.dbconnection = pymysql.connect(host=host, user=user,password=password, database=database_name, port=port,autocommit=True)
        self.cursors = self.dbconnection.cursor(pymysql.cursors.DictCursor)

    def commit(self, sql):
        try:
            self.cursors.execute(sql)
            self.dbconnection.commit()
        except Exception as e:
            print(e.__repr__())
            print(sql)
            self.dbconnection.rollback()


    def select(self, sql):
        try:
            self.cursors.execute(sql)
            self.data = self.cursors.fetchone()
            if self.data is None:
                self.data = {}
        except Exception as e:
            print(e.__repr__())
            print(sql)
            self.data = {}
            
        return self.data

    def close(self):
        self.cursors.close()
        self.dbconnection.close()


if __name__ == "__main__":
    pass
