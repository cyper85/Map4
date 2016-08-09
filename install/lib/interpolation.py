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
cursor3 = db.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

def generateBuildingPolygon(way_id,polygons):
    """Erzeugt Polygone"""
    cursor3.execute("SELECT * FROM planet_osm_ways WHERE id = "+way_id)
    row3 = cursor3.fetchone()
    while row3:
        # Teste auf Polygon
        if(row3['nodes'][0] == row3['nodes'][len(row3['nodes'])-1]):
            polygon = []
            for node in row3['nodes']:
                cursor2.execute("SELECT * FROM planet_osm_nodes WHERE id = "+str(node))
                node_row = cursor2.fetchone()
                while node_row:
                    polygon.append(str(node_row["lon"]/10000000.0)+" "+str(node_row["lat"]/10000000.0))
                    node_row = cursor2.fetchone()
            polygons.append("("+",".join(polygon)+")")
        row3 = cursor3.fetchone()
    return polygons

def is_inter_point(nr, inter):
    if((inter=='all') and re.match(r'^\d+$',nr)):
        return 1
    elif((inter=='even') and re.match(r'^\d+$',nr) and (nr % 2 == 0)):
        return 1
    elif((inter=='odd') and re.match(r'^\d+$',nr) and (nr % 2 == 1)):
        return 1
    elif((inter=='alphabetic') and re.match(r'^\s*\d+\s*[a-zA-Z]\s*$',nr)):
        return 1
    else:
        return 0

def interpol(start,end,line,intertype):
    new = []
    if(intertype=='all'):
	if(start['housenumber'] > end['housenumber']):
            anzahl = start['housenumber'] - end['housenumber']
            anzahl1 = anzahl
            i=1;
            for(anzahl;anzahl>1;anzahl--):
		cursor3.execude("INSERT INTO planet_osm_point (\"addr:housenumber\", \"addr:street\", \"addr:suburb\", \"addr:city\", \"addr:postcode\", way) VALUES (%s,%s,%s,%s,%s,ST_Line_Interpolate_Point(st_linefromtext(%s,4326),%s)),"
                    ,(str(start['housenumber']+i), start['street'], start['suburb'], start['city'], start['postcode'], 'LINESTRING('+','.join(line)+')',str($i/$anzahl1)))
		i++
        else:
            anzahl = end['housenumber'] - start['housenumber'];
            anzahl1 = anzahl;
            i=1;
            for(anzahl;anzahl>1;anzahl--):
		cursor3.execude("INSERT INTO planet_osm_point (\"addr:housenumber\", \"addr:street\", \"addr:suburb\", \"addr:city\", \"addr:postcode\", way) VALUES (%s,%s,%s,%s,%s,ST_Line_Interpolate_Point(st_linefromtext(%s,4326),%s)),"
                    ,(str(start['housenumber']+i), start['street'], start['suburb'], start['city'], start['postcode'], 'LINESTRING('+','.join(line)+')',str($i/$anzahl1)))
		i++
    elif((intertype=='even') or (intertype=='odd'))
	if(start['housenumber']>end['housenumber'])
            anzahl = (start['housenumber'] - end['housenumber'])/2;
            anzahl1 = anzahl;
            i=1;
            for(anzahl;anzahl>1;anzahl--)
		cursor3.execude("INSERT INTO planet_osm_point (\"addr:housenumber\", \"addr:street\", \"addr:suburb\", \"addr:city\", \"addr:postcode\", way) VALUES (%s,%s,%s,%s,%s,ST_Line_Interpolate_Point(st_linefromtext(%s,4326),%s)),"
                    ,(str(start['housenumber']-(i*2)), start['street'], start['suburb'], start['city'], start['postcode'], 'LINESTRING('+','.join(line)+')',str($i/$anzahl1)))
		i++
	else
            anzahl = (end['housenumber'] - start['housenumber'])/2;
            anzahl1 = anzahl;
            i=1;
            for(anzahl;anzahl>1;anzahl--)
		cursor3.execude("INSERT INTO planet_osm_point (\"addr:housenumber\", \"addr:street\", \"addr:suburb\", \"addr:city\", \"addr:postcode\", way) VALUES (%s,%s,%s,%s,%s,ST_Line_Interpolate_Point(st_linefromtext(%s,4326),%s)),"
                    ,(str(start['housenumber']+(i*2)), start['street'], start['suburb'], start['city'], start['postcode'], 'LINESTRING('+','.join(line)+')',str($i/$anzahl1)))
		i++
                
    elif(intertype=='alphabetic')
        number = re.findall(r'\d+',start['housenumber'])
	if(number==re.findall(r'\d+',end['housenumber']))
            end_char = re.findall(r'[a-z]+',lower(end['housenumber']))
            start_char = re.findall(r'[a-z]+',lower(start['housenumber']))
            if(len(start_char) === len(end_char) === 1)
                anzahl = ord(end_char)-ord(start_char)
                if(anzahl > 0)
                    anzahl1 = anzahl;
                    i=1;
                    for(anzahl;anzahl>1;anzahl--)
                        cursor3.execude("INSERT INTO planet_osm_point (\"addr:housenumber\", \"addr:street\", \"addr:suburb\", \"addr:city\", \"addr:postcode\", way) VALUES (%s,%s,%s,%s,%s,ST_Line_Interpolate_Point(st_linefromtext(%s,4326),%s)),"
                            ,(str(number)+chr(start_char-i)), start['street'], start['suburb'], start['city'], start['postcode'], 'LINESTRING('+','.join(line)+')',str($i/$anzahl1)))
                        i++
                elif(anzahl<0)
                    anzahl1 = anzahl;
                    i=1;
                    for(anzahl;anzahl>1;anzahl--)
                        cursor3.execude("INSERT INTO planet_osm_point (\"addr:housenumber\", \"addr:street\", \"addr:suburb\", \"addr:city\", \"addr:postcode\", way) VALUES (%s,%s,%s,%s,%s,ST_Line_Interpolate_Point(st_linefromtext(%s,4326),%s)),"
                            ,(str(number)+chr(start_char+i)), start['street'], start['suburb'], start['city'], start['postcode'], 'LINESTRING('+','.join(line)+')',str($i/$anzahl1)))
                        i++

