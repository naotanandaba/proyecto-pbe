<?php
include_once('C:\xampp\htdocs\proyecto-pbe\Servidor\db.php');
function where_or_and($q, $s){
    $buffer = $s ? " AND" : " WHERE";
    $q .= $buffer;
    return $q;
}
parse_str(rawurldecode($_SERVER['QUERY_STRING']), $constraints);
$start = False;
$query = "SELECT * FROM marks";

if(isset($constraints['subject'])){
    $query = where_or_and($query, $start);
    $query .= " subject=" . "'" . $constraints['subject'] . "'";
    $start = True;
}
if(isset($constraints['name'])){
    $query = where_or_and($query,$start);
    $query .= " name=" . "'" . $constraints['name'] . "'";
    $start = True;
}
if(isset($constraints['mark']['lt'])){
    $query = where_or_and($query, $start);
    $query .= " mark <" . $constraints['mark']['lt'];
    $start = True;
}
if(isset($constraints['mark']['eq'])){
    $query = where_or_and($query, $start);
    $query .= " mark =" . $constraints['mark']['eq'];
    $start = True;
}
if(isset($constraints['mark']['gt'])){
    $query = where_or_and($query, $start);
    $query .= " mark >" . $constraints['mark']['gt'];
    $start = True;
}


if(isset($constraints['limit'])){
    $query .= " LIMIT " . $constraints['limit'];
}


$result = mysqli_query($conn, $query);
if(!$result){
    die("query failed");
}


$data=array();

while ($row = mysqli_fetch_assoc($result)){
    $data[]=$row;
}

echo json_encode($data);

mysqli_close($conn);
