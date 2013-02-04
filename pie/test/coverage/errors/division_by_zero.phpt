--TEST--
Tests if division by zero message is printed right
--FILE--
<?php
test();
function test() {
    $c = 10;
    echo $c/0;
}
?>
--EXPECT_ERROR--
PHP Warning:  Division by zero% on line 5
PHP Stack trace:
PHP   1. {main}() %:0
PHP   2. test() %:2