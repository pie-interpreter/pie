--FILE--
<?php
$a = 4;
$b = & $a;
$b = $b/true;
echo ($b === 4) . "=\n";
$b = 5;
echo ($a === 5) . "=\n";
$c = & $b;
$c = 5.5/2;
echo ($a === 2.75) . "=\n";
echo ($b === 2.75) . "=";

?>
--EXPECT--
1=
1=
1=
1=