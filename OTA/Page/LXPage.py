# -*-coding:utf-8 -*-
from appium.webdriver.common.appiumby import AppiumBy

from OTA.Base.BasePage import BasePage
from OTA.Common.utils import startApp, is_screenState, lightScreen


class LXPage(BasePage):

    def __init__(self, device):
        super().__init__()
        self.appPackageName = "com.yy031.upgrade"
        self.appPackageActive = "com.yy031.upgrade.MainActivity"
        self.device = device
        # 允许框元素
        self.allow = (AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_button")
        # 升级和获取版本元素
        self.pad_update_btn = (AppiumBy.ID, "com.yy031.upgrade:id/start_upgrade")
        self.pad_get_btn = (AppiumBy.ID, "com.yy031.upgrade:id/get_version")
        self.kb_update_btn = (AppiumBy.ID, "com.yy031.upgrade:id/start_keyboard_upgrade")
        self.kb_get_btn = (AppiumBy.ID, "com.yy031.upgrade:id/get_keyboard_version")
        self.tp_update_btn = (AppiumBy.ID, "com.yy031.upgrade:id/start_tp_upgrade")
        self.tp_get_btn = (AppiumBy.ID, "com.yy031.upgrade:id/get_tp_version")
        self.update_result_text = (AppiumBy.ID, "com.yy031.upgrade:id/tv_info")
        self.update_progress_text = (AppiumBy.XPATH, '/hierarchy/android.widget.TextView')

        # copyright
        self.bin_el = (AppiumBy.ID,"com.yy031.upgrade:id/bin_path")

    # 获取driver对象
    def lx_start_driver(self):
        self.start_driver()

    # 强制回到测试页面
    def startApk(self):
        if not is_screenState(self.device):
            # 屏幕亮屏
            lightScreen(self.device)
        startApp(device=self.device, appPackageName=self.appPackageName, appPackageActive=self.appPackageActive)
        self.lx_start_driver()
        el_allow = self.get_ele(self.allow)
        if el_allow:
            el_allow.click()

    # 校验版本
    def is_right_copyright(self, copyrightNum):
        bin = self.get_ele(self.bin_el)
        while not bin:
            bin = self.get_ele(self.bin_el)
        if copyrightNum in bin.text:
            print("版本校验正确")
            return True
        else:
            return False

    def update_pad_ver(self):
        el = self.get_ele(self.pad_update_btn)
        el.click()
        while True:
            flag = self.get_ele(self.update_progress_text)
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
            flag = self.get_ele(self.update_progress_text)
            if not flag:
                break
        if "升级成功" not in self.get_ele(self.update_result_text).text:
            return False
        self.get_ele(self.kb_get_btn).click()
        return True

    def update_tp_ver(self):
        el = self.get_ele(self.tp_update_btn)
        el.click()
        while True:
            flag = self.get_ele(self.update_progress_text)
            if not flag:
                break
        if "success" not in self.get_ele(self.update_result_text).text:
            return False
        self.get_ele(self.tp_get_btn).click()
        return True


if __name__ == '__main__':
    lp = LXPage(device="01234ABC")
    lp.start_driver()
    lp.startApk()
    flag = lp.is_right_copyright(copyrightNum="K0AP16T0A")

    print(flag)
