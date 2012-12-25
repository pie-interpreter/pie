--FILE--
<?php
echo (!true === false) . "=\n"; //true
echo (!false === true) . "=\n"; //true
echo (!"" == false) . "=\n"; //false
echo (!"Cat" == true) . "=\n"; //false
echo (!0 == true) . "=\n"; //true
echo (!5 == false) . "=\n"; //true
echo (!null == true) . "=\n"; //true
$a = 5;
$b = $a;
echo (!$b == false) . "="; //true
?>
--EXPECT--
1=
1=
=
=
1=
1=
1=
1=