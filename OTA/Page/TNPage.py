# -*-coding:utf-8 -*-
from time import sleep

from OTA.Base.BasePage import BasePage
from appium.webdriver.common.appiumby import AppiumBy

from OTA.Common.utils import startApp, slipFun, is_screenState, lightScreen


class TNPage(BasePage):

    # 初始化
    def __init__(self, device):
        super().__init__()
        self.appPackageName = "com.keyboardapp.firmwaredownload.lxI2c"
        self.appPackageActive = "com.keyboardapp.firmwaredownload.MainActivity"
        self.device = device
        # 允许框元素
        self.allow = (AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_button")
        # 升级和获取版本元素
        self.pad_update_btn = (AppiumBy.ID, "com.keyboardapp.firmwaredownload.lxI2c:id/start_upgrade")
        self.pad_get_btn = (AppiumBy.ID, "com.keyboardapp.firmwaredownload.lxI2c:id/get_version")
        self.kb_update_btn = (AppiumBy.ID, "com.keyboardapp.firmwaredownload.lxI2c:id/start_keyboard_upgrade")
        self.kb_get_btn = (AppiumBy.ID, "com.keyboardapp.firmwaredownload.lxI2c:id/get_keyboard_version")
        self.tp_update_btn = (AppiumBy.ID, "com.keyboardapp.firmwaredownload.lxI2c:id/start_tp_upgrade")
        self.tp_get_btn = (AppiumBy.ID, "com.keyboardapp.firmwaredownload.lxI2c:id/get_tp_version")

        # 弹出框
        self.bin_frame = (AppiumBy.ID, "android:id/parentPanel")
        self.bin_frame_flag = False
        # 升级结果元素
        self.update_result_text = (AppiumBy.ID, "com.keyboardapp.firmwaredownload.lxI2c:id/tv_info")

        # 升级进度条元素
        self.update_progress_text = (AppiumBy.ID, "com.keyboardapp.firmwaredownload.lxI2c:id/tv_progress_upgrade")

        # 选择版本元素
        self.bin_path = (AppiumBy.XPATH,
                         "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.TextView[1]")

        # 升级
        self.update_text = (AppiumBy.XPATH, '/hierarchy/android.widget.TextView')

    # 获取driver
    def tn_start_driver(self):
        self.start_driver()

    def installAPK(self):
        pass

    # 启动app,跳转到指定界面
    def startTNApk(self):
        if not is_screenState(self.device):
            print("屏幕灭")
            # 屏幕亮屏
            lightScreen(self.device)
        startApp(device=self.device, appPackageName=self.appPackageName, appPackageActive=self.appPackageActive)
        self.tn_start_driver()
        allow_el = self.get_ele(self.allow)
        print(allow_el)
        if allow_el:
            allow_el.click()

    # 选择版本
    def select_Copyright(self, edition):
        times = 0
        el = self.get_ele(self.bin_path)
        if el:
            if edition in el.text:
                print("版本正确")
                return True
        self.bin_frame_flag = self.get_ele(self.bin_frame)
        # 判断弹出框，点击弹出框
        if not self.bin_frame_flag:
            while not el:
                el = self.get_ele(self.bin_path)
                sleep(1)
            el.click()
        target_edition = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("{}")'.format(edition))
        target = False
        while not target:
            times = times + 1
            slipFun(self.device)
            target = self.get_ele(target_edition)
            if times > 5:
                print("未找到对应版本")
                return False
        if target:
            target.click()
            return True

    def update_pad_ver(self):
        while True:
            el = self.get_ele(self.pad_update_btn)
            sleep(0.5)
            if el:
                break
        el.click()
        while True:
            flag = self.get_ele(self.update_text)
            if not flag:
                break
        if "升级成功" not in self.get_ele(self.update_result_text).text:
            return False
        self.get_ele(self.pad_get_btn).click()
        return True

    def update_kb_ver(self):
        el = self.get_ele(self.kb_update_btn)
        el.click()
        while True:
            flag = self.get_ele(self.update_text)
            if not flag:
                break
        if "升级成功" not in self.get_ele(self.update_result_text).text:
            return False
        self.get_ele(self.kb_get_btn).click()
        return True

    def update_tp_ver(self):
        self.get_ele(self.tp_update_btn).click()
        while True:
            flag = self.get_ele(self.update_text)
            if not flag:
                break
        if "success" not in self.get_ele(self.update_result_text).text:
            return False
        self.get_ele(self.tp_get_btn).click()
        return True


if __name__ == '__main__':
    tp = TNPage(device="01234ABC")
    tp.startTNApk()
    tp.select_Copyright(edition="K09P12T0A")
