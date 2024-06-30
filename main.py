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

for title in notebook_titles:
    frame = ttk.Frame(note)
    note.add(frame, text=title)

    if title == "本地":
        Local(frame).get_local()
    elif title == '关于':
        About(frame).get_about()
    elif title == '远程':
        Remote(frame).get_remote()

root.mainloop()