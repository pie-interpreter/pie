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
echo isset($c) . "=";
?>
--EXPECT--
1=
=
=
=
1=
=