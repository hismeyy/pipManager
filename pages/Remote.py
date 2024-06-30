import threading
import tkinter as tk

import ttkbootstrap as ttk

from utils.PipApi import PipApi


class Remote:
    def __init__(self, frame):
        self.pip_api = PipApi()
        self.frame = frame
        self.install_button = ttk.Button(self.frame, text="安装")
        self.refresh_button = ttk.Button(self.frame, text="刷新")
        self.processing = ttk.Label(self.frame, text="提示信息...", foreground="red")

        self.py_list = ttk.Treeview(self.frame, columns="c1", show="headings")

        self.introduction_label = ttk.LabelFrame(self.frame, text="简介")
        self.introduction_content_label = ttk.Label(self.introduction_label, text="这是一个简介")
        self.version_option_check = ttk.Checkbutton(self.frame, text="指定版本")

        self.version_list_combobox = ttk.Combobox(self.frame, values=["1.0.0"], state="readonly")

    def set_py_list(self, py_list):
        """
        设置py包list
        :param py_list:
        :return:
        """
        items = self.pip_api.get_py_package_list_api()
        for item in items:
            py_list.insert("", tk.END, values=item)

    def get_remote(self):

        # 布局按钮
        self.install_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.refresh_button.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.processing.grid(row=0, column=2, padx=10, pady=10, sticky="w")

        # 创建 Treeview 作为带有表头的列表框
        self.py_list.grid(row=1, column=0, columnspan=50, rowspan=3, padx=10, pady=10, sticky="nsew")
        # 设置列标题
        self.py_list.heading("c1", text="Pip包", anchor="w")
        # 设置列宽
        self.py_list.column("c1", width=300)

        self.introduction_label.grid(row=1, column=51, padx=10, pady=0, sticky="nsew")

        self.introduction_content_label.grid(row=1, column=41, padx=10, pady=10, sticky="nw")

        self.version_option_check.grid(row=2, column=51, padx=10, pady=(30, 0), sticky="sw")
        self.version_list_combobox.grid(row=3, column=51, padx=10, pady=10, sticky="sw")

        def set_py_list_thread_method():
            self.set_py_list(self.py_list)

        # 向列表中添加一些项
        set_py_list_thread = threading.Thread(target=set_py_list_thread_method)
        set_py_list_thread.start()


        # 设置列权重
        self.frame.columnconfigure(0, weight=0)
        self.frame.columnconfigure(1, weight=0)
        self.frame.columnconfigure(2, weight=0)
        self.frame.columnconfigure(3, weight=0)
        self.frame.columnconfigure(3, weight=0)
        self.frame.columnconfigure(51, weight=1)

        self.frame.rowconfigure(1, weight=1)
