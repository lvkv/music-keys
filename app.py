from tkinter import *  # Python 3.x
import _thread
from Note import *
from Tuner import *


class MusicKeys:
    def __init__(self, master):
        # initialize local vars
        self.notes = self.get_note_list()
        self.master = master
        master.title('Music Keys')
        master.resizable(0, 0)
        self.row_counter = 0
        self.mappings = self.get_map_dict()
        self.note_list = self.get_note_list()

        # container
        self.master_frame = Frame(master)
        self.master_frame.grid(columnspan=1)
        heading = Label(self.master_frame, text='Music Keys', font='Helvetica 18 bold')
        heading.grid(columnspan=2, row=self.calc_row(), padx=(50, 50), pady=(5, 10))

        # containers
        self.body = LabelFrame(self.master_frame, text="Key Mappings")
        self.body.grid(columnspan=2, row=self.calc_row())
        self.extra = LabelFrame(self.master_frame, text="New Maps")
        self.extra.grid(columnspan=2, row=self.calc_row(), pady=(10, 5))
        self.buttons = LabelFrame(self.master_frame, text="Save and Run")
        self.buttons.grid(columnspan=2, row=self.calc_row(), pady=(5, 10))

        # show key maps
        for key in self.mappings:
            key_row = self.calc_row()
            Label(self.body, text=self.mappings[key]).grid(row=key_row, column=0)
            variable = StringVar(self.master_frame)
            variable.set(key)
            OptionMenu(self.body, variable, *self.note_list).grid(row=key_row, column=1)

        # button to open dialog for adding new key
        self.add_button = Button(self.extra, text="Add Key", command=self.open_add_dialog)
        self.add_button.grid(row=self.calc_row(), column=1, padx=(5, 1), pady=(2, 2))

        # button to apply changes to key maps
        buttons_row = self.calc_row()
        self.save_button = Button(self.buttons, text="Save")
        self.save_button.grid(column=0, row=buttons_row, padx=(5, 5), pady=(2, 2))

        # button to start listening
        self.run_button = Button(self.buttons, text="Run")
        self.run_button.grid(column=1, row=buttons_row, padx=(5, 5), pady=(2, 2))

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

    def get_note_list(self):
        ans = []
        notes = ['A', 'B', 'C', 'D', 'E', 'F']
        octaves = [3, 4, 5, 6]
        for octave in octaves:
            for note in notes:
                ans.append(note + str(octave))
        return ans

    def run_listener(self, event):
        _thread.start_new_thread(run, (self.mappings,))

    def open_add_dialog(self):
        self.master.update()
        key_add_dialog = AddDialog(self.master, self.mappings)
        self.master.wait_window(key_add_dialog.top)


class AddDialog:
    def __init__(self, parent, note_list):
        top = self.top = Toplevel(parent)
        Label(top, text="Add Keys").grid()

        self.key = Entry(top)
        self.key.grid(row=0, column=0)

        variable = StringVar(parent)
        variable.set(note_list[0])
        OptionMenu(parent, variable, *note_list).grid(row=0, column=1)

        b = Button(top, text="OK", command=self.ok)
        b.grid(row=1)

    def ok(self):
        print("value is", self.key.get())

        self.top.destroy()


root = Tk()
sr = MusicKeys(root)
root.mainloop()
