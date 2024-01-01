#         -*- coding:utf-8 -*-        #
#  Copyright (c) 2019 - 2039 XueQian  #
#        version_added:: 1.4.0          #

from tkinter import messagebox
from tkinter import font
import tkinter as tk
import urllib.request
import subprocess
import threading  # 可能看起来没用，但引用在 272 行（附近）！
import random
import easygui
import shutil
import psutil
import time
import json
import sys
import os

Running = 0
Ctrl_C = 0


def change(name: str, value: str, eval_: str = 'str') -> None:
    global stop_button, Running, Ctrl_C
    # Ctrl_C = 1
    # print(name, value)
    exec(f'global stop_button, Running, Ctrl_C\n{name} = {value}')
    eval(eval_)
    return None


def update_options(value):
    if value == "Java版":
        hexin_options = os.listdir('./hexin/Java Edit')
        cundang_options = ['New'] + os.listdir('./Java Edit')
    elif value == "基岩版":
        hexin_options = os.listdir('./hexin/Bedrock Edit')
        cundang_options = ['New'] + os.listdir('./Bedrock Edit')
    else:
        hexin_options = []
        cundang_options = []
    hexin_var.set(random.choice(hexin_options))
    hexin_choices['menu'].delete(0, 'end')
    for option in hexin_options:
        hexin_choices['menu'].add_command(label=option, command=tk._setit(hexin_var, option))
    cundang_var.set("New")
    cundang_choices['menu'].delete(0, 'end')
    for option in cundang_options:
        cundang_choices['menu'].add_command(label=option, command=tk._setit(cundang_var, option))


