--TEST--
Testing different situatinos for ternary operator.
This test will fail on traditional php interpreter, because of different
ternary operator associativity (PHP's sucks)
--FILE--
<?php
echo true ? "1" : "2";
echo "=";
echo (1 + 2) ? "1" : "2";
echo "=";
echo (12 - 12) ? "1" : "2";
echo "=";

$a = 2;
echo $a == 1 ? "1" :
     $a == 2 ? "2" :
     $a == 3 ? "3" :
     "4";
echo "=";

echo $a ?: "not_a"; // this should output value of $a
echo "=";
echo false ?: "false"; // this should output "false"
?>
--EXPECT--
1=1=2=2=2=false