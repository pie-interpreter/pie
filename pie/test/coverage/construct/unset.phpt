--FILE--
<?php
$a = 5;
unset($a);
echo isset($a) . "=\n";

$a = 5;
$b = 6;
$c = 7;
unset($a, $b, $d);
echo isset($a) . "=\n";
echo isset($b) . "=\n";
echo isset($c) . "=\n";
echo isset($d) . "=";

?>
--EXPECT--
=
=
=
1=
=