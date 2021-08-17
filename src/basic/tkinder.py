from tkinter import *

root = Tk()

root.title('Agenda')
root.resizable(1, 1) # vertical, horizontal 
#root.iconbitman('hola.ico') # tiene que ser en formato ico

frame = Frame(root) # tenemos un marco en la raiz
#frame.pack(side='right', anchor='e') # qeu se distribuya dentro de la ventan principal todo al centro
# se empaqueta en el side que nosotros le demos bottom, left, right
# el valor de anchor es lado de anclaje 
frame.pack(fill='both', expand='1') # para que el wodget hijo pueda tomar toda el tamanio de su widget padre
frame.config(width=480, height=320) # dimensiones del frame
frame.config(cursor='pirate') # modifica el cursor dentro del espacio del frame
frame.config(bg='lightblue') #color del frame
frame.config(bd=25) #25 pixels de borde
frame.config(relief='sunken') # cambiando tipo de borde

root.config(cursor='arrow') # modifica el cursor dentro del espacio del frame
root.config(bg='blue') #color del frame
root.config(bd=15) #25 pixels de borde
root.config(relief='ridge') # cambiando tipo de borde


# debe ir debajo de todo
root.mainloop()