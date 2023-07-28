import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

option = webdriver.ChromeOptions()
from dbiz_autotest_sdk.encrypt import decrypt


def fun(xpath, by="xpath", log=True):
    try:
        driver.find_element(by, xpath)
        return True
    except Exception:
        return False

# user_pwd = decrypt(public_key='0NYSbFH_qXqWPHGyVYbhR_PHSi-b9R25svs-HXQ-wo4=',
#     encryped_pwd='gAAAAABhsGDSeUT7gyKRrjWFDR5sDw6gC7wWi82LWc_KlqcMQkAXVMJ2pvNyotqOa_ob28j7VhBrpNW-bBvwC_8SbVN8RhdApw==')
#
# user_pwd2 = decrypt(public_key='3ut3lU_qt7qYWLSA7ozVeKxbrTnDYvNfbLfef4D7wjk=',
#     encryped_pwd='gAAAAABhrzUGg9jR_GIhbUP5DJZfSFdCBlQ1OlCS_BcfU2Nl2nI91jwdaZFHBznH8_nkgMGFdWNLMTmuXUVix_o-Ejz2YSAkNw==')
# mysql_pwd = decrypt(public_key='p2rrY13HJjzCRqASOiORikKUOGXVtnWKOfrcWPFl5iI=',
#     encryped_pwd='gAAAAABhlMj034gqGsKMTXsw7fvYbT5MDni7ggwZKOGjHFqLLMD968GOa3Rqr5LubdUWBTkOPyD5ebFfR637EKOlWjOWVnGZyg==')
#
#
# print(user_pwd, user_pwd2)

driver = webdriver.Chrome(
    executable_path=r"C:\Users\jing.huang6\PycharmProjects\pythonProject\venv\Scripts\chromedriver.exe")

# driver.implicitly_wait(10)
# driver.get('chrome://setting/clearBrowserData')
# time.sleep(20)
# clearBujtton = driver.execute_script('return document.querySelector("settings-ui").shadowRoot.querySelector("setting-main").shadowRoot.querySelector("setting-basic-page").shadowRoot.querySelector("setting-section > setting-privacy-page").shadowRoot.querySelector("setting-basic-page")')
#


driver.get("https://w3.envision-group.qa.pe2.cc/apps/tq/edas/app/#/User/Login")
time.sleep(3)
driver.refresh()
driver.maximize_window()
time.sleep(3)
name = driver.find_element('id', 'loginName')
name.click()
name.clear()
name.send_keys('autotest.eda')
pwd = driver.find_element('id', 'password')
pwd.click()
pwd.clear()
pwd.send_keys('kiBGbMtW8S')
try:
    driver.find_element('xpath', '//span[text()="远景域账户"]')
    assert1 = True
except Exception:
    assert1 = False

if assert1:
    driver.find_element_by_xpath('//span[text()="远景域账户"]').click()

driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div[2]/div/div/form/div[3]/div/div/span/button').click()


# # 点击交互分析
# moer = driver.find_element_by_link_text('交互分析')
# ActionChains(driver).move_to_element(moer).perform()
# # 点击工作区
# driver.find_element_by_link_text('工作区').click()
#
# # 点击创建我的分析
#
# driver.find_element_by_link_text('创建我的分析').click()

# 点击分析名称栏
# self.move_to_element_(self.find_element_by_xpath('//*[@id="analysisName"]'))
# self.find_element_by_xpath('//*[@id="analysisName"]').clear()
# self.find_element_by_xpath('//*[@id="analysisName"]').send_keys('jing.huang_分析设计')
