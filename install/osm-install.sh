#!/bin/bash

# Download der Daten

wget -q -O /tmp/Ilmenau.osm "http://overpass-api.de/api/interpreter?data=%5Bout%3Axml%5D%3Barea%5B%27de%3Aamtlicher_gemeindeschluessel%27%3D%2716070029%27%5D-%3E.a%3B(way(area.a)%3Bnode(area.a)%3Brelation(area.a)%3B)-%3E.b%3B.b%20out%3B.b%20%3E%3B(._%3B-%20.b%3B)%3Bout%20skel%3B"

osm2pgsql --user=map4 -S config/default.style -lsc -d map4 -C 100 --cache-strategy sparse /tmp/Ilmenau.osm

