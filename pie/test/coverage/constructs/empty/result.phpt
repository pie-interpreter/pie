`--TEST--
This test has php 5.5 behaviour in mind:
empty can work on results of expressions

--FILE--
<?php
function test() {
    return 0;
}

function test1() {
    return false;
}

function test2() {
    return null;
}

function test3() {
    return "null";
}

echo empty(test()) . "=\n";
echo empty(test1()) . "=\n";
echo empty(test2()) . "=\n";
echo empty(test3()) . "=\n";
echo empty(12 * 42) . "=";
?>
--EXPECT--
1=
1=
1=
=
=