from tkinter import *

root = Tk()

frame = Frame(root, width=480, height=320)
frame.pack()

label = Label(frame, text='hola mundo!')
#label.pack() #empaqueta y distribuye uniformemetne a su manera al tamanio de los widwets el contenido
label.place(x=100, y=100)

root.mainloop()