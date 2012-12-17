--FILE--
<?php
$a = 5 + 5;
$b = $a - 15;
echo $b . "=\n";
$c = 3;
$d = 4;
$c = $d;
$d = 6;
echo $c . "=";
?>
--EXPECT--
-5=
4=