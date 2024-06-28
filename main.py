import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from pages.Browse import Browse

# 初始化主窗口
root = ttk.Window(themename="cosmo", alpha=0.95)
root.title("PiPManager")
root.geometry("800x600")

root.place_window_center()

notebook_titles = ["浏览", "已安装", "更新"]
note = ttk.Notebook()
note.pack(fill=BOTH, side=TOP, ipady=250)

for title in notebook_titles:
    frame = ttk.Frame(note)
    note.add(frame, text=title)

    if title == "浏览":
        Browse(frame).get_browse()

root.mainloop()

# # 创建顶部的工具栏
# toolbar = ttk.Frame(root)
# toolbar.pack(side=TOP, fill=X)
#
# # 侧边栏
# sidebar = ttk.Frame(root)
# sidebar.pack(side=LEFT, fill=Y)
#
# # 搜索框
# search_frame = ttk.Frame(toolbar)
# search_frame.pack(side=LEFT, padx=10)
# # search_icon = PhotoImage(file='search_icon.png')  # 使用一个搜索图标
# # search_label = ttk.Label(search_frame, image=search_icon)
#
# # search_label.pack(side=LEFT)
# search_entry = ttk.Entry(search_frame)
# search_entry.pack(side=LEFT, padx=5)
#
# # 标签
#
#
# # 选项下拉菜单
# more_button = ttk.Menubutton(toolbar, text="选项", bootstyle="light")
# more_button.pack(side=RIGHT, padx=10)
# menu = ttk.Menu(more_button)
# option_var = ttk.StringVar()
#
# more_button_options = ["选项1", "选项2", "选项3"]
# for option in more_button_options:
#     menu.add_radiobutton(label=option, value=option, variable=option_var)
# more_button['menu'] = menu
#
# # 左侧分类栏
# sidebar = ttk.Frame(sidebar)
# sidebar.pack(side=LEFT, fill=Y, padx=5)
#
# categories = ["分类", "组", "仓库"]
# for category in categories:
#     cat_frame = ttk.Frame(sidebar)
#     cat_frame.pack(pady=10)
#     cat_label = ttk.Label(cat_frame, text=category, bootstyle="info")
#     cat_label.pack(side=LEFT)
#     cat_arrow = ttk.Label(cat_frame, text="➔", bootstyle="info")
#     cat_arrow.pack(side=RIGHT)
