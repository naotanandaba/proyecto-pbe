<?php
include_once('C:\xampp\htdocs\db.php');
function where_or_and($q, $s){
  $buffer = $s ? " AND" : " WHERE";
  $q .= $buffer;
  return $q;
}
parse_str(rawurldecode($_SERVER['QUERY_STRING']), $constraints);
$start = False;
$query = "SELECT * FROM auth";



if(isset($constraints['student'])){
  $query = where_or_and($query, $start);
  $query .= " student=" . "'" . $constraints['student'] . "'";
  $start = True;
}


if(isset($constraints['limit'])){
  $query .= " LIMIT " . $constraints['limit'];
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