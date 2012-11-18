--FILE--
<?php
echo 5; // simple expression
echo "=";
echo ("hello"); // expression in parenthesis
echo "=";
echo 12, 15, 17; // comma-seperated expressions
?>
--EXPECT--
5=hello=121517
