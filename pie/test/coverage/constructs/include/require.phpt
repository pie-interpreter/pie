--TEST--
Tests 'require' functionality

--FILE--
<?php
echo "OK=\n";
$result = require("noreturn.php");
echo $a . "=\n";
echo "OK=\n";
echo ($result === true). "=\n";
$result = require("return.php");
echo $result . "=";
?>
--EXPECT--
OK=
12=
OK=
1=
20=