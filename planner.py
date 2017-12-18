import json
import os
from pprint import pprint


file_path = input("assgin an input file to open: ")
if not os.path.isfile(file_path):
    file_path = "res/gatech.json"
with open(file_path) as data_file:
    data = json.load(data_file)
portals_json = data['portals']['idOthers']['bkmrk']
pprint(portals_json)
portals = dict()
for i,k in enumerate(portals_json):
    print(k)
    print(i)


