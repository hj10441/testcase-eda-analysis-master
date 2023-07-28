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

data = yaml_read(yaml_name="/config/work_space_element.yml")
config = yaml_read(yaml_name="/config/config.yml")
mysql_password = decrypt(public_key=config["mysql_password_key"], encryped_pwd=config["mysql_password"])
autotest_password = decrypt(public_key=config["autotest_password_key"], encryped_pwd=config["autotest_password"])
autotest2_password = decrypt(public_key=config["autotest2_password_key"], encryped_pwd=config["autotest2_password"])


class EDAWorkSpacePage(BasePage):

    # 交互分析—工作区-点击创建我的分析，弹窗展示分析设计新建界面
    def create_my_analysis(self):
        self.fresh_()
        # 点击--交互分析
        self.move_to_element_(self.find_element_by_xpath(data['analyse']))

        # 点击--分析设计
        self.find_element_by_link_text("工作区").click()

        # 点击--创建我的分析
        self.move_to_element_(self.find_element_by_xpath("//span[text()='创建我的分析']"))
        self.click_()

        # 断言
        asserts = self.asserts("analysisName", by="id")
        return asserts

    # 验证取消功能
    def my_analysis_cancel(self):
        # 点击--取消
        self.move_to_element_(self.find_element_by_xpath(data['cancel']))
        self.click_()

        # 刷新页面
        self.fresh_()

        # 断言
        asserts = self.asserts("analysisName", by="id")
        if asserts:
            return False
        else:
            return True

    # 验证新建分析是否成功
    def create_my_analysis_2(self):
        self.fresh_()
        # 点击--交互分析
        self.move_to_element_(self.find_element_by_xpath(data['analyse']))

        # 点击--工作区
        self.find_element_by_link_text("工作区").click()

        # 点击--创建我的分析
        self.move_to_element_(self.find_element_by_xpath("//span[text()='创建我的分析']"))
        self.click_()

        # 点击--分析名称，输入测试分析
        self.sendkeys_by_text("id", "analysisName", value="测试分析-jing.huang")

        # 点击--分析描述，输入123
        self.sendkeys_by_text("id", "analysisDescription", value="123")

        # 点击--确定
        self.move_to_element_(self.find_element_by_xpath(data['confirm']))
        self.click_()

        # 断言
        asserts = self.asserts(data['test_analysis'])
        return asserts

    # 查看新建测试分析
    def my_analysis(self):
        self.fresh_()
        # 点击--交互分析
        self.move_to_element_(self.find_element_by_xpath(data['analyse']))

        # 点击--工作区
        self.find_element_by_link_text("工作区").click()

        # 点击--测试分析
        self.find_element_by_xpath(
            "//*[@id='root']/div/section/section/section/main/div/div[2]/div/div[2]/div[2]").click()

        # 断言
        asserts = self.asserts(data['test_analysis'])
        return asserts

    # 收藏新建分析
    def collecting_1(self):
        self.fresh_()
        # 点击--交互分析
        self.move_to_element_(self.find_element_by_xpath(data['analyse']))

        # 点击--工作区
        self.find_element_by_link_text("工作区").click()

        # 移动鼠标到测试分析
        self.move_to_element_(self.find_element_by_xpath(data['test_analysis_p']))

        # 点击--收藏图标
        self.move_to_element_(self.find_element_by_xpath("//i[@class='anticon anticon-heart']"))
        self.click_()

        # 断言
        asserts = self.asserts("//span[text()='收藏成功']")
        return asserts

    # 查看收藏新建分析
    def collecting_2(self):
        self.fresh_()
        # 点击--交互分析
        self.move_to_element_(self.find_element_by_xpath(data['analyse']))

        # 点击--工作区
        self.find_element_by_link_text("工作区").click()

        # 点击--我的收藏
        self.find_element_by_xpath("//span[text()='我的收藏']").click()

        # 断言
        asserts = self.asserts(data['test_analysis_p'])
        return asserts

    # 点击查看，跳到分析设计页
    def view_new_analysis(self):
        self.fresh_()
        # 点击--交互分析
        self.move_to_element_(self.find_element_by_xpath(data['analyse']))

        # 点击--工作区
        self.find_element_by_link_text("工作区").click()

        # 移动鼠标到测试分析
        self.move_to_element_(self.find_element_by_xpath(data['test_analysis_p']))

        # 点击--三个点图标
        self.move_to_element_(self.find_element_by_xpath(data['icon']))
        self.click_()

        # 点击--查看
        self.find_element_by_xpath("//li[text()='查看']").click()

        # 断言
        asserts = self.asserts(data['test_analysis'])
        return asserts

    # 取消新建分析收藏
    def collecting_3(self):
        self.fresh_()
        # 点击--交互分析
        self.move_to_element_(self.find_element_by_xpath(data['analyse']))

        # 点击--工作区
        self.find_element_by_link_text("工作区").click()

        # 点击--我的收藏
        self.find_element_by_xpath("//span[text()='我的收藏']").click()

        # 移动鼠标到测试分析
        self.move_to_element_(self.find_element_by_xpath(data['test_analysis_p']))

        # 点击--收藏图标
        self.move_to_element_(self.find_element_by_xpath("//i[@class='anticon anticon-heart']"))
        self.click_()

        # 断言
        asserts = self.asserts("//span[text()='取消收藏成功']")
        return asserts

    # 点击发布，确认是否弹出确认弹框
    def release_1(self):
        self.fresh_()
        # 点击--交互分析
        self.move_to_element_(self.find_element_by_xpath(data['analyse']))

        # 点击--工作区
        self.find_element_by_link_text("工作区").click()

        # 移动鼠标到测试分析
        self.move_to_element_(self.find_element_by_xpath(data['test_analysis_p']))

        # 点击--三个点图标
        self.move_to_element_(self.find_element_by_xpath(data['icon']))
        self.click_()

        # 点击--发布
        self.find_element_by_xpath(data['release']).click()

        # 断言
        asserts = self.asserts(data['confirm'])
        return asserts

    # 点击发布，确认是否弹出确认弹框，点击取消
    def release_2(self):
        self.fresh_()
        # 点击--交互分析
        self.move_to_element_(self.find_element_by_xpath(data['analyse']))

        # 点击--工作区
        self.find_element_by_link_text("工作区").click()

        # 移动鼠标到测试分析
        self.move_to_element_(self.find_element_by_xpath(data['test_analysis_p']))

        # 点击--三个点图标
        self.move_to_element_(self.find_element_by_xpath(data['icon']))
        self.click_()

        # 点击--发布
        self.find_element_by_xpath(data['release']).click()

        # 断言
        asserts = self.asserts(xpath=data['cancel'])

        # 点击--取消
        self.move_to_element_(self.find_element_by_xpath(data['cancel']))
        self.click_()

        return asserts

    # 点击发布，确认是否弹出确认弹框，点击确定
    def release_3(self):
        self.fresh_()
        # 点击--交互分析
        self.move_to_element_(self.find_element_by_xpath(data['analyse']))

        # 点击--工作区
        self.find_element_by_link_text("工作区").click()

        # 移动鼠标到测试分析
        self.move_to_element_(self.find_element_by_xpath(data['test_analysis_p']))

        # 点击--三个点图标
        self.move_to_element_(self.find_element_by_xpath(data['icon']))
        self.click_()

        # 点击--发布
        self.find_element_by_xpath(data['release']).click()

        # 点击--确定
        self.move_to_element_(self.find_element_by_xpath(data['confirm']))
        self.click_()

        # 断言
        asserts = self.asserts("rcDialogTitle0", by="id")

        return asserts

    # 点击发布，选择全部用户，点击分布
    def release_4(self):
        # 调用release_3
        self.release_3()

        # 点击--选项框
        self.find_element_by_xpath("//li[@class='ant-select-search ant-select-search--inline']").click()

        # 点击--全部用户
        self.find_element_by_xpath("//li[text()='全部用户']").click()

        # 点击--设置可见角色
        self.find_element_by_id("rcDialogTitle0").click()

        # 点击--确定
        self.move_to_element_(
            self.find_element_by_xpath("//button[@class='ant-btn ant-btn-primary']/span[text()='确 定']"))
        self.click_()

        # 断言
        asserts = self.asserts("//span[text()='发布成功']")

        return asserts

    # 登录另一个用户，在工作区点击所有发布，显示之前用户发布的分析
    def release_5(self):
        self.fresh_()
        # 点击--账户图标
        self.move_to_element_(self.find_element("xpath", data['account_icon']))
        self.click_()

        # 点击--退出登录
        self.move_to_element_(self.find_element("xpath", data['log_out']))
        self.click_()

        # 登录另一个账户
        self.eda_login(account=config["autotest2_account"], password=autotest2_password)

        self.fresh_()
        # 点击--交互分析
        self.move_to_element_(self.find_element_by_xpath(data['analyse']))

        # 点击--工作区
        self.find_element_by_link_text("工作区").click()

        # 点击--所有发布
        self.find_element_by_xpath(data['all_release']).click()

        asserts = self.asserts(data['test_analysis_p'])

        self.fresh_()

        # 点击--账户图标
        self.move_to_element_(self.find_element("xpath", data['account_icon']))
        self.click_()

        # 点击--退出登录
        self.move_to_element_(self.find_element("xpath", data['log_out']))
        self.click_()

        # 登录另一个账户！
        self.eda_login(account=config["autotest_account"], password=autotest_password)

        # 断言
        return asserts

    # 点击取消发布，在所有发布页消失此分析
    def release_6(self):
        self.fresh_()
        # 点击--交互分析
        self.move_to_element_(self.find_element_by_xpath(data['analyse']))

        # 点击--工作区
        self.find_element_by_link_text("工作区").click()

        # 移动鼠标到测试分析
        self.move_to_element_(self.find_element_by_xpath(data['test_analysis_p']))

        # 点击--三个点图标
        self.move_to_element_(self.find_element_by_xpath(data['icon']))
        self.click_()

        # 点击--取消发布
        self.find_element_by_xpath("//a[text()='取消发布']").click()

        # 点击--确定
        self.move_to_element_(self.find_element_by_xpath(data['confirm']))
        self.click_()

        # 点击--所有发布
        self.find_element_by_xpath(data['all_release']).click()

        # 断言
        asserts = self.asserts(data['test_analysis_p'])
        if asserts:
            return False
        else:
            return True

    # 用户已勾选Test Role权限，查看所有发布
    def release_7(self):
        self.release_3()

        # 点击--选项框
        self.find_element_by_xpath("//li[@class='ant-select-search ant-select-search--inline']").click()

        # 点击--全部用户
        self.find_element_by_xpath("//li[text()='测试用户角色组']").click()

        # 点击--设置可见角色
        self.find_element_by_id("rcDialogTitle0").click()

        # 点击--确定
        self.move_to_element_(
            self.find_element_by_xpath("//button[@class='ant-btn ant-btn-primary']/span[text()='确 定']"))
        self.click_()

        # 点击--所有发布
        self.find_element_by_xpath(data['all_release']).click()

        # 断言
        asserts = self.asserts(data['test_analysis_p'])
        return asserts

    # 用户未勾选Test Role权限，查看所有发布
    def release_8(self):
        # 调用release_5()
        asserts = self.release_5()

        # 断言
        if asserts:
            return True
        else:
            return False

    # 删除新建分析
    def delete_new_analysis(self):
        self.fresh_()

        # 点击--交互分析")
        self.move_to_element_(self.find_element("xpath", data['analyse']))

        # "点击--工作区")
        self.find_element("link text", "工作区").click()

        # "点击--新建分析设计")
        self.find_element("xpath", "//div[@class='ant-card-body']").click()

        # "点击--删除")
        self.move_to_element_(
            self.find_element("xpath", "//div[@style='margin-top: 10px; float: right;']//button[2]//i"))
        self.click_()

        # "点击--确定")
        self.move_to_element_(self.find_element("xpath", data['confirm']))
        self.click_()

        # 断言
        asserts = self.asserts("//div[@style='margin-top: 10px; float: right;']//button[2]//i", log=False)
        if asserts:
            return False
        else:
            return True

    # 过滤--搜索出名称带有"测试"的所有分析
    def filter_1(self):
        self.fresh_()
        # 点击--账户图标
        self.move_to_element_(self.find_element("xpath", data['account_icon']))
        self.click_()

        # 点击--退出登录
        self.move_to_element_(self.find_element("xpath", data['log_out']))
        self.click_()

        # 登录另一个账户
        self.eda_login(account=config["autotest2_account"], password=autotest2_password)

        self.fresh_()
        # 点击--交互分析
        self.move_to_element_(self.find_element_by_xpath(data['analyse']))

        # 点击--工作区
        self.find_element_by_link_text("工作区").click()

        # 点击--我的分析
        self.move_to_element_(self.find_element_by_xpath(data['my_analysis']))
        self.click_()

        # 点击——搜索框
        self.find_element_by_xpath(data['search']).click()

        self.send_key_direct("测试")

        # 点击--搜索
        self.move_to_element_(self.find_element_by_xpath(data['search_button']))
        self.click_()

        # 断言
        asserts = self.asserts(data['test_analysis_design'])
        return asserts

    # 过滤--过滤条件为分析描述并搜索"测试"
    def filter_2(self):
        self.fresh_()

        # 点击--交互分析
        self.move_to_element_(self.find_element_by_xpath(data['analyse']))

        # 点击--工作区
        self.find_element_by_link_text("工作区").click()

        # 点击--我的分析
        self.move_to_element_(self.find_element_by_xpath(data['my_analysis']))
        self.click_()

        # 点击--分析名称
        self.find_element_by_xpath(data['analysis_name']).click()

        # 点击--分析描述
        self.find_element_by_xpath("//li[text()='分析描述']").click()

        # 点击——搜索框
        self.find_element_by_xpath(data['search']).click()

        self.send_key_direct("123")

        # 点击--搜索
        self.move_to_element_(self.find_element_by_xpath(data['search_button']))
        self.click_()

        # 断言
        asserts = self.asserts(data['test_analysis_design'])
        return asserts

    # 过滤--过滤条件为分析名称并搜索"测试"成功后，点击重置
    def filter_3(self):
        self.fresh_()

        # 点击--交互分析
        self.move_to_element_(self.find_element_by_xpath(data['analyse']))

        # 点击--工作区
        self.find_element_by_link_text("工作区").click()

        # 点击--我的分析
        self.move_to_element_(self.find_element_by_xpath(data['my_analysis']))
        self.click_()

        # 点击--分析名称
        self.find_element_by_xpath(data['analysis_name']).click()

        # 点击--分析描述
        self.find_element_by_xpath("//li[text()='分析描述']").click()

        # 点击——搜索框
        self.find_element_by_xpath(data['search']).click()

        self.send_key_direct("123")

        # 点击--搜索
        self.move_to_element_(self.find_element_by_xpath(data['search_button']))
        self.click_()

        # 点击--重置
        self.move_to_element_(self.find_element_by_xpath("//span[text()='重置']"))
        self.click_()

        # 断言
        asserts = self.asserts(data['analysis_name'])
        return asserts

    # 过滤--过滤条件为创建人并搜索"测试"
    def filter_4(self):
        self.fresh_()

        # 点击--交互分析
        self.move_to_element_(self.find_element_by_xpath(data['analyse']))

        # 点击--工作区
        self.find_element_by_link_text("工作区").click()

        # 点击--我的分析
        self.move_to_element_(self.find_element_by_xpath(data['my_analysis']))
        self.click_()

        # 点击--分析名称
        self.find_element_by_xpath(data['analysis_name']).click()

        # 点击--分析描述
        self.find_element_by_xpath("//li[text()='创建人']").click()

        # 点击——搜索框
        self.find_element_by_xpath(data['search']).click()

        self.send_key_direct("jing.huang6")

        # 点击--搜索
        self.move_to_element_(self.find_element_by_xpath(data['search_button']))
        self.click_()

        # 断言
        asserts = self.asserts(data['test_analysis_design'])

        self.fresh_()

        # 点击--账户图标
        self.move_to_element_(self.find_element("xpath", data['account_icon']))
        self.click_()

        # 点击--退出登录
        self.move_to_element_(self.find_element("xpath", data['log_out']))
        self.click_()

        # 登录另一个账户！
        self.eda_login(account=config["autotest_account"], password=autotest_password)

        return asserts

    # 过滤--随机创建多个分析并收藏，选择查看次数，选择降序,查看次数由大到小展示
    def filter_sort(self, sort_style=None, sort_type=None):

        self.fresh_()

        # 点击--交互分析
        self.move_to_element_(self.find_element_by_xpath(data['analyse']))

        # 点击--工作区
        self.find_element_by_link_text("工作区").click()

        # 点击--所有发布
        self.find_element_by_xpath(data['all_release']).click()

        # 点击--更新时间
        self.find_element_by_xpath("//div[text()='更新时间']").click()

        # 点击--查看次数
        self.find_element_by_xpath(f"//li[text()='{sort_type}']").click()

        #
        self.find_element_by_xpath(f"//span[text()='过滤:']").click()

        # 点击--降序
        self.find_element_by_xpath(f"//div[text()='降序']").click()

        # 点击--降序
        self.find_element_by_xpath(f"//li[text()='{sort_style}']").click()

        # 点击--排序
        self.move_to_element_(self.find_element_by_xpath("//span[text()='排序']"))
        self.click_()

    # 选择查看次数，选择降序，查看次数由大到小展示
    def filter_5(self):
        # 调用方法
        self.filter_sort(sort_style="降序", sort_type="查看次数")

        # 点击--降序
        count_div1 = self.find_element_by_xpath(
            "//*[@id='root']/div/section/section/section/main/div/div[2]/div[1]/div[2]/div[3]/span[2]").text
        logger.info(f"count_div1: {count_div1}")

        # 点击--降序
        count_div2 = self.find_element_by_xpath(
            "//*[@id='root']/div/section/section/section/main/div/div[2]/div[2]/div[2]/div[3]/span[2]").text
        logger.info(f"count_div2: {count_div2}")

        # 断言
        if count_div1 >= count_div2:
            return True
        else:
            return False

    # 分析名称，选择升序，名称由a-z由小到大展示
    def filter_6(self):
        # 调用方法
        self.filter_sort(sort_style="升序", sort_type="分析名称")

        # 断言
        asserts = self.asserts(data['test_analysis_demo'])
        return asserts

    # 收藏次数，选择升序，收藏次数由小到大展示
    def filter_7(self):
        # 调用方法
        self.filter_sort(sort_style="升序", sort_type="收藏次数")

        # 断言
        asserts = self.asserts(data['test_analysis_demo'])
        return asserts

    # 创建时间，选择降序，创建时间由最近时间到最远时间展示
    def filter_8(self):
        # 调用方法
        self.filter_sort(sort_style="降序", sort_type="创建时间")

        # 断言
        asserts = self.asserts(data['test_analysis_demo'])
        return asserts

    # 更新时间，选择升序，更新时间由最近时间到最远时间展示
    def filter_9(self):
        # 调用方法
        self.filter_sort(sort_style="降序", sort_type="更新时间")

        # 断言
        asserts = self.asserts(data['test_analysis_demo'])
        return asserts


if __name__ == '__main__':
    EDAWorkSpacePage().release_2()

