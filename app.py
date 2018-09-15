from tkinter import *  # Python 3.x
import _thread
from const import VK_CODE
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
        self.mapping_row = 0
        self.variables = []

        # containers
        self.master_frame = Frame(master)
        self.master_frame.grid(columnspan=1)
        heading = Label(self.master_frame, text='Music Keys', font='Helvetica 18 bold')
        heading.grid(columnspan=2, row=self.calc_row(), padx=(50, 50), pady=(5, 10))

        # containers
        self.body = LabelFrame(self.master_frame, text="Key Mappings")
        self.body.grid(columnspan=2, row=self.calc_row())
        self.extra = LabelFrame(self.master_frame, text="New Maps")
        self.extra.grid(columnspan=2, row=self.calc_row(), pady=(10, 5))
        self.threshbox = LabelFrame(self.master_frame, text="Threshold")
        self.threshbox.grid(columnspan=2, row=self.calc_row(), pady=(5, 5))
        self.buttons = LabelFrame(self.master_frame, text="Save and Run")
        self.buttons.grid(columnspan=2, row=self.calc_row(), pady=(5, 10))

        # show key maps
        for key in self.mappings:
            key_row = self.mapping_row
            Label(self.body, text=self.mappings[key]).grid(row=key_row, column=0)
            variable = StringVar(self.master_frame)
            variable.set(key)
            OptionMenu(self.body, variable, *self.note_list).grid(row=key_row, column=1)
            self.variables.append(variable)
            self.mapping_row += 1

        # button to open dialog for adding new key
        self.add_button = Button(self.extra, text="Add Key", command=self.open_add_dialog)
        self.add_button.grid(row=self.calc_row(), column=1, padx=(5, 0), pady=(2, 2))
        self.slider = Scale(self.threshbox, from_=10, to=60, orient=HORIZONTAL)
        self.slider.grid(row=self.calc_row(), columnspan=2)
        self.slider.set(30)

        # button to apply changes to key maps
        buttons_row = self.calc_row()
        self.save_button = Button(self.buttons, text="Save", command=self.apply_changes)
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
            # str(Note('A', 4)): 'w',
            # str(Note('B', 4)): 'a',
            # str(Note('C', 5)): 's',
            # str(Note('D', 5)): 'd',
            # str(Note('D', 4)): 'spacebar'
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
        input_dict = {}
        key_add_dialog = AddDialog(self.master, self.note_list, input_dict)
        self.master.wait_window(key_add_dialog.top)
        try:
            if input_dict[0] not in VK_CODE:


            for key in input_dict:
                self.mappings[input_dict[key]] = key
            self.update_mappings(input_dict[key])
        except:
            print('You did not change anything!')

    def update_mappings(self, key):
        Label(self.body, text=self.mappings[key]).grid(row=self.mapping_row, column=0)
        variable = StringVar(self.master_frame)
        variable.set(key)
        OptionMenu(self.body, variable, *self.note_list).grid(row=self.mapping_row, column=1)
        self.mapping_row += 1
        self.variables.append(variable)
        self.master.update()
        return

    def apply_changes(self):
        set_threshold(self.slider.get())
        for i in range(self.mapping_row):
            self.mappings[self.variables[i].get()] = self.body.grid_slaves(i, 0)[0].cget("text")


class AddDialog:
    def __init__(self, parent, note_list, input_dict):
        self.input_dict = input_dict
        top = self.top = Toplevel(parent)
        Label(top, text="Add Keys").grid()

        self.key = Entry(top)
        self.key.grid(row=0, column=0)

        self.variable = StringVar(top)
        self.variable.set(note_list[0])
        OptionMenu(top, self.variable, *note_list).grid(row=0, column=1)

        b = Button(top, text="OK", command=self.ok)
        b.grid(row=1)

    def ok(self):
        self.input_dict[self.key.get()] = self.variable.get()
        self.top.destroy()


root = Tk()
sr = MusicKeys(root)
root.mainloop()
