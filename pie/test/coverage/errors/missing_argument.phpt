--TEST--
Tests if missing argument message is printed right
--FILE--
<?php
test(5);
function test($a, $b, $c) {
    return $a;
}
--EXPECT_ERROR--
PHP Warning:  Missing argument 2 for test(), called in %line 2 and defined in %line 3
PHP Warning:  Missing argument 3 for test(), called in %line 2 and defined in %line 3