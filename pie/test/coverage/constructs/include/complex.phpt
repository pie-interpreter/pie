--TEST--
Test inclusion of files with same names but from diffirent paths
--FILE--
<?php
$a = 10;
echo $a . "=\n";
include_once("complex.php");
echo $a . "=\n";
$a = 15;
echo $a . "=\n";
include_once("pie/test/coverage/constructs/include/complex_include_path/path1/complex.php");
echo $a . "=\n";
include_once("pie/test/coverage/constructs/include/complex_include_path/path2/complex.php");
echo $a . "=";
?>
--EXPECT--
10=
path1=
15=
15=
path2=