cursor.execute("SELECT * FROM planet_osm_rels")

row = cursor.fetchone()

while row:
    rel_tags = {}
    rel_member = {}
    while len(row['tags'])>0:
        val = row['tags'].pop()
        key = row['tags'].pop()
        if(key in styledata):
            rel_tags[key] = val
    while len(row['members'])>0:
        val = row['members'].pop()
        key = row['members'].pop()
        rel_member[key] = val
    if (rel_tags["type"] == "site"):
        polygons = []
        for (member_id, member_type) in rel_member.items():
            if(re.match(r'^[w](\d+)+$',member_id)):
                polygons = generateBuildingPolygon(member_id.replace("w",""),polygons)
        if(len(polygons)>0):
            vals = []
            vals_s = ""
            cols = ""
            for (col, val) in rel_tags.items():
                cols += '"'+col+'",'
                vals.append(val)
                vals_s += "%s, "
            cols += '"way", "osm_id", "z_order","way_area"'
            vals.append("POLYGON("+",".join(polygons)+")")
            vals.append(str(row['id']))
            vals.append("0")
            vals.append("0")
            vals_s += "ST_GeomFromText(%s,4326), %s, %s, %s"
            
            cursor2.execute('INSERT INTO "planet_osm_polygon" ('+cols+') VALUES ('+vals_s+')',vals)
    if (rel_tags["type"] == "building"):
        polygons = []
        for (member_id, member_type) in rel_member.items():
            if((re.match(r'^[w](\d+)+$',member_id)) and (member_type == "building")):
                polygons = generateBuildingPolygon(member_id.replace("w",""),polygons)
        if(len(polygons)>0):
            vals = []
            vals_s = ""
            cols = ""
            for (col, val) in rel_tags.items():
                cols += '"'+col+'",'
                vals.append(val)
                vals_s += "%s, "
            cols += '"way", "osm_id", "z_order","way_area"'
            vals.append("POLYGON("+",".join(polygons)+")")
            vals.append(str(row['id']))
            vals.append("0")
            vals.append("0")
            vals_s += "ST_GeomFromText(%s,4326), %s, %s, %s"
            
            cursor2.execute('INSERT INTO "planet_osm_polygon" ('+cols+') VALUES ('+vals_s+')',vals)
    row = cursor.fetchone()

