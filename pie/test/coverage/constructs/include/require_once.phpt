--TEST--
Test file inclusion from relative path several times with require_once
--FILE--
<?php
$a = 10;
echo $a . "=\n";
require_once("pie/test/coverage/constructs/include/several_relative.php");
echo $a . "=\n";
$a = 15;
echo $a . "=\n";
require_once("pie/test/coverage/constructs/include/several_relative.php");
echo $a . "=";
?>
--EXPECT--
10=
12=
15=
15=