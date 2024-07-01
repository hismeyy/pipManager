import threading

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from pages.About import About
from pages.Local import Local
from pages.Remote import Remote

# 初始化主窗口
root = ttk.Window(themename="cosmo", alpha=0.9)
root.title("PiPManager")
root.geometry("600x500")
root.minsize(600, 500)

root.place_window_center()

notebook_titles = ["本地", "远程", "设置", "关于"]

# 本地：用于浏览，操作本地的py包，可以进行查看，搜索，卸载，升级等功能
# 远程：用于获取可安装的py包，可以进行查看，搜索，安装等功能
# 设置：设置python环境，pip镜像，语言等
# 关于：关于PiPManager

note = ttk.Notebook(bootstyle="light")
note.pack(fill=BOTH, expand=True)  # 修改为全局填充


def set_note_page():
    style = ttk.Style()
    style.configure("Modern.Vertical.TScrollbar",
                    gripcount=0,
                    background="#f0f0f0",  # 背景颜色
                    troughcolor="#d0d0d0",  # 槽颜色
                    bordercolor="#b0b0b0",  # 边框颜色
                    arrowcolor="#606060",  # 箭头颜色
                    darkcolor="#a0a0a0",  # 鼠标悬停时的颜色
                    lightcolor="#ffffff",  # 滚动条被点击时的颜色
                    width=10,  # 宽度
                    margin=5,  # 边距
                    troughrelief="flat"  # 槽的浮雕效果设置为平的
                    )

    for title in notebook_titles:
        frame = ttk.Frame(note)
        note.add(frame, text=title)

        if title == "本地":
            def set_local():
                Local(frame).get_local()

            threading.Thread(target=set_local).start()

        elif title == '远程':
            def set_remote():
                Remote(frame).get_remote()

            threading.Thread(target=set_remote).start()

        elif title == '关于':
            def set_about():
                About(frame).get_about()

            threading.Thread(target=set_about).start()


threading.Thread(target=set_note_page).start()

root.mainloop()
