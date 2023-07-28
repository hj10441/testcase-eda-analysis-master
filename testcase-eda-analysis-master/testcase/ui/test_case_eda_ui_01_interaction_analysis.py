# -*- coding: utf-8 -*-
"""
@project : CMS
@author: LYF
@file: test_case_eda_ui_01_interaction_analysis.py
@ide: PyCharm
@time: 2021-07-23 11:41
"""

import os
import sys
import allure
from loguru import logger

sys.path.append(r'D:\autotestdata\testcase-eda-analysis-ui')
curPath = os.path.abspath(os.path.join(os.getcwd(), ".."))
rootPath = os.path.split(curPath)[0]
print(rootPath)
sys.path.append(rootPath)
import pytest
from pageelements.EDA_interaction_analysis import EDAInteractionAnalysisPage
from public.public_function import yaml_read
from dbiz_autotest_sdk.encrypt import decrypt


@allure.feature("EDA-交互分析-数据源管理")
class TestUiEDA:

    def setup_class(self, count=0):
        config = yaml_read(yaml_name="/config/config.yml")
        autotest_name = config["autotest_account"]
        autotest_password = decrypt(public_key=config["autotest_password_key"],
                                    encryped_pwd=config["autotest_password"])
        while count < 3:
            count += 1
            try:
                self.cms_page = EDAInteractionAnalysisPage('状态监测系统')
                self.cms_page.open()
                self.cms_page.max_window()
                logger.info("login eda")
                if self.cms_page.eda_login(account=autotest_name, password=autotest_password):
                    break
            except Exception as e_output:
                logger.info('第%d次登陆失败,原因%s' % (count, e_output))
                self.cms_page.driver.quit()

    def setup(self):
        logger.info("case start")

    def teardown(self):
        allure.attach(self.cms_page.get_screenshot_as_png(), "截图", allure.attachment_type.PNG)
        logger.info("case over")

    def teardown_class(self):
        self.cms_page.driver.quit()

    @allure.title("数据源配置页面-验证表单提示对应的输入框为红色字体校验")
    def test_01_new_data_source(self):
        """进入数据源管理页面，点击+号新增数据源进入数据源管理页面，点击+号新增数据源，验证表单提示对应的输入框为红色字体校验"""
        asserts = self.cms_page.new_data_source()
        assert asserts

    @allure.title("数据源配置页面-验证连接数据库，验证数据库配置错误提示语")
    def test_02_connect_error(self):
        """进入数据源管理页面，点击+号新增数据源进入数据源管理页面，输入一个错误的数据库连接配置，点击连接测试,提示‘连接测试失败！’"""
        asserts = self.cms_page.connect_error()
        assert asserts

    @allure.title("数据源配置页面-验证连接数据库，连接成功提示语")
    def test_03_connect_pass(self):
        """进入数据源管理页面，点击+号新增数据源进入数据源管理页面，输入正确的数据库连接配置，点击连接测试,提示‘连接成功！’"""
        asserts = self.cms_page.connect_pass()
        assert asserts

    @allure.title("数据源配置页面-连接数据库，查询数据表范围")
    def test_04_table_scope(self):
        """进入数据源管理页面，连接数据库，查询数据表范围"""
        asserts = self.cms_page.table_scope()
        assert asserts

    @allure.title("数据源配置页面-验证创建sql提示语")
    def test_05_query_view(self):
        """点击查询视图右侧的＋号，点击确定,出现校验提示，sql名称必填，请输入sql语句"""
        asserts = self.cms_page.query_view()
        assert asserts

    @allure.title("数据源配置页面-验证新增sql语句")
    def test_06_insert_sql(self):
        """输入sql名称，sql语句，sql描述，点击确定，保存视图，视图列表并展开显示，显示对应输入的sql名称，sql语句，sql描述内容"""
        asserts = self.cms_page.insert_sql()
        assert asserts

    @allure.title("数据源配置页面-验证修改sql语句")
    def test_07_update_sql(self):
        """视图列表右侧点击编辑，修改sql名称和sql语句后，点击确定，显示对应修改的sql名称，sql语句，sql描述内容"""
        asserts = self.cms_page.update_sql()
        assert asserts

    @allure.title("数据源配置页面-验证删除sql语句")
    def test_08_delete_sql(self):
        """视图列表右侧点击删除，删除成功"""
        asserts = self.cms_page.delete_sql()
        assert asserts

    @allure.title("数据源配置页面-新增数据源配置")
    def test_09_insert_data_source(self):
        """输入数据源名称为“测试”，输入数据源编码为“test”，输入正确的数据库配置，并且连接成功，新增一个查询视图，点击保存，保存到数据源管理列表"""
        asserts = self.cms_page.insert_data_source()
        assert asserts

    @allure.title("工作区页面-验证数据集是否创建成功")
    def test_10_select_data_set(self):
        """在数据交互分析模块，点击工作区，点击创建我的分析，创建后点击+号按钮，点击数据源类型，下拉查看列表，显示之前输入的数据源名称一致的数据集"""
        asserts = self.cms_page.select_data_set()
        assert asserts

    @allure.title("工作区页面-验证读取数据,读取数据是否成功")
    def test_11_select_reading_data(self):
        """在工作区页面-验证读取数据,读取数据是否成功"""
        asserts = self.cms_page.select_reading_data()
        assert asserts

    @allure.title("工作区页面-验证一键自动添加，自动识别到对应的维度或指标")
    def test_12_add_key(self):
        """工作区-点击一键自动添加，自动识别到对应的维度或指标"""
        asserts = self.cms_page.add_key()
        assert asserts

    @allure.title("工作区页面-删除新建分析设计")
    # @pytest.mark.dependency()
    def test_13_delete_new_analysis(self):
        """删除新建分析设计"""
        asserts = self.cms_page.delete_new_analysis()
        assert asserts

    @allure.title("分析设计页面-验证当前账户无法查看另一个账户创建的数据源")
    # @pytest.mark.dependency(depends=["test_10_delete_new_analysis"], scope="class")
    def test_14_data_source_permission(self):
        """验证当前账户无法查看另一个账户创建的数据源"""
        asserts = self.cms_page.data_source_permission()
        assert asserts

    @allure.title("数据源配置页面-新增一个已有的数据源名称的数据集")
    def test_15_repetition_insert_data_source_name(self):
        """在交互分析模块，点击数据源管理，重新新增一个与数据源名称一致的数据源，点击保存，提示：数据源编码已存在"""
        asserts = self.cms_page.repetition_insert_data_source_name()
        assert asserts

    @allure.title("数据源配置页面-新增一个已有的数据源编码的数据集")
    def test_16_repetition_insert_data_source_encoding(self):
        """在交互分析模块，点击数据源管理，重新新增一个与数据源编码一致的数据源，点击保存，提示：数据源编码已存在"""
        asserts = self.cms_page.repetition_insert_data_source_encoding()
        assert asserts

    @allure.title("数据源配置页面-验证删除数据源时提示语")
    def test_17_delete_data_source_marked_words(self):
        """点击数据源管理右侧的删除图标，提示：是否确认删除当前数据源?"""
        asserts = self.cms_page.delete_data_source_marked_words()
        assert asserts

    @allure.title("数据源配置页面-新增验证删除数据源")
    def test_18_delete_data_source(self):
        """点击数据源管理右侧的删除图标，点击确定，数据源成功删除"""
        asserts = self.cms_page.delete_data_source()
        assert asserts


if __name__ == '__main__':
    pytest.main(['test_case_eda_ui_01_interaction_analysis.py', '-s', '--alluredir', "../../report/tmp"])
    os.system('allure generate ../report/tmp -o  ../report/report --clean')
    os.system(r'allure serve D:\Xiangmu\test_cms\testcase-cms\report\tmp')


