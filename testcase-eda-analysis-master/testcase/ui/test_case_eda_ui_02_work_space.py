# -*- coding: utf-8 -*-
"""
@project : CMS
@author: LYF
@file: test_case_eda_ui_02_work_space.py
@ide: PyCharm
@time: 2021-12-17 10:35
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
from pageelements.EDA_work_space import EDAWorkSpacePage
from public.public_function import yaml_read
from dbiz_autotest_sdk.encrypt import decrypt


@allure.feature("EDA-工作区")
class TestUiEDA:

    def setup_class(self, count=0):
        config = yaml_read(yaml_name="/config/config.yml")
        autotest_name = config["autotest_account"]
        autotest_password = decrypt(public_key=config["autotest_password_key"],
                                    encryped_pwd=config["autotest_password"])
        while count < 4:
            count += 1
            try:
                self.cms_page = EDAWorkSpacePage('状态监测系统!!')
                self.cms_page.open()
                self.cms_page.max_window()
                logger.info("login eda")
                if self.cms_page.eda_login(account=autotest_name, password=autotest_password):
                    break
            except Exception as e_output:
                logger.info('第%d次登陆失败,原因%s' % (count, e_output))
                self.cms_page.driver.quit()

    @staticmethod
    def setup():
        logger.info("case start=====================================")

    def teardown(self):
        allure.attach(self.cms_page.get_screenshot_as_png(), "截图", allure.attachment_type.PNG)
        logger.info("case over======================================")

    def teardown_class(self):
        self.cms_page.driver.quit()

    @allure.title("工作区-点击创建我的分析，弹窗展示分析设计新建界面")
    def test_01_create_my_analysis(self):
        """工作区-点击交互分析的工作区，点击创建我的分析，弹窗展示分析设计新建界面"""
        logger.info("case start: test_01_create_my_analysis")
        asserts = self.cms_page.create_my_analysis()
        assert asserts

    @allure.title("工作区-验证取消创建功能")
    def test_02_my_analysis_cancel(self):
        """工作区-验证取消创建功能"""
        logger.info("test_02_my_analysis_cancel")
        asserts = self.cms_page.my_analysis_cancel()
        assert asserts

    @allure.title("工作区-验证新建分析是否成功")
    def test_03_create_my_analysis_2(self):
        """工作区-验证新建分析是否成功"""
        logger.info("test_03_create_my_analysis_2")
        asserts = self.cms_page.create_my_analysis_2()
        assert asserts

    @allure.title("工作区-验证新建分析是否成功进入")
    def test_04_my_analysis(self):
        """工作区-验证新建分析是否成功进入"""
        logger.info("test_05_collecting")
        asserts = self.cms_page.my_analysis()
        assert asserts

    @allure.title("工作区-收藏测试分析")
    def test_05_collecting_1(self):
        """工作区-收藏测试分析"""
        logger.info("test_05_collecting")
        asserts = self.cms_page.collecting_1()
        assert asserts

    @allure.title("工作区-查看收藏新建分析")
    def test_06_collecting_2(self):
        """工作区-查看收藏新建分析"""
        logger.info("test_06_collecting_2")
        asserts = self.cms_page.collecting_2()
        assert asserts

    @allure.title("工作区-点击查看，跳到分析设计页")
    def test_07_view_new_analysis(self):
        """工作区-点击查看，跳到分析设计页"""
        logger.info("test_07_view_new_analysis")
        asserts = self.cms_page.view_new_analysis()
        assert asserts

    @allure.title("工作区-取消测试分析收藏")
    def test_08_collecting_3(self):
        """工作区-取消测试分析收藏"""
        logger.info("test_07_collecting_3")
        asserts = self.cms_page.collecting_3()
        assert asserts

    @allure.title("工作区-点击分析右上角三个点里的发布，提示：你确定要发布此分析吗")
    def test_09_release_1(self):
        """工作区-点击分析右上角三个点里的发布，提示：你确定要发布此分析吗"""
        logger.info("test_09_release_1")
        asserts = self.cms_page.release_1()
        assert asserts

    @allure.title("工作区-点击分析右上角三个点里的发布，点击取消")
    def test_10_release_2(self):
        """工作区-点击分析右上角三个点里的发布，点击取消"""
        logger.info("test_10_release_2")
        asserts = self.cms_page.release_2()
        assert asserts

    @allure.title("工作区-点击分析右上角三个点里的发布，点击确定")
    def test_11_release_3(self):
        """工作区-点击分析右上角三个点里的发布，点胶机确定"""
        logger.info("test_11_release_3")
        asserts = self.cms_page.release_3()
        assert asserts

    @allure.title("工作区-点击发布，选择全部用户，点击分布")
    def test_12_release_4(self):
        """工作区-点击发布，选择全部用户，点击分布"""
        logger.info("test_12_release_4")
        asserts = self.cms_page.release_4()
        assert asserts

    @allure.title("工作区-登录另一个用户，在工作区点击所有发布，显示之前用户发布的分析")
    def test_13_release_5(self):
        """工作区-登录另一个用户，在工作区点击所有发布，显示之前用户发布的分析"""
        logger.info("test_13_release_5")
        asserts = self.cms_page.release_5()
        assert asserts

    @allure.title("工作区-点击取消发布，在所有发布页消失此分析")
    def test_14_release_6(self):
        """工作区-点击取消发布，在所有发布页消失此分析"""
        logger.info("test_14_release_6")
        asserts = self.cms_page.release_6()
        assert asserts
        logger.info("assert success")

    @allure.title("工作区-用户已勾选Test Role权限，查看所有发布")
    def test_15_release_7(self):
        """工作区-用已勾选Test Role权限，查看所有发布"""
        logger.info("test_15_release_7")
        asserts = self.cms_page.release_7()
        assert asserts

    @allure.title("工作区-用户未勾选Test Role权限，查看所有发布")
    def test_16_release_8(self):
        """工作区-用未勾选Test Role权限，查看所有发布"""
        logger.info("test_16_release_8")
        asserts = self.cms_page.release_8()
        assert asserts

    @allure.title("工作区-删除新建分析")
    def test_17_delete_new_analysis(self):
        """工作区-删除新建分析"""
        logger.info("test_17_delete_new_analysis")
        asserts = self.cms_page.delete_new_analysis()
        assert asserts

    @allure.title("工作区-过滤条件为分析名称,并搜索'测试'")
    def test_18_filter_1(self):
        """工作区-过滤条件为分析名称,并搜索'测试'"""
        logger.info("test_18_filter_1")
        asserts = self.cms_page.filter_1()
        assert asserts

    @allure.title("工作区-过滤条件为分析描述,并搜索'测试'")
    def test_19_filter_2(self):
        """工作区-过滤条件为分析描述,并搜索'测试'"""
        logger.info("test_19_filter_2")
        asserts = self.cms_page.filter_2()
        assert asserts

    @allure.title("工作区-过滤条件为分析名称并搜索'测试'成功后，点击重置")
    def test_20_filter_3(self):
        """工作区-过滤条件为分析名称并搜索"测试"成功后，点击重置'"""
        logger.info("test_20_filter_3")
        asserts = self.cms_page.filter_3()
        assert asserts

    @allure.title("工作区-过滤-过滤条件为创建人并搜索'测试'")
    def test_21_filter_4(self):
        """工作区-过滤条件为创建人并搜索"测试"'"""
        logger.info("test_21_filter_4")
        asserts = self.cms_page.filter_4()
        assert asserts

    @allure.title("工作区-查看次数，选择降序,查看次数由大到小展示")
    def test_22_filter_5(self):
        """工作区-查看次数，选择降序,查看次数由大到小展示"""
        logger.info("test_22_filter_5")
        asserts = self.cms_page.filter_5()
        assert asserts

    @allure.title("工作区-分析名称，选择升序，名称由a-z由小到大展示")
    def test_23_filter_6(self):
        """工作区-分析名称，选择升序，名称由a-z由小到大展示"""
        logger.info("test_23_filter_6")
        asserts = self.cms_page.filter_6()
        assert asserts

    @allure.title("工作区-收藏次数，选择升序，收藏次数由小到大展示")
    def test_24_filter_7(self):
        """工作区-收藏次数，选择升序，收藏次数由小到大展示"""
        logger.info("test_24_filter_7")
        asserts = self.cms_page.filter_7()
        assert asserts

    @allure.title("工作区-创建时间，选择降序，创建时间由最近时间到最远时间展示")
    def test_25_filter_8(self):
        """工作区-创建时间，选择降序，创建时间由最近时间到最远时间展示"""
        logger.info("test_25_filter_8")
        asserts = self.cms_page.filter_8()
        assert asserts

    @allure.title("工作区-更新时间，选择升序，更新时间由最近时间到最远时间展示")
    def test_26_filter_9(self):
        """工作区-更新时间，选择升序，更新时间由最近时间到最远时间展示"""
        logger.info("test_26_filter_9")
        asserts = self.cms_page.filter_9()
        assert asserts


if __name__ == '__main__':
    pytest.main(['test_case_eda_ui_02_work_space.py', '-vs', '--alluredir', "../../report/tmp"])
    # os.system('allure generate ../report/tmp -o  ../report/report --clean')
    # os.system(r'allure serve D:\Xiangmu\test_cms\testcase-cms\report\tmp')

