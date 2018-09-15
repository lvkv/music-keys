from tkinter import *  # Python 3.x
class SimpleScript:
    def __init__(self, master):
        master.title('Simple Script')
        master.resizable(0, 0)

root = Tk()
sr = SimpleScript(root)
root.mainloop()