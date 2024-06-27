import ttkbootstrap as ttk

# 创建主窗口
root = ttk.Window(themename="superhero")
root.title("TTKBootstrap Example")
root.geometry("300x200")

# 添加一个标签
label = ttk.Label(root, text="Hello", font=("Helvetica", 16))
label.pack(pady=20)

# 添加一个按钮
button = ttk.Button(root, text="Click Me")
button.pack(pady=10)

# 运行主循环
root.mainloop()
