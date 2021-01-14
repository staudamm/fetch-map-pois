from tkinter import *

# create root window
root = Tk()

# root window title and dimension
root.title("Fetch map POIs")
# Set geometry(widthxheight)
root.geometry('350x200')


class LabelledButton:
    def __init__(self, root, label, row):
        self.lbl = Label(root, text=label)
        self.lbl.grid(row=row, column=0)

        self.txt = Entry(root, width=20)
        self.txt.grid(row=row, column=1)


key  = LabelledButton(root, "API_KEY", 0)
lat = LabelledButton(root, "Latitude", 1)
lng = LabelledButton(root, "Longitude", 2)
project = LabelledButton(root, "Project name", 3)


# # function to display user text when
# # button is clicked
# def clicked():
#     res = "You wrote" + api_key.get()
#     key_lbl.configure(text=res)


# # button widget with red color text inside
# btn = Button(root, text="Generate json",
#              fg="red", command=clicked)
# # Set Button Grid
# btn.grid(row=4, column=1)

# Execute Tkinter
root.mainloop()
