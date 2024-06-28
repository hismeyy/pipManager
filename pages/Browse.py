import ttkbootstrap as ttk

from utils.PipApi import PipApi


class Browse:
    def __init__(self, frame):
        self.pip_api = PipApi()
        self.frame = frame

    def get_browse(self):
        # 在框架中添加标签和按钮示例
        label = ttk.Label(self.frame, text=f"Hello World")
        label.pack(padx=10, pady=10)
        button = ttk.Button(self.frame, text=f"Button")
        button.pack(padx=10, pady=10)
