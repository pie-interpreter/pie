--FILE--
<?php
$a = 4;
$b = 3.0;
echo ($a >= $b) . "=\n";
$a = 3;
echo ($a >= $b) . "=\n";
echo ($a > $b) . "=";
?>
--EXPECT--
1=
1=
=