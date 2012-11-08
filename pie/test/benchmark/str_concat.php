<?php
$i = 0;
$a = "";
while ($i < 100000) {
    ++$i;
    $a = $a . "1";
}
$b = $a;
$a = 2;
//echo $b;
?>