--FILE--
<?php
$a = 4;
$b = & $a;
$b = $b * false;
echo ($b === 0) . "=\n";
$b = 5;
echo ($a === 5) . "=\n";
$c = & $b;
$c = 5.5 * 2;
echo ($a === 11.0) . "=\n";
echo ($b === 11.0) . "=";

?>
--EXPECT--
1=
1=
1=
1=