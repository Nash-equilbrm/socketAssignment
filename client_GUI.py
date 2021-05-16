from tkinter import *
from tkinter import ttk
import tkinter as tk

TITLE = "Client "

 #ProcessRunning------------------------------------------------------------------------------------------

def doProcessRunning(event):
    def KILL_PR(event):
        RootPR_KILL = Toplevel(RootPR)
        RootPR_KILL.title(40*" "+"KILL")
        RootPR_KILL.geometry("400x50")
        RootPR_KILL.resizable(0, 0)
        RootPR_KILL.grab_set()

        entry = Entry(RootPR_KILL, width = 40)
        buttonPR_KILL_InSide = Button(RootPR_KILL, text = "KILL",width=10, height = 1)

        entry.place(x = 20, y = 15)
        buttonPR_KILL_InSide.place(x = 280, y = 15)
        

    def SHOW_PR(event):
        print("SHOW")

    def DELETE_PR(event):
        print("DELETE")

    def START_PR(event):
        RootPR_START = Toplevel(RootPR)

        RootPR_START.title(40*" "+"START")
        RootPR_START.geometry("400x50")
        RootPR_START.resizable(0, 0)
        RootPR_START.grab_set()
        
        entry = Entry(RootPR_START, width = 40)
        buttonPR_START_InSide = Button(RootPR_START, text = "START",width=10, height = 1)

        entry.place(x = 20, y = 15)
        buttonPR_START_InSide.place(x = 280, y = 15)

    #------------------------------------------------------
    RootPR = Toplevel(Client_windows)
    RootPR.title(55*" "+"Process")
    RootPR.grab_set()

    RootPR.geometry("500x350")
    
    #KILL
    buttonPR_KILL = Button(RootPR, text = 'KILL',padx =33, pady=20)
    buttonPR_KILL.bind("<Button-1>", KILL_PR)
    buttonPR_KILL.place(x =38, y =15)

    #SHOW
    buttonPR_SHOW = Button(RootPR, text = 'SHOW',padx =28, pady=20)
    buttonPR_SHOW.bind("<Button-1>", SHOW_PR)
    buttonPR_SHOW.place(x =140, y =15)

    #DELETE
    buttonPR_SHOW = Button(RootPR, text = 'DELETE',padx =27, pady=20)
    buttonPR_SHOW.bind("<Button-1>", DELETE_PR)
    buttonPR_SHOW.place(x =245, y =15)

    #Start
    buttonPR_SHOW = Button(RootPR, text = 'START',padx =33, pady=20)
    buttonPR_SHOW.bind("<Button-1>", START_PR)
    buttonPR_SHOW.place(x =350, y =15)

    #Table
    tree =ttk.Treeview(RootPR, column=("c1", "c2", "c3"), show='headings')
    vsb = ttk.Scrollbar(RootPR, orient="vertical", command=tree.yview)
    
    tree.bind('<Button-1>', "break")
   
    tree.column("#1", anchor=tk.CENTER, minwidth=0, width=190, stretch= FALSE)
    tree.heading("#1", text="Name Process")
    tree.column("#2", anchor=tk.CENTER, minwidth=0, width=109 ,stretch=FALSE)
    tree.heading("#2", text="ID Process")
    tree.column("#3", anchor=tk.CENTER, minwidth=0, width=109, stretch=FALSE)
    tree.heading("#3", text="Count Thread")
    tree.place(x = 38, y = 100)
    vsb.place(x=38+190+109+109, y=100, height=227)

#APPRunning-----------------------------------------------------------------------------------------------

