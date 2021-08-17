import tkinter as tk
import tkinter.ttk as ttk
# from tkinter import *
# from tkinter import PhotoImage
# from tkinter.ttk import * 
        
class App(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        super().__init__()
        
        self.title("MONITOR DE CAMARAS")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True) 
        
        self.frame_cameras = []
        self.dimension_position(600, 400)
        
        icon = tk.PhotoImage(file='./assets/download.png')
        
        for i in range(3):
            self.frame_cameras.append(tk.Frame(container, bd=2, relief='ridge'))
            self.frame_cameras[i].pack(side='left', fill='both', expand=1, padx=5, pady=5)
            
            button = ttk.Button(self.frame_cameras[i],
                      image=icon,
                      compound='left',
                      text='descarga')
            button.pack(side='top', expand=True)
            
            
        Frame_Controls(container)
        self.mainloop()
        
             
    

class Frame_Controls(tk.Frame):
    
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        
        self.download_icon = tk.PhotoImage(file='./assets/download.png')
        
        self.button = ttk.Button(
                parent,
                image=self.download_icon,
                text="Download",
                compound=tk.LEFT,
                command=lambda: print('hola mundo')
            )
        self.button.pack(
                    side='bottom',
                   ipadx=5, 
                   ipady=5, 
                   expand=False)    

App()