--FILE--
<?php
$a = 4;
$a /= true;
echo ($a === 4.0) . "=\n";
$b = true;
$b /= 2;
echo ($b === 0.5) . "=\n";
$b = false;
$b /= 2;
echo ($b === 0.0) . "=";
?>
--EXPECT--
=
1=
=