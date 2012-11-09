--FILE--
<?php
$a = 5;
echo $a . "=\n";
$b = (unset) $a;
echo ($b === null). "=\n";
echo $a . "=";
?>
--EXPECT--
5=
1=
5=