def doAPPRunning(event):

    def KILL_AR(event):
        RootAR_KILL = Toplevel(RootAR)
        RootAR_KILL.title(40*" "+"KILL")
        RootAR_KILL.geometry("400x50")
        RootAR_KILL.resizable(0, 0)
        RootAR_KILL.grab_set()

        entry = Entry(RootAR_KILL, width = 40)
        buttonAR_KILL_InSide = Button(RootAR_KILL, text = "KILL",width=10, height = 1)

        entry.place(x = 20, y = 15)
        buttonAR_KILL_InSide.place(x = 280, y = 15)

    def SHOW_AR(event):
        print("SHOW")

    def DELETE_AR(event):
        print("DELETE")

    def START_AR(event):
        RootAR_START = Toplevel(RootAR)
        RootAR_START.title(40*" "+"START")
        RootAR_START.geometry("400x50")
        RootAR_START.resizable(0, 0)
        RootAR_START.grab_set()

        entry = Entry(RootAR_START, width = 40)
        buttonAR_START_InSide = Button(RootAR_START, text = "START",width=10, height = 1)

        entry.place(x = 20, y = 15)
        buttonAR_START_InSide.place(x = 280, y = 15)

    #--------------------------------------------
    RootAR = Toplevel(Client_windows)
    RootAR.title(55*" "+"ListApp")
    RootAR.grab_set()
    RootAR.geometry("500x350")
    #KILL
    buttonAR_KILL = Button(RootAR, text = 'KILL',padx =33, pady=20)
    buttonAR_KILL.bind("<Button-1>", KILL_AR)
    buttonAR_KILL.place(x =38, y =15)
    #SHOW
    buttonPR_SHOW = Button(RootAR, text = 'SHOW',padx =28, pady=20)
    buttonPR_SHOW.bind("<Button-1>", SHOW_AR)
    buttonPR_SHOW.place(x =140, y =15)
    #DELETE
    buttonPR_SHOW = Button(RootAR, text = 'DELETE',padx =27, pady=20)
    buttonPR_SHOW.bind("<Button-1>", DELETE_AR)
    buttonPR_SHOW.place(x =245, y =15)
    #Start
    buttonPR_SHOW = Button(RootAR, text = 'START',padx =33, pady=20)
    buttonPR_SHOW.bind("<Button-1>", START_AR)
    buttonPR_SHOW.place(x =350, y =15)
    #Table
    tree =ttk.Treeview(RootAR, column=("c1", "c2", "c3"), show='headings')
    vsb = ttk.Scrollbar(RootAR, orient="vertical", command=tree.yview)
    
    tree.bind('<Button-1>', "break")
   
    tree.column("#1", anchor=tk.CENTER, minwidth=0, width=190, stretch= FALSE)
    tree.heading("#1", text="Name Application")
    tree.column("#2", anchor=tk.CENTER, minwidth=0, width=109 ,stretch=FALSE)
    tree.heading("#2", text="ID Application")
    tree.column("#3", anchor=tk.CENTER, minwidth=0, width=109, stretch=FALSE)
    tree.heading("#3", text="Count Thread")
    tree.place(x = 38, y = 100)
    vsb.place(x=38+190+109+109, y=100, height=227)

#KEYSTROKE------------------------------------------------------------------------------------------------

def doKEYSTROKE(event):
    def HOOK(event):
        pass 

    def UNLOCK(event):  
        pass

    def PRINT(event):
        pass

    def DELETE(event):
        pass

    #-----------------------------------------------------------------------------------    

    RootK = Toplevel(Client_windows)
    RootK.title(55*" "+"Keystroke")
    RootK.grab_set()
    RootK.geometry("500x350")
    
    #HOOK
    buttonK_HOOK = Button(RootK, text = 'HOOK',padx =33, pady=20)
    buttonK_HOOK.bind("<Button-1>", HOOK)
    buttonK_HOOK.place(x =38, y =15)

    #UNLOCK
    buttonK_UNLOCK = Button(RootK, text = 'UNLOCK',padx =33, pady=20)
    buttonK_UNLOCK.bind("<Button-1>", UNLOCK)
    buttonK_UNLOCK.place(x =140, y =15)

    #PRINT
    buttonK_PRINT = Button(RootK, text = 'PRINT',padx =33, pady=20)
    buttonK_PRINT.bind("<Button-1>", PRINT)
    buttonK_PRINT.place(x =245, y =15)

    #DELETE
    buttonK_DELETE = Button(RootK, text = 'DELETE',padx =33, pady=20)
    buttonK_DELETE.bind("<Button-1>", DELETE)
    buttonK_DELETE.place(x =350, y =15)
  
    #TABLE
    text = Text(RootK)
    text.place(x = 38, y = 90, width = 425, height = 230)
    text.insert('end', '.....')         #insert Text
    text.configure(state='disabled')

