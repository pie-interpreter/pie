--FILE--
<?php
$a = 4;
$a /= 2;
echo ($a === 2) . "=\n";
echo ($a === 2.0) . "=\n";
$b = 5;
$b /= 2;
echo ($b === 2.5) . "=";
?>
--EXPECT--
1=
=
1=