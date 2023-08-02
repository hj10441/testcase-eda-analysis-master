import os
import sys
import allure
from loguru import logger

sys.path.append(r'D:\autotestdata\testcase-eda-analysis-ui')
curPath = os.path.abspath(os.path.join(os.getcwd(), ".."))
rootPath = os.path.split(curPath)[0]
# print(rootPath)
sys.path.append(rootPath)
import pytest
from pageelements.EDA_work_space_analysis import EDAPage
from public.public_function import yaml_read
from dbiz_autotest_sdk.encrypt import decrypt


@allure.feature("EDA-交互分析-分析设计")
class TestUiEDA:

    def setup_class(self, count=0):
        config = yaml_read(yaml_name="/config/config.yml")
        autotest_name = config["autotest2_account"]
        autotest_password = decrypt(public_key=config["autotest2_password_key"],
                                    encryped_pwd=config["autotest2_password"])
        while count < 3:
            count += 1
            try:
                self.cms_page = EDAPage('状态监测系统')
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

    # @allure.title("分析设计-验证创建分析设计")
    # def test_01_into_work_space(self):
    #     assert self.cms_page.create_my_analysis()

    # @allure.title("分析设计-验证VDM添加数据集成功")
    # def test_02_workspace_vdmdata_query1(self):
    #   assert self.cms_page.add_workspace_vdm_data()
    #
    # @allure.title("分析设计-验证VDM时间范围过大提示语")
    # def test_03_workspace_vdmdata_query2(self):
    #     assert self.cms_page.vdmdata_query2()
    #
    # @allure.title("分析设计-验证vdm折线图创建成功")
    # def test_04_workspace_vdmdata_query3(self):
    #     assert self.cms_page.vdmdata_query3()
    #
    # @allure.title("分析设计-展示vdm柱状图失败")
    # def test_05_workspace_vdmdata_query4(self):
    #     assert self.cms_page.vdmdata_query4()

    # @allure.title("分析设计-展示vdm折线图")
    # def test_05_workspace_vdmdata_query5(self):
    #     assert self.cms_page.vdmdata_query5()

    # @allure.title("分析设计-展示vdm图表内容")
    # def test_05_workspace_vdmdata_query6(self):
    #     assert self.cms_page.vdmdata_query6()

    # @allure.title("分析设计-删除vdm分析设计")
    # def test_06_workspace_vdmdata_query_n(self):
    #     assert self.cms_page.vdmdata_query_n()

    # @allure.title("分析设计-创建dt10min分析设计")
    # def test_n_workspace_add_dt10min_data1(self):
    #     assert self.cms_page.add_workspace_dt10min_data1()
    #
    # @allure.title("分析设计-画出dt10min散点图分析设计")
    # def test_n_workspace_add_dt10min_data2(self):
    #     assert self.cms_page.add_workspace_dt10min_data2()
    #
    # @allure.title("分析设计-画出dt10min折线图分析设计")
    # def test_n_workspace_add_dt10min_data3(self):
    #     assert self.cms_page.add_workspace_dt10min_data3()
    #
    # @allure.title("分析设计-画出dt10min折线图分析设计")
    # def test_n_workspace_add_dt10min_data_4(self):
    #     assert self.cms_page.add_workspace_dt10min_data_4()
    #
    # @allure.title("分析设计-画出dt10min柱状图分析设计")
    # def test_n_workspace_add_dt10min_data5(self):
    #     assert self.cms_page.add_workspace_dt10min_data5()
    #
    # @allure.title("分析设计-根据dt10min柱状图设置参考线")
    # def test_n_workspace_add_dt10min_data6(self):
    #     assert self.cms_page.add_workspace_dt10min_data6()
    #
    # @allure.title("分析设计-根据dt10min柱状图进行分bin图展示")
    # def test_n_workspace_add_dt10min_data7(self):
    #     assert self.cms_page.add_workspace_dt10min_data7()
    #
    # @allure.title("分析设计-根据dt10min柱状图取消分bin图展示并点击下钻")
    # def test_n_workspace_add_dt10min_data8(self):
    #     assert self.cms_page.add_workspace_dt10min_data8()
    #
    # @allure.title("分析设计-画出dt10min表格分析设计")
    # def test_n_workspace_add_dt10min_data9(self):
    #     assert self.cms_page.add_workspace_dt10min_data9()
    #
    # @allure.title("分析设计-保存dt10min表格分析设计")
    # def test_n_workspace_add_dt10min_data10(self):
    #     assert self.cms_page.add_workspace_dt10min_data10()
    #
    # @allure.title("分析设计-画出dt10min表格分析设计并验证")
    # def test_n_workspace_add_dt10min_data11(self):
    #     assert self.cms_page.add_workspace_dt10min_data11()

    # def test_04_workspace_dt10min_data_table(self):
    #    assert self.cms_page.dt10min_scatter_diagram()

    # def test_n_delete_work_space_analysis(self):
    #     assert self.cms_page.delete_my_analysis()

    @allure.title("分析设计-创建SOE分析设计-所有事件")
    def test_n_workspace_add_soe_data1(self):
        assert self.cms_page.add_workspace_soe_data1()

    @allure.title("分析设计-画出SOE-所有事件表格图分析设计")
    def test_n_workspace_add_soe_data2(self):
        assert self.cms_page.add_workspace_soe_data2()

    @allure.title("分析设计-创建SOE分析设计-所有输出Tracelog事件")
    def test_n_workspace_add_soe_data3(self):
        assert self.cms_page.add_workspace_soe_data3()

    @allure.title("分析设计-画出SOE-所有输出Tracelog事件表格图分析设计")
    def test_n_workspace_add_soe_data4(self):
        assert self.cms_page.add_workspace_soe_data4()

    @allure.title("分析设计-创建SOE分析设计-所有选择的事件")
    def test_n_workspace_add_soe_data5(self):
        assert self.cms_page.add_workspace_soe_data5()

    @allure.title("分析设计-画出SOE-所有输出Tracelog事件表格图分析设计")
    def test_n_workspace_add_soe_data6(self):
        assert self.cms_page.add_workspace_soe_data6()


if __name__ == '__main__':
    # pytest.main(['test_case_eda_ui_04_work_space_analysis.py', '-vs'])
    pytest.main(['test_case_eda_ui_04_work_space_analysis.py', '-vs', '--alluredir', "../../report/tmp"])
    os.system('allure generate ../report/tmp -o  ../report/report --clean')
    os.system(r'allure serve C:\Xiangmu\test_cms\testcase-cms\report\tmp')
