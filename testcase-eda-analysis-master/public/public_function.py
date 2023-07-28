#!/usr/bin/env python3
# -*-coding:utf-8-*-
# author by JackFerrous
# Version 2.1.2
# __author__ = "ferrous.feng"
import codecs
import ftplib
import logging
import os
import random, time, datetime
from datetime import date
import sys

import paramiko

sys.path.append(r'D:\autotestdata\testcase-eda-analysis-ui')
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(os.path.split(rootPath)[0])
import yaml
from loguru import logger
from xlutils.copy import copy
import xlrd


# class NoConfigKeyError(Exception):


"""
# def getConfig(section, key):
#     import configparser
#     import sys
#     #  获取配置文件中指定的参数111
#
#     # 地址需要变更
#     if test_api_path not in sys.path:
#         sys.path.append(test_api_path)
#     conf = configparser.ConfigParser()
#     # print(test_api_path)
#     conf.read('{}/disconf.ini'.format(test_api_path))
#     # s1=conf.items(section)
#     # print('path:',sys.path())
#     s = conf.options(section)
#     # print('section:',section,s)
#     if key.lower() in s:
#         # print(key)
#         value = conf.get(section, key)
#         # print(value)
#     else:
#         raise NoConfigKeyError("no KEY NAMED %s in SECTION--%s in FILE disconf.ini" % (key, section))
#     return (value)
#
#
# def setConfig(section, name, value):
#     import configparser
#     import sys
#     # 地址需要变更
#     if test_api_path not in sys.path:
#         sys.path.append(test_api_path)
#     conf = configparser.ConfigParser()
#     # print(test_api_path)
#     conf.read('{}//disconf.ini'.format(test_api_path))
#     conf.set(section, name, value)
#     f = open('{}//disconf.ini'.format(test_api_path), 'r+')
#     conf.write(f)
#     f.close()

    1- 读取excel数据
def get_excelData(sheetName, startRow, endRow, body=6, repsData=8):
    resList = []
    excelDir = '../data/松勤-教管系统接口测试用例-v1.4.xls'
    workBook = xlrd.open_workbook(excelDir, formatting_info=True)
    workSheet = workBook.sheet_by_name(sheetName)
    # 获取单元格
    for one in range(startRow - 1, endRow):
        resList.append((workSheet.cell(one, body).value, workSheet.cell(one, repsData).value))
    return resList


"""


# 读取excel数据
def excel_read(fileName, SheetName="Sheet1"):
    data = xlrd.open_workbook(fileName)
    table = data.sheet_by_name(SheetName)

    # 获取总行数、总列数,ncols = table.ncols
    nrows = table.nrows
    if nrows > 1:
        # 获取第一行的内容，列表格式
        keys = table.row_values(0)
        # print(keys)
        listApiData = []
        # 获取每一行的内容，列表格式
        for col in range(1, nrows):
            values = table.row_values(col)
            if len(values[0]) > 0:
                # keys，values这两个列表一一对应来组合转换为字典
                api_dict = dict(zip(keys, values))
                # print(api_dict)
                listApiData.append(api_dict)

        return listApiData
    else:
        # print("表格未填写数据")
        return []


# 返回上级目录
def superior_path():
    module_parent_path = os.path.join(os.path.dirname(os.path.dirname(__file__)))
    return module_parent_path


# 当前目录
def current_path():
    module_parent_path = os.path.join(os.path.dirname(__file__))
    return module_parent_path


# 获取ini文件
def get_ini(section, key):
    import configparser
    cf = configparser.ConfigParser()
    dir_path = current_path()
    ini_path = dir_path + '/disconf.ini'
    cf.read(ini_path)
    value = cf.get(section, key)
    return value


