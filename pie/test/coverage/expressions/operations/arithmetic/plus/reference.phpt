--FILE--
<?php
$a = "43";
$b = & $a;
$b = $b + 17;
echo ($a === 60) . "=\n";
$c = & $b;
$c = $c + $b;
echo ($a === 120) . "=";
?>
--EXPECT--
1=
1=