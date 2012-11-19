--TEST--
Test file inclusion from the working directory (in this case - from the top
directory, where run_tests.py is situated)
--FILE--
<?php
$a = 10;
echo $a . "=\n";
include("do_not_delete_include_test.php");
echo $a . "=\n";
echo relative() . "=";
?>
--EXPECT--
10=
12=
15=