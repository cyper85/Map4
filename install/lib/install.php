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
function insert_address($id, $row) {
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

function insert_coords($id, $geo, $mp, $debug = false) {
    global $mysql;
    $mysql->real_query("INSERT INTO `coords_tmp` (`id`,`geometrie`, `mittelpunkt`) VALUES('{$id}','{$geo}','{$mp}') ON DUPLICATE KEY UPDATE id = '{$id}'");
}

function insert_names($id, $row) {
    $stmt = $conn->prepare("INSERT IGNORE INTO names (id, type, name) VALUES ('{$id}', ?, ?)");
    $stmt->bind_param("ss", $type, $name);
    
    if(strlen($row['name'])>0) {
        $type = "name";
        $name = $row['name'];
        $stmt->execute();
    }
    if(strlen($row['name:de'])>0) {
        $type = "name:de";
        $name = $row['name:de'];
        $stmt->execute();
    }
    if(strlen($row['name:en'])>0) {
        $type = "name:en";
        $name = $row['name:en'];
        $stmt->execute();
    }
    if(strlen($row['official_name'])>0) {
        $type = "official_name";
        $name = $row['official_name'];
        $stmt->execute();
    }
    if(strlen($row['int_name'])>0) {
        $type = "int_name";
        $name = $row['int_name'];
        $stmt->execute();
    }
    if(strlen($row['nat_name'])>0) {
        $type = "nat_name";
        $name = $row['nat_name'];
        $stmt->execute();
    }
    if(strlen($row['reg_name'])>0) {
        $type = "reg_name";
        $name = $row['reg_name'];
        $stmt->execute();
    }
    if(strlen($row['loc_name'])>0) {
        $type = "loc_name";
        $name = $row['loc_name'];
        $stmt->execute();
    }
    if(strlen($row['alt_name'])>0) {
        $type = "alt_name";
        $name = $row['alt_name'];
        $stmt->execute();
    }
    if(strlen($row['hist_name'])>0) {
        $type = "hist_name";
        $name = $row['hist_name'];
        $stmt->execute();
    }
    if(strlen($row['old_name'])>0) {
        $type = "old_name";
        $name = $row['old_name'];
        $stmt->execute();
    }
    if(strlen($row['name:historic'])>0) {
        $type = "name:historic";
        $name = $row['name:historic'];
        $stmt->execute();
    }
    if(strlen($row['name:old'])>0) {
        $type = "name:old";
        $name = $row['name:old'];
        $stmt->execute();
    }
    if(strlen($row['short_name'])>0) {
        $type = "short_name";
        $name = $row['short_name'];
        $stmt->execute();
    }
    
    $stmt->close();
}