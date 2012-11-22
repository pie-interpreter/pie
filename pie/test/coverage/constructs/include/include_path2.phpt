--TEST--
Test file inclusion with path from include_path

ATTENTION: to work correctly, "pie/test/coverage/constructs/include/include_path" should be
defined in include_path in conf/pie.ini

--FILE--
<?php
$a = 10;
echo $a . "=\n";
include("test_path/include_test.php");
echo $a . "=";
?>
--EXPECT--
10=
include_path=