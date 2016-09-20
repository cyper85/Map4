<?php

/* 
 * Copyright (c) 2016 andreas.
 * All rights reserved. This program and the accompanying materials
 * are made available under the terms of the Eclipse Public License v1.0
 * which accompanies this distribution, and is available at
 * http://www.eclipse.org/legal/epl-v10.html
 *
 * Contributors:
 *    andreas - initial API and implementation and/or initial documentation
 */

$mysql->real_query("CREATE TEMPORARY TABLE `address_tmp` LIKE `address`");

// Adressen einfügen
function insert_adress($id, $row) {
    global $mysql;
    $address = array();
    
    $address['name'] = $row['name'];
    $level = $row['level'];
    if (strlen($level) == 0) {
        $level = $row['building:level'];
    }
    if (strlen($level) > 0) {
        $levels = preg_split('/\s*[;]\s*/', $level);
        $levels = array_unique($levels,SORT_NUMERIC);
        $address['level'] = json_encode($levels);
    }

    if ((strlen($row['addr:housenumber']) == 0) && (strlen($row['addr:housename']) == 0)) {
        $addr_result = pg_query("SELECT * FROM planet_osm_polygon WHERE ST_IsValid(way) = TRUE AND ST_IsValid('" . $row['way'] . "') = TRUE AND ST_Intersects('" . $row['way'] . "',way) AND (\"addr:housenumber\" IS NOT NULL OR \"addr:housename\" IS NOT NULL) AND \"addr:street\" IS NOT NULL AND round(CAST(ST_Distance_Sphere(ST_Centroid(way),ST_Centroid('" . $row['way'] . "')) AS numeric),1) < 200");
        if (!($addr_result) OR ! ($row = pg_fetch_assoc($addr_result))) {
            return false;
        }
    }

    //Fehlende PLZ holen	
    $address['postcode'] = $row['addr:postcode'];
    if ((strlen($row['addr:postcode']) == 0) && (strlen($row['addr:postcode']) == 0)) {
        $plz_result = pg_query("SELECT * FROM planet_osm_polygon WHERE ST_Intersects('" . $row['way'] . "',way) AND \"postal_code\" IS NOT NULL");
        if ($rowplz = pg_fetch_assoc($plz_result)) {
            $address['postcode'] = $rowplz['postal_code'];
        }
    } else {
        $address['postcode'] = $row['addr:postcode'];
    }
    $address['number'] = $row['addr:housenumber'];
    if ($id != 0) {
        $address['id'] = $id;
    }

    $address['name'] = normalize_text($row['addr:housename']);
    $address['street'] = normalize_text($row['addr:street']);
    $address['city'] = normalize_text($row['addr:city']);
    $address['suburb'] = normalize_text($row['addr:suburb']);
    if (strlen($address['suburb']) == 0) {
        $address['suburb'] = normalize_text($row['addr:hamlet']);
    }
    if (strlen($address['suburb']) == 0) {
        $address['suburb'] = normalize_text($row['addr:village']);
    }

    foreach ($address as $k => $v) {
        $keys[] = "`$k`";
        if (strlen($v) == 0) {
            $values[] = "NULL";
        } else {
            $values[] = "'" . $mysql->real_escape_string($v) . "'";
        }
    }

    $mysql->real_query("INSERT INTO `address_tmp` (" . implode(',', $keys) . ") VALUES (" . implode(',', $values) . ") ON DUPLICATE KEY UPDATE id = '" . $id . "'");
    return true;
}