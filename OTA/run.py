# -*-coding:utf-8 -*-

from threading import Thread
from time import sleep
from tkinter import *
from tkinter import ttk
from tkinter import messagebox, filedialog

from OTA.Common.utils import get_devices, screen_cut_fun, startApp
from OTA.Page.LXPage import LXPage
from OTA.Page.TNPage import TNPage

from OTA.Common.log import Logger


class OTAGui:

    def __init__(self):
        self.root = Tk()
        self.root.title("OTA升降级测试")
        self.root.geometry("570x280+750+250")
        self.root.resizable(width=False, height=False)
        # 操作的设备
        self.device = ""
        self.devices = []

        # 操作的MCU
        self.mcu = ""
        # 结果保存的路径
        self.file_path = StringVar()
        self.mcu_selects = ['PAD-MCU', 'KB-MCU', 'TP-MCU', '一键升级所有']
        self.mcu_value = StringVar()
        # 电脑连接的所有设备
        self.deviceVar = StringVar()
        self.high_edition = StringVar()
        self.low_edition = StringVar()
        self.times = StringVar()
        self.time_value = StringVar()
        self.logger = ""
        self.status = StringVar()
        # 谷歌浏览器
        self.gooleSearch_package = "com.google.android.googlequicksearchbox"
        self.gooleSearch_activity = "com.google.android.apps.gsa.searchnow.SearchNowActivity"
        # 创建页面主体
        self.main_module()

    def main_module(self):
        top_frame = Frame(self.root, width=550)
        top_frame.grid(row=0, column=0, padx=15, pady=5)
        # 设备选择模块
        self.devices = get_devices()
        label_device = Label(top_frame, text="选择设备：")
        label_device.grid(row=0, column=0, padx=5, pady=5)
        combox_devices = ttk.Combobox(top_frame, textvariable=self.deviceVar, values=self.devices, width=10)
        combox_devices.grid(row=0, column=1, pady=5)
        combox_devices.bind('<<ComboboxSelected>>', self.select_device_event)
        # 结果存放路径
        label_resultPath = Label(top_frame, text="结果存放路径：")
        label_resultPath.grid(row=0, column=2, padx=3)
        entry_path = Entry(top_frame, textvariable=self.file_path, width=25, state="readonly")
        entry_path.grid(row=0, column=3)
        btn_select_path = Button(top_frame, text="选择结果路径", command=self.select_file_path)
        btn_select_path.grid(row=0, column=4, padx=5)
        # 底部参数模块
        bottom_frame = LabelFrame(self.root, text="操作设置")
        bottom_frame.grid(row=1, column=0, padx=5, pady=20)
        # MCU模块选择
        label_mcu = Label(bottom_frame, text="选择MCU：")
        label_mcu.grid(row=0, column=0, padx=5, pady=5)
        combox_mcu = ttk.Combobox(bottom_frame, textvariable=self.mcu_value, values=self.mcu_selects, width=10)
        combox_mcu.grid(row=0, column=1, pady=5, sticky="W")
        combox_mcu.bind('<<ComboboxSelected>>', self.select_mcu_event)
        # 高版本选择
        label_high_edition = Label(bottom_frame, text="高版本：", width=8)
        label_high_edition.grid(row=0, column=2, pady=5)
        entry_high_edition = Entry(bottom_frame, width=15, textvariable=self.high_edition)
        entry_high_edition.grid(row=0, column=3, pady=5)
        # 低版本
        label_low_edition = Label(bottom_frame, text="低版本：")
        label_low_edition.grid(row=0, column=4, pady=5)
        entry_low_edition = Entry(bottom_frame, width=15, textvariable=self.low_edition)
        entry_low_edition.grid(row=0, column=5, pady=5, padx=5)
        # 验证次数
        label_times = Label(bottom_frame, text="验证次数：")
        label_times.grid(row=1, column=0, padx=5, pady=5)
        entry_times_edition = Entry(bottom_frame, width=10, textvariable=self.times)
        entry_times_edition.grid(row=1, column=1, pady=5, sticky="W")
        # 操作时长（单位：s）
        label_operator = Label(bottom_frame, text="操作时长:")
        label_operator.grid(row=1, column=2, columnspan=2, pady=5, sticky="W")
        entry_time = Entry(bottom_frame, width=15, textvariable=self.time_value)
        entry_time.grid(row=1, column=3)
        # 状态
        label_status_tag = Label(bottom_frame, text="状态:")
        label_status_tag.grid(row=1, column=4)
        label_status = Label(bottom_frame, text="未开始", textvariable=self.status, fg="red")
        label_status.grid(row=1, column=5)
        # 由低到高按钮
        btn_update = Button(bottom_frame, text="开始升降级", command=self.thread_start_fun)
        btn_update.grid(row=2, column=0, columnspan=6, ipadx=10, ipady=10, pady=20)

    # 选择文件路径事件
    def select_file_path(self):
        select_folder = filedialog.askdirectory()
        self.file_path.set(select_folder)

    # 选择设备事件
    def select_device_event(self, event):
        self.devices = get_devices()
        self.device = self.deviceVar.get()

    def select_mcu_event(self, event):
        self.mcu = self.mcu_value.get()

    def thread_start_fun(self):
        thread_start = Thread(target=self.start_update)
        thread_start.start()

    # 操作
    def operator_fun(self, log_msg, messagebox_msg):
        self.logger.info(msg=log_msg)
        if int(self.time_value.get()) != 0:
            startApp(device=self.device, appPackageName=self.gooleSearch_package,
                     appPackageActive=self.gooleSearch_activity)
            sleep(int(self.time_value.get()))
            messagebox.showinfo(message=messagebox_msg)

    def update_process(self, app_type, app_driver, update_mcu, times, update_mcu_fun):
        if app_type == "tp":
            self.status.set(value="开始第" + str(times) + "次降级")
            app_driver.startTNApk()
            is_ver_exist = app_driver.select_Copyright(edition=self.low_edition.get())
            if is_ver_exist:
                self.status.set(value="降级中！")
                pad_flag = update_mcu_fun()
                if not pad_flag:
                    screen_cut_fun(device=self.device, path=self.file_path.get())
                    self.logger.error(msg="第" + str(times) + "次" + update_mcu + "降级失败")
                    self.status.set(value="第" + str(times) + "降级失败")
                    return False
                else:
                    self.operator_fun(log_msg="第" + str(times) + "次" + update_mcu + "降级成功",
                                      messagebox_msg="验证时间到，即将升级到高版本，请点击确定")
                    return True
            else:
                messagebox.showwarning(title="警告", message="低版本版本号错误")
                return False
        elif app_type == "lx":
            self.status.set(value="开始第" + str(times) + "次升级")
            app_driver.startApk()
            is_ver_exist = app_driver.is_right_copyright(copyrightNum=self.high_edition.get())
            if is_ver_exist:
                self.status.set(value="升级中！")
                pad_flag = update_mcu_fun()
                if not pad_flag:
                    screen_cut_fun(device=self.device, path=self.file_path.get())
                    self.status.set(value="第" + str(times) + "升级失败")
                    self.logger.error(msg="第" + str(times) + update_mcu + "升级失败")
                    return False
                else:
                    str_t = "第" + str(times) + "次" + update_mcu + "升级成功"
                    self.operator_fun(log_msg=str_t, messagebox_msg="验证时间到，即将降版本，请点击确定")
                    return True
            else:
                messagebox.showwarning(title="警告", message="高版本版本号错误")
                return False

    # 升降级
    def start_update(self):
        self.status.set(value="开始升降级")
        # 判断信息是否填写完整
        if not self.msg_write_is_complete():
            return False
        self.logger = Logger("result", self.file_path.get(), self.device)
        message = "选择的设备：" + self.device + ",选择的MCU：" + self.mcu_value.get() + ",高版本：" + self.high_edition.get() + ", 低版本：" + self.low_edition.get() + ",验证的次数：" + self.times.get() + ",操作的间隔：" + self.time_value.get()
        self.logger.info(msg=message)
        times = 0
        # 获取页面对象
        tp = TNPage(device=self.device)
        lx = LXPage(device=self.device)
        # 获取与手机通信的driver
        # 升降机次数
        while times < int(self.times.get()):
            # 升级次数
            times = times + 1
            if self.mcu_value.get() == "PAD-MCU":
                if times == 1:
                    flag = self.update_process(app_type="tp", app_driver=tp, update_mcu="PAD-MCU", times=times,
                                               update_mcu_fun=tp.update_pad_ver)
                # 高版本升级
                flag = self.update_process(app_type="lx", app_driver=lx, update_mcu="PAD-MCU", times=times,
                                           update_mcu_fun=lx.update_pad_ver)
                # 低版本
                flag = self.update_process(app_type="tp", app_driver=tp, update_mcu="PAD-MCU", times=times,
                                           update_mcu_fun=tp.update_pad_ver)

            elif self.mcu_value.get() == "KB-MCU":
                if times == 1:
                    flag = self.update_process(app_type="tp", app_driver=tp, update_mcu="KB-MCU", times=times,
                                               update_mcu_fun=tp.update_kb_ver)

                # 高版本升级
                flag = self.update_process(app_type="lx", app_driver=lx, update_mcu="KB-MCU", times=times,
                                           update_mcu_fun=lx.update_kb_ver)

                # 低版本
                flag = self.update_process(app_type="tp", app_driver=tp, update_mcu="KB-MCU", times=times,
                                           update_mcu_fun=tp.update_kb_ver)

            elif self.mcu_value.get() == "TP-MCU":
                if times == 1:
                    flag = self.update_process(app_type="tp", app_driver=tp, update_mcu="TP-MCU", times=times,
                                               update_mcu_fun=tp.update_tp_ver)
                # 高版本升级
                flag = self.update_process(app_type="lx", app_driver=lx, update_mcu="TP-MCU", times=times,
                                           update_mcu_fun=lx.update_tp_ver)
                # 低版本
                flag = self.update_process(app_type="tp", app_driver=tp, update_mcu="TP-MCU", times=times,
                                           update_mcu_fun=tp.update_tp_ver)
            else:
                flag = self.update_process(app_type="tp", app_driver=tp, update_mcu="PAD-MCU", times=times,
                                           update_mcu_fun=tp.update_pad_ver)
                flag = self.update_process(app_type="tp", app_driver=tp, update_mcu="PAD-MCU", times=times,
                                           update_mcu_fun=tp.update_kb_ver)
                flag = self.update_process(app_type="tp", app_driver=tp, update_mcu="PAD-MCU", times=times,
                                           update_mcu_fun=tp.update_tp_ver)
                flag = self.update_process(app_type="lx", app_driver=lx, update_mcu="KB-MCU", times=times,
                                           update_mcu_fun=lx.update_pad_ver)
                flag = self.update_process(app_type="lx", app_driver=lx, update_mcu="KB-MCU", times=times,
                                           update_mcu_fun=lx.update_kb_ver)
                flag = self.update_process(app_type="lx", app_driver=lx, update_mcu="KB-MCU", times=times,
                                           update_mcu_fun=lx.update_tp_ver)
            self.status.set(value="执行结束")

    def msg_write_is_complete(self):
        if self.device == "":
            messagebox.showwarning(title="警告", message="请选择测试设备")
            return False
        if self.file_path.get() == "":
            messagebox.showwarning(title="警告", message="请选择结果路径")
            return False
        if self.mcu_value.get() == "":
            messagebox.showwarning(title="警告", message="请选择测试MCU")
            return False
        if self.high_edition.get() == "":
            messagebox.showwarning(title="警告", message="请填写高版本的版本号")
            return False
        if self.high_edition.get() != "":
            if len(self.high_edition.get()) != 9:
                messagebox.showwarning(title="警告", message="版本号错误，应为9位版本号")
                return False
        if self.low_edition.get() == "":
            messagebox.showwarning(title="警告", message="请填写低版本的版本号")
            return False
        if self.low_edition.get() != "":
            if len(self.low_edition.get()) != 9:
                messagebox.showwarning(title="警告", message="版本号错误，应为9位版本号")
                return False
        if self.times.get() == "":
            messagebox.showwarning(title="警告", message="请填写验证次数")
            return False
        if self.times.get() != "":
            if not self.times.get().isdigit():
                messagebox.showwarning(title="警告", message="验证次数请填写数字")
                return False
        if self.time_value.get() == "":
            messagebox.showwarning(title="警告", message="请填写操作时间")
            return False
        if self.time_value.get() != "":
            if not self.time_value.get().isdigit():
                messagebox.showwarning(title="警告", message="操作时长请填写数字")
                return False
        return True


if __name__ == '__main__':
    ota = OTAGui()
    ota.root.mainloop()
