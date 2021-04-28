<?php
include_once('C:\xampp\htdocs\db.php');
function where_or_and($q, $s){
    $buffer = $s ? " AND" : " WHERE";
    $q .= $buffer;
    return $q;
}
parse_str(rawurldecode($_SERVER['QUERY_STRING']), $cons);
$start = False;
$query = "SELECT * FROM timetables";
$date = new DateTime();

if(isset($cons['subject'])){
    $query = where_or_and($query, $start);
    $query .= " subject=" . "'" . $cons['subject'] . "'";
    $start = True;
}
if(isset($cons['room'])){
    $query = where_or_and($query, $start);
    $query .= " room=" . "'" . $cons['room'] . "'";
    $start=True;
}
if(isset($cons['hour']['lt'])){
    $query = where_or_and($query, $start);
    $query .= " hour < ";
    if($cons['hour']['lt'] === "now"){
        $query .= $date->format('His') ;
    }
    else {
        $query .= $cons['hour']['lt'];
    }
    $start = True;

}
if(isset($cons['hour']['eq'])){
    $query = where_or_and($query, $start);
    $query .= " hour = ";
    if($cons['hour']['eq'] === "now"){
        $query .= $date->format('His') ;
    }
    else {
        $query .= $cons['hour']['eq'];
    }
    $start = True;
}
if(isset($cons['hour']['gt'])){
    $query = where_or_and($query, $start);
    $query .= " hour > ";
    if($cons['hour']['gt'] === "now"){
        $query .= $date->format('His') ;
    }
    else {
        $query .= $cons['hour']['gt'];
    }
    $start = True;
}
if(isset($cons['day']['gte'])){
    $query = where_or_and($query, $start);
    $query .= " day >=";
    if($cons['day']['gte'] === "now") {
         $query .= "'" . $date->format('D') . "'";
    } else {
        $query .= "'" . $cons['day']['gte'] . "'";
    }
    $start = True;
}
if(isset($cons['day']['eq'])){
    $query = where_or_and($query, $start);
    $query .= " day =";
    if($cons['day']['eq'] === "now") {
        $query .= "'" . $date->format('D') . "'";
    } else {
        $query .= "'" . $cons['day']['eq'] . "'";
    }
    $start = True;
}
if(isset($cons['day']['lte'])){
    $query = where_or_and($query, $start);
    $query .= " day <=";
    if($cons['day']['lte'] === "now") {
        $query .= "'" . $date->format('D') . "'";
    } else {
        $query .= "'" . $cons['day']['lte'] . "'";
    }
    $start = True;
}

if(isset($cons['limit'])){
    $query .= " LIMIT " . $cons['limit'];
    $start = True;
}


$query .= ";";
$result = mysqli_query($conn, $query);
if(!$result){
    die("query failed");
}



$data=array();
while($row = mysqli_fetch_assoc($result)){
    $data[]=$row;
}

echo json_encode($data);
$conn->close();