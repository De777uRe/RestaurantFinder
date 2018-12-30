import requests
import json
import tkinter as tk

APIKEY = ''


class Application(tk.Frame):
    restaurantlist = []

    def __init__(self, passedlist, master=None):
        super().__init__(master)
        self.master = master
        self.quit = tk.Button()
        self.mylist = tk.Listbox()
        self.scrollbar = tk.Scrollbar()
        self.restaurantlist = passedlist
        self.create_widgets()

    def create_widgets(self):
        self.mylist = tk.Listbox(root)
        self.mylist.grid(row=0, column=0, sticky='nsew')
        self.scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL)
        self.scrollbar.config(command=self.mylist.yview)
        for restaurant in self.restaurantlist:
            self.mylist.insert(tk.END, restaurant)
        self.scrollbar.grid(row=0, column=1,  sticky='ns')
        self.mylist.config(yscrollcommand=self.scrollbar.set)
        self.quit = tk.Button(root, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.grid(row=1, column=0)
        tk.Grid.columnconfigure(root, 0, weight=1)
        tk.Grid.columnconfigure(root, 1, weight=1)
        tk.Grid.rowconfigure(root, 0, weight=1)


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
        info = ";".join(map(str, [result["name"], result["geometry"]["location"]["lat"],
                                  result["geometry"]["location"]["lng"], result.get("rating", 0), result["place_id"]]))
        displaylist.append(result["name"])
        print(info)
    inpagetoken = res.get("next_page_token", None)
    print("here -->> ", inpagetoken)
    return inpagetoken


pagetoken = None

displayList = []

for i in range(20):
    displayList.append("restaurant" + str(i))

# while True:
#     pagetoken = findrestaurants(displayList, inpagetoken=pagetoken)
#     if pagetoken:
#         print("PAGE TOKEN: " + pagetoken)
#     import time
#
#     time.sleep(3)
#
#     if not pagetoken:
#         break

print("RETRIEVED THESE RESTAURANTS:")
print(displayList)

root = tk.Tk()
app = Application(displayList, master=root)
app.mainloop()
