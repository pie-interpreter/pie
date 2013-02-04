--FILE--
<?php
$a = 5;
function foo(&$a = 10) {
    $a++;
    echo $a;
}
foo();
foo($a);
echo $a;
?>
--EXPECT--
1166