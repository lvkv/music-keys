from tkinter import *  # Python 3.x
from Note import *

class MusicKeys:

    def __init__(self, master):
        self.master = master
        master.title('Simple Script')
        master.resizable(0, 0)
        self.row_counter=0
        self.keys=self.get_dict();

        self.master_frame = Frame(master)
        self.master_frame.grid(columnspan=1)

        self.title_label = Label(master, text="Music Keys")
        self.title_label.grid(row=self.calc_row())

        self.body = LabelFrame(master, text="Key Mappings")
        self.body.grid(columnspan=2, sticky=W, row=self.calc_row())

        
        for key in self.keys:
            Label(master, text=key).grid(row=self.calc_row())

        buttons_row = self.calc_row()
        self.save_button = Button(master, text="Save")
        self.save_button.grid(column=0, row=buttons_row)

        self.run_button = Button(master, text="Run")
        self.run_button.grid(column=1, row=buttons_row)

    def calc_row(self):
        self.row_counter+=1
        return self.row_counter - 1

#    def gen_body(self, master):

    def get_dict(self):
        mappings = {
            'w': Note('A', 4),
            'a': Note('B', 4),
            's': Note('C', 5),
            'd': Note('D', 5),
            " ": Note('D', 4)
        }
        return mappings

root = Tk()
sr = MusicKeys(root)
root.mainloop()