#FixRegistry----------------------------------------------------------------------------
def doFixRegistry(event):
    def doBrower(event):
        pass
    def doSendMessenger(event):
        pass
    def Send(event):
        pass
    def Delete(event):
        pass
    def SelectFunction(event):
        def GetValue():
            print("get")
        def SetValue():
            print("Set")
        def DltValue():
            print("Dlt")
        def CreateKey():    
            print("CK")
        def DltKey():
            print("DltK")
        def Select(x):
            switch = {        
                " Get value": GetValue(),
                " Set value": SetValue(),
                " Delete value": DltValue(),
                " Create key": CreateKey(),
                " Delete key": DltKey(),
            }
            return switch.get(x)
        
        Select(FunctionChoosen.get())

       # ' Get value','  value',' Delete value',' Create key', ' Delete key'


    RootFR = Toplevel(Client_windows)
    RootFR.title(55*" "+"Fix Keystroke")
    RootFR.grab_set()
    RootFR.geometry("500x450")

    #Brower---------------
    LinkEntry = Entry(RootFR)
    LinkEntry.place(x = 10, y = 10, width = 370)
    LinkEntry.insert('end', 'Link...')

    Button_Brower = Button(RootFR, text = "Brower")
    Button_Brower.place(x = 390, y = 10, width = 100)
    Button_Brower.bind("<Button-1>", doBrower)

    #SendMessage-----------
    textBox = Text(RootFR)
    textBox.place(x = 10, y = 40, width = 370, height = 100)
    textBox.insert('end', "Message")
    
    Button_SendMessage = Button(RootFR, text = "Send Message")
    Button_SendMessage.place(x = 390, y = 40, width = 100, height = 100)
    Button_SendMessage.bind("<Button-1>", doSendMessenger)

    #Fix------------------
    Label_Fix = Label(RootFR, text  = "Fix Value " + 85*'-')
    Label_Fix.place(x = 10, y = 145)

    #Combobox
    FunctionChoosen = ttk.Combobox(RootFR,state="readonly")
    FunctionChoosen.set("Select function") 
    FunctionChoosen['values'] = (' Get value',' Set value',' Delete value',' Create key', ' Delete key')
    FunctionChoosen.place(x = 10, y =165, width = 477)
    FunctionChoosen.bind('<<ComboboxSelected>>', SelectFunction)

    RootFR.mainloop()
    #Link
    LinkEntry_2 = Entry(RootFR)
    LinkEntry_2.place(x = 10, y = 193, width = 477)
    LinkEntry_2.insert('end', 'Link')


#INIT WINDOW
Client_windows = Tk()
Client_windows.title(80*" "+TITLE)
Client_windows.geometry("600x400")

#Create buttons
InputField = Entry(Client_windows,width = 50)
InputField.place(x = 100,y=50)


Connect_button = Button(Client_windows,text = "Connect",padx =25, pady=1)
Connect_button.place(x = 440, y = 50)

ProcessRunning_button = Button(Client_windows, text = "Process Running", padx = 10, pady = 120)
ProcessRunning_button.bind("<Button-1>", doProcessRunning)
ProcessRunning_button.place(x =54, y =100)

AppRunning_button = Button(Client_windows, text = "App Running", padx = 80, pady = 30)
AppRunning_button.bind("<Button-1>", doAPPRunning)
AppRunning_button.place(x =184, y =100)

Shutdown_button =  Button(Client_windows, text = "Shutdown", padx = 20, pady = 23)
Shutdown_button.place(x =184, y =200)

ScreenShot_button =  Button(Client_windows, text = "PrintScreen", padx = 31, pady = 23)
ScreenShot_button.place(x =289, y =200)

Keystroke_button = Button(Client_windows, text = "Keystroke", padx =25, pady =53)
Keystroke_button.bind("<Button-1>", doKEYSTROKE)
Keystroke_button.place(x = 437, y = 100)

RegistryOverwrite_button = Button(Client_windows, text = "Fix Registry", padx = 82, pady = 30)
RegistryOverwrite_button.bind("<Button-1>", doFixRegistry)
RegistryOverwrite_button.place(x = 184, y = 279)

Exit_button = Button(Client_windows, text="Exit", padx =40, pady = 47)
Exit_button.place(x = 437, y =245)

Client_windows.mainloop()