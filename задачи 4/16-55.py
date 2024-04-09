from tkinter import *

root = Tk()

top = Toplevel(root)

def open_dialog():
    dialog = Toplevel(root)
    dialog.title("hehehheheh")
    dialog.geometry("1500x1500")

button = Button(root, text="Open Dialog", command=open_dialog)
button.pack()

top.mainloop()