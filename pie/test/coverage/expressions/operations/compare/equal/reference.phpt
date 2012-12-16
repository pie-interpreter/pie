--FILE--
<?php
$a = "test";
$b = & $a;
$c = "test";
$d = & $c;
echo ($a === $c) . "=";
--EXPECT--
1=