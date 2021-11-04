
import tkinter as tk
from tkinter import * 
from tkinter import messagebox as mb
  
  
def call():
    res = mb.askquestion('Exit Application', 
                         'Do you really want to exit')
      
    if res == 'yes' :
        root.destroy()
          
    else :
        mb.showinfo('Return', 'Returning to main application')
  
# Driver's code
root = tk.Tk()
canvas = tk.Canvas(root, 
                   width = 200, 
                   height = 200)
  
canvas.pack()
b = Button(root,
           text ='Quit Application',
           command = call)
  
canvas.create_window(100, 100, 
                     window = b)
  
root.mainloop()