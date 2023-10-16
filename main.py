from tkinter import messagebox
from tkinter import font
import tkinter as tk
import urllib.request
import subprocess
import threading
import random
import easygui
import shutil
import json
import sys
import os

exit_code = 0
# 获取Minecraft版本列表数据
data = json.loads(urllib.request.urlopen("https://launchermeta.mojang.com/mc/game/version_manifest.json").read())
versions = [v["id"] for v in data["versions"] if v["type"] == "release"]


class MinecraftLauncher:
    def __init__(self, master):
        self.master = master
        self.master.title("Minecraft Server Launcher")
        self.master.geometry("310x187")
        self.master.resizable(False, False)
        self.master.protocol("WM_DELETE_WINDOW", None)

        # 设置字体
        self.custom_font = font.Font(family="CMSXTJ", size=12)

        # 创建选择版本的区域
        self.version_label = tk.Label(self.master, text="选择版本：", font=self.custom_font)
        self.version_label.place(x=10, y=10)
        self.version_options = ["Java版", "基岩版"]
        self.version_var = tk.StringVar()
        self.version_var.set(self.version_options[0])
        self.version_choices = tk.OptionMenu(self.master, self.version_var, *self.version_options,
                                             command=self.update_options)
        self.version_choices.config(font=self.custom_font)
        self.version_choices.place(x=90, y=7)

        # 创建选择核心的区域
        self.hexin_label = tk.Label(self.master, text="选择核心：", font=self.custom_font)
        self.hexin_label.place(x=10, y=53)
        self.hexin_options = os.listdir('./hexin/Java Edit')
        self.hexin_var = tk.StringVar()
        self.hexin_var.set(random.choice(self.hexin_options))
        self.hexin_choices = tk.OptionMenu(self.master, self.hexin_var, *self.hexin_options)
        self.hexin_choices.config(font=self.custom_font)
        self.hexin_choices.place(x=90, y=50)

        # 创建选择存档的区域
        self.cundang_label = tk.Label(self.master, text="选择存档：", font=self.custom_font)
        self.cundang_label.place(x=10, y=96)
        self.cundang_var = tk.StringVar()
        self.cundang_var.set("New")
        self.cundang_options = ['New'] + os.listdir('./Java Edit')
        if 'jre-17.0.2-full' in self.cundang_options:
            self.cundang_options.remove('jre-17.0.2-full')
        self.cundang_choices = tk.OptionMenu(self.master, self.cundang_var, *self.cundang_options)
        self.cundang_choices.config(font=self.custom_font)
        self.cundang_choices.place(x=90, y=93)

        # 创建按钮区域
        self.run_button = tk.Button(self.master, text="运行", command=self.run_minecraft, font=self.custom_font)
        self.run_button.place(x=10, y=140)

        # 创建打开存档的按钮
        self.open_button = tk.Button(self.master, text="打开存档", command=self.open_cundang, font=self.custom_font)
        self.open_button.place(x=60, y=140)

        self.down_button = tk.Button(self.master, text="下载", command=self.down_minecraft, font=self.custom_font)
        self.down_button.place(x=143, y=140)

        self.exit_button = tk.Button(self.master, text="退出", command=self.master.quit, font=self.custom_font)
        self.exit_button.place(x=193, y=140)

    def update_options(self, value):
        if value == "Java版":
            self.hexin_options = os.listdir('./hexin/Java Edit')
            self.cundang_options = ['New'] + os.listdir('./Java Edit')
        elif value == "基岩版":
            self.hexin_options = os.listdir('./hexin/Bedrock Edit')
            self.cundang_options = ['New'] + os.listdir('./Bedrock Edit')
        self.hexin_var.set(random.choice(self.hexin_options))
        self.hexin_choices['menu'].delete(0, 'end')
        for option in self.hexin_options:
            self.hexin_choices['menu'].add_command(label=option, command=tk._setit(self.hexin_var, option))
        self.cundang_var.set("New")
        self.cundang_choices['menu'].delete(0, 'end')
        for option in self.cundang_options:
            self.cundang_choices['menu'].add_command(label=option, command=tk._setit(self.cundang_var, option))

    def run_minecraft(self):
        hexin = self.hexin_var.get()

        if self.version_var.get() == "Java版":
            if self.cundang_var.get() == 'New':
                cundang = easygui.enterbox('存档名', '存档名')
                if cundang is None or cundang == '':
                    return
                shutil.copytree('./muban/Java Edit', './Java Edit/' + cundang)
            else:
                cundang = self.cundang_var.get()
            threading.Thread(target=lambda: self.run_time(cundang, hexin, 'java')).start()

        elif self.version_var.get() == "基岩版":
            if self.cundang_var.get() == 'New':
                cundang = easygui.enterbox('存档名', '存档名')
                if cundang is None or cundang == '':
                    return
                shutil.copytree('./muban/Bedrock Edit', './Bedrock Edit/' + cundang)
            else:
                cundang = self.cundang_var.get()
            threading.Thread(target=lambda: self.run_time(cundang, hexin, '')).start()

    def open_cundang(self):
        cundang = self.cundang_var.get()
        if cundang == 'New':
            return
        if self.version_var.get() == "Java版":
            os.startfile(f"Java Edit\\{cundang}")
        elif self.version_var.get() == "基岩版":
            os.startfile(f"Bedrock Edit\\{cundang}")

    def down_minecraft(self):
        c = easygui.buttonbox('附带', '附带', ['nothing', 'plugins', 'plugins & mod'])
        if c == 'nothing':
            version = easygui.choicebox("选择 Java版 版本", "Minecraft启动器", choices=versions)
            if not version:
                return
            data = json.loads(
                urllib.request.urlopen(f"https://launchermeta.mojang.com/mc/game/version_manifest.json").read())
            url = [v["url"] for v in data["versions"] if v["id"] == version][0]
            data = json.loads(urllib.request.urlopen(url).read())
            url = data["downloads"]["client"]["url"]
            messagebox.showinfo(message="正在下载，请稍等片刻...", title="Minecraft启动器")
            urllib.request.urlretrieve(url, f"./hexin/Java Edit/server-{version}.jar")
            easygui.msgbox("下载完成！", "Minecraft启动器")
        elif c == 'plugins':
            os.system('start https://getbukkit.org/download/craftbukkit')
        else:
            os.system('start https://mohistmc.com/download/')

    def run_time(self, cundang, hexin, b):
        if b == 'java':
            self.run_button.config(state="disabled")
            os.chdir('./Java Edit/' + cundang)
            subprocess.run(
                r'"C:\{minec}\services\Java Edit\jre-17.0.2-full\bin\java" -jar "C:\{minec}\services\hexin\Java Edit' + '\\' + hexin + '"')
            easygui.msgbox('运行完毕')
            os.chdir('../..')
            self.run_button.config(state="normal")
        else:
            self.run_button.config(state="disabled")
            os.chdir('./Bedrock Edit/' + cundang)
            subprocess.run(r'"C:\{minec}\services\hexin\Bedrock Edit' + '\\' + hexin + '"')
            easygui.msgbox('运行完毕')
            os.chdir('../..')
            self.run_button.config(state="normal")

    def exit(self):
        global exit_code
        a = easygui.enterbox('您使用的是未激活的程序，不激活对导致您无法使用某些功能\n请输入激活秘钥以使用全部功能！', '激活')
        if a == '':
            if exit_code <= 3:
                exit_code += 1
                easygui.msgbox('秘钥错误，请重新输入！', '秘钥错误')
            else:
                self.master.quit()
                sys.exit()
        else:
            easygui.msgbox('秘钥错误，请重新输入！', '秘钥错误')
        return



if __name__ == "__main__":
    root = tk.Tk()
    root.iconbitmap(r"D:\xue\ico\xue.ico")
    launcher = MinecraftLauncher(root)
    root.mainloop()