def run_minecraft():
    global run_button, stop_button, Ctrl_C, Running, s, whil, a

    def jiancha():
        global run_button, stop_button, Ctrl_C, Running, s, whil, a
        while 1:
            if Ctrl_C == 1 and s == 0:
                s_label.configure(text="正在关闭")
                # TODO: 我不想使用kill方法强制关闭，而是使用stop指令关闭，但还没有找到方法。
                # time.sleep(1)
                # print('关闭命令', a.pid, psutil.Process(a.pid).children(recursive=True)[-1].pid)
                subprocess.Popen(f'taskkill -f -pid {psutil.Process(a.pid).children(recursive=True)[-1].pid}', shell=False, stdout=subprocess.PIPE, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)

                # os.kill(psutil.Process(a.pid).children(recursive=True)[-1].pid, signal.CTRL_C_EVENT)
                # a.kill()
                # a.communicate(b'stop\n')
                s = 1
            if whil == 0:
                break
            time.sleep(1)

    hexin = hexin_var.get()

    kongzhi = tk.Toplevel()
    kongzhi.iconbitmap(file_ + r"\xue.ico")
    run_button.config(state="disabled")

    # information = []
    if version_var.get() == "Java版":
        if cundang_var.get() == 'New':
            cundang = easygui.enterbox('存档名', '存档名')
            if cundang is None or cundang == '':
                return
            shutil.copytree('./muban/Java Edit', './Java Edit/' + cundang)
        else:
            cundang = cundang_var.get()

        # threading.Thread(target=lambda: run_time(cundang, hexin, 'java')).start()
        os.chdir('./Java Edit/' + cundang)
        information = ["Java版", cundang, hexin]
        command = r'"..\..\jre\bin\java" -jar "..\..\hexin\Java Edit' + rf'\{hexin}" gui'

    else:  # elif version_var.get() == "基岩版":
        if cundang_var.get() == 'New':
            cundang = easygui.enterbox('存档名', '存档名')
            if cundang is None or cundang == '':
                return
            shutil.copytree('./muban/Bedrock Edit', './Bedrock Edit/' + cundang)
        else:
            cundang = cundang_var.get()
        # threading.Thread(target=lambda: run_time(cundang, hexin, '')).start()
        os.chdir('./Bedrock Edit/' + cundang)
        information = ["Java版", cundang, hexin]
        command = r'"..\..\hexin\Bedrock Edit' + rf'\{hexin}"'

    # threading.Thread(target=lambda: run_time(command)).start()

    if information[0] == "Java版":
        kongzhi.title("Control Panle")
        kongzhi.geometry("310x187")
        kongzhi.resizable(False, False)
        kongzhi.protocol("WM_DELETE_WINDOW", None)

        statue_label = tk.Label(kongzhi, text="状态：", font=custom_font)
        statue_label.place(x=10, y=10)

        s_label = tk.Label(kongzhi, text='加载中', font=custom_font)
        s_label.place(x=100, y=10)

        stop_button = tk.Button(kongzhi, text="直接停止",
                                command=lambda: change('Ctrl_C', '1', 'stop_button.config(state="disabled")'),
                                font=custom_font)
        stop_button.place(x=200, y=10)

        '''statue_label = tk.Label(kongzhi, text="状态：", font=custom_font)
statue_label.place(x=10, y=10)

s_label = tk.Label(kongzhi, text='加载中', font=custom_font)
s_label.place(x=100, y=10)

stop_button = tk.Button(kongzhi, text="直接停止",
                        command=lambda: change('Ctrl_C', '1', 'stop_button.config(state="disabled")'),
                        font=custom_font)
stop_button.place(x=200, y=10)'''

        time.sleep(1000)

        Running = 1
        a = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
        s = 0
        whil = 1
        now = '出现未知错误！'
        lastlog = []
        # todo

        threading.Thread(target=jiancha).start()
        while 1:
            line = a.stdout.readline()
            if not line:
                break
            elif b'For help, type "help"' in line:
                s_label.configure(text="运行中")
            elif b"Stopping the server" in line:
                s_label.configure(text="正在关闭")
                now = '运行完毕'
            elif b"FAILED TO BIND TO PORT" in line:
                now = '端口被占用！'
            elif b"EULA" in line or b"eula" in line:
                now = '您需要同意最终用户许可协议才能运行服务器。'
                os.system(r'notepad eula.txt')
            # print(line, b"FAILED TO BIND TO PORT" in line)

            if len(lastlog) == 30:
                del lastlog[0]
            lastlog.append(line)

        whil = 0

        run_button.config(state="normal")
        kongzhi.destroy()
        if now != '运行完毕' and Ctrl_C == 0:
            name = f"./{time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))}log_（{information[0]})({information[1]})({information[2]}）.txt"
            logfile = open(name, 'wb')
            logtext = command.encode() + b'\n'
            for ii in lastlog:
                logtext += ii
            logfile.write(logtext)
            logfile.close()
            messagebox.showinfo(message=now + '\n最后30条日志被保存在：' + os.path.abspath(name), title="Minecraft启动器")
        if Ctrl_C == 1:
            messagebox.showinfo(message='已结束', title="Minecraft启动器")
        else:
            messagebox.showinfo(message=now, title="Minecraft启动器")
        Ctrl_C = 0
    else:  # information[0] == "基岩版"
        Running = 1
        subprocess.run(command)
        messagebox.showinfo(message="运行完毕", title="Minecraft启动器")
    Running = 0
    os.chdir('../..')


def open_cundang():
    cundang = cundang_var.get()
    if cundang == 'New':
        return
    if version_var.get() == "Java版":
        os.startfile(f"Java Edit\\{cundang}")
    elif version_var.get() == "基岩版":
        os.startfile(f"Bedrock Edit\\{cundang}")


def down_minecraft():
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
        messagebox.showinfo(message="下载完成！", title="Minecraft启动器")
    elif c == 'plugins':
        os.system('start https://getbukkit.org/download/craftbukkit')
    else:
        os.system('start https://mohistmc.com/download/')


def quit():
    global root, exit_button
    exit_button.config(state="disabled")
    if Running == 1:
        if Ctrl_C == 1:
            messagebox.showinfo(message="请等待服务器关闭。", title="Minecraft启动器")
            exit_button.config(state="normal")
            return 1
        messagebox.showinfo(message="请先关闭服务器。", title="Minecraft启动器")
        exit_button.config(state="normal")
        return 1
    root.quit()
    sys.exit()


