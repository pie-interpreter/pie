--TEST--
Tests if missing argument message is printed right
--FILE--
<?php
test(5);
function test($a, $b, $c) {
    return $a;
}
?>
--EXPECT_ERROR--
PHP Warning:  Missing argument 2 for test(), called in % on line 2 and defined in % on line 3
PHP Stack trace:
PHP   1. {main}() %:0
PHP   2. test() %:2
PHP Warning:  Missing argument 3 for test(), called in % on line 2 and defined in % on line 3
PHP Stack trace:
PHP   1. {main}() %:0
PHP   2. test() %:2