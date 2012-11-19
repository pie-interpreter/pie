--TEST--
Test file inclusion from relative path several times
--FILE--
<?php
$a = 10;
echo $a . "=\n";
include("pie/test/coverage/constructs/include/several_relative.php");
echo $a . "=\n";
$a = 15;
echo $a . "=\n";
include("pie/test/coverage/constructs/include/several_relative.php");
echo $a . "=";
?>
--EXPECT--
10=
12=
15=
12=