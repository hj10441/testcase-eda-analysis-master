# coding=utf-8
'''
Created on 2020-01-19
@author: jackferrous
Project:基础类BasePage，封装所有页面都公用的方法，
定义open函数，重定义find_element，switch_frame，send_keys等函数。
在初始化方法中定义驱动driver，基本url，title
WebDriverWait提供了显式等待方式。
'''
# 修改部分方法，参数的命名
__version__ = "0.2.0"

import csv
import filecmp
import math
import operator
import os
import random
import socket
import sys
import time
import datetime
from functools import reduce
from seletools.actions import drag_and_drop

import win32api
import win32clipboard as w
import win32con
from PIL import Image
from loguru import logger
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from public.public_function import yaml_read
from testcase.create_new_driver import newDriverObject

sys.setrecursionlimit(1000000)

IP__ = socket.gethostbyname(socket.gethostname())


class NoElementException: pass


class FilenameExccept: pass


class NoConfigKeyError: pass


class BasePage(object):
    """
    BasePage封装所有页面都公用的方法，例如driver, url ,FindElement等
    """

    project_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    test_data_dir = project_path + '/testdata'
    # test_pic_dir = project_path + '/screenshot/'
    test_pic_dir = project_path + '/assert_picture/'
    test_api_dir = project_path + '/report/'
    test_excel = '/elementsexpressiondev.xlsx'

    # 初始化driver、url、pagetitle等
    # 实例化BasePage类时，最先执行的就是__init__方法，该方法的入参，其实就是BasePage类的入参。
    # __init__方法不能有返回值，只能返回None
    # self只实例本身，相较于类Page而言。

    def __init__(self, page_title=None):
        self.driver = newDriverObject().driver_return()
        self.datas = yaml_read(yaml_name="/config/config.yml")
        self.page_title = page_title
        self.vk_CODE = {'n': 0x4E, 'i': 0x49, 'm': 0x4D, 'enter': 0x0D, 'ctrl': 0x11, 'a': 0x41, 'v': 0x56, 'x': 0x58,
                        'p': 0x50, 's': 0x53, 'w': 0x57, 'o': 0x4F, 'r': 0x52, 'd': 0x44}
        self.level1 = 0.1
        self.level2 = 0.2
        self.level3 = 0.3
        self.level4 = 0.4
        self.level5 = 0.5
        self.level6 = 0.8
        self.level7 = 1
        self.level8 = 1.2
        self.level9 = 1.5
        self.level10 = 2
        self.level11 = 3
        self.level12 = 4
        self.level13 = 5
        self.level14 = 6
        self.level15 = 8
        self.level16 = 10
        self.level17 = 15
        self.level18 = 600
        '''初始化需要用到的参数'''
        self.elementsExpressionList, self.listParam, self.operationLinks = get_element_and_param_expression()
        # 定位器，通过元素属性定位元素对象
        for elementsExpression in self.elementsExpressionList:
            setattr(self, elementsExpression['expressionname'],
                    (getattr(By, elementsExpression['pattern']), elementsExpression['xpath']))
        for paramExpression in self.listParam:
            setattr(self, paramExpression['paramsname'], paramExpression['value'])
        if hasattr(self, 'urlParam'):
            self.base_url = "https://w3.envision-group.qa.pe2.cc/apps/tq/edas/app/#/"

    # def eda_login(self, account=None, password=None):
    #     """登陆EDA系统"""
    #     # 用户名
    #     self.find_element('id', 'okta-signin-username').click()
    #
    #     # 输入用户名
    #     name = self.find_element("id", 'okta-signin-username')
    #     name.click()
    #     name.clear()
    #     name.send_keys(account)
    #     logger.info(f"input account：{account}")
    #
    #     # 密码
    #     pwd = self.find_element("id", "okta-signin-password")
    #     pwd.click()
    #     pwd.clear()
    #
    #     # 输入密码
    #     pwd.send_keys(password)
    #     logger.info("input password：encrypted key")
    #
    #     # 点击登录
    #     self.find_element("id", "okta-signin-submit").click()
    #
    #     # 查看元素是否存在
    #     asserts = self.asserts("//h1[text()='工程数据分析']", log=True)
    #     return asserts
    def eda_login(self, account=None, password=None):
        """登陆EDA系统"""
        # 用户名
        self.find_element('id', 'loginName').click()

        # 输入用户名
        name = self.find_element("xpath", "//*[@id='loginName']")
        name.click()
        name.clear()
        name.send_keys(account)
        logger.info(f"input account：{account}")

        # 密码
        pwd = self.find_element("xpath", "//*[@id='password']")
        pwd.click()
        pwd.clear()

        # 输入密码
        pwd.send_keys(password)
        logger.info("input password：encrypted key")

        # 取消勾选远景域账户
        # self.find_element("xpath", "//span[text()='远景域登录']").click()

        # 点击登录
        self.find_element("xpath", "//button[contains(@class,'ant-btn')]").click()

        # 查看元素是否存在
        asserts = self.asserts("//h1[text()='工程数据分析']", log=False)
        return asserts

    # 截图
    def get_screenshot_as_png(self):
        return self.driver.get_screenshot_as_png()

    # 元素断言
    def asserts(self, xpath, by="xpath", log=True):
        try:
            self.find_element(by, xpath)
            if log:
                logger.info("assert success")
            return True
        except Exception:
            if log:
                logger.info("assert failed")
            return False

    def windows_copy(self, copyparam):
        i = 0
        while i < 10:
            i += 1
            try:
                self.set_text(copyparam)
                self.get_text()
                self.key_down('ctrl')
                self.key_up('v')
                self.key_down('v')
                self.key_up('ctrl')
                self.key_up('enter')
                self.key_down('enter')
                self.time_sleep('level5')
                break
            except Exception as e:
                logger.info('第[ %d ]次粘贴[ %s ]失败,原因%s' % (i, copyparam, e))
            self.time_sleep('level5')

    def windows_execute(self, execfile):
        i = 0
        while i < 5:
            i += 1
            try:
                os.system(self.exectuePathParam + execfile)
                break
            except Exception:
                pass
        else:
            logger.info('拷贝文件路径失败')

    # 通过title断言进入的页面是否正确。
    # 使用title获取当前窗口title，检查输入的title是否在当前title中，返回比较结果（True 或 False）
    def on_page(self, pagetitle):
        return pagetitle in self.driver.title

    # 打开页面，并校验页面链接是否加载正确
    # 以单下划线_开头的方法，在使用import *时，该方法不会被导入，保证该方法为类私有的。
    def _open(self, url, pagetitle=''):
        # 使用get打开访问链接地址
        self.driver.get(url)
        time.sleep(0.5)
        # 使用assert进行校验，打开的窗口title是否与配置的title一致。调用on_page()方法
        # assert(self.on_page(pagetitle), u"打开开页面失败 %s"%url)

    # 定义open方法，调用_open()进行打开链接
    def open(self, url=''):
        if url == '':
            self._open(self.base_url, self.page_title)
            time.sleep(0.5)
        else:
            self._open(url)
            time.sleep(0.5)

    # 重写元素定位方法
    def find_element(self, *loc, is_highlight=1):
        try:
            # 确保元素是可见的。
            # 注意：以下入参为元组的元素，需要加*。Python存在这种特性，就是将入参放在元组里。
            WebDriverWait(self.driver, 30).until(lambda driver: driver.find_element(*loc).is_displayed())
            logger.info(f"Element success: {loc}")
            # 注意：以下入参本身是元组，不需要加*
            WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located(loc))
            if is_highlight == 1:
                self.highlight(self.driver.find_element(*loc))
            time.sleep(0.5)
            return self.driver.find_element(*loc)
        except Exception:
            logger.info(u"%s 页面中未能找到 %s 元素" % (self, loc))
            return self.driver.find_element(loc)

    # 重写元素定位方法
    def find_element_by_xpath(self, xpath, by="xpath", is_highlight=1):
        try:
            # 确保元素是可见的。
            # 注意：以下入参为元组的元素，需要加*。Python存在这种特性，就是将入参放在元组里。
            WebDriverWait(self.driver, 30).until(lambda driver: driver.find_element(by, xpath).is_displayed())
            logger.info(f"""Element success: ('{by}', "{xpath}")""")
            # 注意：以下入参本身是元组，不需要加*
            WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((by, xpath)))
            if is_highlight == 1:
                self.highlight(self.driver.find_element(by, xpath))
            time.sleep(0.5)
            return self.driver.find_element(by, xpath)
        except Exception as e:
            logger.info(u"""页面中未能找到 ('xpath', '%s') 元素""" % xpath)
            return e

    def find_element_by_id(self, xpath, by="id", is_highlight=1):
        try:
            # 确保元素是可见的。
            # 注意：以下入参为元组的元素，需要加*。Python存在这种特性，就是将入参放在元组里。
            WebDriverWait(self.driver, 30).until(lambda driver: driver.find_element(by, xpath).is_displayed())
            logger.info(f"""Element success: ('{by}', "{xpath}")""")
            # 注意：以下入参本身是元组，不需要加*
            WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((by, xpath)))
            if is_highlight == 1:
                self.highlight(self.driver.find_element(by, xpath))
            time.sleep(0.5)
            return self.driver.find_element(by, xpath)
        except Exception as e:
            logger.info(u"""页面中未能找到 ('xpath', "%s") 元素""" % xpath)
            return e

    def find_element_by_link_text(self, xpath, by="link text", is_highlight=1):
        try:
            # 注意：以下入参为元组的元素，需要加*。Python存在这种特性，就是将入参放在元组里。
            WebDriverWait(self.driver, 30).until(lambda driver: driver.find_element(by, xpath).is_displayed())
            logger.info(f"""Element success: ('{by}', "{xpath}") """)
            # 注意：以下入参本身是元组，不需要加*
            WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((by, xpath)))
            if is_highlight == 1:
                self.highlight(self.driver.find_element(by, xpath))
            time.sleep(0.5)
            return self.driver.find_element(by, xpath)
        except Exception as e:
            logger.info(u"""页面中未能找到 ('xpath', "%s") 元素""" % xpath)
            return e

    def verify_element(self, *loc):
        try:
            self.driver.find_element(*loc)
            return True
        except Exception:
            return False

    def verify_element_abs(self, *loc):
        try:
            self.find_element(*loc)
            return True
        except Exception:
            return False

    def element_invisible(self, *loc, ishighlight=1):
        try:
            # 确保元素是可见的。
            # 注意：以下入参为元组的元素，需要加*。Python存在这种特性，就是将入参放在元组里。
            WebDriverWait(self.driver, 10).until(lambda driver: driver.find_element(*loc).is_displayed())
            # 注意：以下入参本身是元组，不需要加*
            WebDriverWait(self.driver, 10).until_not(EC.visibility_of_element_located(loc))
            time.sleep(0.2)
            return True
        except Exception:
            return False

    def find_elements(self, *loc):
        if self.verify_element(*loc):
            # 确保元素是可见的。
            # 注意：以下入参为元组的元素，需要加*。Python存在这种特性，就是将入参放在元组里。
            WebDriverWait(self.driver, 10).until(lambda driver: driver.find_elements(*loc))
            # 注意：以下入参本身是元组，不需要加*
            self.highlight(self.driver.find_element(*loc))
            time.sleep(0.5)
            return self.driver.find_elements(*loc)
        else:
            return None

    def elements_count(self, *loc):

        els = self.find_elements(*loc)
        if els:
            return len(els)
        else:
            return 0

    # 重写switch_frame方法
    def switch_frame_(self, loc):
        self.driver.switch_to_frame(loc)
        time.sleep(0.2)

    def switch_frame_default_(self):
        self.driver.switch_to_default_content()
        time.sleep(0.2)

    # 定义script方法，用于执行js脚本，返回执行结果
    def script(self, src):
        self.driver.execute_script(src)
        time.sleep(0.2)

    # 重写定义send_keys方法
    def send_keys_(self, loc, value, clear_first=True, click_first=True):
        try:
            loc = getattr(self, "%s" % loc)  # getattr相当于实现self.loc
            if click_first:
                self.find_element(*loc).click()
                self.time_sleep('level3')
            if clear_first:
                self.find_element(*loc).clear()
                self.time_sleep('level3')
                self.find_element(*loc).send_keys(value)
                logger.info(f"Input: {value}")
                self.time_sleep('level7')
        except AttributeError:
            logger.info(u"%s 页面中未能找到 %s 元素" % (self, str(loc)))

    def sendkeys_by_text(self, by, xpath, value):
        """根据文本来输入元素"""
        send_keys_xpath = self.find_element(by, xpath)
        send_keys_xpath.click()
        send_keys_xpath.clear()
        self.time_sleep('level5')
        send_keys_xpath.send_keys(value)
        logger.info(f"输入: {value}")

    def max_window(self):
        self.driver.maximize_window()

    def set_window_size(self, width, height):
        self.driver.set_window_size(width, height)

    def move_to_element_(self, mouse):
        self.highlight(mouse)
        ActionChains(self.driver).move_to_element(mouse).perform()
        self.time_sleep('level1')

    def click_(self):
        ActionChains(self.driver).click().perform()
        self.time_sleep('level1')

    def content_click(self):
        ActionChains(self.driver).context_click().perform()

    def back_(self):
        self.driver.back()
        logger.info("back")

    def fresh_(self):
        self.driver.refresh()
        logger.info("refresh the page")

    def get_handle_(self):
        return self.driver.current_window_handle

    def enter_to_window_(self, window_):
        self.driver.switch_to_window(window_)

    def close_driver(self):
        return self.driver.close()

    def move_by_offset_(self, x, y):
        return ActionChains(self.driver).move_by_offset(x, y)

    def send_key_direct(self, keys):
        try:

            ActionChains(self.driver).send_keys(keys).perform()
            logger.info(f"输入: {keys}")
        except Exception:
            logger.info("error")

    @staticmethod
    def get_file_size(filepath):
        return os.path.getsize(filepath)

    @staticmethod
    def selected_by_text(element_, text_):
        # 操作下拉框，按文本选择
        Select(element_).select_by_visible_text(text_)
        time.sleep(0.8)

    @staticmethod
    def selected_by_index(element_, index_):
        # 操作下拉框，按索引选择
        Select(element_).select_by_index(index_)
        time.sleep(0.5)

    @staticmethod
    def selected_by_value(element_, value_):
        # 操作下拉框，按值选择
        Select(element_).select_by_value(value_)
        time.sleep(0.5)

    def click_ok(self):
        if self.verify_element(*self.stateCurveOKLoc):
            self.find_element(*self.stateCurveOKLoc).click()
            self.time_sleep('level3')

    # 拖动
    def dragger_(self, x, ele=None):
        try:
            self.move_to_element_(ele)
            for i in range(x):
                ActionChains(self.driver).click_and_hold().perform()
                time.sleep(0.2)
                ActionChains(self.driver).move_by_offset(100, -10).perform()
                time.sleep(0.2)
                ActionChains(self.driver).release().perform()
                time.sleep(0.2)
        except:
            raise

    # 将一个元素拖到另一个位置
    def dragpageelement(self, ele1, ele2):
        try:
            logger.info("移动开始")
            ActionChains(self.driver).drag_and_drop(ele1, ele2).perform()
            logger.info('移动成功')

        except Exception as e:
            logger.info("拖拽元素失败")
            raise e

    # 黄竞-解决元素拖拽失败问题：{dragpageelement}方法由于库的设计者问题有时还会失败，但是开发者提供了新的方法
    def drag_and_drop_(self, ele1, ele2):
        try:
            logger.info('拖拽开始')
            drag_and_drop(self.driver, ele1, ele2)
            logger.info('拖拽结束')
            self.time_sleep('level1')
        except Exception as e:
            logger.info("拖曳失败")
            raise e

    def get_all_handles_(self):
        return self.driver.window_handles

    # 截图
    def screen_shot(self, picturename):
        # 截图只传文件名，文件路径写在配置或者全局变量，入口统一
        self.driver.save_screenshot(BasePage.test_pic_dir + picturename)

    def picture_shot(self, picturename, picture2name, *loc):
        im = Image.open(BasePage.test_pic_dir + picturename)
        im = im.crop(*loc)  # 截取图片
        im.save(BasePage.test_pic_dir + picture2name)

    def highlight(self, element):
        """
        元素高亮显示
        :param element: 元素对象
        :return: 无
        """
        self.driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element,
                                   "border: 2px solid red;")

    # 对比两张图片的相似度
    @staticmethod
    def image_compare_(img1='', img2=''):
        result = 9999999
        try:
            image1 = Image.open(img1)
            image2 = Image.open(img2)
            h1 = image1.histogram()
            h2 = image2.histogram()
            result = math.sqrt(reduce(operator.add, list(map(lambda one, two: (one - two) ** 2, h1, h2))) / len(h1))
        except Exception as e:
            logger.info(e)
            raise
        finally:
            logger.info('{},{}相差度:{}'.format(img1, img2, result))
        return result

    # 对比两张图片的相似度是否一致
    @staticmethod
    def image_comparison(img_one, img_two):
        t1 = Image.open(img_one)
        t2 = Image.open(img_two)
        result = operator.eq(t1, t2)
        if os.path.exists(img_one):
            os.remove(img_one)
        if os.path.exists(img_two):
            os.remove(img_two)
        return result

    # 获取alter提示内容
    def get_alter_text(self):
        return self.driver.switch_to.alert.text

    def alter_accept(self):
        self.driver.switch_to.alert.accept()

    # 校验两个文件中，数据是否一样，传带校验文件的路径
    # 检验两个文件是否一样
    @staticmethod
    def check_file(fp1, fp2):
        if fp1.__str__() and fp2.__str__():
            try:
                return filecmp.cmp(fp1, fp2)
            except Exception as e:
                logger.info(e)
                raise
        else:
            logger.info("FileName is error 文件名不对")

    # 校验文件是否新下载,若下载，返回最新下载文件的文件名,传文件路径，文件检验名
    @staticmethod
    def check_new_file(filepath, filekey):
        dirlist = os.listdir(filepath)
        if not dirlist:
            return
        else:
            dirlist = sorted(dirlist, key=lambda x: os.path.getmtime(os.path.join(filepath, x)), reverse=True)
            for file in dirlist:
                if filekey in file:
                    logger.info('校验通过的file:', file)
                    # createdTime = time.strftime('%Y%m%d%H%M',time.localtime(os.stat(file).st_ctime))
                    # now = time.strftime('%Y%m%d%H%M')
                    # if abs(int(now) - int(createdTime)) < 10:
                    return "{}//{}".format(filepath, file)

    # 获取配置文件中指定的参数
    def get_config(self, section, key):
        import configparser
        # 地址需要变更
        if BasePage.test_data_dir not in sys.path:
            sys.path.append(BasePage.test_data_dir)
        conf = configparser.ConfigParser()
        conf.read("{}//disconf.ini".format(BasePage.test_data_dir), encoding="utf-8-sig")
        # logger.info('path:',sys.path())
        s = conf.options(section)
        # logger.info('section:', section, s)
        if key.lower() in s:
            # logger.info(key)
            value = conf.get(section, key)
        # logger.info(value)
        else:
            logger.info("no KEY NAMED %s in SECTION--%s in FILE disconf.ini" % (key, section))
        return value

    def set_config(self, section, name, value):
        import configparser
        # 地址需要变更
        if BasePage.test_data_dir not in sys.path:
            sys.path.append(BasePage.test_data_dir)
        conf = configparser.ConfigParser()
        # logger.info(test_api_path)
        conf.read('{}//disconf.ini'.format(BasePage.test_data_dir), encoding="utf-8-sig")
        conf.set(section, name, value)
        f = open('{}//disconf.ini'.format(BasePage.test_data_dir), 'r+', encoding="utf-8-sig")
        conf.write(f)
        f.close()

    def create_no(self, range_type=3):
        if range_type == 1:
            time_string = str(time.strftime("%Y%m%d%H%M%S"))
        elif range_type == 2:
            time_string = str(time.strftime("%Y-%m-%d"))
        elif range_type == 3:
            time_string = str(time.strftime("%m%d%H%M%S")) + str(random.randint(10, 99))
        elif range_type == 4:
            time_string = str(time.strftime("%Y%m%d"))
        else:
            time_string = "NoRangeType0"
        return time_string

    def time_sleep(self, level):
        time.sleep(getattr(self, level))

    def get_text(self):
        '''获取剪切板'''
        d = ""
        i = 0
        while i < 5:
            i += 1
            try:
                self.time_sleep('level2')
                w.OpenClipboard()
                d = w.GetClipboardData(win32con.CF_TEXT)
                w.CloseClipboard()
                break
            except Exception:
                pass
        return d

    def set_text(self, as_tring):
        '''设置剪切板'''
        i = 0
        while i < 5:
            i += 1
            try:
                self.time_sleep('level2')
                w.OpenClipboard()
                w.EmptyClipboard()
                w.SetClipboardData(win32con.CF_UNICODETEXT, as_tring)
                w.CloseClipboard()
                break
            except Exception:
                pass

    def key_down(self, key_name):
        '''键盘按下'''
        win32api.keybd_event(self.vk_CODE[key_name], 0, 0, 0)

    def key_up(self, key_name):
        '''键盘抬起'''
        win32api.keybd_event(self.vk_CODE[key_name], 0, win32con.KEYEVENTF_KEYUP, 0)

    def get_page_source(self):
        '''获取页面的源码'''
        return self.driver.page_source

    @staticmethod
    def get_excel_valve_by_cell(fileexcel, sheet_name, x, y):
        import xlrd
        return xlrd.open_workbook(fileexcel).sheet_by_name(sheet_name).cell_value(x, y)

    # 父级选择框
    def select_father(self, element_, param_):
        '''传入数据依次为下拉框的定位和选项值'''
        # 不做异常判断，如果异常直接返给上一级
        selectelement = self.find_element(*element_)
        self.selected_by_text(selectelement, param_)

    def select_father_by_value(self, element_, param_):
        '''传入数据依次为下拉框的定位和选项值'''
        # 不做异常判断，如果异常直接返给上一级
        selectelement = self.find_element(*element_)
        self.selected_by_value(selectelement, param_)

    def select_children(self, element_, xpath_, param_, element2=None):
        '''子级下拉框，传入数据依次为元素定位器，xpath表达式，选项值'''
        # element2为空白处点击的元素
        if len(param_) == 0:
            logger.info("error")
        else:
            self.find_element(*element_).click()
            self.time_sleep('level5')
            self.find_element(*('xpath', xpath_.format(param_))).click()
            self.time_sleep('level5')
        if element2 is not None:
            # 点击空白部分让选项框消失
            self.find_element(*element2).click()
            self.time_sleep('level5')

    def select_date(self, yy, mm, dd, element):
        '''选择时间，尽量可以复用'''
        # yy-年，四位数字 mm-月，1-12 dd-日，1-28(这边限制到28号)
        if isinstance(yy, int) and isinstance(mm, int) and isinstance(mm,
                                                                      int) and 1999 < yy < 2899 and 0 < mm < 13 and 0 < dd < 32:
            self.find_element(*element).click()
            self.time_sleep('level10')
            # 默认的选择框
            self.switch_frame_(self.find_element(*self.dateIFrameLoc))
            # 选择时间脚本是默认的
            self.script(self.timeScriptParam.format(yy, mm, dd))
            self.time_sleep('level5')
            self.switch_frame_default_()
            self.time_sleep('level5')
        else:
            raise TypeError("传入数据类型错误")

    def select_start_date(self, loc):
        '''时间取250天之前的数据'''
        now_ = datetime.datetime.now()
        one_year_ago_ = datetime.timedelta(days=350)
        one_year_ago = now_ - one_year_ago_
        self.select_date(one_year_ago.year, one_year_ago.month, one_year_ago.day, loc)

    def select_end_date(self, loc):
        self.select_date(int(time.strftime("%Y")), int(time.strftime("%m")), int(time.strftime("%d")), loc)

    def get_data_count(self, *loc):
        self.time_sleep('level5')
        text_ = self.find_element(*loc).text or '共0条'
        # logger.info(text_)
        return int(self.get_pattern_text(text_, '共(.*?)条')[0].replace(' ', ''))

    @staticmethod
    def check_time_with_now(endtime="", starttime=""):
        '''校验时间和现在时间差几秒'''
        # 返回结果是秒,第二个参数不穿默认是和当前时间做对比
        import re
        matchpattern = "[\d]{4}-[\d]{1,2}-[\d]{1,2} [\d]{1,2}:[\d]{1,2}:[\d]{1,2}"
        datetime = __import__('datetime')
        date = __import__('time')
        endtime = len(endtime) > 0 and endtime or date.strftime('%Y-%m-%d %H:%M:%S')
        starttime = len(starttime) > 0 and starttime or date.strftime('%Y-%m-%d %H:%M:%S')
        # 时间格式：2020-01-20 15:42:18
        if re.match(matchpattern, endtime) != None or re.match(matchpattern, starttime) != None:
            d1 = datetime.datetime.strptime(endtime, "%Y-%m-%d %H:%M:%S")
            d2 = datetime.datetime.strptime(starttime, "%Y-%m-%d %H:%M:%S")
            # logger.info("[DEBUG]:",(d2 - d1).seconds)
            return (d2 - d1).seconds
        else:
            return

    def get_start_and_end_time(self, startelement, endelement):
        '''获取开始时间和结束时间'''
        # 参数分别为：开始时间定位的参数名，结束时间定位的参数名
        starttime = self.find_element(*getattr(self, startelement)).get_attribute('textContent')
        endtime = self.find_element(*getattr(self, endelement)).get_attribute('textContent')
        return starttime, endtime

    @staticmethod
    def get_pattern_text(text_, pattern_):
        import re
        result = re.findall(pattern_, text_)
        if isinstance(result, list):
            if len(result) > 0:
                return result
        else:
            return None

    # selenium_driver.quit()


