"""a small python utility to plan single central portal layered fields"""
import json
import os
from pprint import pprint
import operator
import math

def on_left_compare(anchor,point1):
    def on_left(point2):
        # although the coordinate is stretched with only lat and log info, the relative geometry position still holds
        # lat as y, lnt as x (vector from point to anchor)
        val = (point2.lng - anchor.lng)*(point1.lat - anchor.lat) - (point2.lat - anchor.lat)*(point1.lng - anchor.lng)
        if val > 0:
            return True
        elif val < 0:
            return False
        else:
            return None
    return on_left

def angle_d(anchor,point1):
    a=distance(anchor,point1)
    def included_angle(point2): 
        b = distance(anchor,point2)
        c = distance(point1,point2)
        cos = (a*a+b*b-c*c)/(2*a*b)
        return math.acos(cos)
    return included_angle
        

def distance(origin, destination):
    lat1, lng1 = origin.lat, origin.lng
    lat2, lng2 = destination.lat, destination.lng
    radius = 6371 # km

    dlat = math.radians(lat2-lat1)
    dlng = math.radians(lng2-lng1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlng/2) * math.sin(dlng/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d

class Portal:
    def __init__(self,json,id):
        self.id = id
        self.name = json['label']
        latlng = json['latlng'].split(",")
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
    portals.append(Portal(portals_json[k],i))

sorted_portals = sorted(portals, key=operator.attrgetter("name"))
for po in sorted_portals:
    print(po)
del sorted_portals

anchor_num = input("please choose the portal you would like to use as anchor: ")
anchor_num = int(anchor_num)
if anchor_num >= len(portals) or anchor_num < 0:
    raise Exception('invalid anchor portal id')
    
base_num = input("please choose the portal you would like to use to form the first edge: ")
base_num = int(base_num)
if base_num >= len(portals) or base_num < 0:
    raise Exception('invalid base portal id')

anchor = portals[anchor_num]
base = portals[base_num]


portals.pop(anchor_num)
portals.remove(base)
print("the portal your chose as anchor is: "+str(anchor))

left_list = []
right_list = []
on_left = on_left_compare(anchor,base)
for i in portals:
    is_on_left = on_left(i)
    if is_on_left is True:
        left_list.append(i)
    elif is_on_left is False:
        right_list.append(i)

angle_dist = angle_d(anchor, base)
left_list.sort(key=angle_dist)
right_list.sort(key=angle_dist)
print("on left portals:")
for i in left_list:
    print(str(i))



