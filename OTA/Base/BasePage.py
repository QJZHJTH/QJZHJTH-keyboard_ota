# -*-coding:utf-8 -*-
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:

    def __init__(self):
        self.caps = None
        self.driver = None

    def start_driver(self):
        self.caps = {"platformName": "Android", "appium:platformVersion": "13.0", "appium:deviceName": "联想"}
        self.driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", self.caps)

    def get_ele(self, loc):
        try:
            print(*loc)
            el = WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*loc))
            return el
        except Exception as e:
            return False

    def click(self, el):
        el.click()


if __name__ == '__main__':
    bp = BasePage()
    bp.start_driver()
    print(bp.driver.device_time)
