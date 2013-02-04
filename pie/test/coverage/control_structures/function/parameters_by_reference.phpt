--FILE--
<?php
$a = 5;
function foo(&$a) {
    $a++;
}
foo($a);
echo $a;

echo "=";

$a = 5;
function foo2(&$a, &$b) {
    $a++;
    $b++;
}
foo2($a, $a);
echo $a;

?>
--EXPECT--
6=7