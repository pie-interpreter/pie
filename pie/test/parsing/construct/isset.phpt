--COMPILEONLY--
--FILE--
<?php
$a = 1;
echo isset($a) . "=\n";
echo isset($b) . "=\n";
echo isset($a, $b) . "=\n";
echo isset($b, $a) . "=\n";
?>
--EXPECT--
1=
=
=
=