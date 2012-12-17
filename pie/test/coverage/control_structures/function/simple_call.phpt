--FILE--
<?php
function test($a) {
    return $a * 10;
}
echo test(15);

echo "=";

function test2($a, $b) {
    return $a * $b;
}
echo test2(15, 10);
?>
--EXPECT--
150=150