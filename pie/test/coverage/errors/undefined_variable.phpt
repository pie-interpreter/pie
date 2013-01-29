--TEST--
Tests if undefined variable message is printed right
--FILE--
<?php
echo $b;
test();
function test() {
    echo $c;
}
?>
--EXPECT_ERROR--
PHP Notice:  Undefined variable: b%line 2
PHP Stack trace:
PHP   1. {main}() %:0
PHP Notice:  Undefined variable: c%line 5
PHP Stack trace:
PHP   1. {main}() %:0
PHP   2. test() %:3