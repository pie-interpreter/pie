--FILE--
<?php
$a = 5;
function test(&$a) {
    $a++;
}
test($a);
echo $a;

echo "=";

$a = 5;
function test2(&$a, &$b) {
    $a++;
    $b++;
}
test2($a, $a);
echo $a;

?>
--EXPECT--
6=7