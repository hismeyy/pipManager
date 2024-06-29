import tkinter as tk
import webbrowser
from tkinter import ttk


class About:
    def __init__(self, frame):
        self.frame = frame

    def get_about(self):
        # 软件信息标签
        info = [
            ("软件名称:", "PiPManager"),
            ("版本:", "1.0.0"),
            ("开发者:", "MaxCosmos, Fang"),
            ("许可证:", "GPL（GNU General Public License）")
        ]

        # 添加软件信息标签
        for i, (label, text) in enumerate(info):
            ttk.Label(self.frame, text=label, font=("Helvetica", 10, "bold")).grid(row=i, column=0, sticky=tk.W,
                                                                                   padx=10, pady=5)
            ttk.Label(self.frame, text=text, font=("Helvetica", 10)).grid(row=i, column=1, sticky=tk.W, padx=10, pady=5)

        # 添加开发者信息标签
        dev_info_row = len(info)
        ttk.Label(self.frame, text="源码地址:", font=("Helvetica", 10, "bold")).grid(row=dev_info_row, column=0,
                                                                                     sticky=tk.W, padx=10, pady=5)
        link = ttk.Label(self.frame, text="https://github.com/hismeyy/pipManager", font=("Helvetica", 10, "underline"),
                         foreground="blue", cursor="hand2")
        link.grid(row=dev_info_row, column=1, sticky=tk.W, padx=10, pady=5)
        link.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/hismeyy/pipManager"))

        # 添加版权声明标签
        copyright_row = dev_info_row + 2
        ttk.Label(self.frame, text="版权声明:", font=("Helvetica", 10, "bold")).grid(row=copyright_row, column=0,
                                                                                     sticky=tk.W, padx=10, pady=5)
        ttk.Label(self.frame, text="© 2024 MaxCosmos 和 Fang. 保留所有权利。", font=("Helvetica", 10)).grid(
            row=copyright_row, column=1, sticky=tk.W, padx=10, pady=5)

        # 添加更新日志标签
        changelog_row = copyright_row + 1
        ttk.Label(self.frame, text="更新日志:", font=("Helvetica", 10, "bold")).grid(row=changelog_row, column=0,
                                                                                     sticky=tk.W, padx=10, pady=5)
        ttk.Label(self.frame, text="版本 1.0.0 - 初始发布", font=("Helvetica", 10)).grid(row=changelog_row, column=1,
                                                                                         sticky=tk.W, padx=10, pady=5)

        # 添加感谢名单标签
        thanks_row = changelog_row + 1
        ttk.Label(self.frame, text="感谢名单:", font=("Helvetica", 10, "bold")).grid(row=thanks_row, column=0,
                                                                                     sticky=tk.W, padx=10, pady=5)
        ttk.Label(self.frame, text="感谢所有为PiPManager开发做出贡献的人员和组织。", font=("Helvetica", 10)).grid(
            row=thanks_row, column=1, sticky=tk.W, padx=10, pady=5)
