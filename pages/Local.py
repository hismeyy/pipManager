import ttkbootstrap as ttk

from utils.PipApi import PipApi


class Local:
    def __init__(self, frame):
        self.pip_api = PipApi()
        self.frame = frame

    def get_local(self):
        # 在框架中添加标签和按钮示例

        # 布局方式
        # 1. pack() 布局管理器
        # 2. grid() 布局管理器
        # 3. place() 布局管理器

        label = ttk.Label(self.frame, text=f"Hello World")
        label.grid(row=5, column=1, padx=20, pady=20)
        button = ttk.Button(self.frame, text=f"Button")
        button.grid(row=5, column=2, padx=10, pady=10)
