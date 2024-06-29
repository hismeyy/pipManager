import threading
import tkinter as tk

import ttkbootstrap as ttk

from utils.PipApi import PipApi


class Local:
    def __init__(self, frame):
        self.pip_api = PipApi()
        self.frame = frame

    def set_py_list(self, py_list):
        """
        设置py包list
        :param py_list:
        :return:
        """
        items = self.pip_api.get_pip_list_api()
        for item in items:
            py_list.insert("", tk.END, values=item)

    def get_package_version_last(self, package_name):
        package_version_list = self.pip_api.get_package_versions_api(package_name)
        if len(package_version_list) != 0:
            package_version_last = package_version_list[0]
            return package_version_last

    def update_py_list(self, py_list):
        """
        修改py包List
        :param py_list:
        :return:
        """

        def get_package_version_last_and_update_list_thread_method(package_name, new_values, item_id):
            package_version_last = self.get_package_version_last(package_name)
            new_values.append(package_version_last)
            py_list.item(item_id, values=new_values)

        # 获取所有行的item ID
        items = py_list.get_children()
        for item_id in items:
            # 假设我们要修改第一个item的第3列元素
            current_values = py_list.item(item_id, "values")

            # 修改第3列元素（索引为2）
            new_values = list(current_values)

            # 查询包对应的最高版本，开启多线程设置
            get_package_version_last_and_update_list_thread = threading.Thread(
                target=get_package_version_last_and_update_list_thread_method,
                args=(current_values[0], new_values, item_id))
            get_package_version_last_and_update_list_thread.start()

    def get_local(self):
        # 在框架中添加标签和按钮示例

        # 布局方式
        # 1. pack() 布局管理器
        # 2. grid() 布局管理器
        # 3. place() 布局管理器

        uninstall_button = ttk.Button(self.frame, text="卸载")
        update_button = ttk.Button(self.frame, text="更新")

        # 布局按钮
        uninstall_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        update_button.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # 创建 Treeview 作为带有表头的列表框
        py_list = ttk.Treeview(self.frame, columns=("c1", "c2", "c3"), show="headings")
        py_list.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        # 设置列标题
        py_list.heading("c1", text="软件包", anchor="w")
        py_list.heading("c2", text="当前版本", anchor="w")
        py_list.heading("c3", text="最高版本", anchor="w")
        # 设置列宽
        py_list.column("c1", width=150)
        py_list.column("c2", width=150)
        py_list.column("c3", width=150)

        def set_py_list_thread_method():
            self.set_py_list(py_list)

        set_py_list_thread = None

        def update_py_list_thread_method():
            set_py_list_thread.join()
            self.update_py_list(py_list)

        # 向列表中添加一些项
        set_py_list_thread = threading.Thread(target=set_py_list_thread_method)
        set_py_list_thread.start()

        update_py_list_thread = threading.Thread(target=update_py_list_thread_method)
        update_py_list_thread.start()

        # 使得列自动扩展以填满空白区域
        self.frame.columnconfigure(0, weight=0)
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(1, weight=1)
