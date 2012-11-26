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
echo isset($d) . "=\n";

// references
$d = &$c;
echo isset($d) . "=\n";
unset($d);
echo isset($d) . "=\n";
echo isset($c) . "=";
?>
--EXPECT--
=
=
=
1=
=
1=
=
1=