import requests
import json
import tkinter as tk

APIKEY = ''


class Application(tk.Frame):
    restaurantlist = []
    labels = []

    def __init__(self, passedList, master=None):
        super().__init__(master)
        self.master = master
        self.quit = tk.Button()
        self.mylist = tk.Listbox()
        self.scrollbar = tk.Scrollbar(self)
        self.restaurantlist = passedList
        # self.pack_propagate(0)
        self.pack(fill=tk.BOTH, expand=1)
        self.create_widgets()

    def create_widgets(self):
        # testlabel = tk.Label(self, text='test')
        # self.labels.append(testlabel)
        # testlabel.pack()

        # for restaurant in self.restaurantlist:
        #     newlabel = tk.Label(self, text=restaurant)
        #     newlabel.pack()
        self.scrollbar.pack(side= tk.RIGHT, fill=tk.Y)
        self.mylist = tk.Listbox(self, yscrollcommand=self.scrollbar.set)
        for restaurant in self.restaurantlist:
            self.mylist.insert(tk.END, restaurant)
        self.mylist.pack(side=tk.TOP, fill=tk.BOTH)
        self.scrollbar.config(command=self.mylist.yview)
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")


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


# app = QApplication(sys.argv)
# label = QLabel("<font color=red size=40>Hello World!</font>")
# label = QLabel("<font color=red size=40>" + str(generator.x) + "</font>")
# label = QLabel("TEST");
# label.show()
# app.exec_()

pagetoken = None

displayList = []

while True:
    pagetoken = findrestaurants(displayList, inpagetoken=pagetoken)
    if pagetoken:
        print("PAGE TOKEN: " + pagetoken)
    import time

    time.sleep(5)

    if not pagetoken:
        break

print("RETRIEVED THESE RESTAURANTS:")
print(displayList)

root = tk.Tk()
app = Application(displayList, master=root)
app.mainloop()
