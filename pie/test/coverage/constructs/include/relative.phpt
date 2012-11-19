--TEST--
Test file inclusion from relative path
--FILE--
<?php
$a = 10;
echo $a . "=\n";
include("pie/test/coverage/constructs/include/relative.php");
echo $a . "=\n";
echo relative() . "=";
?>
--EXPECT--
10=
12=
15=