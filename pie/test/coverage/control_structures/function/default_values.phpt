--FILE--
<?php
function test($a = 15) {
    return $a * 10;
}
echo test();

echo "=";

function test2($a = 15, $b = 10) {
    return $a * $b;
}
echo test2();

echo "=";

function test3($a = 15, $b) {
    return $a * $b;
}
echo test2(15, 10);
?>
--EXPECT--
150=150=150