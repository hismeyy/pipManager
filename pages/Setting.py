import re
import tkinter as tk
from tkinter import filedialog

import requests
import ttkbootstrap as ttk
from ttkbootstrap import PRIMARY


class Setting:
    def __init__(self, frame):
        self.entry_var = tk.StringVar()
        self.frame = frame
        self.file_choose_button = ttk.Button(self.frame, text="选择文件", command=self.file_path)
        self.entry_file = ttk.Entry(self.frame, width=30, style=PRIMARY, state="readonly", textvariable=self.entry_var)
        self.entry_url = ttk.Entry(self.frame, width=30, style=PRIMARY)
        self.pip_mirror_label = ttk.Label(self.frame, text="镜像源地址")
        self.ping_result_label = ttk.Label(self.frame, text="", foreground="red")
        self.ping_button = ttk.Button(self.frame, text="ping", command=self.process_url)
        self.theme_choose_list = ttk.Combobox(self.frame,
                                              values=["cosmo", "cyborg", "darkly", "flatly", "journal", "litera",
                                                      "lumen", "lux", "materia", "minty", "pulse", "sandstone",
                                                      "simplex", "sketchy", "slate", "solar", "spacelab", "superhero",
                                                      "united", "yeti"])

        self.theme_choose_label = ttk.Label(self.frame, text="主题")
        self.save_button = ttk.Button(self.frame, text="保存")
        self.cancel_button = ttk.Button(self.frame, text="取消")

        #     布局
        self.file_choose_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_file.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.entry_url.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        self.pip_mirror_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.ping_button.grid(row=1, column=2, padx=10, pady=10, sticky="w")
        self.ping_result_label.grid(row=1, column=3, padx=10, pady=10, sticky="w")
        self.theme_choose_list.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        self.theme_choose_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.save_button.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.cancel_button.grid(row=3, column=1, padx=10, pady=10, sticky="w")

    def file_path(self):
        self.choose_file_path = filedialog.askopenfilename()
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
