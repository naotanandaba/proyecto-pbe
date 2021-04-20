<?php
include ("db.php");
$query = "SELECT * FROM timetables";
echo $_GET['limit'];
$query .= " LIMIT " . $_GET['limit'];
$result = mysqli_query($conn, $query);
if(!$result){
    die("query failed");

}
$data= array();

while ($row = mysqli_fetch_array($result)){
    $data[]=$row;
}
echo json_encode($data, );

?>