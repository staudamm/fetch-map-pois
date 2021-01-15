from tkinter import *
from tkinter.filedialog import askdirectory
import os
import json
from fetch import category_to_subcats, create_map_pois, validate_gui_data, API_KEY


class CatSelector(Frame):
    def __init__(self, parent, *args):
        super(CatSelector, self).__init__(parent, *args)
        Label(self, text='Select POIs').grid()
        self.buttons = {}
        row_idx = 1
        for cat in category_to_subcats.keys():
            cb = IntVar()
            btn = Checkbutton(self, text=cat, variable=cb)
            btn.grid(row=row_idx, sticky='W')
            self.buttons[cat] = cb
            row_idx += 1

    def get(self):
        return {cat: cb.get() for cat, cb in self.buttons.items()}


class LabelledButton:
    WIDTH = 40

    def __init__(self, parent, label, row, text=''):
        self.__lbl = Label(parent, text=label)
        self.__lbl.grid(row=row, column=0)

        self.__txt_field = Entry(parent, width=self.WIDTH)
        self.__txt_field.grid(row=row, column=1)

        if text:
            self.__txt_field.insert(0, text)

    def get(self):
        return self.__txt_field.get()


class DirectorySelector:
    def __init__(self, parent, row):
        self.__lbl = Label(parent, text='')
        self.__lbl.grid(row=row, column=1)

        self.__btn = Button(parent, text='Select target folder', command=self.select)
        self.__btn.grid(row=row, column=0)

    def select(self):
        path = askdirectory(title='Select Folder')  # shows dialog box and return the path
        self.__lbl.config(text=path)

    def get(self):
        return self.__lbl.cget('text')


class Gui(Tk):
    __size = '550x350'
    __title = "Fetch map POIs"

    def __init__(self, **kwargs):
        super(Gui, self).__init__(**kwargs)
        self.title(self.__title)
        self.geometry(self.__size)
        self.__create_buttons()

    def __create_buttons(self):
        self.key = LabelledButton(self, "API_KEY", 0, text=API_KEY)
        self.lat = LabelledButton(self, "Latitude", 1)
        self.lng = LabelledButton(self, "Longitude", 2)
        self.project = LabelledButton(self, "Project name", 3)
        self.cat_selector = CatSelector(self)
        self.cat_selector.grid(row=4, column=1)
        self.target_selector = DirectorySelector(self, 5)

        self.generate_btn = Button(self, text="Generate json", command=self.generate_json)
        self.generate_btn.grid(row=6, column=0)

    def fetch_data(self):
        data = {'api_key': self.key.get(),
                'lat_lng': {'lat': self.lat.get(), 'lng': self.lng.get()},
                'project_name': self.project.get(),
                'target_path': self.target_selector.get(),
                'categories': self.cat_selector.get()
                }
        return data

    def generate_json(self):
        data = self.fetch_data()
        validate_gui_data(data)
        json_body = create_map_pois(data)
        target_file = os.path.join(data['target_path'], data['project_name'] + '_pois.json')

        with open(target_file, 'w') as f:
            json.dump(json_body, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    gui = Gui()
    gui.mainloop()