def get_element_and_param_expression():
    '''读取元素数据'''
    # 需要初始化并最终返回的参数，建议在开头定义
    import xlrd
    list_expression = []
    list_param = []
    operation_links = []
    # logger.info(BasePage.test_data_dir + BasePage.test_excel)
    data = xlrd.open_workbook(BasePage.test_data_dir + BasePage.test_excel)
    tablelist = [data.sheet_by_name('Expression'), data.sheet_by_name('Param'), data.sheet_by_name('Operationlinks')]
    # 获取总行数、总列数
    for i, table in enumerate(tablelist):
        nrows = table.nrows
        ncols = table.ncols
        if nrows > 1:
            # 获取第一列的内容，列表格式
            keys = table.row_values(0)
            # logger.info(keys)
            # 获取每一行的内容，列表格式
            for col in range(1, nrows):
                values = table.row_values(col)
                # keys，values这两个列表一一对应来组合转换为字典
                api_dict = dict(zip(keys, values))
                # logger.info(api_dict)
                if i == 0:
                    list_expression.append(api_dict)
                elif i == 1:
                    list_param.append(api_dict)
                elif i == 2:
                    operation_links.append(api_dict)
        else:
            # logger.info("表格未填写数据")
            pass
    return list_expression, list_param, operation_links


def readfile(filename):
    """
    以列表形式读
    :param filename:
    :return:
    """
    with open(filename, 'r', encoding="utf8") as c:
        reader = csv.reader(c)
        # reader是一个可迭代对象
        csv_list = [item for item in reader]
        return csv_list[1]


if __name__ == '__main__':
    BasePage().image_compare_(img1=r'D:\Xiangmu\test_cms\testcase-cms\public\1.png',
                              img2=r'D:\Xiangmu\test_cms\testcase-cms\public\2.png')
