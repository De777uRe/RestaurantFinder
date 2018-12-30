"""
Here the TreeView widget is configured as a multi-column listbox
with adjustable column width and column-header-click sorting.
"""
try:
    import Tkinter as tk
    import tkFont
    import ttk
except ImportError:  # Python 3
    import tkinter as tk
    import tkinter.font as tkFont
    import tkinter.ttk as ttk

import requests
import json


class MultiColumnListbox(object):
    """use a ttk.TreeView as a multicolumn ListBox"""

    def __init__(self):
        self.tree = None
        self._setup_widgets()
        self._build_tree()

    def _setup_widgets(self):
        container = ttk.Frame()
        container.pack(fill='both', expand=True)
        # create a treeview with dual scrollbars
        self.tree = ttk.Treeview(columns=table_headers, show="headings")
        vsb = ttk.Scrollbar(orient="vertical",
                            command=self.tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal",
                            command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set,
                            xscrollcommand=hsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=container)
        vsb.grid(column=1, row=0, sticky='ns', in_=container)
        hsb.grid(column=0, row=1, sticky='ew', in_=container)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

    def _build_tree(self):
        for col in table_headers:
            self.tree.heading(col, text=col.title(),
                              command=lambda c=col: sortby(self.tree, c, 0))
            # adjust the column's width to the header string
            self.tree.column(col,
                             width=tkFont.Font().measure(col.title()))

        for item in display_list:
            self.tree.insert('', 'end', values=item)
            # adjust column's width if necessary to fit each value
            for ix, val in enumerate(item):
                col_w = tkFont.Font().measure(val)
                if self.tree.column(table_headers[ix], width=None) < col_w:
                    self.tree.column(table_headers[ix], width=col_w)


def sortby(tree, col, descending):
    """sort tree contents when a column header is clicked on"""
    # grab values to sort
    data = [(tree.set(child, col), child) \
            for child in tree.get_children('')]
    # if the data to be sorted is numeric change to float
    # data =  change_numeric(data)
    # now sort the data in place
    data.sort(reverse=descending)
    for ix, item in enumerate(data):
        tree.move(item[1], '', ix)
    # switch the heading so it will sort in the opposite direction
    tree.heading(col, command=lambda col=col: sortby(tree, col, \
                                                     int(not descending)))


def findrestaurants(displaylist, inpagetoken=None):
    lat = 32.699730
    lon = -97.424780
    radius = 24140
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lon}&radius={radius}&type=restaurant&key={APIKEY}"
    print(url)
    if inpagetoken:
        url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken={inpagetoken}&key={APIKEY}"
    response = requests.get(url)
    res = json.loads(response.text)
    print("here results ---->>> ", len(res["results"]))
    for result in res["results"]:
        reslat = result["geometry"]["location"]["lat"]
        reslon = result["geometry"]["location"]["lng"]
        info = ";".join(map(str, [result["name"], result["geometry"]["location"]["lat"],
                                  result["geometry"]["location"]["lng"], result.get("rating", 0), result["place_id"]]))
        disturl = f"https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={lat},{lon}&destinations={reslat},{reslon}&key={DISTAPIKEY}"
        distresponse = requests.get(disturl)
        distres = json.loads(distresponse.text)

        calcdist = 0

        for row in distres["rows"]:
            for element in row["elements"]:
                calcdist = element["distance"]["value"]/5280
                print(calcdist)

        displaylist.append((result["name"], calcdist))
        print(info)
    inpagetoken = res.get("next_page_token", None)
    print("here -->> ", inpagetoken)
    return inpagetoken


# the test data ...

# car_header = ['car', 'repair']
table_headers = ['Restaurant', 'Distance']
# car_list = [
#     ('Hyundai', 'brakes'),
#     ('Honda', 'light'),
#     ('Lexus', 'battery'),
#     ('Benz', 'wiper'),
#     ('Ford', 'tire'),
#     ('Chevy', 'air'),
#     ('Chrysler', 'piston'),
#     ('Toyota', 'brake pedal'),
#     ('BMW', 'seat')
# ]

APIKEY = ''
DISTAPIKEY = ''
pagetoken = None

display_list = []

# for i in range(20):
#     display_list.append(("restaurant" + str(i), 10))

while True:
    pagetoken = findrestaurants(display_list, inpagetoken=pagetoken)
    if pagetoken:
        print("PAGE TOKEN: " + pagetoken)
    import time

    time.sleep(3)

    if not pagetoken:
        break

print("RETRIEVED THESE RESTAURANTS:")
print(display_list)


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Restaurant Finder")
    listbox = MultiColumnListbox()
    root.mainloop()
