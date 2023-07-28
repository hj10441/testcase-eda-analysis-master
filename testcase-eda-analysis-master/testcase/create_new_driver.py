# -*-coding:utf-8-*-
import time
from selenium import webdriver


class newDriverObject(object):
    def __init__(self):
        try:
            option = webdriver.ChromeOptions()
            # option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
            option.add_argument('-ignore-certificate-errors')
            option.add_argument('-ignore -ssl-errors')
            self.driver = webdriver.Chrome(options=option, executable_path=r"C:\Users\jing.huang6\PycharmProjects\pythonProject\venv\Scripts\chromedriver.exe")
        except Exception as e:
            print(e)
        time.sleep(0.5)

    def driver_return(self):
        return self.driver
