--TEST--
Tests if division by zero message is printed right
--FILE--
<?php
test();
function test() {
    $c = 10;
//    echo $c/0;
}
--EXPECT_ERROR--
PHP Warning:  Division by zero%line 6