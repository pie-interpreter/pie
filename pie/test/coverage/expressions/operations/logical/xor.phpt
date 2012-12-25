--FILE--
<?php
$a = "test";
$b = 4;
echo ($a xor $b) . "=\n"; //false
$a = "";
echo ($a xor $b) . "=\n"; //true
$b = null;
echo ($a xor $b) . "=\n"; //false
$a = true;
echo ($a xor $b) . "="; //true
?>
--EXPECT--
=
1=
=
1=