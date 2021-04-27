<?php
include ("db.php");
function where_or_and($q, $s){
  $buffer = $s ? " AND" : " WHERE";
  $q .= $buffer;
  return $q;
}
parse_str($_SERVER['QUERY_STRING']);
$start = False;
$query = "SELECT * FROM marks";

if(isset($subject)){ 
  $query .= " WHERE subject=" . "'" . $subject . "'";
  $start = True;
}
if(isset($name)){

  $query = where_or_and($query,$start);

  $query .= " name=" . "'" . $name . "'";
  $start=True;
}
if(isset($mark[lt])){
  $query = where_or_and($query, $start);
  $query .= " mark <=" . $mark[lt];
  $start = True;
}
if(isset($mark[eq])){
   $query = where_or_and($query, $start);
   $query .= " mark =" . $mark[eq];
   $start = True;
 }
if(isset($mark[gt])){
   $query = where_or_and($query, $start);
   $query .= " mark >=" . $mark[gt];
   $start = True;
 }

if(isset($limit)){
  $query .= " LIMIT " . $limit;
}
$result = mysqli_query($conn, $query);
if(!$result){
    die("query failed");
}

while ($row = mysqli_fetch_assoc($result)){
    $data[]=$row;
}
echo json_encode($data);
mysqli_close($conn);
?>
