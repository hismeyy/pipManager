import re
import tkinter as tk
from tkinter import filedialog

import requests
import ttkbootstrap as ttk
from ttkbootstrap import PRIMARY


class Setting:
    def __init__(self, frame):
        self.frame = frame

        # 组件
        self.py_setting = ttk.LabelFrame(self.frame, text="PiPManager设置")
        self.entry_var = tk.StringVar()
        self.file_choose_button = ttk.Button(self.py_setting, text="python解释器", command=self.file_path,
                                             style="outline")
        self.entry_file = ttk.Entry(self.py_setting, width=60, style=PRIMARY, state="readonly",
                                    textvariable=self.entry_var)

        self.pip_mirror_label = ttk.Label(self.py_setting, text="设置PiP镜像源：", style="primary")
        self.entry_url = ttk.Entry(self.py_setting, width=43, style=PRIMARY)

        self.ping_button = ttk.Button(self.py_setting, text="测试PiP镜像源", command=self.process_url,
                                      style="success-outline")
        self.ping_result_label = ttk.Label(self.py_setting, text="", foreground="red")

        selected_theme = tk.StringVar()
        # 主题
        style = ttk.Style()
        theme_names = style.theme_names()  # 以列表的形式返回多个主题名
        current_theme = style.theme.name
        selected_theme.set(current_theme)
        self.theme_choose_list = ttk.Menubutton(self.py_setting, textvariable=selected_theme, style="success-outline",
                                                width=10)
        menu = tk.Menu(self.theme_choose_list, tearoff=True)

        self.theme_choose_label = ttk.Label(self.py_setting, text="设置窗口主题：", style="primary")

        def update_theme(theme_name):
            selected_theme.set(theme_name)
            style.theme_use(theme_name)

        for value in theme_names:
            menu.add_command(label=value, command=lambda v=value: update_theme(v))
        self.theme_choose_list.config(menu=menu)

        # 布局

        self.py_setting.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        self.file_choose_button.grid(row=0, column=0, padx=5, pady=10, sticky="w")

        self.entry_file.grid(row=0, column=1, columnspan=2, padx=5, pady=10, sticky="w")

        self.pip_mirror_label.grid(row=1, column=0, padx=5, pady=10, sticky="w")
        self.entry_url.grid(row=1, column=1, padx=5, pady=10, sticky="w")
        self.ping_button.grid(row=1, column=2, padx=5, pady=10, sticky="w")
        self.ping_result_label.grid(row=2, column=1, padx=5, pady=0, sticky="w")

        self.theme_choose_label.grid(row=3, column=0, padx=5, pady=20, sticky="w")
        self.theme_choose_list.grid(row=3, column=1, padx=5, pady=20, sticky="w")

        # 设置行列权重
        self.frame.rowconfigure(0, weight=0)
        self.frame.columnconfigure(0, weight=0)
        self.frame.columnconfigure(1, weight=0)
        self.frame.columnconfigure(2, weight=1)

    def file_path(self):
        self.choose_file_path = filedialog.askopenfilename(filetypes=[("Executable files", "*.exe")])
        self.entry_var.set(self.choose_file_path)

    @staticmethod
    def ping(url):
        time = requests.get(url, timeout=1).elapsed.total_seconds()
        return time

    def process_url(self):
        url = self.entry_url.get()
        if url == "":
            self.ping_result_label.config(text="请输入地址")
        else:
            url_pattern = re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')
            if url_pattern.match(url):
                self.ping_result_label.config(text="")
                result = self.ping(url)
                self.ping_result_label.config(text=f"{result}s")
            else:
                self.ping_result_label.config(text="请输入正确的地址")
