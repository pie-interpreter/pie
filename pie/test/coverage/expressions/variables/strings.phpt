--FILE--
<?php
$a = "Hello";
$b = $a;
$a = $a . ", World!";
echo $a . "=\n";
echo $b . "=";
?>
--EXPECT--
Hello, World!=
Hello=