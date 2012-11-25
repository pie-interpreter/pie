--FILE--
<?php
$a = "Hello";
echo empty($a) . "=\n";
$a = "";
echo empty($a) . "=\n";
$a = 1;
echo empty($a) . "=\n";
$a = -1;
echo empty($a) . "=\n";
$a = 0;
echo empty($a) . "=\n";
$a = (float)"-1.0";
echo empty($a) . "=\n";
$a = (float)"0.0";
echo empty($a) . "=\n";
$a = "1";
echo empty($a) . "=\n";
$a = "0";
echo empty($a) . "=\n";
$a = null;
echo empty($a) . "=\n";
$a = true;
echo empty($a) . "=\n";
$a = false;
echo empty($a) . "=\n";
// check for non-existing variable
echo empty($b) . "=\n";
// check for reference
$b = &$a;
echo empty($b) . "=\n";
$a = 1;
echo empty($b) . "=";
?>
--EXPECT--
=
1=
=
=
1=
=
1=
=
1=
1=
=
1=
1=
1=
=