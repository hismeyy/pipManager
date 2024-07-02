import threading

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from pages.About import About
from pages.Local import Local
from pages.Remote import Remote


class MainWin():
    def __init__(self):
        # 初始化主窗口
        self.root = ttk.Window(themename="cosmo", alpha=0.95)
        self.root.title("PiPManager")
        self.root.geometry("600x500")
        self.root.minsize(600, 500)
        self.root.place_window_center()
        self.root.attributes("-disabled", True)

        self.notebook_titles = ["本地", "远程", "设置", "关于"]

        # 本地：用于浏览，操作本地的py包，可以进行查看，搜索，卸载，升级等功能
        # 远程：用于获取可安装的py包，可以进行查看，搜索，安装等功能
        # 设置：设置python环境，pip镜像，语言等
        # 关于：关于PiPManager

        self.note = ttk.Notebook()
        self.note.pack(fill=BOTH, expand=True)  # 修改为全局填充

        threading.Thread(target=self.init_notebook).start()
        self.show_waiting_window()

    def start(self):
        self.root.mainloop()

    def init_notebook(self):
        thread_list = []
        for title in self.notebook_titles:
            frame = ttk.Frame(self.note)
            self.note.add(frame, text=title)
            if title == "本地":
                local = Local(frame)
                local_thread = threading.Thread(target=local.get_local)
                local_thread.start()
                thread_list.append(local_thread)
            elif title == '远程':
                remote = Remote(frame)
                remote_thread = threading.Thread(target=remote.get_remote())
                remote_thread.start()
                thread_list.append(remote_thread)
            elif title == '设置':
                pass
            elif title == '关于':
                about = About(frame)
                about_thread = threading.Thread(target=about.get_about())
                about_thread.start()
                thread_list.append(about_thread)

        for thread in thread_list:
            thread.join()

        self.close_waiting_window()

    def show_waiting_window(self):
        self.waiting_window = ttk.Toplevel(self.root)
        self.waiting_window.title("请稍等")
        self.waiting_window.geometry("200x20")
        self.waiting_window.overrideredirect(True)  # 去掉窗口边框
        self.waiting_window.grab_set()  # 模态窗口
        self.waiting_window.attributes("-disabled", True)

        window_width = 200
        window_height = 50

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)

        self.waiting_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

        label = ttk.Label(self.waiting_window, text="数据加载中，请稍候...", foreground="red")
        label.pack(expand=True)
        label.place(relx=0.5, rely=0.5, anchor='center')

    def close_waiting_window(self):
        if self.waiting_window:
            self.waiting_window.destroy()
            self.waiting_window = None
            self.root.attributes("-disabled", False)


if __name__ == '__main__':
    main_win = MainWin()
    main_win.start()
