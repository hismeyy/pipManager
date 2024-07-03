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
        self.file_choose_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry = ttk.Entry(self.frame, width=30, style=PRIMARY, state="readonly", textvariable=self.entry_var)
        self.entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.entry = ttk.Entry(self.frame, width=30, style=PRIMARY)
        self.entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        self.pip_mirror_label = ttk.Label(self.frame, text="镜像源地址")
        self.pip_mirror_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.ping_result_label = ttk.Label(self.frame, text="", foreground="red")
        info = self.process_url()
        self.ping_result_label.config(text=info)

        self.ping_result_label.grid(row=1, column=3, padx=10, pady=10, sticky="w")

        self.theme_choose_list = ttk.Combobox(self.frame,
                                              values=["cosmo", "cyborg", "darkly", "flatly", "journal", "litera",
                                                      "lumen", "lux", "materia", "minty", "pulse", "sandstone",
                                                      "simplex", "sketchy", "slate", "solar", "spacelab", "superhero",
                                                      "united", "yeti"])
        self.theme_choose_list.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        self.theme_choose_label = ttk.Label(self.frame, text="主题")
        self.theme_choose_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.save_button = ttk.Button(self.frame, text="保存")
        self.save_button.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.cancel_button = ttk.Button(self.frame, text="取消")
        self.cancel_button.grid(row=3, column=1, padx=10, pady=10, sticky="w")

    def file_path(self):
        self.choose_file_path = filedialog.askopenfilename()
        self.entry_var.set(self.choose_file_path)

    @staticmethod
    def ping(url):
        time = requests.get(url, timeout=1).elapsed.total_seconds()
        return time

    def process_url(self):
        url = self.entry_var.get()
        if url == "":
            self.ping_result_label.config(text="请输入地址")
        else:

            url_pattern = re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')
            if url_pattern.match(url):
                result = self.ping(url)
                return result
            else:
                self.ping_result_label.config(text="请输入正确的地址")
