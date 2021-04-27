?php
include_once("/var/www/dominio_pbe/db.php");
function where_or_and($q, $s){
  $buffer = $s ? " AND" : " WHERE";
  $q .= $buffer;
  return $q;
}
parse_str($_SERVER['QUERY_STRING'], $constraints);
$start = False;
$query = "SELECT * FROM students";




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