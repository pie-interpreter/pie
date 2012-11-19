--TEST--
Test file inclusion from the directory where calling script is situated
--FILE--
<?php
$a = 10;
echo $a . "=\n";
include("from_script_path.php");
echo $a . "=\n";
echo relative() . "=\n";
echo $b . "=";
?>
--EXPECT--
10=
12=
15=
10=