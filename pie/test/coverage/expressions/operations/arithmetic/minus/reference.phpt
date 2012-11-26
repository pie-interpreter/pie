--FILE--
<?php
$a = "43";
$b = & $a;
$b = $b - 13;
echo ($a === 30) . "=\n";
$c = & $b;
$c = $c - $b;
echo ($a === 0) . "=";
?>
--EXPECT--
1=
1=