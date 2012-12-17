--FILE--
<?php
function foo($a) {
    return $a * 10;
}
echo foo(15);

echo "=";

function foo2($a, $b) {
    return $a * $b;
}
echo foo2(15, 10);
?>
--EXPECT--
150=150