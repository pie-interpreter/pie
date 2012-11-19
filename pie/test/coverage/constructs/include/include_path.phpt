--TEST--
Test file inclusion from include_path

ATTENTION: to work correctly, "pie/test/coverage/constructs/include/include_path" should be
defined in include_path in conf/pie.ini

--FILE--
<?php
$a = 10;
echo $a . "=\n";
include("include_path_test.php");
echo $a . "=\n";
echo relative() . "=";
?>
--EXPECT--
10=
12=
15=