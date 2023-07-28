# -*- coding: utf-8 -*-
"""
@project : CMS
@author: LYF
@file: test_case_eda_ui_03_data_center.py
@ide: PyCharm
@time: 2021-12-29 10:10
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
from pageelements.EDA_data_center import EDADataCenter
from public.public_function import yaml_read
from dbiz_autotest_sdk.encrypt import decrypt


@allure.feature("EDA- ")
class TestUiEDA:

    def setup_class(self, count=0):
        config = yaml_read(yaml_name="/config/config.yml")
        autotest_name = config["autotest_account"]
        autotest_password = decrypt(public_key=config["autotest_password_key"],
                                    encryped_pwd=config["autotest_password"])
        while count < 4:
            count += 1
            try:
                self.page = EDADataCenter('状态监测系统')
                self.page.open()
                self.page.max_window()
                logger.info("login eda")
                if self.page.eda_login(account=autotest_name, password=autotest_password):
                    break
            except Exception as e_output:
                logger.info('第%d次登陆失败,原因%s' % (count, e_output))
                self.page.driver.quit()

    @staticmethod
    def setup():
        logger.info("case start=====================================")

    def teardown(self):
        allure.attach(self.page.get_screenshot_as_png(), "截图", allure.attachment_type.PNG)
        logger.info("case over======================================")

    def teardown_class(self):
        self.page.driver.quit()

    # @allure.title("数据中心-平台数据查询目录列表")
    # def test_01_query_directory(self):
    #     """数据中心-平台数据查询-查询目录列表"""
    #     asserts = self.page.query_directory()
    #     assert asserts
    #
    # @allure.title("数据中心-点击全量风场资产数据，点击右侧快速过滤，弹窗展示")
    # def test_02_rapid_filtration_1(self):
    #     """数据中心-点击全量风场资产数据，点击右侧快速过滤，弹窗展示"""
    #     asserts = self.page.rapid_filtration_1()
    #     assert asserts
    #
    # @allure.title("数据中心-快速过滤窗口，点击取消，弹窗关闭")
    # def test_03_rapid_filtration_2(self):
    #     """数据中心-快速过滤窗口，点击取消，弹窗关闭"""
    #     asserts = self.page.rapid_filtration_2()
    #     assert asserts
    #
    # @allure.title("数据中心-输入风场CN号，检查列表筛选结果")
    # def test_04_rapid_filtration_3(self):
    #     """数据中心-输入风场CN号，检查列表筛选结果"""
    #     asserts = self.page.rapid_filtration_3()
    #     assert asserts
    #
    # @allure.title("数据中心-输入风机号，检查列表筛选结果")
    # def test_05_rapid_filtration_4(self):
    #     """数据中心-输入风机号，检查列表筛选结果"""
    #     asserts = self.page.rapid_filtration_4()
    #     assert asserts
    #
    # @allure.title("数据中心-点击右侧导出过滤后数据图标，导出excel，验证内容为列表筛选的结果")
    # def test_06_rapid_filtration_5(self):
    #     """数据中心-点击右侧导出过滤后数据图标，导出excel，验证内容为列表筛选的结果"""
    #     asserts = self.page.rapid_filtration_5()
    #     assert asserts
    #
    # @allure.title("数据中心-验证清除过滤按钮")
    # def test_07_rapid_filtration_6(self):
    #     """数据中心-验证过清除过滤按钮"""
    #     asserts = self.page.rapid_filtration_6()
    #     assert asserts
    #
    # @allure.title("数据中心-点击集成测试环境所有风机数据量，验证搜索框模糊查询")
    # def test_08_rapid_filtration_7(self):
    #     """数据中心 - 点击集成测试环境所有风机数据量，验证搜索框模糊查询"""
    #     asserts = self.page.rapid_filtration_7()
    #     assert asserts
    #
    # @allure.title("数据中心-点击集成测试环境所有风机数据量，验证过滤功能")
    # def test_09_rapid_filtration_8(self):
    #     """数据中心 - 点击集成测试环境所有风机数据量，验证搜索框模糊查询"""
    #     asserts = self.page.rapid_filtration_8()
    #     assert asserts
    #
    # @allure.title("数据中心-点击集成测试环境所有风机数据量，验证清除功能")
    # def test_10_rapid_filtration_9(self):
    #     """数据中心 - 点击集成测试环境所有风机数据量，验证搜索框模糊查询"""
    #     asserts = self.page.rapid_filtration_9()
    #     assert asserts

    @allure.title("数据中心-验证DigitalTwin-10minData正常查询")
    def test_11_data_quality_query_1(self):
        """数据中心-验证DigitalTwin-10minData正常查询"""
        asserts = self.page.data_quality_query_1()
        assert asserts

    @allure.title("数据中心-验证DigitalTwin-1sData正常查询")
    def test_12_data_quality_query_2(self):
        """数据中心-验证DigitalTwin-1sData正常查询"""
        asserts = self.page.data_quality_query_2()
        assert asserts

    @allure.title("数据中心-验证SOE-Event正常查询")
    def test_13_data_quality_query_3(self):
        """数据中心-验证SOE-Event正常查询"""
        asserts = self.page.data_quality_query_3()
        assert asserts

    @allure.title("数据中心-验证Highspeed-IPC正常查询")
    def test_14_data_quality_query_4(self):
        """数据中心-验证Highspeed-IPC正常查询"""
        asserts = self.page.data_quality_query_4()
        assert asserts

    @allure.title("数据中心-验证Highspeed-LaseForTower正常查询")
    def test_15_data_quality_query_5(self):
        """数据中心-验证Highspeed-LaseForTower正常查询"""
        asserts = self.page.data_quality_query_5()
        assert asserts

    @allure.title("数据中心-验证Highspeed-Offshore正常查询")
    def test_16_data_quality_query_6(self):
        """数据中心-验证Highspeed-Offshore正常查询"""
        asserts = self.page.data_quality_query_6()
        assert asserts

    @allure.title("数据中心-验证Highspeed-Vibration正常查询")
    def test_17_data_quality_query_7(self):
        """数据中心-验证Highspeed-Vibration正常查询"""
        asserts = self.page.data_quality_query_7()
        assert asserts

    @allure.title("数据中心-验证CMS正常查询")
    def test_18_data_quality_query_8(self):
        """数据中心-验证CMS正常查询"""
        asserts = self.page.data_quality_query_8()
        assert asserts

    @allure.title("数据中心-验证Scada正常查询")
    def test_19_data_quality_query_9(self):
        """数据中心-验证Scada正常查询"""
        asserts = self.page.data_quality_query_9()
        assert asserts

    @allure.title("数据中心-验证Tracelog正常查询")
    def test_20_data_quality_query_10(self):
        """数据中心-验证Tracelog正常查询"""
        asserts = self.page.data_quality_query_10()
        assert asserts

    @allure.title("数据中心-验证VDM正常查询")
    def test_21_data_quality_query_11(self):
        """数据中心-验证VDM正常查询"""
        asserts = self.page.data_quality_query_11()
        assert asserts


if __name__ == '__main__':
    pytest.main(['test_case_eda_ui_03_data_center.py', '-vs'])
    # pytest.main(['test_case_eda_ui_03_data_center.py', '-vs', '--alluredir', "../../report/tmp"])
    # os.system('allure generate ../report/tmp -o  ../report/report --clean')
    # os.system(r'allure serve D:\Xiangmu\test_cms\testcase-cms\report\tmp')

