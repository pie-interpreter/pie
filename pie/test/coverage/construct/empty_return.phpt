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
echo empty(test3()) . "=";
?>
--EXPECT--
1=
1=
1=
=