import os
import time

from loguru import logger
import socket
from pageelements.base_page import BasePage, readfile
from public.public_function import yaml_read
from dbiz_autotest_sdk.encrypt import decrypt

data = yaml_read(yaml_name="/config/work_space_analysis.yml")
config = yaml_read(yaml_name="/config/config.yml")
mysql_password = decrypt(public_key=config["mysql_password_key"], encryped_pwd=config["mysql_password"])
autotest_password = decrypt(public_key=data["autotest_password_key"], encryped_pwd=data["autotest_password"])
autotest2_password = decrypt(public_key=config["autotest2_password_key"], encryped_pwd=config["autotest2_password"])


class EDAPage(BasePage):

    # 交互分析——工作区——创建我的分析
    def create_my_analysis(self):

        # 刷新界面
        self.fresh_()

        # 点击交互分析
        self.move_to_element_(self.find_element('xpath', data['interaction_analysis']))

        # 点击工作区
        self.find_element_by_link_text('工作区').click()

        # 点击创建我的分析
        self.find_element('xpath', data['create_analysis']).click()

        # 点击分析名称栏
        self.move_to_element_(self.find_element_by_xpath('//*[@id="analysisName"]'))

        # 清空默认分析名
        self.find_element_by_xpath('//*[@id="analysisName"]').clear()

        # 输入分析名
        self.find_element_by_xpath('//*[@id="analysisName"]').send_keys('jing.huang_分析设计')

        # 点击确定
        self.move_to_element_(self.find_element_by_xpath(data['confirm']))
        self.click_()

        # 读取跳转后的创建分析名进行确定
        key = self.find_element_by_xpath(
            '//*[@id="root"]/div/section/section/section/main/div[1]/div[1]/div[1]/div/span[1]').text
        if key == 'jing.huang_分析设计':
            return True
        else:
            return False

    # 分析设计中添加风机配置数据
    def add_workspace_vdm_data(self):
        # 点击工程数据分析
        self.find_element_by_xpath('//*[@id="logo"]/a/h1').click()

        # 刷新界面
        self.fresh_()

        # 点击交互分析
        self.move_to_element_(self.find_element('xpath', data['interaction_analysis']))

        # 点击工作区
        self.find_element_by_link_text('工作区').click()

        # 点击创建我的分析
        self.find_element('xpath', data['create_analysis']).click()

        # 点击分析名称栏
        self.move_to_element_(self.find_element_by_xpath('//*[@id="analysisName"]'))

        # 清空默认分析名
        self.find_element_by_xpath('//*[@id="analysisName"]').clear()

        # 输入分析名
        self.find_element_by_xpath('//*[@id="analysisName"]').send_keys('vdm分析设计')

        # 点击确定
        self.move_to_element_(self.find_element_by_xpath(data['confirm']))
        self.click_()

        # 点击添加数据集“+”号
        self.find_element_by_xpath(
            "//*[@id='root']/div/section/section/section/main/div[1]/div[4]/div[1]/div[2]/div/div/div[1]/div[1]/div[1]/div/div[2]/div/button").click()

        # 点击数据集名称并清空数据集名
        self.find_element('id', "dataName").clear()

        # 输入新的数据集名称--测试VDM数据
        self.find_element('id', "dataName").send_keys("测试vdm数据")

        # 点击数据源类型框
        self.find_element('id', "dataSourceType").click()

        # 选择数据源--样机测试数据
        self.find_element_by_xpath("//li[text()='样机测试数据']").click()

        # 点击风场选择框
        self.find_element_by_xpath('//*[@id="wind_farm"]/div/span/i').click()

        # 选择风场--山西广灵望狐
        self.find_element_by_xpath('//li[text()="山西广灵望狐(Guangling_Wanghu)"]').click()

        # 点击风机选择框
        self.find_element_by_xpath('//*[@id="wind_turbine"]/div/span/i').click()

        # 选择风机--EN30_LZ156_90HH_SXGL_WH55
        self.find_element_by_xpath('//li[text()="EN30_LZ156_90HH_SXGL_WH55"]').click()

        self.find_element('id', 'accessGroups').click()

        # 用来页面加载
        self.time_sleep('level13')

        # 选择前五条通道
        self.find_element_by_xpath('//div[text()="B1Pitch_Motor_Spd"]').click()
        self.find_element_by_xpath('//div[text()="B1Pitch_Motor_Trq"]').click()
        self.find_element_by_xpath('//div[text()="B1_D001500_BS000T180"]').click()
        self.find_element_by_xpath('//div[text()="B1_D001500_BS090T270"]').click()
        self.find_element_by_xpath('//div[text()="B1_D001500_MxB"]').click()

        # 点击添加按钮
        self.move_to_element_(self.find_element_by_xpath('//span[text()="添 加"]'))
        self.click_()

        # 点击确定
        self.move_to_element_(self.find_element_by_xpath('//span[text()="确 定"]'))
        self.click_()

        # 断言
        asserts = self.asserts('//span[text()="添加数据集成功"]')

        return asserts

    # 验证时区过大提示语
    def vdmdata_query2(self):

        # 点击新增图元分析
        self.find_element_by_xpath(
            '//*[@id="root"]/div/section/section/section/main/div[1]/div[1]/div[2]/button[2]').click()

        self.drag_and_drop_(self.find_element_by_xpath('//div[text()="Date_Time"]'),
                            self.find_element_by_xpath(
                                '//*[@id="root"]/div/section/section/section/main/div[1]/div[4]/div[2]/div[2]/div/div[3]/div[1]/div/div[2]/div/div/div/div'))

        self.drag_and_drop_(self.find_element_by_xpath('//div[text()="B1Pitch_Motor_Spd(rpm)"]'),
                            self.find_element_by_xpath(
                                '//*[@id="root"]/div/section/section/section/main/div[1]/div[4]/div[2]/div[2]/div/div[3]/div[1]/div/div[3]/div/div/div/div'))

        self.time_sleep('level13')

        # 点击预览按钮
        self.find_element_by_xpath(
            '//*[@id="root"]/div/section/section/section/main/div[1]/div[4]/div[2]/div[2]/div/div[3]/div[1]/div/div[1]/div/div[2]/div/button[1]').click()

        asserts = self.asserts('//span[text()="时间范围过大，只支持1小时内的时序分析"]')

        return asserts

        # 修改时区过大，并画出图像

    def vdmdata_query3(self):
        # 选择开始时间框
        self.find_element_by_xpath('//input[@placeholder="开始日期"]').click()
        self.find_element_by_xpath('//td[@title="2019年12月5日"]/div[text()="5"]').click()
        self.find_element_by_xpath('//td[@title="2019年12月5日"]/div[text()="5"]').click()
        self.find_element_by_xpath('//input[@placeholder="开始日期"]').click()
        self.find_element_by_xpath('//a[text()="选择时间"]').click()
        self.find_element_by_xpath('//ul/li[text()="13"]').click()

        # 点击预览按钮
        self.find_element_by_xpath(
            '//*[@id="root"]/div/section/section/section/main/div[1]/div[4]/div[2]/div[2]/div/div[3]/div[1]/div/div[1]/div/div[2]/div/button[1]').click()

        self.time_sleep('level15')

        '''这里用来判定折线图是否成功创建'''
        # 截图
        self.screen_shot('vdm_broken_line_model_contrast.jpg')

        # img1为模板图片，测试环境因为不会随便添加数据，所以每次截图应该都是一样的
        img1 = BasePage.test_pic_dir + r'/vdm_broken_line_model.jpg'
        img2 = BasePage.test_pic_dir + r'/vdm_broken_line_model_contrast.jpg'

        # 比对两张图片不一致率
        result = self.image_compare_(img1, img2)

        # 将本次截图删除
        os.remove(img2)

        # 判定如果本次截图和模板图片相差度是否为0，如果不是0则返回False
        if result == 0:
            return True
        else:
            return False

    # 展示柱状图失败
    def vdmdata_query4(self):

        # 点击新增指标
        self.drag_and_drop_(self.find_element_by_xpath('//div[text()="Max.B1Pitch_Motor_Spd(rpm)"]'),
                            self.find_element_by_xpath(
                                '//*[@id="root"]/div/section/section/section/main/div[1]/div[4]/div[2]/d'
                                'iv[2]/div/div[3]/div[1]/div/div[3]/div/div/div/div'))

        self.time_sleep('level14')

        # 点击柱状图按钮
        self.find_element_by_xpath(
            '//*[@id="root"]/div/section/section/section/main/div[1]/div[4]/div[2]/div[2]/div/div[2]/div[2]/d'
            'iv/div[2]/div[1]/div/label[3]').click()

        # 点击预览按钮
        self.find_element_by_xpath(
            '//*[@id="root"]/div/section/section/section/main/div[1]/div[4]/div[2]/div[2]/div/div[3]/d'
            'iv[1]/div/div[1]/div/div[2]/div/button[1]').click()

        asserts = self.find_element_by_xpath('//span[text()="当前选择图表类型与字段的变量类型不一致"]')

        return asserts

    # 展示vdm散点图成功
    # def vdmdata_query_5(self):
    # 清除通道
    # 将Datatime列拖到x轴
    # 将对应的通道列拖到y轴
    # 点击散点图图案
    # 比对图片
    # 判定

    # 展示vdm图表成功
    # def vdmdata_query_6(self):
    # 清除通道
    # 将Datatime列拖到x轴
    # 将对应的通道列拖到y轴
    # 点击图表图案
    # 比对图片
    # 判定

    # 删除vdm视图
    def vdmdata_query_n(self):

        # 点击删除
        self.move_to_element_(self.find_element_by_xpath(
            '//*[@id="root"]/div/section/section/section/main/div[1]/div[1]/div[3]/button[2]/i'))
        self.click_()

        # 点击二次确定按钮
        self.move_to_element_(self.find_element_by_xpath(data['confirm']))
        self.click_()

        # 判定是否删除vdm数据分析设计
        asserts = self.asserts('//p[text()="测试vdm数据"]')

        if asserts:
            return False
        else:
            return True

    # 创建dt10min数据分析
    def add_workspace_dt10min_data1(self):
        # 点击工程数据分析
        self.find_element_by_xpath('//*[@id="logo"]/a/h1').click()

        # 刷新界面
        self.fresh_()

        # 点击交互分析
        self.move_to_element_(self.find_element('xpath', data['interaction_analysis']))

        # 点击工作区
        self.find_element_by_link_text('工作区').click()

        # 点击搜索框输入分析名
        self.find_element('xpath',
                          '//*[@id="root"]/div/section/section/section/main/div/div[1]/div[2]/input').send_keys(
            'jing.huang')

        # 点击搜索
        self.move_to_element_(self.find_element_by_xpath(data['confirm1']))
        self.click_()

        # 判定是否有名为“jing.huang_分析设计”的设计
        asserts = self.asserts('//p[text()="jing.huang_分析设计"]')

        # 如果“jing.huang_分析设计”已存在
        if asserts:
            self.delete_my_analysis(name="jing.huang_分析设计")
            asserts = self.add_workspace_dt10min_data1()
            return asserts

        # 如果“jing.huang_分析设计”不存在
        else:
            # 点击创建我的分析
            self.find_element('xpath', data['create_analysis']).click()

            # 点击分析名称栏
            self.move_to_element_(self.find_element_by_xpath('//*[@id="analysisName"]'))

            # 清空默认分析名
            self.find_element_by_xpath('//*[@id="analysisName"]').clear()

            # 输入分析名
            self.find_element_by_xpath('//*[@id="analysisName"]').send_keys('jing.huang_分析设计')

            # 点击确定
            self.move_to_element_(self.find_element_by_xpath(data['confirm']))
            self.click_()

            # 点击添加数据集“+”号
            logger.info("点击数据集“+”号按钮")
            self.move_to_element_(self.find_element_by_xpath('//i[@aria-label="图标: plus"]'))
            self.click_()

            # 点击数据集名称并清空数据集名
            self.find_element('id', "dataName").clear()

            # 输入新的数据集名称--测试dt10min数据
            self.find_element('id', "dataName").send_keys("测试dt10min数据")

            # 点击数据源类型框
            self.find_element('id', "dataSourceType").click()

            # 选择数据源--样机测试数据
            self.find_element_by_xpath("//li[text()='DigitalTwin-10min数据']").click()

            # 点击风场选择框
            self.find_element_by_id("windField").click()

            # 选择风场--点击快速过滤
            self.move_to_element_(self.find_element_by_xpath('//span[text()="快速过滤"]'))
            self.click_()

            # 选择输入框输入风场CN号
            self.find_element('id', "cnNumber").send_keys('CN-01/09')

            # 点击确定按钮
            logger.info('点击确定按钮')
            self.move_to_element_(self.find_element_by_xpath('//div[3]/div/button[2]/span[text()="确 定"]'))
            self.click_()

            logger.info('再次点击确定按钮')
            self.move_to_element_(self.find_element_by_xpath('//span[text()="确 定"]'))
            self.click_()

            # 点击风机选择框
            logger.info('点击风机选择框')
            self.move_to_element_(self.find_element_by_id("turbine"))
            self.click_()

            # 点击选择风机--详细维度过滤
            logger.info('点击风机详细维度过滤')
            self.move_to_element_(self.find_element_by_xpath('//span[text()="详细维度过滤"]'))
            self.click_()

            # 点击选择风机
            logger.info('点击选择风机')
            self.find_element_by_xpath('//div[@title="NMBL.T1_L1.WTG001"]').click()
            self.find_element_by_xpath('//div[@title="NMBL.T1_L1.WTG002"]').click()
            self.find_element_by_xpath('//div[@title="NMBL.T1_L1.WTG003"]').click()

            # 点击确定
            logger.info('点击风机选择确定按钮')
            self.move_to_element_(self.find_element_by_xpath('//div[2]/div[3]/div/button[2]/span[text()="确 定"]'))
            self.click_()

            # 再次点击确定
            logger.info('点击风机选择框内的确定按钮')
            self.move_to_element_(self.find_element_by_xpath('//div/div[2]/button[4]/span[text()="确 定"]'))
            self.click_()

            # 点击时间选择框输入时间范围
            logger.info('输入开始时间')
            self.find_element_by_xpath('//input[@placeholder="开始时间"]').click()

            self.find_element_by_xpath('//div[text()="10"]').click()
            self.find_element_by_xpath('//div[text()="15"]').click()

            # 点击确定
            logger.info('点击日期栏确定按钮')
            self.find_element_by_xpath('//a[text()="确 定"]').click()

            # 点击风机维度框
            self.find_element_by_xpath('//*[@id="timeDimension"]').click()

            # 选择风场风机维度
            self.find_element_by_xpath('//div[text()="风机名"]').click()
            self.find_element_by_xpath('//div[text()="风机主数据ID"]').click()
            self.find_element_by_xpath('//div[text()="USCADA简称"]').click()
            self.find_element_by_xpath('//div[text()="齿轮箱物料号"]').click()
            self.find_element_by_xpath('//div[text()="风场名"]').click()

            # 点击维度确定按钮
            logger.info('定位确定按钮')
            self.move_to_element_(self.find_element_by_xpath(
                '//form/div/div[1]/div[5]/div[2]/div/span/div[2]/div/div/div/div/div[2]/button[2]/span[text()="确 定"]'))
            logger.info('点击确定按钮')
            self.click_()

            # 点击通道添加框
            logger.info('点击通道框')
            self.find_element_by_xpath('//*[@id="passageway"]').click()

            # 点击添加通道
            logger.info('点击添加对应通道')
            self.move_to_element_(self.find_element_by_xpath('//div[text()="叶根1Mxy弯矩LDD分布"]'))
            self.click_()

            self.move_to_element_(self.find_element_by_xpath('//div[@title="叶根2Mxy弯矩LDD分布"]'))
            self.click_()

            self.move_to_element_(self.find_element_by_xpath('//div[@title="叶根3Mxy弯矩LDD分布"]'))
            self.click_()

            self.move_to_element_(self.find_element_by_xpath('//div[@title="轮毂中心My(旋转坐标系)的M10等效疲劳"]'))
            self.click_()

            self.move_to_element_(self.find_element_by_xpath('//div[@title="轮毂中心My(静止坐标系)的M10原始等效疲劳"]'))
            self.click_()

            # 点击添加按钮
            logger.info("点击添加按钮")
            self.move_to_element_(self.find_element_by_xpath('//span[text()="添 加"]'))
            self.click_()

            # 点击编辑数据集确定按钮
            logger.info("点击确认按钮")
            self.move_to_element_(self.find_element_by_xpath('//div/div[2]/div[3]/button[2]/span["确 定"]'))
            self.click_()

            # 判定数据集是否成功创建
            asserts = self.asserts('//span[text()="[DT]测试dt10min数据"]')
            return asserts

    # 画出dt10min散点图
    def add_workspace_dt10min_data2(self):
        # 点击图元分析
        self.move_to_element_(self.find_element_by_xpath('//span[text()="图元分析"]'))
        self.click_()

        self.drag_and_drop_(self.find_element_by_xpath('//div[text()="Date_Time"]'),
                            self.find_element_by_xpath(
                                '//*[@id="root"]/div/section/section/section/main/div[1]/di'
                                'v[4]/div[2]/div[2]/div/div[3]/div[1]/div/div[2]/div/div/div/div'))

        self.drag_and_drop_(self.find_element_by_xpath('//div[text()="Stat_WindSpeedAve(m/s)"]'),
                            self.find_element_by_xpath(
                                '//*[@id="root"]/div/section/section/section/main/div[1]/di'
                                'v[4]/div[2]/div[2]/div/div[3]/div[1]/div/div[3]/div/div/div/div'))

        self.drag_and_drop_(self.find_element_by_xpath('//div[text()="Stat_ActivePowerAve(kW)"]'),
                            self.find_element_by_xpath(
                                '//*[@id="root"]/div/section/section/section/main/div[1]/di'
                                'v[4]/div[2]/div[2]/div/div[3]/div[1]/div/div[3]/div/div/div/div'))

        self.time_sleep('level13')

        # 点击预览按钮
        logger.info("点击预览按钮")
        self.move_to_element_(self.find_element_by_xpath('//i[@aria-label="图标: eye"]'))
        self.click_()

        self.time_sleep('level12')

        '''这里用来判定散点图是否成功创建'''
        # 截图
        self.screen_shot('dt10min_Scatterplot_model.jpg')
        self.screen_shot('dt10min_Scatterplot_model_contrast.jpg')

        # img1为模板图片，测试环境因为不会随便添加数据，所以每次截图应该都是一样的
        img1 = BasePage.test_pic_dir + r'dt10min_Scatterplot_model.jpg'
        img2 = BasePage.test_pic_dir + r'dt10min_Scatterplot_model_contrast.jpg'

        # 比对两张图片不一致率
        logger.info("比对散点图不一致率")
        result = self.image_compare_(img1, img2)

        # 将本次截图删除
        logger.info("删除比对的DT10min散点图")
        os.remove(img2)

        # 判定如果本次截图和模板图片相差度是否为0，如果不是0则返回False
        if result == 0:
            return True
        else:
            return False

        # 画出dt10min折线图

    def add_workspace_dt10min_data3(self):
        # 点击折线图按钮
        logger.info("点击折线图按钮")
        self.find_element_by_xpath(
            '//*[@id="root"]/div/section/section/section/main/div[1]/div[4]/div[2]/div[2]/div/div[2]/div[2]/d'
            'iv/div[2]/div[1]/div/label[2]').click()

        self.time_sleep('level12')

        '''这里用来判定折线图是否成功创建'''
        # 截图
        logger.info("截图-模板图")
        self.screen_shot('dt10min_broken_line_model.jpg')

        logger.info("截图-比对图")
        self.screen_shot('dt10min_broken_line_model_contrast.jpg')

        # img1为模板图片，测试环境因为不会随便添加数据，所以每次截图应该都是一样的
        img1 = BasePage.test_pic_dir + r'dt10min_broken_line_model.jpg'
        img2 = BasePage.test_pic_dir + r'dt10min_broken_line_model_contrast.jpg'

        # 比对两张图片不一致率
        logger.info("比对折线图不一致率")
        result = self.image_compare_(img1, img2)

        # 将本次截图删除
        logger.info("删除比对的DT10min折线图")
        os.remove(img2)

        # 判定如果本次截图和模板图片相差度是否为0，如果不是0则返回False
        if result == 0:
            return True
        else:
            return False

    # 点击进行值过滤
    def add_workspace_dt10min_data_4(self):
        # 点击值过滤图标
        logger.info("点击值过滤旁边的“+”号按钮")
        time.sleep(10)
        self.find_element_by_xpath(
            '/html/body/div[1]/div/section/section/section/main/div[1]/div[4]/div[2]/div[2]/div'
            '/div[2]/div[1]/div/div[2]/div/div[2]/div[1]/i').click()

        # 点击选择框
        self.move_to_element_(self.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[2]/div[2]/div/div[1]'
                                                         '/div[2]/span/span/span[2]/i[@aria-label="图标: down"]'))
        self.click_()

        # 点击选择过滤字段
        logger.info("选择过滤字段")
        self.find_element_by_xpath('//span[text()="Stat_ActivePowerAve"]').click()

        # 点击选择过滤条件
        logger.info("选择过滤公式")
        self.move_to_element_(self.find_element_by_xpath('//span[text()="添加且(AND)条件"]'))
        self.click_()

        self.find_element_by_xpath('//table/tbody[@class="ant-table-tbody"]/tr/td[4]/div/div/span'
                                   '/i[@aria-label="图标: down"]').click()

        self.move_to_element_(
            self.find_element_by_xpath('//li[@label="大于(>)"]'))
        self.click_()

        # 数据过滤值
        logger.info("输入过滤值")
        self.find_element_by_xpath(
            '//table/tbody[@class="ant-table-tbody"]/tr/td[5]/input[@type="text"]').send_keys(5)
        # 点击确定
        logger.info("点击确定按钮")
        self.move_to_element_(self.find_element_by_xpath('//span[text()="确 定"]'))
        self.click_()

        # 点击预览
        logger.info("点击预览按钮")
        self.move_to_element_(self.find_element_by_xpath('//i[@aria-label="图标: eye"]'))
        self.click_()

        self.time_sleep('level13')

        '''这里用来图表判定是否成功展示'''
        # 截图
        self.screen_shot('dt10min_filter_model.jpg')  # 该截图用作模板，只有第一次使用，之后注释掉该行代码
        time.sleep(5)  # 等一会删除掉
        logger.info("截图-比对图：图表")
        self.screen_shot('dt10min_filter_model_contrast.jpg')

        # img1为模板图片，测试环境因为不会随便添加数据，所以每次截图应该都是一样的
        img1 = BasePage.test_pic_dir + r'dt10min_filter_model.jpg'
        img2 = BasePage.test_pic_dir + r'dt10min_filter_model_contrast.jpg'

        # 比对两张图片不一致率
        result = self.image_compare_(img1, img2)

        # 将本次截图删除
        logger.info("删除对比图")
        os.remove(img2)

        # 判定如果本次截图和模板图片相差度是否为0，如果不是0则返回False
        if result == 0:
            return True
        else:
            return False

    # 画出dt10min柱状图
    def add_workspace_dt10min_data5(self):
        # 点击柱状图按钮
        self.find_element_by_xpath(
            '//*[@id="root"]/div/section/section/section/main/div[1]/div[4]/div[2]/div[2]/div/div[2]/div[2]/d'
            'iv/div[2]/div[1]/div/label[3]').click()

        # 将X轴换成风机名
        self.drag_and_drop_(self.find_element_by_xpath('//div[text()="风机名"]'),
                            self.find_element_by_xpath(
                                '//*[@id="root"]/div/section/section/section/main/div[1]/di'
                                'v[4]/div[2]/div[2]/div/div[3]/div[1]/div/div[2]/div/div/div/div'))

        # 点击预览按钮
        logger.info("点击预览按钮")
        self.move_to_element_(self.find_element_by_xpath('//i[@aria-label="图标: eye"]'))
        self.click_()

        '''这里用来判定柱状图是否成功创建'''
        # 截图
        self.time_sleep('level14')

        logger.info("截图-模版图")
        self.screen_shot('dt10min_histogram_model.jpg')  # 该截图用作模板，只有第一次使用，之后注释掉该行代码

        logger.info("截图-比对图")
        self.screen_shot('dt10min_histogram_model_contrast.jpg')

        # img1为模板图片，测试环境因为不会随便添加数据，所以每次截图应该都是一样的
        img1 = BasePage.test_pic_dir + r'/dt10min_histogram_model.jpg'
        img2 = BasePage.test_pic_dir + r'/dt10min_histogram_model_contrast.jpg'

        # 比对两张图片不一致率
        logger.info("比对柱状图不一致率")
        result = self.image_compare_(img1, img2)

        # 将本次截图删除
        os.remove(img2)

        # 判定如果本次截图和模板图片相差度是否为0，如果不是0则返回False
        if result == 0:
            return True
        else:
            return False

    # 展示dt10min参考线图
    def add_workspace_dt10min_data6(self):
        # 定位y轴图标，删除一条数据
        self.find_element_by_xpath('//*[@id="root"]/div/section/section/section/main/div[1]/div[4]/div[2]/div[2]/div'
                                   '/div[3]/div[1]/div/div[3]/div/div/div/div/ul/li[1]/div/strong/img').click()
        # 点击删除
        self.find_element_by_xpath('//div[text()="删除"]').click()
        # 定位y轴图标，点击一条数据的下拉图标
        self.find_element_by_xpath('//*[@id="root"]/div/section/section/section/main/div[1]/div[4]/div[2]/div[2]'
                                   '/div/div[3]/div[1]/div/div[3]/div/div/div/div/ul/li[1]/div/strong/img').click()

        # 点击标记参考线
        self.find_element_by_xpath('//div[text()="标记参考线"]').click()
        # 点击添加参考线
        self.move_to_element_(self.find_element_by_xpath('//span[text()="添加参考线"]'))
        self.click_()

        # 点击确定
        self.move_to_element_(self.find_element_by_xpath('//span[text()="确 定"]'))
        self.click_()

        # 点击预览按钮
        logger.info("点击预览按钮")
        self.move_to_element_(self.find_element_by_xpath('//i[@aria-label="图标: eye"]'))
        self.click_()

        # 截图
        self.time_sleep('level14')

        logger.info("截图-模版图")
        self.screen_shot('dt10min_reference_line_model.jpg')  # 该截图用作模板，只有第一次使用，之后注释掉该行代码

        logger.info("截图-比对图")
        self.screen_shot('dt10min_reference_line_model_contrast.jpg')

        # img1为模板图片，测试环境因为不会随便添加数据，所以每次截图应该都是一样的
        img1 = BasePage.test_pic_dir + r'dt10min_reference_line_model.jpg'
        img2 = BasePage.test_pic_dir + r'dt10min_reference_line_model_contrast.jpg'

        # 比对两张图片不一致率
        logger.info("比对柱状图不一致率")
        result = self.image_compare_(img1, img2)

        # 将本次截图删除
        os.remove(img2)

        # 判定如果本次截图和模板图片相差度是否为0，如果不是0则返回False
        if result == 0:
            return True
        else:
            return False

    # 展示dt10min分bin图表
    def add_workspace_dt10min_data7(self):
        # 定位y轴图标，点击一条数据的下拉图标
        logger.info("点击Y轴的通道下拉图标")
        self.find_element_by_xpath('//*[@id="root"]/div/section/section/section/main/div[1]/div[4]/div[2]/div[2]'
                                   '/div/div[3]/div[1]/div/div[3]/div/div/div/div/ul/li[1]/div/strong/img').click()

        # 点击设置分Bin统计
        logger.info("点击-设置分Bin统计")
        self.find_element_by_xpath('//div[text()="设置分Bin统计"]').click()

        # 点击确定按钮
        logger.info("点击确定按钮")
        self.move_to_element_(
            self.find_element_by_xpath('//div[@role="document"]/div[@class="ant-modal-content"]/'
                                       'div[@class="ant-modal-footer"]/button[3]'))
        self.click_()

        # 截图
        self.time_sleep('level14')

        logger.info("截图-模版图")
        self.screen_shot('dt10min_bin_model.jpg')  # 该截图用作模板，只有第一次使用，之后注释掉该行代码

        logger.info("截图-比对图")
        self.screen_shot('dt10min_bin_model_contrast.jpg')

        # img1为模板图片，测试环境因为不会随便添加数据，所以每次截图应该都是一样的
        img1 = BasePage.test_pic_dir + r'dt10min_bin_model.jpg'
        img2 = BasePage.test_pic_dir + r'dt10min_bin_model_contrast.jpg'

        # 比对两张图片不一致率
        logger.info("比对分bin图不一致率")
        result = self.image_compare_(img1, img2)

        # 将本次截图删除
        logger.info("删除对比图")
        os.remove(img2)

        # 判定如果本次截图和模板图片相差度是否为0，如果不是0则返回False
        if result == 0:
            return True
        else:
            return False

    # 关闭分bin图，点击下钻
    def add_workspace_dt10min_data8(self):
        # 定位y轴图标，点击一条数据的下拉图标
        logger.info("点击Y轴的通道下拉图标")
        self.find_element_by_xpath('//*[@id="root"]/div/section/section/section/main/div[1]/div[4]/div[2]/div[2]'
                                   '/div/div[3]/div[1]/div/div[3]/div/div/div/div/ul/li[1]/div/strong/img').click()

        # 点击设置分Bin统计
        logger.info("点击-设置分Bin统计")
        self.find_element_by_xpath('//div[text()="设置分Bin统计"]').click()

        # 点击关闭分bin统计
        logger.info("点击关闭分Bin统计")
        self.move_to_element_(self.find_element_by_xpath('//*[text()="关闭分Bin统计"]'))
        self.click_()

        time.sleep(10)
        # 点击图片进行下钻
        logger.info("点击表格图片进行下钻-通过坐标")
        dr = self.move_by_offset_(287.94, 0)
        dr.click()
        dr.perform()
        self.time_sleep('level13')

        # 保存下钻图元
        logger.info("点击保存下钻图元")
        self.move_to_element_(self.find_element_by_xpath('//*[text()="保 存"]'))
        self.click_()

        # 断言
        asserts = self.asserts('//*[text()="当前图元保存成功"]')
        return asserts

    # 展示dt10min图表
    def add_workspace_dt10min_data9(self):
        # 点击数据表按钮
        logger.info("点击图表图标")
        self.find_element_by_xpath(
            '//*[@id="root"]/div/section/section/section/main/div[1]/div[4]/div[2]/div[2]/div/div[2]/div[2]/d'
            'iv/div[2]/div[1]/div/label[4]').click()

        # 点击预览按钮
        logger.info("点击预览按钮")
        self.move_to_element_(self.find_element_by_xpath('//*[@id="root"]/div/section/section/section/main/div[1]'
                                                         '/div[4]/div[2]/div[2]/div/div[3]/div[1]/div/div[1]/div/'
                                                         'div[2]/div/button[1]'))
        self.click_()

        self.time_sleep('level13')

        '''这里用来判定图表是否成功展示'''
        # 截图
        self.screen_shot('dt10min_table_data_model.jpg')  # 该截图用作模板，只有第一次使用，之后注释掉该行代码
        logger.info("截图-比对图：图表")
        self.screen_shot('dt10min_table_data_model_contrast.jpg')

        # img1为模板图片，测试环境因为不会随便添加数据，所以每次截图应该都是一样的
        img1 = BasePage.test_pic_dir + r'dt10min_table_data_model.jpg'
        img2 = BasePage.test_pic_dir + r'dt10min_table_data_model_contrast.jpg'

        # 比对两张图片不一致率
        result = self.image_compare_(img1, img2)

        # 将本次截图删除
        logger.info("删除对比图")
        os.remove(img2)

        # 判定如果本次截图和模板图片相差度是否为0，如果不是0则返回False
        if result == 0:
            return True
        else:
            return False

    # 保存dt10min图表
    def add_workspace_dt10min_data10(self):
        # 点击保存按钮
        logger.info("点击保存按钮")
        self.move_to_element_(self.find_element_by_xpath('//i[@aria-label="图标: save"]'))
        self.click_()

        # 断言
        asserts = self.asserts('//*[text()="当前图元保存成功"]')
        return asserts

    # 确认图元保存到总览
    def add_workspace_dt10min_data11(self):
        # 点击总览按钮
        logger.info("点击总览图标")
        self.move_to_element_(self.find_element_by_xpath('//span[text()="总 览"]'))
        self.click_()

        # 截图进行比对
        self.time_sleep('level12')

        # 截图
        logger.info("截图-模板图")
        self.screen_shot('dt10min_overview_model.jpg')  # 该截图用作模板，只有第一次使用，之后注释掉该行代码

        logger.info("截图-比对图：图表")
        self.screen_shot('dt10min_overview_model_contrast.jpg')

        # img1为模板图片，测试环境因为不会随便添加数据，所以每次截图应该都是一样的
        img1 = BasePage.test_pic_dir + r'dt10min_overview_model.jpg'
        img2 = BasePage.test_pic_dir + r'dt10min_overview_model_contrast.jpg'

        # 比对两张图片不一致率
        result = self.image_compare_(img1, img2)

        # 将本次截图删除
        logger.info("删除对比图")
        os.remove(img2)

        # 判定如果本次截图和模板图片相差度是否为0，如果不是0则返回False
        if result == 0:
            return True
        else:
            return False

    # 删除我的分析创建
    def delete_my_analysis(self, name='jing.huang_分析设计'):

        # 点击工程数据分析
        logger.info("点击工程数据分析图标")
        self.find_element_by_xpath('//*[@id="logo"]/a/h1').click()

        # 刷新界面
        logger.info("刷新页面")
        self.fresh_()

        # 点击交互分析
        logger.info("点击交互分析")
        self.move_to_element_(self.find_element('xpath', data['interaction_analysis']))

        # 点击工作区
        logger.info('点击工作区')
        self.find_element_by_link_text('工作区').click()

        # 点击搜索框输入分析名
        logger.info('点击搜索框输入分析名')
        self.find_element('xpath',
                          '//*[@id="root"]/div/section/section/section/main/div/div[1]/div[2]/input').send_keys(
            name)

        # 点击搜索
        logger.info('点击搜索')
        self.move_to_element_(self.find_element_by_xpath(data['confirm1']))
        self.click_()

        # 点击进入分析设计
        logger.info('点击进入分析设计')
        self.find_element_by_xpath(
            '//*[@id="root"]/div/section/section/section/main/div/div[2]/div/div[2]/div[2]/div').click()

        # 点击删除
        logger.info('点击删除')
        self.move_to_element_(self.find_element_by_xpath(
            '//*[@id="root"]/div/section/section/section/main/div[1]/div[1]/div[3]/button[2]/i'))
        self.click_()

        # 点击二次确定按钮
        logger.info('点击二次确定按钮')
        self.move_to_element_(self.find_element_by_xpath(data['confirm']))
        self.click_()

        # 点击工程数据分析
        logger.info('点击工程数据分析')
        self.find_element_by_xpath('//*[@id="logo"]/a/h1').click()

        # 刷新界面
        logger.info('刷新界面')
        self.fresh_()

        # 点击交互分析
        logger.info('点击交互分析')
        self.move_to_element_(self.find_element('xpath', data['interaction_analysis']))

        # 点击工作区
        logger.info('点击工作区')
        self.find_element_by_link_text('工作区').click()

        # 进行判定删除的分析设计是否还存在
        logger.info('行判定删除的分析设计是否还存在')
        asserts = self.asserts('//p[text()={}]'.format(name))

        # 断言
        if asserts:
            return False
        else:
            return True

    # 创建soe数据分析--所有事件
    def add_workspace_soe_data1(self):
        # 点击工程数据分析
        logger.info("点击工程数据分析")
        self.find_element_by_xpath('//*[@id="logo"]/a/h1').click()

        # 刷新界面
        self.fresh_()

        # 点击交互分析
        logger.info('点击交互分析')
        self.move_to_element_(self.find_element('xpath', data['interaction_analysis']))
        self.click_()

        # 点击工作区
        logger.info('点击工作区')
        self.find_element_by_link_text('工作区').click()

        # 点击搜索框输入分析名
        logger.info('输入分析名：jing.huang_soe分析设计_所有事件')
        self.find_element('xpath',
                          '//*[@id="root"]/div/section/section/section/main/div/div[1]/div[2]/input').send_keys(
            'jing.huang_soe分析设计_所有事件')

        # 点击搜索
        logger.info('点击搜索')
        self.move_to_element_(self.find_element_by_xpath(data['confirm1']))
        self.click_()

        # 判定是否有名为“jing.huang_soe分析设计_所有事件”的设计
        logger.info('判定是否有jing.huang_soe分析设计_所有事件')
        asserts = self.asserts('//p[text()="jing.huang_soe分析设计_所有事件"]')

        # 如果“jing.huang_soe分析设计_所有事件”已存在
        if asserts:
            logger.info('删除jing.huang_soe分析设计_所有事件')
            self.delete_my_analysis(name="jing.huang_soe分析设计_所有事件")

            logger.info('重调用创建jing.huang_soe分析设计_所有事件')
            asserts = self.add_workspace_soe_data1()
            return asserts

        # 如果“jing.huang_soe分析设计_所有事件”不存在
        else:
            # 点击创建我的分析
            logger.info('点击创建我的分析')
            self.find_element('xpath', data['create_analysis']).click()

            # 点击分析名称栏
            logger.info('点击分析名称栏')
            self.move_to_element_(self.find_element_by_xpath('//*[@id="analysisName"]'))

            # 清空默认分析名
            logger.info('清空分析名')
            self.find_element_by_xpath('//*[@id="analysisName"]').clear()

            # 输入分析名
            logger.info('输入分析名：jing.huang_soe分析设计_所有事件')
            self.find_element_by_xpath('//*[@id="analysisName"]').send_keys('jing.huang_soe分析设计_所有事件')

            # 点击确定
            logger.info('点击确定')
            self.move_to_element_(self.find_element_by_xpath(data['confirm']))
            self.click_()

            # 点击添加数据集“+”号
            logger.info("点击数据集“+”号按钮")
            self.move_to_element_(self.find_element_by_xpath('//i[@aria-label="图标: plus"]'))
            self.click_()

            # 点击数据集名称并清空数据集名
            logger.info('清空数据集名')
            self.find_element('id', "dataName").clear()

            # 输入新的数据集名称--测试SOE数据
            logger.info('输入新数据集名：测试SOE数据_所有数据')
            self.find_element('id', "dataName").send_keys("测试SOE数据_所有事件")

            # 点击数据源类型框
            logger.info('点击数据源选择框')
            self.find_element('id', "dataSourceType").click()

            # 选择数据源--事件数据
            logger.info('点击事件数据')
            self.find_element_by_xpath("//li[text()='事件数据']").click()

            # 点击风场选择框
            logger.info('点击风场选择框')
            self.find_element_by_id("windField").click()

            # 选择风场--点击快速过滤
            logger.info('点击快速过滤')
            self.move_to_element_(self.find_element_by_xpath('//span[text()="快速过滤"]'))
            self.click_()

            # 选择输入框输入风场CN号
            logger.info('输入风场：CN-03/02')
            self.find_element('id', "cnNumber").send_keys('CN-03/02')

            # 点击确定按钮
            logger.info('点击确定按钮')
            self.move_to_element_(self.find_element_by_xpath('//div[3]/div/button[2]/span[text()="确 定"]'))
            self.click_()

            logger.info('再次点击确定按钮')
            self.move_to_element_(self.find_element_by_xpath('//span[text()="确 定"]'))
            self.click_()

            # 点击风机选择框
            logger.info('点击风机选择框')
            self.move_to_element_(self.find_element_by_id("turbine"))
            self.click_()

            # 点击选择风机--详细维度过滤
            logger.info('点击风机详细维度过滤')
            self.move_to_element_(self.find_element_by_xpath('//span[text()="详细维度过滤"]'))
            self.click_()

            # 点击选择风机
            logger.info('点击选择风机')
            self.find_element_by_xpath('//div[@title="SXGL.T1_L1.WTG001"]').click()
            self.find_element_by_xpath('//div[@title="SXGL.T1_L2.WTG024"]').click()
            self.find_element_by_xpath('//div[@title="SXGL.T1_L1.WTG001"]').click()

            # 点击确定
            logger.info('点击风机选择确定按钮')
            self.move_to_element_(self.find_element_by_xpath('//div[2]/div[3]/div/button[2]/span[text()="确 定"]'))
            self.click_()

            # 再次点击确定
            logger.info('点击风机选择框内的确定按钮')
            # time.sleep(100)
            self.move_to_element_(self.find_element_by_xpath(
                                '//form/div/div[1]/div[2]/div[2]/div/span/div[2]/div/div/div/div'
                                '/div[2]/div/button[2]/span[text()="确 定"]'))
            self.click_()

            # 点击时间选择框输入时间范围
            logger.info('输入开始时间')
            self.find_element_by_xpath('//input[@placeholder="开始时间"]').click()

            self.find_element_by_xpath('//div[text()="23"]').click()
            self.find_element_by_xpath('//div[text()="31"]').click()

            # 点击确定
            logger.info('点击日期栏确定按钮')
            self.find_element_by_xpath('//a[text()="确 定"]').click()

            # 点击风机维度框
            self.find_element_by_xpath('//*[@id="timeDimension"]').click()

            # 选择风场风机维度
            self.find_element_by_xpath('//div[text()="风机名"]').click()
            self.find_element_by_xpath('//div[text()="风机主数据ID"]').click()
            self.find_element_by_xpath('//div[text()="USCADA简称"]').click()
            self.find_element_by_xpath('//div[text()="风场名"]').click()

            # 点击维度确定按钮
            logger.info('定位确定按钮')
            # time.sleep(100)
            self.move_to_element_(self.find_element_by_xpath(
                '//form/div/div[1]/div[5]/div[2]/div/span/div[2]/div/div/div/div/div[2]/div/button[2]/span[text()="确 定"]'))
            logger.info('点击确定按钮')
            self.click_()

            # 点击所有事件
            logger.info('点击所有事件')
            self.move_to_element_(self.find_element_by_xpath('//span[text()="所有事件"]'))
            self.click_()

            # 点击编辑数据集确定按钮
            logger.info("点击确认按钮")
            self.move_to_element_(self.find_element_by_xpath('//div/div[2]/div[3]/button[2]/span["确 定"]'))
            self.click_()

            # 判定数据集是否成功创建
            asserts = self.asserts('//span[text()="[SOE]测试SOE数据_所有事件"]')
            return asserts

    # 画出soe表格图
    def add_workspace_soe_data2(self):
        # 点击图元分析
        self.move_to_element_(self.find_element_by_xpath('//span[text()="图元分析"]'))
        self.click_()

        self.drag_and_drop_(self.find_element_by_xpath('//div[text()="Date_Time"]'),
                            self.find_element_by_xpath(
                                '//*[@id="root"]/div/section/section/section/main/div[1]/di'
                                'v[4]/div[2]/div[2]/div/div[3]/div[1]/div/div[2]/div/div/div/div'))

        self.drag_and_drop_(self.find_element_by_xpath('//div[text()="所有事件"]'),
                            self.find_element_by_xpath(
                                '//*[@id="root"]/div/section/section/section/main/div[1]/di'
                                'v[4]/div[2]/div[2]/div/div[3]/div[1]/div/div[3]/div/div/div/div'))

        self.time_sleep('level13')

        # 点击预览按钮
        logger.info("点击预览按钮")
        self.move_to_element_(self.find_element_by_xpath('//i[@aria-label="图标: eye"]'))
        self.click_()

        self.time_sleep('level12')

        '''这里用来判定散点图是否成功创建'''
        # 截图
        self.screen_shot('soe_Table_all_case_model.jpg')
        self.screen_shot('soe_Table_all_case_model_contrast.jpg')

        # img1为模板图片，测试环境因为不会随便添加数据，所以每次截图应该都是一样的
        img1 = BasePage.test_pic_dir + r'soe_Table_all_case_model.jpg'
        img2 = BasePage.test_pic_dir + r'soe_Table_all_case_model_contrast.jpg'

        # 比对两张图片不一致率
        logger.info("比对散点图不一致率")
        result = self.image_compare_(img1, img2)

        # 将本次截图删除
        logger.info("删除比对的SOE图表")
        os.remove(img2)

        # 判定如果本次截图和模板图片相差度是否为0，如果不是0则返回False
        if result == 0:
            return True
        else:
            return False

    # 创建soe数据分析-所有输出Tracelog时间的
    def add_workspace_soe_data3(self):
        # 点击工程数据分析
        logger.info("点击工程数据分析")
        self.find_element_by_xpath('//*[@id="logo"]/a/h1').click()

        # 刷新界面
        self.fresh_()

        # 点击交互分析
        logger.info('点击交互分析')
        self.move_to_element_(self.find_element('xpath', data['interaction_analysis']))
        self.click_()

        # 点击工作区
        logger.info('点击工作区')
        self.find_element_by_link_text('工作区').click()

        # 点击搜索框输入分析名
        logger.info('输入分析名：soe分析设计_所有输出Tracelog的事件')
        self.find_element('xpath',
                          '//*[@id="root"]/div/section/section/section/main/div/div[1]/div[2]/input').send_keys(
            'soe分析设计_所有输出Tracelog的事件')

        # 点击搜索
        logger.info('点击搜索')
        self.move_to_element_(self.find_element_by_xpath(data['confirm1']))
        self.click_()

        # 判定是否有名为“soe分析设计_所有输出Tracelog的事件”的设计
        logger.info('判定是否有soe分析设计_所有输出Tracelog的事件')
        asserts = self.asserts('//p[text()="soe分析设计_所有输出Tracelog的事件"]')

        # 如果“jing.huang_分析设计”已存在
        if asserts:
            logger.info('删除soe分析设计_所有输出Tracelog的事件')
            self.delete_my_analysis(name="soe分析设计_所有输出Tracelog的事件")

            logger.info('重调用创建soe分析设计_所有输出Tracelog的事件')
            asserts = self.add_workspace_soe_data3()
            return asserts

        # 如果“jing.huang_分析设计”不存在
        else:
            # 点击创建我的分析
            logger.info('点击创建我的分析')
            self.find_element('xpath', data['create_analysis']).click()

            # 点击分析名称栏
            logger.info('点击分析名称栏')
            self.move_to_element_(self.find_element_by_xpath('//*[@id="analysisName"]'))

            # 清空默认分析名
            logger.info('清空分析名')
            self.find_element_by_xpath('//*[@id="analysisName"]').clear()

            # 输入分析名
            logger.info('输入分析名：soe分析设计_所有输出Tracelog的事件')
            self.find_element_by_xpath('//*[@id="analysisName"]').send_keys('soe分析设计_所有输出Tracelog的事件')

            # 点击确定
            logger.info('点击确定')
            self.move_to_element_(self.find_element_by_xpath(data['confirm']))
            self.click_()

            # 点击添加数据集“+”号
            logger.info("点击数据集“+”号按钮")
            self.move_to_element_(self.find_element_by_xpath('//i[@aria-label="图标: plus"]'))
            self.click_()

            # 点击数据集名称并清空数据集名
            logger.info('清空数据集名')
            self.find_element('id', "dataName").clear()

            # 输入新的数据集名称--测试SOE数据
            logger.info('输入新数据集名：测试SOE数据_所有输出Tracelog的事件')
            self.find_element('id', "dataName").send_keys("测试SOE数据_所有输出Tracelog的事件")

            # 点击数据源类型框
            logger.info('点击数据源选择框')
            self.find_element('id', "dataSourceType").click()

            # 选择数据源--事件数据
            logger.info('点击事件数据')
            self.find_element_by_xpath("//li[text()='事件数据']").click()

            # 点击风场选择框
            logger.info('点击风场选择框')
            self.find_element_by_id("windField").click()

            # 选择风场--点击快速过滤
            logger.info('点击快速过滤')
            self.move_to_element_(self.find_element_by_xpath('//span[text()="快速过滤"]'))
            self.click_()

            # 选择输入框输入风场CN号
            logger.info('输入风场：CN-03/02')
            self.find_element('id', "cnNumber").send_keys('CN-03/02')

            # 点击确定按钮
            logger.info('点击确定按钮')
            self.move_to_element_(self.find_element_by_xpath('//div[3]/div/button[2]/span[text()="确 定"]'))
            self.click_()

            logger.info('再次点击确定按钮')
            self.move_to_element_(self.find_element_by_xpath('//span[text()="确 定"]'))
            self.click_()

            # 点击风机选择框
            logger.info('点击风机选择框')
            self.move_to_element_(self.find_element_by_id("turbine"))
            self.click_()

            # 点击选择风机--详细维度过滤
            logger.info('点击风机详细维度过滤')
            self.move_to_element_(self.find_element_by_xpath('//span[text()="详细维度过滤"]'))
            self.click_()

            # 点击选择风机
            logger.info('点击选择风机')
            self.find_element_by_xpath('//div[@title="SXGL.T1_L1.WTG001"]').click()
            self.find_element_by_xpath('//div[@title="SXGL.T1_L2.WTG024"]').click()
            self.find_element_by_xpath('//div[@title="SXGL.T1_L1.WTG001"]').click()

            # 点击确定
            logger.info('点击风机选择确定按钮')
            self.move_to_element_(self.find_element_by_xpath('//div[2]/div[3]/div/button[2]/span[text()="确 定"]'))
            self.click_()

            # 再次点击确定
            logger.info('点击风机选择框内的确定按钮')
            self.move_to_element_(self.find_element_by_xpath(
                                '//form/div/div[1]/div[2]/div[2]/div/span/div[2]/div/div/div/div'
                                '/div[2]/div/button[2]/span[text()="确 定"]'))
            self.click_()

            # 点击时间选择框输入时间范围
            logger.info('输入开始时间')
            self.find_element_by_xpath('//input[@placeholder="开始时间"]').click()

            self.find_element_by_xpath('//div[text()="23"]').click()
            self.find_element_by_xpath('//div[text()="31"]').click()

            # 点击确定
            logger.info('点击日期栏确定按钮')
            self.find_element_by_xpath('//a[text()="确 定"]').click()

            # 点击风机维度框
            self.find_element_by_xpath('//*[@id="timeDimension"]').click()

            # 选择风场风机维度
            self.find_element_by_xpath('//div[text()="风机名"]').click()
            self.find_element_by_xpath('//div[text()="风机主数据ID"]').click()
            self.find_element_by_xpath('//div[text()="USCADA简称"]').click()
            self.find_element_by_xpath('//div[text()="风场名"]').click()

            # 点击维度确定按钮
            logger.info('定位确定按钮')
            self.move_to_element_(self.find_element_by_xpath(
                '//form/div/div[1]/div[5]/div[2]/div/span/div[2]/div/div/div/div/div[2]'
                '/div/button[2]/span[text()="确 定"]'))
            logger.info('点击确定按钮')
            self.click_()

            # 点击所有事件
            logger.info('所有输出Tracelog的事件')
            self.move_to_element_(self.find_element_by_xpath('//span[text()="所有输出Tracelog的事件"]'))
            self.click_()

            # 点击编辑数据集确定按钮
            logger.info("点击确认按钮")
            self.move_to_element_(self.find_element_by_xpath('//div/div[2]/div[3]/button[2]/span["确 定"]'))
            self.click_()

            # 判定数据集是否成功创建
            asserts = self.asserts('//span[text()="[SOE]测试SOE数据_所有输出Tracelog的事件"]')
            return asserts

    # 画出soe表格图
    def add_workspace_soe_data4(self):
        # 点击图元分析
        self.move_to_element_(self.find_element_by_xpath('//span[text()="图元分析"]'))
        self.click_()

        self.drag_and_drop_(self.find_element_by_xpath('//div[text()="Date_Time"]'),
                            self.find_element_by_xpath(
                                '//*[@id="root"]/div/section/section/section/main/div[1]/di'
                                'v[4]/div[2]/div[2]/div/div[3]/div[1]/div/div[2]/div/div/div/div'))

        self.drag_and_drop_(self.find_element_by_xpath('//div[text()="所有输出Tracelog的事件"]'),
                            self.find_element_by_xpath(
                                '//*[@id="root"]/div/section/section/section/main/div[1]/di'
                                'v[4]/div[2]/div[2]/div/div[3]/div[1]/div/div[3]/div/div/div/div'))

        self.time_sleep('level13')

        # 点击预览按钮
        logger.info("点击预览按钮")
        self.move_to_element_(self.find_element_by_xpath('//i[@aria-label="图标: eye"]'))
        self.click_()

        self.time_sleep('level12')

        '''这里用来判定散点图是否成功创建'''
        # 截图
        self.screen_shot('soe_Table_all_tracelog_case_model.jpg')
        self.screen_shot('soe_Table_all_tracelog_case_model_contrast.jpg')

        # img1为模板图片，测试环境因为不会随便添加数据，所以每次截图应该都是一样的
        img1 = BasePage.test_pic_dir + r'soe_Table_all_tracelog_case_model.jpg'
        img2 = BasePage.test_pic_dir + r'soe_Table_all_tracelog_case_model_contrast.jpg'

        # 比对两张图片不一致率
        logger.info("比对soe图表不一致率")
        result = self.image_compare_(img1, img2)

        # 将本次截图删除
        logger.info("删除比对的soe图表")
        os.remove(img2)

        # 判定如果本次截图和模板图片相差度是否为0，如果不是0则返回False
        if result == 0:
            return True
        else:
            return False

    # 创建soe数据分析-自定义
    def add_workspace_soe_data5(self):
        # 点击工程数据分析
        logger.info("点击工程数据分析")
        self.find_element_by_xpath('//*[@id="logo"]/a/h1').click()

        # 刷新界面
        self.fresh_()

        # 点击交互分析
        logger.info('点击交互分析')
        self.move_to_element_(self.find_element('xpath', data['interaction_analysis']))
        self.click_()

        # 点击工作区
        logger.info('点击工作区')
        self.find_element_by_link_text('工作区').click()

        # 点击搜索框输入分析名
        logger.info('输入分析名：soe分析设计_自定义')
        self.find_element('xpath',
                          '//*[@id="root"]/div/section/section/section/main/div/div[1]/div[2]/input').send_keys(
            'soe分析设计_自定义')

        # 点击搜索
        logger.info('点击搜索')
        self.move_to_element_(self.find_element_by_xpath(data['confirm1']))
        self.click_()

        # 判定是否有名为“soe分析设计_自定义”的设计
        logger.info('判定是否有soe分析设计_自定义')
        asserts = self.asserts('//p[text()="soe分析设计_自定义"]')

        # 如果“jing.huang_分析设计”已存在
        if asserts:
            logger.info('删除soe分析设计_自定义')
            self.delete_my_analysis(name="soe分析设计_自定义")

            logger.info('重调用创建soe分析设计_自定义')
            asserts = self.add_workspace_soe_data5()
            return asserts

        # 如果“soe分析设计_自定义”不存在
        else:
            # 点击创建我的分析
            logger.info('点击创建我的分析')
            self.find_element('xpath', data['create_analysis']).click()

            # 点击分析名称栏
            logger.info('点击分析名称栏')
            self.move_to_element_(self.find_element_by_xpath('//*[@id="analysisName"]'))

            # 清空默认分析名
            logger.info('清空分析名')
            self.find_element_by_xpath('//*[@id="analysisName"]').clear()

            # 输入分析名
            logger.info('输入分析名：soe分析设计_自定义')
            self.find_element_by_xpath('//*[@id="analysisName"]').send_keys('soe分析设计_自定义')

            # 点击确定
            logger.info('点击确定')
            self.move_to_element_(self.find_element_by_xpath(data['confirm']))
            self.click_()

            # 点击添加数据集“+”号
            logger.info("点击数据集“+”号按钮")
            self.move_to_element_(self.find_element_by_xpath('//i[@aria-label="图标: plus"]'))
            self.click_()

            # 点击数据集名称并清空数据集名
            logger.info('清空数据集名')
            self.find_element('id', "dataName").clear()

            # 输入新的数据集名称--测试SOE数据_自定义
            logger.info('输入新数据集名：测试SOE数据_自定义')
            self.find_element('id', "dataName").send_keys("测试SOE数据_自定义")

            # 点击数据源类型框
            logger.info('点击数据源选择框')
            self.find_element('id', "dataSourceType").click()

            # 选择数据源--事件数据
            logger.info('点击事件数据')
            self.find_element_by_xpath("//li[text()='事件数据']").click()

            # 点击风场选择框
            logger.info('点击风场选择框')
            self.find_element_by_id("windField").click()

            # 选择风场--点击快速过滤
            logger.info('点击快速过滤')
            self.move_to_element_(self.find_element_by_xpath('//span[text()="快速过滤"]'))
            self.click_()

            # 选择输入框输入风场CN号
            logger.info('输入风场：CN-03/02')
            self.find_element('id', "cnNumber").send_keys('CN-03/02')

            # 点击确定按钮
            logger.info('点击确定按钮')
            self.move_to_element_(self.find_element_by_xpath('//div[3]/div/button[2]/span[text()="确 定"]'))
            self.click_()

            logger.info('再次点击确定按钮')
            self.move_to_element_(self.find_element_by_xpath('//span[text()="确 定"]'))
            self.click_()

            # 点击风机选择框
            logger.info('点击风机选择框')
            self.move_to_element_(self.find_element_by_id("turbine"))
            self.click_()

            # 点击选择风机--详细维度过滤
            logger.info('点击风机详细维度过滤')
            self.move_to_element_(self.find_element_by_xpath('//span[text()="详细维度过滤"]'))
            self.click_()

            # 点击选择风机
            logger.info('点击选择风机')
            self.find_element_by_xpath('//div[@title="SXGL.T1_L1.WTG001"]').click()
            self.find_element_by_xpath('//div[@title="SXGL.T1_L2.WTG024"]').click()
            self.find_element_by_xpath('//div[@title="SXGL.T1_L1.WTG001"]').click()

            # 点击确定
            logger.info('点击风机选择确定按钮')
            self.move_to_element_(self.find_element_by_xpath('//div[2]/div[3]/div/button[2]/span[text()="确 定"]'))
            self.click_()

            # 再次点击确定
            logger.info('点击风机选择框内的确定按钮')
            self.move_to_element_(self.find_element_by_xpath(
                                '//form/div/div[1]/div[2]/div[2]/div/span/div[2]/div/div/div/div'
                                '/div[2]/div/button[2]/span[text()="确 定"]'))
            self.click_()

            # 点击时间选择框输入时间范围
            logger.info('输入开始时间')
            self.find_element_by_xpath('//input[@placeholder="开始时间"]').click()

            self.find_element_by_xpath('//div[text()="23"]').click()
            self.find_element_by_xpath('//div[text()="31"]').click()

            # 点击确定
            logger.info('点击日期栏确定按钮')
            self.find_element_by_xpath('//a[text()="确 定"]').click()

            # 点击风机维度框
            self.find_element_by_xpath('//*[@id="timeDimension"]').click()

            # 选择风场风机维度
            self.find_element_by_xpath('//div[text()="风机名"]').click()
            self.find_element_by_xpath('//div[text()="风机主数据ID"]').click()
            self.find_element_by_xpath('//div[text()="USCADA简称"]').click()
            self.find_element_by_xpath('//div[text()="风场名"]').click()

            # 点击维度确定按钮
            logger.info('定位确定按钮')
            self.move_to_element_(self.find_element_by_xpath(
                '//form/div/div[1]/div[5]/div[2]/div/span/div[2]/div/div/div/div/div[2]/div/button[2]/span[text()="确 定"]'))
            logger.info('点击确定按钮')
            self.click_()

            # 这里选择对应的数据信息
            # # 点击添加通道
            # logger.info('点击添加对应通道')
            # self.move_to_element_(self.find_element_by_xpath('//div[text()="叶根1Mxy弯矩LDD分布"]'))
            # self.click_()
            #
            # self.move_to_element_(self.find_element_by_xpath('//div[@title="叶根2Mxy弯矩LDD分布"]'))
            # self.click_()
            #
            # self.move_to_element_(self.find_element_by_xpath('//div[@title="叶根3Mxy弯矩LDD分布"]'))
            # self.click_()
            #
            # self.move_to_element_(self.find_element_by_xpath('//div[@title="轮毂中心My(旋转坐标系)的M10等效疲劳"]'))
            # self.click_()
            #
            # self.move_to_element_(self.find_element_by_xpath('//div[@title="轮毂中心My(静止坐标系)的M10原始等效疲劳"]'))
            # self.click_()

            # 点击添加按钮
            # logger.info("点击添加按钮")
            # self.move_to_element_(self.find_element_by_xpath('//span[text()="添 加"]'))
            # self.click_()

            # 点击编辑数据集确定按钮
            logger.info("点击确认按钮")
            self.move_to_element_(self.find_element_by_xpath('//div/div[2]/div[3]/button[2]/span["确 定"]'))
            self.click_()

            # 判定数据集是否成功创建
            asserts = self.asserts('//span[text()="[SOE]soe分析设计_自定义"]')
            return asserts

    # 画出soe表格图
    def add_workspace_soe_data6(self):
        # 点击图元分析
        self.move_to_element_(self.find_element_by_xpath('//span[text()="图元分析"]'))
        self.click_()

        self.drag_and_drop_(self.find_element_by_xpath('//div[text()="Date_Time"]'),
                            self.find_element_by_xpath(
                                '//*[@id="root"]/div/section/section/section/main/div[1]/di'
                                'v[4]/div[2]/div[2]/div/div[3]/div[1]/div/div[2]/div/div/div/div'))

        self.drag_and_drop_(self.find_element_by_xpath('//div[text()="所有选择的事件"]'),
                            self.find_element_by_xpath(
                                '//*[@id="root"]/div/section/section/section/main/div[1]/di'
                                'v[4]/div[2]/div[2]/div/div[3]/div[1]/div/div[3]/div/div/div/div'))

        self.time_sleep('level13')

        # 点击预览按钮
        logger.info("点击预览按钮")
        self.move_to_element_(self.find_element_by_xpath('//i[@aria-label="图标: eye"]'))
        self.click_()

        self.time_sleep('level12')

        '''这里用来判定散点图是否成功创建'''
        # 截图
        self.screen_shot('soe_Table_all_tracelog_case_model.jpg')
        self.screen_shot('soe_Table_all_tracelog_case_model_contrast.jpg')

        # img1为模板图片，测试环境因为不会随便添加数据，所以每次截图应该都是一样的
        img1 = BasePage.test_pic_dir + r'soe_Table_all_tracelog_case_model.jpg'
        img2 = BasePage.test_pic_dir + r'soe_Table_all_tracelog_case_model_contrast.jpg'

        # 比对两张图片不一致率
        logger.info("比对soe图表不一致率")
        result = self.image_compare_(img1, img2)

        # 将本次截图删除
        logger.info("删除比对的soe图表")
        os.remove(img2)

        # 判定如果本次截图和模板图片相差度是否为0，如果不是0则返回False
        if result == 0:
            return True
        else:
            return False
