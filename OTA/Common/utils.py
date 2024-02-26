# -*-coding:utf-8 -*-
import os

# 获取所有连接的设备
from time import sleep


# 获取手机系统时间
def get_phone_time(device):
    data = os.popen("adb -s {} shell date".format(device)).read()
    data = data.strip("\n")
    return data

# 获取所有连接的设备
def get_devices():
    ret = os.popen('adb devices').readlines()
    device_lists = []
    for item in ret:
        if '\tdevice\n' in item:
            device_lists.append(item[:item.index('\t')])
    return device_lists


# 判断apk是否安装
def apkIsInstall(device, apkPackage=None):
    return os.popen(
        'adb -s {} shell pm list packages | find "com.keyboardapp.firmwaredownload.lxI2c"'.format(device)).readlines()


# 安装apk
def installApk(path):
    os.system("adb install {}".format(path))


# 获取当前运行apk的包名
def currentRunPackage(device):
    return os.popen("adb -s {} shell dumpsys window | findstr mCurrentFocus".format(device)).read()


# 启动app
def startApp(device, appPackageName, appPackageActive):
    print(1)
    os.popen("adb -s {} root".format(device))
    os.popen("adb -s {} shell am start -n {}/{}".format(device, appPackageName, appPackageActive))


# 滑动
def slipFun(device):
    os.popen("adb -s " + device + " shell input swipe 1500 960 1500  450")


# 判断屏幕亮灭状态
def is_screenState(device):
    try:
        cmd = 'adb -s ' + device + ' shell dumpsys power | findstr "Display Power: state="'
        res = os.popen(cmd).read()
        if "mHoldingDisplaySuspendBlocker=true" in res:
            return True
        else:
            return False
    except Exception as e:
        print('获取手机屏幕点亮状态异常', e)
        return False


# 亮屏进入主页面
def lightScreen(device):
    os.popen("adb -s " + device + " shell input keyevent 224")
    sleep(1)
    slipFun(device)


# 判断mcu个数
def mcu_count_fun():
    data = os.popen("adb shell getevent -i").readlines()
    times = 0
    for item in data:
        if "add device" in item:
            times = times + 1
    return times


def screen_cut_fun(device, path):
    data = get_phone_time(device)
    data_list = data.split(" ")
    temp = data_list[3].replace(":", "-")
    data_list[3] = temp
    pic_name = data_list[3]
    print(pic_name)
    # 进行截图
    cut_cmd = "adb -s " + device + " shell screencap -p /sdcard/" + pic_name + ".png"
    os.system(cut_cmd)
    # 获取截图照片
    get_cmd = "adb -s " + device + " pull /sdcard/" + pic_name + ".png " + path
    res = os.popen(get_cmd).read()
    if "1 file pulled" in res:
        return True
    else:
        return False


if __name__ == '__main__':
    # flag = screen_cut_fun(device="01234ABC", path=r"D:\result")
    gooleSearch_package = "com.google.android.googlequicksearchbox"
    gooleSearch_activity = "com.google.android.apps.gsa.searchnow.SearchNowActivity"
    startApp(device="01234ABC", appPackageName=gooleSearch_package, appPackageActive=gooleSearch_activity)