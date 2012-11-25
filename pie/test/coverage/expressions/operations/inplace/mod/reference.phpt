--TEST--
Test in-place for reference
--FILE--
<?php
$a = 50;
$b = & $a;
$a %= 4;
echo $b . "=\n";
echo $a . "=\n";
$c = & $b;
$b %= 3;
echo $b . "=\n";
echo $c . "=\n";
echo $a . "=";
--EXPECT--
2=
2=
2=
2=
2=