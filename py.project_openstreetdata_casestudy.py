#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xlrd
import os
import csv
import xml.etree.ElementTree as ET
from collections import defaultdict
from pprint import pprint
import re
import codecs




# Load in files brought in from Mapzen and create Sample file to do basic queries
filename = 'udacity_project_openstreetdata_rjl/bozeman_MT.osm'  # Replace this with your osm file
samplefile = 'udacity_project_openstreetdata_rjl/sample.osm'

# Explore the basic details of the sample file: count tags

# def count_tags(samplefile):
    tags = {}
    for event, el in ET.iterparse(samplefile):
        if el.tag in tags:
            tags[el.tag] += 1
        else:
            tags[el.tag] = 1
    return tags
bozeman_tags = count_tags(samplefile)

pprint(bozeman_tags)

# Getting to know about the contributing Users to the map
def get_user(element):
    return

# Determine the User Ids of the those that contributed to the map
def process_map_users(filename):
    users = set()
    for event, element in ET.iterparse(filename):
        for key in element.attrib:
            if key == 'uid':
                users.add(element.attrib[key])
    return users

users = process_map_users(filename)

# Check

pprint(users)

# How to determine the amount of users that contributed to this map?
len(users)

###  Tags in the OpenStreet Map
# The nodes, ways and other tags are detailed above.
# However we have to clean the street names and consolidate these tags.
# To get the street tags, we have to loop through the subtags
# under a major tag. We use iterparse like in
# the process_map_tagtypes functions below:

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

def key_type(element, keys):
    if element.tag == 'tag':
        try:
            lowermo = lower.search(element.attrib['k'])
            lowermo.group()
            keys["lower"] += 1
        except AttributeError:
            try:
                lower_colonmo = lower_colon.search(element.attrib['k'])
                lower_colonmo.group()
                keys["lower_colon"] += 1
            except AttributeError:
                try:
                    problemcharmo = problemchars.search(element.attrib['k'])
                    problemcharmo.group()
                    keys["problemchars"] += 1
                except AttributeError:
                    keys["other"] += 1
    return keys

# tagtypes
def process_map_tagtypes(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other":0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)
    return keys

keys = process_map_tagtypes(filename)

# Check
pprint(keys)

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons"]
# Mapping names
mapping = { "St": "Street",
            "St.": "Street",
            "st": "Street",
            "ST": "Street",
            "street": "Street",
            "Ave": "Avenue",
            "Ave.": "Avenue",
            "Avene": "Avenue",
            "Blvd": "Boulevard",
            "Blvd.": "Boulevard",
            "Dr": "Drive",
            "Dr.": "Drive",
            "Ct": "Court",
            "Ct.": "Court",
            "Ln": "Lane",
            "Pl": "Place",
            "Pl.": "Place",
            "lane": "Lane",
            "Rd": "Road",
            "Rd.": "Road",
            "Trl": "Trail",
            "Pkwy": "Parkway",
            "N.": "North"}

# def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


# audit function
def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types



# For any streets that need to be renamed after not passing the audit function above
def update_name(name, mapping):
    parts = name.split()
    newname = []
    for part in parts:
        if part in mapping.keys():
            newname.append(mapping[part])
        else:
            newname.append(part)
    name = ' '.join(newname)
    return name

# applying the audit to the errant street types
st_types = audit(filename)


len(st_types)

pprint(st_types)

# Print the names the old way
for st_type, ways in st_types.items():
    for name in ways:
        pprint(name)

# Print the names the newly mapped ways way
for st_type, ways in st_types.items():
    for name in ways:
        better_name = update_name(name, mapping)
        pprint(better_name)

# Next file is the preping the database file 'project_openstreetdata_preparing_db.py'
