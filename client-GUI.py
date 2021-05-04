from tkinter import *

TITLE = "Client "


#INIT WINDOW
Client_windows = Tk()
Client_windows.title(TITLE)
Client_windows.geometry("600x400")

#Create buttons
InputField = Entry(Client_windows,width = 50)
InputField.place(x = 100,y=50)


Connect_button = Button(Client_windows,text = "Kết nối",padx =25, pady=1)
Connect_button.place(x = 440, y = 50)

ProcessRunning_button = Button(Client_windows, text = "Process Running", padx = 10, pady = 120)
ProcessRunning_button.place(x =54, y =100)

AppRunning_button = Button(Client_windows, text = "App Running", padx = 80, pady = 30)
AppRunning_button.place(x =184, y =100)

Shutdown_button =  Button(Client_windows, text = "Tắt máy", padx = 10, pady = 23)
Shutdown_button.place(x =184, y =200)

ScreenShot_button =  Button(Client_windows, text = "Chụp màn hình", padx = 31, pady = 23)
ScreenShot_button.place(x =268, y =200)

Keystroke_button = Button(Client_windows, text = "Keystroke", padx =25, pady =53)
Keystroke_button.place(x = 437, y = 100)

RegistryOverwrite_button = Button(Client_windows, text = "Sửa Registry", padx = 82, pady = 30)
RegistryOverwrite_button.place(x = 184, y = 279)

Exit_button = Button(Client_windows, text="Thoát", padx =36, pady = 47)
Exit_button.place(x = 437, y =245)





Client_windows.mainloop()