# 写入excel
def excel_write(results=None, newsheet=0, startRow=0, colNum=10, open_file_name="/testdatas/point_SIT_03.xls",
               save_file_name=None):
    data = xlrd.open_workbook(open_file_name, formatting_info=True)
    newWorkBook = copy(data)
    writeSheet = newWorkBook.get_sheet(newsheet)
    writeSheet.write(startRow + 1, colNum, results)
    newWorkBook.save(save_file_name)


# 读取yaml文件
def yaml_read(yaml_name):
    yml_path = open(superior_path() + yaml_name, encoding="UTF-8")
    datas = yaml.load(yml_path, Loader=yaml.FullLoader)  # 预防警告
    return datas

    # FTP文件上传下载


class FTP_OP:
    ftp = ftplib.FTP()

    def __init__(self, host, port=21):
        self.ftp.connect(host, port)
        self.ftp.encoding = 'gbk'

    def Login(self, user, passwd):
        self.ftp.login(user, passwd)
        print(self.ftp.welcome)

    def DownLoadFile(self, LocalFile, RemoteFile):  # 下载单个文件
        file_handler = open(LocalFile, 'wb')
        self.ftp.retrbinary('RETR ' + RemoteFile, file_handler.write)
        file_handler.close()
        return True

    def UpLoadFile(self, LocalFile, RemoteFile):  # 上传单个文件
        file_handler = open(LocalFile, 'rb')
        self.ftp.storbinary('STOR ' + RemoteFile, file_handler)
        file_handler.close()
        return True

    def DownLoadFileTree(self, LocalDir, RemoteDir):  # 下载整个目录下的文件
        # print("远程文件夹remoteDir:", RemoteDir)
        if not os.path.exists(LocalDir):
            os.makedirs(LocalDir)
        self.ftp.cwd(RemoteDir)
        RemoteNames = self.ftp.nlst()
        # print("远程文件目录:", RemoteNames)
        for file in RemoteNames:
            Local = os.path.join(LocalDir, file)
            print("正在下载", self.ftp.nlst(file))
            if file.find(".") == -1:
                if not os.path.exists(Local):
                    os.makedirs(Local)
                self.DownLoadFileTree(Local, file)
            else:
                self.DownLoadFile(Local, file)
        self.ftp.cwd("..")
        return

    def close(self):
        self.ftp.quit()


# command命令
def cmd_server(hostname, username, password, cmd):
    ssh = paramiko.SSHClient()
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, username=username, password=password)
    stdin_, stdout_, stderr_ = ssh.exec_command(cmd)
    stdout_.channel.recv_exit_status()
    ssh.close()
    result = stdout_.read().decode('utf-8')[:-1]
    logger.info(result)
    # print(time + ' | ' + result)
    return result


# SFTP上传文件
def sftp_upload(url, username, password, source_path):
    data_list = []
    transport = paramiko.Transport((url, 22))
    transport.connect(username=username, password=password)
    sftp_upload = paramiko.SFTPClient.from_transport(transport)
    old_path = "../testdata/HN/"
    old_names = os.listdir("old_path")
    times = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    for old_name in old_names:
        os.rename(old_path + old_name,
                  f"../testdata/HN/HNQJ_50" + "_" + times + "_CH" + old_name.split("_CH")[1])
    # 遍历目录下的文件名
    new_names = os.listdir(old_path)
    for new_name in new_names:
        os.rename("../testdata/HN/" + new_name,
                  f"../testdata/HN/HNQJ_50" + "_" + times + "_CH" + new_name.split("_CH")[1])
        sftp_upload.put(f"../testdata/HN/{new_name}",
                        source_path + new_name)
        data_list.append(new_name)
        logger.info(new_name + "---上传成功")
    transport.close()
    logger.info(data_list)
    return data_list


def module_path():
    return os.getcwd()


# 日志输出报告
class PropogateHandler(logging.Handler):
    def emit(self, record):
        logging.getLogger(record.name).handle(record)


logger.add(PropogateHandler(), format="| {time:YYYY-MM-DD HH:mm:ss} - {message}")


