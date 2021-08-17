import tkinter as tk
from tkinter import *

# Button options for all pages.
BTN_OPTS = [dict(text="Button 1", fg='white'),
            dict(text="Button 2", fg='blue'),
            dict(text="Button 3", fg='orange')]


def make_buttons(parent, bg_colour):
    return [Button(parent, bg=bg_colour, **opts) for opts in BTN_OPTS]


class Tkinter(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, SecondPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        print(type(frame))
        frame.tkraise()
        frame.winfo_toplevel().geometry("860x864")
        frame.configure(bg='#000000')


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        Button(
                self, 
                text='SecondPage',
                compound='left',
                command=lambda: controller.show_frame(SecondPage)
            ).pack()
        for btn in make_buttons(self, 'Pink'):
            btn.pack()


class SecondPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        Button(self, text='StartPage',
               command=lambda: controller.show_frame(StartPage)).pack()
        for btn in make_buttons(self, 'green'):
            btn.pack()

app = Tkinter()
app.mainloop()