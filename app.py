from tkinter import *  # Python 3.x
from Note import *
from Tuner import *
import _thread


class MusicKeys:
    def __init__(self, master):
        self.notes = self.get_note_list()
        self.master = master
        master.title('Simple Script')
        master.resizable(0, 0)
        self.row_counter = 0
        self.mappings = self.get_map_dict()
        self.master_frame = Frame(master)
        self.master_frame.grid(columnspan=1)

        self.title_label = Label(master, text="Music Keys")
        self.title_label.grid(row=self.calc_row())

        self.body = LabelFrame(master, text="Key Mappings")
        self.body.grid(columnspan=2, sticky=W, row=self.calc_row())

        for key in self.mappings:
            Label(master, text=key).grid(row=self.calc_row(), columnspan=1)

        buttons_row = self.calc_row()
        self.save_button = Button(master, text="Save")
        self.save_button.grid(column=0, row=buttons_row)

        self.run_button = Button(master, text="Run")
        self.run_button.grid(column=1, row=buttons_row)

        # Binding buttons to functions
        self.run_button.bind('<Button-1>', self.run_listener)

    def calc_row(self):
        self.row_counter += 1
        return self.row_counter - 1

    #    def gen_body(self, master):

    def get_map_dict(self):
        mappings = {
            str(Note('A', 4)): 'w',
            str(Note('B', 4)): 'a',
            str(Note('C', 5)): 's',
            str(Note('D', 5)): 'd',
            str(Note('D', 4)): ' '
        }
        return mappings

    def run_listener(self, event):
        _thread.start_new_thread(run, (self.mappings,))

    def get_note_list(self):
        ans = []
        notes = ['A', 'B', 'C', 'D', 'E', 'F']
        octaves = [3, 4, 5, 6]
        for octave in octaves:
            for note in notes:
                ans.append(note + str(octave))
        return ans


root = Tk()
sr = MusicKeys(root)
root.mainloop()
