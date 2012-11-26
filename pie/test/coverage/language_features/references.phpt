--FILE--
<?php
$a = 10;
$b = & $a;
echo $b . "=\n";

$b++;
echo $a  . "=\n";
echo $b  . "=\n";

/*
function foo(&$b, $c) {
    $b++;
    $c++;
}

$c = 20;
foo($b, $c);
echo $b . "=\n";
echo $c  . "=\n";
function &bar() {
    $a = 30;
    return $a;
}
$d = bar();
echo $d . "="; */
?>
--EXPECT--
10=
11=
11=