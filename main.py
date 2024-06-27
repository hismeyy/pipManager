import tkinter as tk

# 创建主窗口
root = tk.Tk()
root.title("Hello World Window")

# 创建一个标签并将其放置在窗口中
label = tk.Label(root, text="Hello, World!")
label.pack()

# 运行主循环
root.mainloop()