'''
def run_time(command):
    global run_button, Running, Outgoing, Ctrl_C
    # subprocess.run(command)
    a = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)

    s = 0
    while True:
        line = a.stdout.readline()
        if not line:
            break

        if b'For help, type "help"' in line:
            Outgoing = 1
        elif b"Stopping the server" in line:
            break
        if Ctrl_C == 1 and s == 0:
            a.kill()
            # a.communicate(b'stop\n')
            s = 1
            time.sleep(1)

    easygui.msgbox('运行完毕')

    Running = 0
    Outgoing = 0
    Ctrl_C = 0

    os.chdir('../..')
    return
'''

try:
    data = json.loads(urllib.request.urlopen("https://launchermeta.mojang.com/mc/game/version_manifest.json").read())
    versions = [v["id"] for v in data["versions"] if v["type"] == "release"]
except:
    versions = ['1.19.4']

if __name__ == '__main__':
    # 判断是否第一次开启
    if not os.path.isdir('./hexin'):
        def makedirs(a: list):
            es = ''
            for i in a:
                try:
                    os.makedirs(i)
                except Exception as e:
                    es += str(e)
            return


        makedirs(
            ['.\hexin\Bedrock Edit', '.\hexin\Java Edit', '.\muban\Bedrock Edit', '.\muban\Java Edit', '.\Bedrock Edit',
             '.\Java Edit'])
        with open(r'.\muban\Java Edit\eula.txt', 'w') as e:
            e.write('#Created by XueQian\neula=true')

        messagebox.showinfo(message='欢入！\n请将核心放置在 hexin 文件夹中，模板放置在 muban 文件夹中。然后重启程序。', title="Minecraft启动器")
        sys.exit()

    root = tk.Tk()
    file_ = os.path.dirname(os.path.abspath(__file__))
    root.iconbitmap(file_ + r"\xue.ico")

    root.title("Minecraft Server Launcher")
    root.geometry("310x187")
    root.resizable(False, False)
    root.protocol("WM_DELETE_WINDOW", None)

    # 设置字体
    custom_font = font.Font(family="CMSXTJ", size=12)

    # 创建选择版本的区域
    version_label = tk.Label(root, text="选择版本：", font=custom_font)
    version_label.place(x=10, y=10)
    version_options = ["Java版", "基岩版"]
    version_var = tk.StringVar()
    version_var.set(version_options[0])
    version_choices = tk.OptionMenu(root, version_var, *version_options,
                                    command=update_options)
    version_choices.config(font=custom_font)
    version_choices.place(x=90, y=7)

    # 创建选择核心的区域
    hexin_label = tk.Label(root, text="选择核心：", font=custom_font)
    hexin_label.place(x=10, y=53)
    hexin_options = os.listdir('./hexin/Java Edit')
    hexin_var = tk.StringVar()
    hexin_var.set(random.choice(hexin_options))
    hexin_choices = tk.OptionMenu(root, hexin_var, *hexin_options)
    hexin_choices.config(font=custom_font)
    hexin_choices.place(x=90, y=50)

    # 创建选择存档的区域
    cundang_label = tk.Label(root, text="选择存档：", font=custom_font)
    cundang_label.place(x=10, y=96)
    cundang_var = tk.StringVar()
    cundang_var.set("New")
    cundang_options = ['New'] + os.listdir('./Java Edit')
    if 'jre-17.0.2-full' in cundang_options:
        cundang_options.remove('jre-17.0.2-full')
    cundang_choices = tk.OptionMenu(root, cundang_var, *cundang_options)
    cundang_choices.config(font=custom_font)
    cundang_choices.place(x=90, y=93)

    # 创建按钮区域
    run_button = tk.Button(root, text="运行", command=lambda: eval('threading.Thread(target=run_minecraft).start()'),
                           font=custom_font)
    run_button.place(x=10, y=140)

    # 创建打开存档的按钮
    open_button = tk.Button(root, text="打开存档", command=open_cundang, font=custom_font)
    open_button.place(x=60, y=140)

    down_button = tk.Button(root, text="下载", command=down_minecraft, font=custom_font)
    down_button.place(x=143, y=140)

    exit_button = tk.Button(root, text="退出", command=quit, font=custom_font)
    exit_button.place(x=193, y=140)

    root.mainloop()
