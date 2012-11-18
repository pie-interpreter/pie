--COMPILEONLY--
--FILE--
<?php
$a = 10;
$b = & $a;
echo $b;
echo "=";

$b++;
echo $a, $b;
echo "=";
/*
function foo(&$b, $c) {
    $b++;
    $c++;
}

$c = 20;
foo($b, $c);
echo $b, $c;
echo "=";

function &bar() {
    $a = 30;
    return $a;
}
$d = bar();
echo $d;*/
?>
--EXPECT--
10=1111=1220=30