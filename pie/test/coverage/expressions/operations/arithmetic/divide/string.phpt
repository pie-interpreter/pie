--FILE--
<?php
$a = 4/"2.0";
echo ($a === 2.0) . "=\n";
$a = 4/"2";
echo ($a === 2) . "=\n";
$a = "2.0"/"2";
echo ($a === 1.0) . "=\n";
$a = "2.0"/"0.5";
echo ($a === 4.0) . "=\n";
$a = "10"/"2";
echo ($a === 5) . "=";
?>
--EXPECT--
1=
1=
1=
1=
1=