#!/usr/bin/env python2
#encoding: UTF-8

# Copyright (c) 2016 Andreas Neumann <andr.neumann@googlemail.com>.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v1.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v10.html
#
# Contributors:
#    Andreas Neumann <andr.neumann@googlemail.com> - initial API and implementation and/or initial documentation

import psycopg2
import psycopg2.extras
import re

# Vorbereiten des Arrays:
with open("config/default.style") as f:
    styledata = f.readlines()

styledata = [re.sub(r'(\#.*)$',"",element,re.M).strip() for element in styledata]
styledata = [re.sub(r'^(.*delete\s*)$',"",element,re.M).strip() for element in styledata]
styledata = [re.sub(r'^((node|way)(,(node|way))?\s*)',"",element,re.M).strip() for element in styledata]
styledata = [re.sub(r'(\s*(polygon|linear|nocache)?\s*)$',"",element,re.M).strip() for element in styledata]
styledata = [re.sub(r'(\s*(polygon|linear|nocache)[,]?\s*)$',"",element,re.M).strip() for element in styledata]
styledata = [re.sub(r'(\s*(polygon|linear|nocache)[,]?\s*)$',"",element,re.M).strip() for element in styledata]
styledata = [re.sub(r'(\s*(text|realArray|real|int4)\s*)$',"",element,re.M).strip() for element in styledata]
styledata = filter(None, styledata)

# Datenbank verbinden
db = psycopg2.connect("dbname=map4 user=map4")
cursor = db.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
cursor2 = db.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

def generateBuildingPolygon(way_id,polygons):
    cursor.execute("SELECT * FROM planet_osm_ways WHERE id = "+way_id)
    row = cursor.fetchone()
    while row:
        # Teste auf Polygon
        if(row['nodes'][0] == row['nodes'][len(row['nodes'])-1]):
            polygon = []
            for node in row['nodes']:
                cursor2.execute("SELECT * FROM planet_osm_nodes WHERE id = "+node_id)
                node_row = cursor2.fetchone()
                while node_row:
                    polygon.append((node_row["lon"]/10000000)+" "+(node_row["lat"]/10000000))
                    node_row = cursor2.fetchone()
            polygons.append("("+polygon.join(",")+")")
        row = cursor.fetchone()
    return polygons

cursor.execute("SELECT * FROM planet_osm_rels")

row = cursor.fetchone()

while row:
    print row['tags']
    rel_tags = {}
    while len(row['tags'])>0:
        val = row['tags'].pop()
        key = row['tags'].pop()
        if(key in styledata):
            rel_tags[key] = val
    if (rel_tags["type"] == "site"):
        polygons = []
        rel_member = []
        print 
    row = cursor.fetchone()

if __name__ == "__main__":
    print "Hello World"
