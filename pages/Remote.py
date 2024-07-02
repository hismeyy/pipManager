import queue
import threading
import tkinter as tk

import ttkbootstrap as ttk

from utils.PipApi import PipApi


class Remote:
    def __init__(self, frame):
        self.pip_api = PipApi()
        self.frame = frame
        # 组件
        self.install_button = ttk.Button(self.frame, text="安装")
        self.processing = ttk.Label(self.frame, text="", foreground="red")
        self.py_list = ttk.Treeview(self.frame, columns="c1", show="headings")

        self.vsb = ttk.Scrollbar(self.py_list, orient="vertical", command=self.py_list.yview)

        self.introduction_label = ttk.LabelFrame(self.frame, text="简介")
        self.introduction_content_label = ttk.Label(self.introduction_label, text="这是一个简介")
        self.version_option_check = ttk.Checkbutton(self.frame, text="指定版本")
        self.version_list_combobox = ttk.Combobox(self.frame, values=["1.0.0"], state="readonly")

        # 布局
        self.install_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.processing.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        self.py_list.grid(row=1, column=0, columnspan=2, rowspan=3, padx=10, pady=10, sticky="nsew")
        self.py_list.heading("c1", text="Pip包", anchor="w")
        self.py_list.column("c1", width=200)
        self.vsb.pack(side="right", fill="y")

        self.introduction_label.grid(row=1, column=2, padx=10, pady=0, sticky="nsew")
        self.introduction_content_label.grid(row=1, column=2, padx=10, pady=10, sticky="nw")
        self.version_option_check.grid(row=2, column=2, padx=10, pady=(30, 0), sticky="sw")
        self.version_list_combobox.grid(row=3, column=2, padx=10, pady=10, sticky="sw")

        self.py_list.configure(yscrollcommand=self.vsb.set)
        # 设置行列权重
        self.frame.columnconfigure(0, weight=0)
        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=1)
        self.frame.columnconfigure(3, weight=0)
        self.frame.rowconfigure(1, weight=1)

        self.queue = queue.Queue()

        self.frame.after(100, self.set_py_list)

    def set_py_list(self):
        """
        更新py包list
        :return:
        """
        while not self.queue.empty():
            item = self.queue.get()
            self.py_list.insert("", tk.END, values=item)

    def get_py_list(self):
        """
        设置py包list
        :return:
        """
        items = self.pip_api.get_py_package_list_api()
        for item in items:
            self.queue.put(item)

    def get_remote(self):
        set_py_list_thread = threading.Thread(target=self.get_py_list)
        set_py_list_thread.start()
