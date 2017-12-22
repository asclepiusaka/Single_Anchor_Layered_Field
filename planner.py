import json
import os
from pprint import pprint
import operator

def onLeft(anchor,point1,point2):
    # although the coordinate is stretched with only lat and log, the relative geometry relation still holds
    # lat as y, lnt as x
    val = (point2.lnt - anchor.lnt)*(point1.lat - anchor.lat) - (point2.lat - anchor.lat)*(point1.lnt - anchor.lnt)
    if val > 0:
        return True
    elif val < 0:
        return False
    else:
        return None



class portal:
    def __init__(self,json,id):
        self.id = id
        self.name = json['label']
        latlng = json['latlng']
        latlng = latlng.split(',')
        self.lat = float(latlng[0])
        self.lng = float(latlng[1])

    def __str__(self):
        return "{:03d}: {}".format(self.id,self.name)

    
file_path = input("assgin an input file to open: ")
if not os.path.isfile(file_path):
    file_path = "res/gatech.json"
with open(file_path) as data_file:
    data = json.load(data_file)
portals_json = data['portals']['idOthers']['bkmrk']
pprint(portals_json)
portals = []
for i,k in enumerate(portals_json):
    portals.append(portal(portals_json[k],i))

sorted_portals = sorted(portals,key=operator.attrgetter("name"))
for po in sorted_portals:
    print(po)
del sorted_portals

anchor_num = input("please choose the portal you would like to use as anchor: ")
anchor_num = int(anchor_num)
if anchor_num >= len(portals) or anchor_num < 0:
    raise Exception('invalid portal id')

anchor = portals[anchor_num]
portals.pop(anchor_num)
print("the portal your chose as anchor is: "+str(anchor))

edge_num = intput("please choose the portal you would like to use to form the first edge")
left_list = []
right_list = []

