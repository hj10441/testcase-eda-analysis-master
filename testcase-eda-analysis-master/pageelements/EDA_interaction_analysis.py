# -*- coding: utf-8 -*-
"""
@project : Galileo
@author: LYF
@file: EDA_interaction_analysis.py
@ide: PyCharm
@time: 2021-11-11 14:35
"""
import time
from loguru import logger
from pageelements.base_page import BasePage
from public.public_function import yaml_read
from dbiz_autotest_sdk.encrypt import decrypt

data = yaml_read(yaml_name="/config/interaction_analysis_element.yml")
config = yaml_read(yaml_name="/config/config.yml")
mysql_password = decrypt(public_key=config["mysql_password_key"], encryped_pwd=config["mysql_password"])
autotest_password = decrypt(public_key=config["autotest_password_key"], encryped_pwd=config["autotest_password"])
autotest2_password = decrypt(public_key=config["autotest2_password_key"], encryped_pwd=config["autotest2_password"])

select_database = "select * from test"
class EDAInteractionAnalysisPage(BasePage):

    # 交互分析—数据源管理-新增数据源
    def new_data_source(self):
        self.fresh_()
        # 点击交互分析
        self.move_to_element_(self.find_element("xpath", data["interaction_analysis"]))
        # 点击数据源管理
        self.find_element_by_link_text(data["data_source_management"]).click()
        # 点击加号
        self.find_element("xpath", data["plus"]).click()
        # 断言
        asserts = self.asserts("//div[text()='请输入数据库名！']")
        return asserts

    # 交互分析—数据源管理-查询视图
    def query_view(self):
        # 点击查询视图加号
        self.move_to_element_(
            self.find_element("xpath", "//button[@class='ant-btn ant-btn-link']/i[@class='anticon anticon-plus']"))
        self.click_()
        try:
            # 点击确定
            self.move_to_element_(self.find_element("xpath", data['confirm']))
            self.click_()
        except Exception:
            # 点击确定
            self.move_to_element_(
                self.find_element("xpath", "/html/body/div[6]/div/div[2]/div/div[2]/div[3]/div/button[2]"))
            self.click_()

        # 断言
        sql_name = self.find_element("xpath", "//div[text()='SQL名称必填！']").text
        sql_sentence = self.find_element("xpath", "//div[text()='请输入SQL语句！']").text
        if sql_name == "SQL名称必填！" and sql_sentence == "请输入SQL语句！":
            return True
        else:
            return False

    # 交互分析—数据源管理-连接数据库，验证数据库配置提示语
    def connect(self, sourceName="test", dataSourceCode="test", customIpAddress="172.20.32.162", customPort=3308,
                dataBaseName="edas", dataBaseUsername="edas", dataBasePassword=mysql_password):

        logger.info("点击--数据源名称输入框")
        self.sendkeys_by_text("xpath", "//input[@id='sourceName']", value=sourceName)

        logger.info("点击--数据源编码输入框")
        self.sendkeys_by_text("xpath", "//input[@id='dataSourceCode']", value=dataSourceCode)

        logger.info("点击--服务器IP地址输入框")
        self.sendkeys_by_text("xpath", "//input[@id='customIpAddress']", value=customIpAddress)

        logger.info("点击--端口号输入框")
        self.sendkeys_by_text("xpath", "//input[@id='customPort']", value=customPort)

        logger.info("点击--数据库名输入框")
        self.sendkeys_by_text("xpath", "//input[@id='dataBaseName']", value=dataBaseName)

        logger.info("点击--用户名输入框")
        self.sendkeys_by_text("xpath", "//input[@id='dataBaseUsername']", value=dataBaseUsername)

        logger.info("点击--密码输入框")
        logger.info("输入密码: 密码已加密")
        dataBasePassword_xpath = self.find_element("xpath", "//input[@id='dataBasePassword']")
        dataBasePassword_xpath.clear()
        dataBasePassword_xpath.click()
        dataBasePassword_xpath.send_keys(dataBasePassword)

        self.move_to_element_(self.find_element("xpath", "//span[text()='连接测试']"))
        self.click_()

    # 交互分析—数据源管理-连接数据库，查询数据表范围
    def table_scope(self):
        logger.info("连接数据库 ")
        self.connect(sourceName="test", dataSourceCode="test", customIpAddress="10.109.128.23", customPort=3307,
                     dataBaseName="edas", dataBaseUsername="edas", dataBasePassword=mysql_password)

        # time.sleep(30)  # 暂停调试用--黄竞
        logger.info("点击--数据表范围下拉框")
        self.find_element("xpath", "//*[@id='sqlTableInfo']").click()
        # time.sleep(30)  # 暂停调试用--黄竞
        logger.info("验证数据表是否存在")
        self.find_element("xpath", "//*[text()='flyway_schema_history']").click()
        self.find_element("xpath", "//*[text()='oil_relation_meta_data']").click()
        self.find_element("xpath", "//*[text()='t_analysis_object']").click()
        # 断言
        asserts = self.asserts("//*[text()='t_analysis_role_mapping']")
        print('点击确定')
        time.sleep(20)
        self.move_to_element_(self.find_element("xpath", data['confirm']))
        self.click_()
        print('点击确定完毕')
        time.sleep(20)
        return asserts

    # 交互分析—数据源管理-连接数据库，验证数据库配置错误提示语
    def connect_error(self):
        self.connect()

        # 断言
        time.sleep(40)
        if self.asserts("//label[text()='连接测试失败！']"):
            return True
        else:
            return False

    # 交互分析—数据源管理-连接数据库，验证数据库配置正确提示语
    def connect_pass(self):
        self.connect(sourceName="test", dataSourceCode="test", customIpAddress="10.109.128.23", customPort=3307,
                     dataBaseName="edas", dataBaseUsername="edas", dataBasePassword=mysql_password)
        # 断言
        asserts = self.asserts(data['database_status'])
        return asserts

    # 交互分析—数据源管理-新增sql
    def insert_sql(self, sqlName="查询4", querySqlStr=select_database, note="test"):
        logger.info("点击--sql名称输入框")
        self.find_element("id", "sqlName").click()
        self.send_key_direct(sqlName)

        logger.info("点击--sql语句输入框")
        self.find_element("xpath", "//textarea[@id='querySqlStr']").click()
        self.send_key_direct(querySqlStr)

        logger.info("点击--sql描述输入框")
        self.find_element("id", "note").click()
        self.send_key_direct(note)

        # logger.info("点击--确定")
        self.move_to_element_(self.find_element("xpath", "//div[@class='ant-modal-footer']//div//span[text()='确 定']"))
        self.click_()

        # 断言
        text_querySqlStr = self.find_element("xpath", "//div[text()='select * from test']").text
        text_note = self.find_element("xpath", "//div[text()='test']").text
        if text_querySqlStr == select_database and text_note == "test":
            return True
        else:
            return False

    # 交互分析—数据源管理-编辑sql
    def update_sql(self):
        logger.info("点击-编辑")
        self.find_element("xpath", "//span[text()='编辑']").click()

        logger.info("点击-sql名称输入框")
        self.find_element("id", "sqlName").click()
        self.send_key_direct("123")

        logger.info("点击-sql语句输入框")
        self.find_element("xpath", "//textarea[@id='querySqlStr']").click()
        self.send_key_direct("123")

        logger.info("点击-sql描述输入框")
        self.find_element("id", "note").click()
        self.send_key_direct("123")

        logger.info("点击-确定")
        self.move_to_element_(self.find_element("xpath", "//div[@class='ant-modal-footer']//div//span[text()='确 定']"))
        self.click_()

        # 断言
        text_querySqlStr = self.find_element("xpath", "//div[text()='select * from test123']").text
        text_note = self.find_element("xpath", "//div[text()='test123']").text
        if text_querySqlStr == "select * from test123" and text_note == "test123":
            logger.info(True)
            return True
        else:
            return False

    # 交互分析—数据源管理-删除sql
    def delete_sql(self):
        logger.info("点击-删除")
        self.find_element("xpath", "//span[text()='删除']").click()

        logger.info("点击-是")
        self.move_to_element_(self.find_element("xpath", "//span[text()='是']"))
        self.click_()

        # 断言
        if self.asserts("//div[text()='查询123']"):
            return False
        else:
            return True

    # 交互分析—数据源管理-新增数据源配置
    def insert_data_source(self):
        logger.info("进入数据源配置 ")
        self.new_data_source()

        logger.info("连接数据库 ")
        self.connect(sourceName="test_jing.huang", dataSourceCode="test_jing", customIpAddress="10.109.128.23",
                     customPort=3307,
                     dataBaseName="edas", dataBaseUsername="edas", dataBasePassword=mysql_password)

        time.sleep(5)
        if self.asserts(data['database_status']):
            logger.info("数据库连接成功！！")
        else:
            logger.info("数据库连接失败！！")
            return False

        logger.info("点击--查询视图加号")
        self.move_to_element_(
            self.find_element("xpath", "//button[@class='ant-btn ant-btn-link']/i[@class='anticon anticon-plus']"))
        self.click_()

        logger.info("添加sql语句")
        self.insert_sql(sqlName="select_test", querySqlStr=select_database, note="test")

        logger.info("点击--保存 ")
        self.move_to_element_(self.find_element("xpath", data['save']))
        self.click_()

        # 断言
        asserts = self.asserts(data['login_name'])
        return asserts

    # 交互分析—工作区-验证数据集是否创建成功
    def select_data_set(self):
        self.fresh_()

        logger.info("点击--交互分析 ")
        self.move_to_element_(self.find_element("xpath", data['analyse']))

        logger.info("点击--工作区 ")
        self.find_element_by_link_text("工作区").click()

        logger.info("点击--创建我的分析")
        self.move_to_element_(self.find_element("xpath", "//span[text()='创建我的分析']"))
        self.click_()

        # logger.info("点击--确定")
        self.move_to_element_(self.find_element("xpath", data['confirm']))
        self.click_()

        logger.info("点击--数据集加号")
        self.find_element("xpath", "//div[@class='ant-card-extra']/div/button").click()

        logger.info("点击--数据源类型下拉框 ")
        self.find_element("xpath", "//div[@role='combobox']").click()

        # 断言--显示之前输入的数据源名称一致的数据集
        asserts = self.asserts(data['assert_name'])
        return asserts

    # 交互分析—工作区-验证读取数据是否成功
    def select_reading_data(self):
        logger.info("点击--数据源类型下拉框")
        self.find_element("xpath", data['assert_name']).click()

        logger.info("点击--请输入SQL语句查询内容输入框")
        self.find_element("xpath", "//div[text()='请输入SQL语句查询内容']").click()
        self.send_key_direct("select * from flyway_schema_history")

        logger.info("点击--读取数据")
        self.move_to_element_(self.find_element("xpath", "//span[text()='读取数据']"))
        self.click_()

        # 断言
        asserts = self.asserts("//span[text()='installed_rank']")
        return asserts

    # 交互分析—工作区-验证点击一键自动添加，自动识别到对应的维度或指标
    def add_key(self):
        logger.info("点击--一键自动添加")
        self.move_to_element_(self.find_element("xpath", "//span[text()='一键自动添加']"))
        self.click_()

        # 断言
        asserts_dimensionality = self.asserts("//span[text()='installed_on']")
        asserts_target = self.asserts("//span[text()='installed_rank']")
        if asserts_target and asserts_dimensionality:
            return True

    # 删除新建分析设计
    def delete_new_analysis(self):
        self.fresh_()

        logger.info("点击--交互分析 ")
        self.move_to_element_(self.find_element("xpath", data['analyse']))

        logger.info("点击--工作区")
        self.find_element_by_link_text("工作区").click()

        logger.info("点击--新建分析设计")
        self.find_element("xpath", "//div[@class='ant-card-body']").click()

        logger.info("点击--删除 ")
        self.move_to_element_(
            self.find_element("xpath", "//div[@style='margin-top: 10px; float: right;']//button[2]//i"))
        self.click_()

        logger.info("点击--确定")
        self.move_to_element_(self.find_element("xpath", data['confirm']))
        self.click_()

        # 断言
        asserts = self.asserts("//div[@style='margin-top: 10px; float: right;']//button[2]//i")
        if asserts:
            return False
        else:
            return True

    # 交互分析—数据源管理-新增数据源只显示于创建者账号，其他账号不显示
    def data_source_permission(self):
        self.fresh_()
        logger.info("点击--分析中心  ")
        self.move_to_element_(self.find_element("xpath", data["interaction_analysis"]))

        logger.info("点击--数据源管理 ")
        self.find_element_by_link_text(data["data_source_management"]).click()

        logger.info("点击--test_yunfu.li ")
        self.move_to_element_(self.find_element("xpath", data['login_name']))
        self.click_()

        logger.info("点击--编辑图标")
        self.move_to_element_(self.find_element("xpath", "//i[@class='anticon anticon-edit']"))
        self.click_()

        logger.info("点击--物理位置")
        self.move_to_element_(self.find_element("id", "dataPhysicalLocation"))
        self.click_()

        self.send_key_direct("test123")

        logger.info("点击--数据源描述")
        self.move_to_element_(self.find_element("id", "dataSourceInfo"))
        self.click_()

        self.send_key_direct("test123")

        logger.info("点击--保存 ")
        self.move_to_element_(self.find_element("xpath", data['save']))
        self.click_()

        logger.info("点击--账户图标")
        self.move_to_element_(self.find_element("xpath", "//img[@alt='avatar']"))
        self.click_()

        logger.info("点击--退出登录")
        self.move_to_element_(self.find_element("xpath", "//span[text()='退出登录']"))
        self.click_()

        logger.info("登录另一个账户！")
        self.eda_login(account=config["autotest2_account"], password=autotest2_password)

        logger.info("进入交互分析查看")
        logger.info("点击--交互分析  ")
        self.move_to_element_(self.find_element("xpath", data['analyse']))

        logger.info("点击--工作区")
        self.find_element_by_link_text("工作区").click()

        logger.info("点击--我的分析")
        self.find_element("xpath",
                          "//*[@id='root']/div/section/section/section/main/div/div[2]/div[1]/div[2]/div[2]").click()

        logger.info("点击--数据集加号")
        self.find_element("xpath", '//*[@id="root"]/div/section/section/section/main/div[1]/div[4]/div[1]/div[2]/div/div/div[1]/div[1]/div[1]/div/div[2]/div/button[3]').click()

        logger.info("点击--数据源类型下拉框")
        self.find_element("xpath", "//div[@role='combobox']").click()

        # 断言--显示之前输入的数据源名称一致的数据集
        asserts = self.asserts(data['assert_name'])

        self.fresh_()

        logger.info("点击--账户图标")
        self.move_to_element_(self.find_element("xpath", "//img[@alt='avatar']"))
        self.click_()

        logger.info("点击--退出登录")
        self.move_to_element_(self.find_element("xpath", "//span[text()='退出登录']"))
        self.click_()

        logger.info("登录另一个账户！")
        self.eda_login(account=config["autotest_account"], password=autotest_password)

        logger.info(asserts)

        # 断言--当前账户无法查看另一个账户创建的数据源
        if asserts:
            return False
        else:
            return True

    # 交互分析—数据源管理-新增一个已有的数据源名称的数据集
    def repetition_insert_data_source_name(self):
        logger.info("进入数据源配置")
        self.new_data_source()

        logger.info("连接数据库")
        self.connect(sourceName="test_jing.huang", dataSourceCode="test123", customIpAddress="10.109.128.23",
                     customPort=3307, dataBaseName="edas", dataBaseUsername="edas", dataBasePassword=mysql_password)

        time.sleep(5)
        if self.asserts(data['database_status']):
            logger.info("数据库连接成功！！！")
        else:
            logger.info("数据库连接失败！！！")
            return False

        logger.info("点击--保存")
        self.move_to_element_(self.find_element("xpath", data['save']))
        self.click_()

        # 断言
        asserts = self.asserts("//span[text()='数据库名称test_jing.huang已存在.']")
        return asserts

    # 交互分析—数据源管理-新增一个已有的数据源编码的数据集
    def repetition_insert_data_source_encoding(self):
        logger.info("进入数据源配置")
        self.new_data_source()

        logger.info("连接数据库")
        self.connect(sourceName="test_jing.huang_2", dataSourceCode="test_jing", customIpAddress="10.109.128.23",
                     customPort=3307, dataBaseName="edas", dataBaseUsername="edas", dataBasePassword=mysql_password)

        time.sleep(5)
        if self.asserts(data['database_status']):
            logger.info("数据库连接成功！！！")
        else:
            logger.info("数据库连接失败！！！")
            return False

        logger.info("点击--保存")
        self.move_to_element_(self.find_element("xpath", data['save']))
        self.click_()

        # 断言
        asserts = self.asserts("//span[text()='数据库编码test_jing已存在.']")
        return asserts

    # 交互分析—数据源管理-验证删除数据源时提示语
    def delete_data_source_marked_words(self):
        self.fresh_()

        logger.info("点击--交互分析")
        self.move_to_element_(self.find_element("xpath", data['analyse']))

        logger.info("点击--数据源管理")
        self.find_element_by_link_text("数据源管理").click()

        logger.info("点击--test_yunfu.li")
        self.find_element("xpath", data['login_name']).click()

        logger.info("点击--删除")
        self.move_to_element_(self.find_element("xpath", "//i[@class='anticon anticon-delete']"))
        self.click_()

        # 断言
        asserts = self.asserts("//div[text()='是否确认删除当前数据源?']")
        return asserts

    # 交互分析—数据源管理-验证删除数据源
    def delete_data_source(self):
        self.fresh_()

        logger.info("点击--交互分析")
        self.move_to_element_(self.find_element("xpath", data['analyse']))

        logger.info("点击--数据源管理")
        self.find_element_by_link_text("数据源管理").click()

        logger.info("点击--test_yunfu.li")
        self.find_element("xpath", data['login_name']).click()

        logger.info("点击--删除")
        self.move_to_element_(self.find_element("xpath", "//i[@class='anticon anticon-delete']"))
        self.click_()

        logger.info("点击--确定")
        self.move_to_element_(self.find_element("xpath", data['confirm']))
        self.click_()

        # 断言
        asserts = self.asserts(data['login_name'])
        if asserts:
            return False
        else:
            return True
