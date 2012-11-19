--TEST--
Tests return functionality in including file

--FILE--
<?php
echo "OK=\n";
$result = include("noreturn.php");
echo $a . "=\n";
echo "OK=\n";
echo ($result === true). "=\n";
$result = include("return.php");
echo $result . "=";
?>
--EXPECT--
OK=
12=
OK=
1=
20=