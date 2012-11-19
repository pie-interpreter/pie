--TEST--
Test file inclusion from include_path which includes another file

ATTENTION: to work correctly, "pie/test/coverage/constructs/include/include_path" should be
defined in include_path in conf/pie.ini

--FILE--
<?php
$a = 10;
echo $a . "=\n";
include("include_path_and_calling_path.php");
echo $a . "=\n";
echo relative() . "=\n";
echo $b . "="
?>
--EXPECT--
10=
12=
15=
10=