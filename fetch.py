import os
import json

from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askdirectory

from googleplaces import GooglePlaces, types
from config import API_KEY


''' ---------------------------------
    
    SECTION 1: LogIc

--------------------------------- '''


category_to_subcats = {
    'bakery': [types.TYPE_BAKERY],
    'medical': [types.TYPE_DENTIST, types.TYPE_DOCTOR, types.TYPE_HOSPITAL],
    'culture': [types.TYPE_CHURCH, types.TYPE_MOVIE_THEATER, types.TYPE_ART_GALLERY, types.TYPE_MUSEUM],
    'gastronomy': [types.TYPE_RESTAURANT, types.TYPE_CAFE, types.TYPE_BAR],
    'post': [types.TYPE_POST_BOX, types.TYPE_POST_OFFICE],
    'shop': [types.TYPE_SHOE_STORE, types.TYPE_GROCERY_OR_SUPERMARKET]
}


def create_obj_dict(subcat, name, lat, lng):
    return {
        "type": "Feature",
        "properties": {
          "name": name,
          "subCat": subcat
        },
        "geometry": {
          "type": "Point",
          "coordinates": [lat, lng]
        }
      }


def fetch_for_category(places_api, category, coordinates, radius):
    subcat_list = category_to_subcats[category]
    query_result = places_api.nearby_search(
        lat_lng=coordinates,
        types=subcat_list,
        radius=radius)

    feature_list = []
    for place in query_result.places:
        subcats = set(subcat_list) & set(place.types)
        feature_list.append(
            create_obj_dict(
                subcats.pop(),
                place.name,
                float(place.geo_location['lat']),
                float(place.geo_location['lng'])
            ))
    return {"type": "FeatureCollection", "features": feature_list}


def create_map_pois(gui_data):
    places_api = GooglePlaces(gui_data['api_key'])

    pois = {}
    for cat in gui_data['categories']:
        pois[cat+"Pois"] = fetch_for_category(places_api, cat, gui_data['lat_lng'], gui_data['radius'])
    return pois


def validate_gui_data(data):
    errors = []
    if not data['lat_lng']['lat']:
        errors.append('Latitude must not be empty')
    if not data['lat_lng']['lng']:
        errors.append('Longitude must not be empty')
    if not data['radius']:
        errors.append('Radius must not be empty')
    else:
        data['radius'] = int(data['radius'])
    if not data['project_name']:
        errors.append('Project must be named')
    if not len(data['categories']):
        errors.append('At least one category must be selected')
    if not data['target_path']:
        errors.append('TargetPath must be specified')
    return data, errors


''' ---------------------------------

    SECTION 2: UI

--------------------------------- '''


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
        selected_cats = []
        for cat, cb in self.buttons.items():
            if cb.get():
                selected_cats.append(cat)
        return selected_cats


class LabelledButton:
    def __init__(self, parent, label, row, text=''):
        self.__lbl = Label(parent, text=label)
        self.__lbl.grid(row=row, column=0)

        self.__txt_field = Entry(parent, width=TEXT_WIDTH)
        self.__txt_field.grid(row=row, column=1)

        if text:
            self.__txt_field.insert(0, text)

    def get(self):
        return self.__txt_field.get()


class DirectorySelector:
    def __init__(self, parent, row):
        self.__lbl = Label(parent, text='', width=TEXT_WIDTH)
        self.__lbl.grid(row=row, column=1)

        self.__btn = Button(parent, text='Select target folder', command=self.select)
        self.__btn.grid(row=row, column=0)

    def select(self):
        path = askdirectory(title='Select Folder')  # shows dialog box and return the path
        self.__lbl.config(text=path)

    def get(self):
        return self.__lbl.cget('text')


TEXT_WIDTH = 35


class Gui(Tk):
    __size = '530x380'
    __title = "Fetch map POIs"

    def __init__(self, **kwargs):
        super(Gui, self).__init__(**kwargs)

        p1 = PhotoImage(file='./icon.png')
        self.iconphoto(False, p1)
        self.title("Fetch map POIs")

        self.title(self.__title)
        self.geometry(self.__size)
        self.__create_buttons()

    def __create_buttons(self):
        self.key = LabelledButton(self, "API_KEY", 0, text=API_KEY)
        self.lat = LabelledButton(self, "Latitude", 1)
        self.lng = LabelledButton(self, "Longitude", 2)
        self.radius = LabelledButton(self, "Radius (meter)", 3, text='2000')
        self.project = LabelledButton(self, "Project name", 4)
        self.cat_selector = CatSelector(self)
        self.cat_selector.grid(row=5, column=1)
        self.target_selector = DirectorySelector(self, 6)

        self.generate_btn = Button(self, text="Generate json", command=self.generate_json)
        self.generate_btn.grid(row=7, column=0)

    def fetch_data(self):
        data = {'api_key': self.key.get(),
                'lat_lng': {'lat': self.lat.get(), 'lng': self.lng.get()},
                'radius': self.radius.get(),
                'project_name': self.project.get(),
                'target_path': self.target_selector.get(),
                'categories': self.cat_selector.get()
                }
        return data

    def generate_json(self):
        data = self.fetch_data()
        validated_data, errors = validate_gui_data(data)

        if len(errors):
            messagebox.showerror("Data Missing", '\n'.join(errors))
        else:
            json_body = create_map_pois(validated_data)
            target_file = os.path.join(validated_data['target_path'], validated_data['project_name'] + '_pois.json')

            with open(target_file, 'w') as f:
                json.dump(json_body, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("Success", "Json generated, check \n" + target_file)


if __name__ == '__main__':
    gui = Gui()
    gui.mainloop()
