# -*- coding: utf-8 -*-
"""
@project : Galileo
@author: LYF
@file: EDA_data_center.py
@ide: PyCharm
@time: 2021-12-29 10:00
"""
import os
import time

from loguru import logger
import socket
from pageelements.base_page import BasePage, readfile
from public.public_function import yaml_read
from dbiz_autotest_sdk.encrypt import decrypt

data = yaml_read(yaml_name="/config/data_center_element.yml")
config = yaml_read(yaml_name="/config/config.yml")
mysql_password = decrypt(public_key=config["mysql_password_key"], encryped_pwd=config["mysql_password"])
autotest_password = decrypt(public_key=config["autotest_password_key"], encryped_pwd=config["autotest_password"])
autotest2_password = decrypt(public_key=config["autotest2_password_key"], encryped_pwd=config["autotest2_password"])

failed = 'assert failed'
success = "assert success"


class EDADataCenter(BasePage):

    # 进入数据中心公用方法
    def enter_data_center(self):
        # 刷新页面
        self.fresh_()

        # 点击--数据中心
        self.move_to_element_(self.find_element_by_xpath(data['data_center']))

        time.sleep(1)

        # 点击--平台数据查询
        self.find_element_by_link_text("平台数据查询").click()

    # 数据中心-平台数据查询-查询目录列表
    def query_directory(self):
        # 进入数据中心
        self.enter_data_center()

        # 点击--风场风机资产主数据
        self.find_element_by_xpath(
            "//*[@id='root']/div/section/section/section/main/div/div[2]/div/div/div[1]/div[2]/ul/li[1]/div").click()
        self.find_element_by_xpath(
            "//*[@id='1410158166003490817$Menu']/li[2]").click()
        self.asserts("//div[text()='风场风机资产主数据']", log=False)

        # 点击--DT通道说明表
        self.find_element_by_xpath("//li[text()='DT通道说明表']").click()
        self.asserts("//div[text()='DT通道说明表']", log=False)

        # 点击--Digital Twin数据运行特征介绍表
        self.find_element_by_xpath("//li[text()='Digital Twin数据运行特征介绍表']").click()

        # 点击--DigitalTwin秒级通道说明列表
        self.find_element_by_xpath("//li[text()='DigitalTwin秒级通道说明列表']").click()

        # 点击--集成测试环境所有风机数据量
        self.find_element_by_xpath(data['all_fan']).click()
        self.asserts("//div[text()='集成测试环境所有风机数据量']", log=False)

        # 断言
        asserts = self.asserts("//div[text()='集成测试环境所有风机数据量']")
        return asserts

    # 数据中心-数据中心-点击全量风场资产数据，点击右侧快速过滤，弹窗展示
    def rapid_filtration_1(self):
        self.enter_data_center()

        # 点击--风场风机资产主数据
        self.find_element_by_xpath(
            "//*[@id='root']/div/section/section/section/main/div/div[2]/div/div/div[1]/div[2]/ul/li[1]/div").click()
        self.find_element_by_xpath(
            "//*[@id='1410158166003490817$Menu']/li[2]").click()

        # 点击--快速过滤
        self.move_to_element_(self.find_element_by_xpath(data['filtration']))
        self.click_()

        # 断言
        asserts = self.asserts(
            "//div[text()='显示列']")
        return asserts

    # 数据中心-快速过滤窗口，点击取消，弹窗关闭
    def rapid_filtration_2(self):
        self.enter_data_center()

        # 点击--风场风机资产主数据,升级后需要先点击表才能开始过滤
        self.find_element_by_xpath(
            "//*[@id='root']/div/section/section/section/main/div/div[2]/div/div/div[1]/div[2]/ul/li[1]/div").click()

        # 点击风场表
        self.find_element_by_xpath(
            "//*[@id='1410158166003490817$Menu']/li[2]").click()

        # 点击--快速过滤
        self.move_to_element_(self.find_element_by_xpath(data['filtration']))
        self.click_()

        # 点击--取消
        self.move_to_element_(self.find_element_by_xpath("//span[text()='取 消']"))
        self.click_()

        # 断言
        asserts = self.asserts("//div[text()='快速过滤']", log=False)
        if asserts:
            logger.info(failed)
            return False
        else:
            logger.info("assert success")
            return True

    # 数据中心-输入风场CN号，检查列表筛选结果
    def rapid_filtration_3(self):
        self.enter_data_center()

        # 点击--伽利略数据平台主数据,升级后需要先点击表才能开始过滤
        self.find_element_by_xpath('//div[@title="伽利略数据平台主数据"]').click()

        # 点击风场表
        self.find_element_by_xpath('//li[@title="全量风场资产数据"]').click()

        # 点击--快速过滤
        self.move_to_element_(self.find_element_by_xpath(data['filtration']))
        self.click_()

        # 点击--显示列筛选框
        self.find_element_by_xpath(
            '/html/body/div[3]/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/div[2]/div/div[1]/div/div[1]').click()

        # 点击--风场cn号列
        self.find_element_by_xpath(
            '//div[@title="风场cn号"]').click()

        # 点击--风机cn号列
        self.find_element_by_xpath(
            '//div[@title="风场名称"]').click()

        # 点击--确定
        self.move_to_element_(self.find_element_by_xpath(data['confirm']))
        self.click_()

        # 点击展示字段框
        self.find_element_by_xpath(
            "/html/body/div[3]/div/div[2]/div/div[2]/div[2]/div[3]/div/div[2]/div/div[1]/div[2]/div/div/div").click()

        # 点击--风场cn号
        self.find_element_by_xpath('//li[text()="风场cn号"]').click()

        # 点击--添加或(OR)条件
        self.move_to_element_(self.find_element_by_xpath('//span[text()="添加或(OR)条件"]'))
        self.click_()

        # 输入风场cn号
        self.find_element_by_xpath(
            '//div/table/tbody/tr/td[4]/div/div/div').click()

        self.find_element_by_xpath('//li[text()="包含"]').click()

        self.find_element_by_xpath('//table/tbody/tr/td[5]/input').send_keys('CN-25/25')

        # 点击--确定
        self.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/div[2]/div[3]/div/button[2]').click()

        # 校验
        self.find_element_by_xpath("//span[text()='CN-25/25']")

        # 断言
        asserts = self.asserts("//div[text()='CN-25/25']")
        return asserts

    # 数据中心-输入风机号，检查列表筛选结果
    def rapid_filtration_4(self):
        self.enter_data_center()

        # 点击--风场风机资产主数据,升级后需要先点击表才能开始过滤
        self.find_element_by_xpath('//div[@title="伽利略数据平台主数据"]').click()

        # 点击--风场风机资产主数据
        self.find_element_by_xpath("//li[text()='风场风机资产主数据']").click()

        # 点击--快速过滤
        self.move_to_element_(self.find_element_by_xpath(data['filtration']))
        self.click_()

        # 点击--显示列筛选框
        self.find_element_by_xpath(
            '/html/body/div[3]/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/div[2]/div/div[1]/div/div[1]').click()

        # 点击--风场cn号列
        self.find_element_by_xpath('//div[@title="风场cn号"]').click()

        # 点击--风机cn号列
        self.find_element_by_xpath('//div[@title="风机cn号"]').click()

        # 点击--确定
        self.move_to_element_(self.find_element_by_xpath(data['confirm']))
        self.click_()

        # 点击展示字段框
        self.find_element_by_xpath(
            "/html/body/div[3]/div/div[2]/div/div[2]/div[2]/div[3]/div/div[2]/div/div[1]/div[2]/div/div/div").click()

        # 点击--风机cn号
        self.find_element_by_xpath('//li[text()="风机cn号"]').click()

        # 点击--添加或(OR)条件
        self.move_to_element_(self.find_element_by_xpath('//span[text()="添加或(OR)条件"]'))
        self.click_()

        # 输入风场cn号
        self.find_element_by_xpath(
            '//div/table/tbody/tr/td[4]/div/div/div').click()

        self.find_element_by_xpath('//li[text()="包含"]').click()

        self.find_element_by_xpath('//table/tbody/tr/td[5]/input').send_keys('CN-25/25-B-001')

        # 点击--确定
        self.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/div[2]/div[3]/div/button[2]').click()

        # 校验
        self.find_element_by_xpath("//div[text()='CN-25/25-B-001']")

        # 断言
        asserts = self.asserts("//div[text()='CN-25/25-B-001']")
        return asserts

    # 数据中心-数据中心界面，点击右侧导出过滤后数据图标，导出excel，内容为列表筛选的结果
    def rapid_filtration_5(self):
        self.enter_data_center()

        # 点击--伽利略数据平台主数据,升级后需要先点击表才能开始过滤
        self.find_element_by_xpath('//div[@title="伽利略数据平台主数据"]').click()

        # 点击风场表
        self.find_element_by_xpath('//li[@title="全量风场资产数据"]').click()

        # 点击--快速过滤
        self.move_to_element_(self.find_element_by_xpath(data['filtration']))
        self.click_()

        # 点击--显示列筛选框
        self.find_element_by_xpath(
            '/html/body/div[3]/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/div[2]/div/div[1]/div/div[1]').click()

        # 点击--风场cn号列
        self.find_element_by_xpath(
            '//div[@title="风场cn号"]').click()

        # 点击--风场名称列
        self.find_element_by_xpath(
            '//div[@title="风场名称"]').click()

        # 点击--风场缩写列
        self.find_element_by_xpath(
            '//div[@title="风场缩写"]').click()

        # 点击--区域列
        self.find_element_by_xpath(
            '//div[@title="区域"]').click()

        # 点击--项目号列
        self.find_element_by_xpath(
            '//div[@title="项目号"]').click()

        # 点击--确定
        self.move_to_element_(self.find_element_by_xpath(data['confirm']))
        self.click_()

        # 点击展示字段框
        self.find_element_by_xpath(
            "/html/body/div[3]/div/div[2]/div/div[2]/div[2]/div[3]/div/div[2]/div/div[1]/div[2]/div/div/div").click()

        # 点击--风场cn号
        self.find_element_by_xpath('//li[text()="风场cn号"]').click()

        # 点击--添加或(OR)条件
        self.move_to_element_(self.find_element_by_xpath('//span[text()="添加或(OR)条件"]'))
        self.click_()

        # 输入风场cn号
        self.find_element_by_xpath(
            '//div/table/tbody/tr/td[4]/div/div/div').click()

        self.find_element_by_xpath('//li[text()="包含"]').click()

        self.find_element_by_xpath('//table/tbody/tr/td[5]/input').send_keys('CN-03/16')

        # 点击--确定
        self.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/div[2]/div[3]/div/button[2]').click()

        # 校验
        self.find_element_by_xpath("//span[text()='CN-03/16']")

        # 点击--导出过滤数据图标
        self.move_to_element_(self.find_element_by_xpath("//i[@class='anticon anticon-export']"))
        self.click_()

        self.time_sleep(level='level16')

        # 获取计算机名称
        hostname = socket.gethostname()
        if hostname == "L-007167":  # 我自己改的自己的电脑名称
            path = r"C:\Users\jing.huang6\Downloads\export.csv"
        else:
            path = "C:/Users/Administrator/Downloads/export.csv"

        csv_content = readfile(path)

        # 删除导出的csv文件
        os.remove(path)

        # 断言
        if csv_content == ['CN-03/16', '江苏九鼎山西绛县衡水紫金山', 'SXJX', '晋', 'P-0249']:
            logger.info(success)
            return True
        else:
            logger.info(failed)
            return False

    # 数据中心-验证清除过滤按钮
    def rapid_filtration_6(self):

        self.enter_data_center()

        # 点击--风场风机资产主数据,升级后需要先点击表才能开始过滤
        self.find_element_by_xpath('//div[@title="伽利略数据平台主数据"]').click()

        # 点击--风场风机资产主数据
        self.find_element_by_xpath(data['all_fan']).click()

        # 点击--快速过滤
        self.move_to_element_(self.find_element_by_xpath(data['filtration']))
        self.click_()

        # 点击--显示列筛选框
        self.find_element_by_xpath(
            '/html/body/div[3]/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/div[2]/div/div[1]/div/div[1]').click()

        # 点击--风场cn号列
        self.find_element_by_xpath('//div[@title="风场名称"]').click()

        # 点击--风机cn号列
        self.find_element_by_xpath('//div[@title="风机cn号"]').click()

        # 点击--确定
        self.move_to_element_(self.find_element_by_xpath(data['confirm']))
        self.click_()

        # 点击--确定
        self.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/div[2]/div[3]/div/button[2]').click()

        # 点击--集成风场名称列--原因为搜索图案平时是隐藏的，点击后进行展示方可操作
        self.find_element_by_xpath('//span[text()="风场名称"]').click()

        # 点击--风场名称右侧搜索图标
        self.move_to_element_(self.find_element_by_xpath(data['icon']))
        self.click_()

        # 点击--搜索框
        self.find_element_by_xpath(data['search']).click()

        # 输入--海上
        self.send_key_direct("海上")

        # 点击--清空过滤
        self.move_to_element_(self.find_element_by_xpath("//span[text()='清空过滤']"))
        self.click_()

        # 断言
        asserts = self.asserts("//div[text()='CN-23/53-B-001']")
        return asserts

    # 数据中心-点击集成测试环境所有风机数据量，验证搜索框模糊查询
    def rapid_filtration_7(self):

        self.enter_data_center()

        # 点击--风场风机资产主数据,升级后需要先点击表才能开始过滤
        self.find_element_by_xpath('//div[@title="伽利略数据平台主数据"]').click()

        # 点击--风场风机资产主数据
        self.find_element_by_xpath(data['all_fan']).click()

        # 点击--快速过滤
        self.move_to_element_(self.find_element_by_xpath(data['filtration']))
        self.click_()

        # 点击--显示列筛选框
        self.find_element_by_xpath(
            '/html/body/div[3]/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/div[2]/div/div[1]/div/div[1]').click()

        # 点击--风场cn号列
        self.find_element_by_xpath('//div[@title="风场名称"]').click()

        # 点击--风机cn号列
        self.find_element_by_xpath('//div[@title="风机cn号"]').click()

        # 点击--确定
        self.move_to_element_(self.find_element_by_xpath(data['confirm']))
        self.click_()

        # 点击--确定
        self.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/div[2]/div[3]/div/button[2]').click()

        # 点击--集成测试环境所有风机数据量
        self.find_element_by_xpath('//span[text()="风场名称"]').click()

        # 点击--风场名称右侧搜索图标
        self.move_to_element_(self.find_element_by_xpath(data['icon']))
        self.click_()

        # 点击--搜索框
        self.find_element_by_xpath(data['search']).click()

        # 输入--海上
        self.send_key_direct("海上")

        # 断言
        asserts = self.asserts("//div[text()='江苏九思海上']")
        return asserts

    # 数据中心-点击集成测试环境所有风机数据量，验证过滤功能
    def rapid_filtration_8(self):

        self.enter_data_center()

        # 点击--风场风机资产主数据,升级后需要先点击表才能开始过滤
        self.find_element_by_xpath('//div[@title="伽利略数据平台主数据"]').click()

        # 点击--风场风机资产主数据
        self.find_element_by_xpath(data['all_fan']).click()

        # 点击--快速过滤
        self.move_to_element_(self.find_element_by_xpath(data['filtration']))
        self.click_()

        # 点击--显示列筛选框
        self.find_element_by_xpath(
            '/html/body/div[3]/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/div[2]/div/div[1]/div/div[1]').click()

        # 点击--风场cn号列
        self.find_element_by_xpath('//div[@title="风场名称"]').click()

        # 点击--风机cn号列
        self.find_element_by_xpath('//div[@title="风机cn号"]').click()

        # 点击--确定
        self.move_to_element_(self.find_element_by_xpath(data['confirm']))
        self.click_()

        # 点击--确定
        self.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/div[2]/div[3]/div/button[2]').click()

        # 点击--集成测试环境所有风机数据量
        self.find_element_by_xpath('//span[text()="风场名称"]').click()

        # 点击--风场名称右侧搜索图标
        self.move_to_element_(self.find_element_by_xpath(data['icon']))
        self.click_()

        # 点击--搜索框
        self.find_element_by_xpath(data['search']).click()

        # 输入--海上
        self.send_key_direct("江苏九思海上")

        # 点击--导出过滤数据图标
        self.move_to_element_(self.find_element_by_xpath("//i[@class='anticon anticon-export']"))
        self.click_()

        time.sleep(10)
        # 获取计算机名称
        hostname = socket.gethostname()
        if hostname == "L-007167":
            path = r"C:\Users\jing.huang6\Downloads\export.csv"
        else:
            path = "C:/Users/Administrator/Downloads/export.csv"

        csv_content = readfile(path)[0]

        # 删除导出的csv文件
        os.remove(path)

        # 断言
        if csv_content == "江苏九思海上":
            logger.info(success)
            return True
        else:
            logger.info(failed)
            return False

    # 数据中心-点击集成测试环境所有风机数据量，验证清除功能
    def rapid_filtration_9(self):

        self.enter_data_center()

        # 点击--风场风机资产主数据,升级后需要先点击表才能开始过滤
        self.find_element_by_xpath('//div[@title="伽利略数据平台主数据"]').click()

        # 点击--风场风机资产主数据
        self.find_element_by_xpath(data['all_fan']).click()

        # 点击--快速过滤
        self.move_to_element_(self.find_element_by_xpath(data['filtration']))
        self.click_()

        # 点击--显示列筛选框
        self.find_element_by_xpath(
            '/html/body/div[3]/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/div[2]/div/div[1]/div/div[1]').click()

        # 点击--风场cn号列
        self.find_element_by_xpath('//div[@title="风场名称"]').click()

        # 点击--风机cn号列
        self.find_element_by_xpath('//div[@title="风机cn号"]').click()

        # 点击--确定
        self.move_to_element_(self.find_element_by_xpath(data['confirm']))
        self.click_()

        # 点击--确定
        self.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/div[2]/div[3]/div/button[2]').click()

        # 点击--集成测试环境所有风机数据量
        self.find_element_by_xpath('//span[text()="风场名称"]').click()

        # 点击--风场名称右侧搜索图标
        self.move_to_element_(self.find_element_by_xpath(data['icon']))
        self.click_()

        # 点击--搜索框
        self.find_element_by_xpath(data['search']).click()

        # 输入--海上
        self.send_key_direct("海上")

        # 点击清空过滤
        self.move_to_element_(self.find_element_by_xpath("//span[text()='清空过滤']"))
        self.click_()

        # 断言
        asserts = self.asserts(
            '//div[text()="CN-23/53-B-001"]')

        if asserts:
            logger.info(success)
            return True
        else:
            logger.info(failed)
            return False

    # 数据中心-数据质量查询通用方法
    def data_quality_query_public(self, data_type=None):

        # 刷新页面
        self.fresh_()

        # 点击--数据中心
        self.move_to_element_(self.find_element_by_xpath(data['data_center']))
        time.sleep(1)

        # 点击--平台数据查询
        self.find_element_by_link_text("数据质量查询").click()

        # 点击--请选择数据源类型
        self.find_element_by_xpath("//div[text()='请选择数据源类型']").click()

        # 点击--数据源类型
        self.find_element_by_xpath(f"//li[text()='{data_type}']").click()

        # 点击--风场下拉框
        self.find_element_by_xpath(
            "//form[@class='ant-form ant-form-horizontal']/div[2]/div/div[2]/div/span/div/div[1]/div/div").click()

        # 选择--区域
        self.find_element_by_xpath("//div[text()='CL-01/02']").click()

        # 点击--确 定
        self.move_to_element_(self.find_element_by_xpath(data['confirm']))
        self.click_()

        # 点击--风机下拉框
        self.find_element_by_xpath(
            "//form[@class='ant-form ant-form-horizontal']/div[3]/div[2]").click()

        # 选择--区域
        self.find_element_by_xpath("//div[text()='CL-01/02-B-001']").click()

        # 点击--确 定
        self.move_to_element_(self.find_element_by_xpath(
            "//form[@class='ant-form ant-form-horizontal']/div[3]/div[2]/div/span/div/div[2]/div/div/div/div/div[2]/button[2]/span"))
        self.click_()

        # 点击--查 询
        self.move_to_element_(self.find_element_by_xpath("//span[text()='查 询']"))
        self.click_()

        # 点击--下钻风机
        try:
            self.find_element_by_xpath("//div[text()='下钻风机']").click()
        except Exception as e:
            logger.info(e)

    # 数据中心-验证DigitalTwin-10minData正常查询
    def data_quality_query_1(self):

        # 调用数据质量查询通用方法
        self.data_quality_query_public(data_type="DigitalTwin-10minData")

        # 断言
        asserts = self.asserts(data['fan_quality'])
        return asserts

    # 数据中心-验证DigitalTwin-1sData正常查询
    def data_quality_query_2(self):
        # 调用数据质量查询通用方法
        self.data_quality_query_public(data_type="DigitalTwin-1sData")

        # 断言
        asserts = self.asserts(data['fan_quality'])
        return asserts

    # 数据中心-验证SOE-Event正常查询
    def data_quality_query_3(self):
        # 调用数据质量查询通用方法
        self.data_quality_query_public(data_type="SOE-Event")

        # 断言
        asserts = self.asserts("//h3[text()='SOE-Event数据近半年各周次入仓数据量统计']")
        return asserts

    # 数据中心-验证Highspeed-IPC正常查询
    def data_quality_query_4(self):
        # 调用数据质量查询通用方法
        self.data_quality_query_public(data_type="Highspeed-IPC")

        # 断言
        asserts = self.asserts(data['fan_quality'])
        return asserts

    # 数据中心-验证Highspeed-LaseForTower正常查询
    def data_quality_query_5(self):
        # 调用数据质量查询通用方法
        self.data_quality_query_public(data_type="Highspeed-LaseForTower")

        # 断言
        asserts = self.asserts(data['fan_quality'])
        return asserts

    # 数据中心-验证Highspeed-Offshore正常查询
    def data_quality_query_6(self):
        # 调用数据质量查询通用方法
        self.data_quality_query_public(data_type="Highspeed-Offshore")

        # 断言
        asserts = self.asserts(data['fan_quality'])
        return asserts

    # 数据中心-验证Highspeed-Vibration正常查询
    def data_quality_query_7(self):
        # 调用数据质量查询通用方法
        self.data_quality_query_public(data_type="Highspeed-Vibration")

        # 断言
        asserts = self.asserts(data['fan_quality'])
        return asserts

    # 数据中心-验证CMS正常查询
    def data_quality_query_8(self):
        # 调用数据质量查询通用方法
        self.data_quality_query_public(data_type="CMS")

        # 断言
        asserts = self.asserts(data['fan_quality'])
        return asserts

    # 数据中心-验证Scada正常查询
    def data_quality_query_9(self):
        # 调用数据质量查询通用方法
        self.data_quality_query_public(data_type="Scada")

        # 断言
        asserts = self.asserts(data['fan_quality'])
        return asserts

    # 数据中心-验证Tracelog正常查询
    def data_quality_query_10(self):
        # 调用数据质量查询通用方法
        self.data_quality_query_public(data_type="Tracelog")

        # 断言
        asserts = self.asserts(data['fan_quality'])
        return asserts

    # 数据中心-验证VDM正常查询
    def data_quality_query_11(self):
        # 刷新页面
        self.fresh_()

        # 点击--数据中心
        self.move_to_element_(self.find_element_by_xpath(data['data_center']))
        time.sleep(1)

        # 点击--平台数据查询
        self.find_element_by_link_text("数据质量查询").click()

        # 点击--请选择数据源类型
        self.find_element_by_xpath("//div[text()='请选择数据源类型']").click()

        # 点击--数据源类型
        self.find_element_by_xpath("//li[text()='VDM样机测试数据']").click()

        # 点击--请选择风场
        self.find_element_by_xpath("//div[text()='请选择风场']").click()

        # 选择--风场
        self.find_element_by_xpath("//li[text()='山西广灵望狐(Guangling_Wanghu)']").click()

        # 点击--请选择风机
        self.find_element_by_xpath("//*[@id='turbine']/div/div").click()

        # 选择--区域
        self.find_element_by_xpath("//li[text()='EN30_LZ156_90HH_SXGL_WH55']").click()

        # 点击--请选择测试类型
        self.find_element_by_xpath("//*[@id='dataType']/div/div").click()

        # 点击--测试类型
        self.find_element_by_xpath("//li[text()='Type Certification']").click()

        # 点击--查 询
        self.move_to_element_(self.find_element_by_xpath("//span[text()='查 询']"))
        self.click_()

        # 断言
        asserts = self.asserts("//h3[text()='VDM样机统计通道每天数据量']")
        return asserts


if __name__ == '__main__':
    EDADataCenter().data_quality_query_11()