# Fehlende Straßennamen ergänzen
cursor.execute("select st_astext(way) as way, osm_id as id from planet_osm_point where \"addr:street\" IS NULL AND (\"addr:housenumber\" IS NOT NULL OR \"addr:housename\" IS NOT NULL)");
row = cursor.fetchone()
while row:
    cursor2.execute("SELECT name FROM planet_osm_roads WHERE ST_DWithin(way,ST_GeomFromText(%s,4326), 200) AND name != '' AND highway IN  ('residential','living_street','primary','secondary','tertiary','unclassified','road','service','pedestrian') ORDER BY ST_distance(way, ST_GeomFromText(%s,4326)) limit 1;",(row['way'],row['way']))
    row2 = cursor2.fetchone()
    if row2:
        cursor3.execute('UPDATE planet_osm_point SET "addr:street" = %s WHERE "osm_id" = %s',(row2['name'],row['id']))
    row = cursor.fetchone()

cursor.execute("select st_astext(way) as way, osm_id as id from planet_osm_line where \"addr:street\" IS NULL AND (\"addr:housenumber\" IS NOT NULL OR \"addr:housename\" IS NOT NULL)");
row = cursor.fetchone()
while row:
    cursor2.execute("SELECT name FROM planet_osm_roads WHERE ST_DWithin(way,ST_GeomFromText(%s,4326), 200) AND name != '' AND highway IN  ('residential','living_street','primary','secondary','tertiary','unclassified','road','service','pedestrian') ORDER BY ST_distance(way, ST_GeomFromText(%s,4326)) limit 1;",(row['way'],row['way']))
    row2 = cursor2.fetchone()
    if row2:
        cursor3.execute('UPDATE planet_osm_line SET "addr:street" = %s WHERE "osm_id" = %s',(row2['name'],row['id']))
    row = cursor.fetchone()

cursor.execute("select st_astext(way) as way, osm_id as id from planet_osm_polygon where \"addr:street\" IS NULL AND (\"addr:housenumber\" IS NOT NULL OR \"addr:housename\" IS NOT NULL)");
row = cursor.fetchone()
while row:
    cursor2.execute("SELECT name FROM planet_osm_roads WHERE ST_DWithin(way,ST_GeomFromText(%s,4326), 200) AND name != '' AND highway IN  ('residential','living_street','primary','secondary','tertiary','unclassified','road','service','pedestrian') ORDER BY ST_distance(way, ST_GeomFromText(%s,4326)) limit 1;",(row['way'],row['way']))
    row2 = cursor2.fetchone()
    if row2:
        cursor3.execute('UPDATE planet_osm_polygon SET "addr:street" = %s WHERE "osm_id" = %s',(row2['name'],row['id']))
    row = cursor.fetchone()

# Interpolationen von Adressdaten

cursor.execute("select \"addr:interpolation\" as inter, st_astext(way) as street from planet_osm_line where \"addr:interpolation\" IS NOT NULL")
interpolation = cursor.fetchone()
while interpolation:
    linepoints = ()
    start = ()
    coordinates = re.sub(r'[^0-9,. ]',"",interpolation["street"]).split(",")
    for coordinate in coordinates:
        print coordinate
        cursor2.execute('SELECT "addr:housenumber" AS housenumber,"addr:postcode" AS postcode,"addr:street" AS street,"addr:city" AS city,"addr:suburb" AS suburb, st_astext(way) AS koord FROM planet_osm_point WHERE "addr:housenumber" IS NOT NULL AND way = st_pointfromtext(\'POINT('+str(coordinate)+')\',4326)')
        print cursor2.query
        point = cursor2.fetchone()
        if(point):
            # Wenn bereits Startwert festgelegt & Punkt wichtig
            if((len(start)>0)and(is_inter_point(point['housenumber'],interpolation['inter']))):
                # Punkt hinzufügen
                linepoints.append(coordinate)
                # Interpolieren
                interpol(start,point,linepoints,interpolation['inter'])
                # Neuen Startwert festlegen
                start = point
                # Liniencache leeren
                linepoints = Array(coordinate)
            elif((len(start)==0) and (is_inter_point(point['housenumber'],interpolation['inter']))):
                # Startwert festlegen
                start = point
                # Liniencache leeren
                linepoints = [coordinate]
            else:
                # unwichtiger Punkt
                linepoints.append(coordinate)
        else:
            linepoints.append(coordinate)
    interpolation = cursor.fetchone()