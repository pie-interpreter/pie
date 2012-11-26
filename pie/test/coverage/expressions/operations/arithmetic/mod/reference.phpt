--FILE--
<?php
$a = 4;
$b = & $a;
$b = $b % 3;
echo ($b === 1) . "=\n";
echo ($a === 1) . "=";
?>
--EXPECT--
1=
1=