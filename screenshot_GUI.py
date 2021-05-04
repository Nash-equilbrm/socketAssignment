from tkinter import*

TITLE = "PIC"

pic_windows =Tk()
pic_windows.title(TITLE)
pic_windows.geometry("600x400")



img = ImageTk.PhotoImage(Image.open(path))
panel = tk.Label(pic_windows, image = img)
panel.pack(side = "bottom", fill = "both", expand = "yes")
root.mainloop()



pic_windows.mainloop()