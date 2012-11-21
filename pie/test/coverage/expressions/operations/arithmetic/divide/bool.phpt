--FILE--
<?php
$a = 4/true;
echo ($a === 4.0) . "=\n";
$b = true/2;
echo ($b === 0.5) . "=\n";
$b = false/2;
echo ($b === 0.0) . "=";
?>
--EXPECT--
=
1=
=