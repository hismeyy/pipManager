import logging
import threading
import tkinter as tk

import ttkbootstrap as ttk

from utils.PipApi import PipApi


class Remote:
    def __init__(self, frame):
        self.update_list = None
        self.root = None  # 确保 root 被初始化为 None
        self.lock = threading.Lock()  # 添加锁以确保线程安全
        self.update_thread_event = threading.Event()  # 添加一个事件用于线程通信
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
        with self.lock:  # 使用锁来保护数据一致性
            self.py_list = py_list
        items = self.pip_api.get_py_package_list_api()
        if self.root and self.root.winfo_exists():  # 检查 root 是否存在
            self.root.after(0, self.update_list, items)  # 确保在有有效的 root 对象时调用 after 方法
        for item in items:
            py_list.insert("", tk.END, values=item)

    INSERT_LOCATION = " "
    END_INDEX = tk.END

    def update_list(self, items):
        # 检查 Treeview 是否存在
        if self.py_list.winfo_exists():
            if not items:  # 检查 items 是否为空，如果是，则不执行插入操作
                print("No items to update.")  # 根据实际情况，这里可以改为更合适的处理方式
                return

            try:
                # 为了提高性能，减少对 Treeview 控件操作的次数，可以先构建要插入的数据结构
                # 假设 Treeview 控件提供了批量插入的方法，这里用 fake_bulk_insert 方法来表示
                items = self.pip_api.get_py_package_list_api()
                values = [(item[0], item[1]) for item in items]

                # Batch insert items
                for value in values:
                    self.py_list.insert("", tk.END, values=value)
            except Exception as e:
                # 添加了异常处理，以避免因单个错误导致整个程序崩溃
                print(f"An error occurred while updating the list: {e}")
                # 这里可以记录日志、提示用户或采取其他错误处理措施
        else:
            print("Treeview does not exist.")  # 根据实际情况，这里可以改为更合适的处理方式

    def get_remote(self):
        self._init_widgets()  # 初始化控件
        self._configure_grid()  # 配置 grid
        self._start_update_thread()  # 开始更新线程

    def _init_widgets(self):
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

    def _configure_grid(self):
        # 正确配置列和行的权重
        self.frame.columnconfigure(0, weight=0)
        self.frame.columnconfigure(1, weight=0)
        self.frame.columnconfigure(2, weight=0)
        self.frame.columnconfigure(51, weight=1)
        self.frame.rowconfigure(1, weight=1)

    # def _start_update_thread(self):
    #     def set_py_list_thread_method():
    #         self.set_py_list(self.py_list)
    #
    #     set_py_list_thread = threading.Thread(target=set_py_list_thread_method)
    #     set_py_list_thread.start()  # 开始线程，注意没有使用 .join()，以保持UI响应性

    def _start_update_thread(self):
        # 修改线程方法为一个命名私有方法
        def set_py_list_thread_method():
            try:
                self.set_py_list(self.py_list)
            except Exception as e:
                logging.error(f"Error in update thread: {e}")  # 记录异常信息
                self.update_thread_event.set()  # 发送事件以通知异常

        set_py_list_thread = threading.Thread(target=set_py_list_thread_method)
        set_py_list_thread.start()  # 保持UI响应性，不使用.join()

# 注意：由于这是一个类，您还需要创建类的实例并调用 get_remote 方法来运行它。
