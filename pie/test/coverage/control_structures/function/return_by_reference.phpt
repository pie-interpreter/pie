--FILE--
<?php
$a = 5;
function &foo(&$a) {
    return $a;
}
$b = &foo($a);
$b++;
echo $b;
echo $a;
?>
--EXPECT--
66