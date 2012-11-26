--FILE--
<?php
$a = 1;
echo isset($a) . "=\n";
echo isset($b) . "=\n";
echo isset($a, $b) . "=\n";
echo isset($b, $a) . "=\n";
$b = 1;
echo isset($b, $a) . "=\n";
$c = null;
echo isset($c) . "=\n";
$d = & $b;
echo isset($b) . "=\n";
$b = null;
echo isset($b) . "=";
?>
--EXPECT--
1=
=
=
=
1=
=
1=
=