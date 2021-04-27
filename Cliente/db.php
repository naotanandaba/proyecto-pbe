<?php

$conn = mysql_connect(
    'sql11.freesqldatabase.com:3306',
    'sql11407041',
    '2q8mGNLwAE',
    'sql11407041',
);
if (!$conn) {
    die('No pudo conectarse: ' . mysql_error());
}
echo 'Conectado satisfactoriamente';

?>