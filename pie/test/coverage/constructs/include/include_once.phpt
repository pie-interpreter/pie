--TEST--
Test file inclusion from relative path several times with include_once
--FILE--
<?php
$a = 10;
echo $a . "=\n";
// this trick to check if files are included by their absolute position
$result = include_once("pie/../pie/test/coverage/constructs/include/several_relative.php");
echo ($result === 5) . "=\n";
echo $a . "=\n";
$a = 15;
echo $a . "=\n";
$result = include_once("pie/test/coverage/constructs/include/several_relative.php");
echo ($result === true) . "=\n";
$result = require_once("pie/test/coverage/constructs/include/several_relative.php");
echo ($result === true) . "=\n";
echo $a . "=";
?>
--EXPECT--
10=
1=
12=
15=
1=
1=
15=