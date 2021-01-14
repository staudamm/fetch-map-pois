from tkinter import *
from tkinter.filedialog import askdirectory
import os

from fetch import category_to_subcats


# create root window
root = Tk()

# root window title and dimension
root.title("Fetch map POIs")
root.geometry('450x350')


class CatSelector(Frame):
    def __init__(self, parent, *args):
        super(CatSelector, self).__init__(parent, *args)
        Label(self, text='Select POIs').grid()
        self.buttons = {}
        row_idx = 1
        for cat in category_to_subcats.keys():
            btn = Checkbutton(self, text=cat)
            btn.grid(row=row_idx, sticky='W')
            self.buttons[cat] = btn
            row_idx += 1


class LabelledButton:
    def __init__(self, root, label, row):
        self.__lbl = Label(root, text=label)
        self.__lbl.grid(row=row, column=0)

        self.__txt_field = Entry(root, width=20)
        self.__txt_field.grid(row=row, column=1)

    def get(self):
        return self.__txt_field.get()


class DirectorySelector:
    def __init__(self, parent, row):
        self.__lbl = Label(root, text=os.path.abspath('.'))
        self.__lbl.grid(row=row, column=1)

        self.__btn = Button(parent, text='Select target folder', command=self.select)
        self.__btn.grid(row=row, column=0)

    def select(self):
        path = askdirectory(title='Select Folder')  # shows dialog box and return the path
        self.__lbl.config(text=path)

    def get_path(self):
        return self.__lbl.cget('text')


def generate_json():
    print(target_selector.get_path())


key = LabelledButton(root, "API_KEY", 0)
lat = LabelledButton(root, "Latitude", 1)
lng = LabelledButton(root, "Longitude", 2)
project = LabelledButton(root, "Project name", 3)


cat_selector = CatSelector(root)
cat_selector.grid(row=4, column=1)

target_selector = DirectorySelector(root, 5)

generate_btn = Button(root, text="Generate json", command=generate_json)
# Set Button Grid
generate_btn.grid(row=6, column=0)




# Execute Tkinter
root.mainloop()
