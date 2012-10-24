<?php
function inc($a) {
    return $a + 1;
}
$i = 0;
$a = 0;
while($i < 10000000) {
    $a = inc($a);
    $i = $i + 1;
}
echo $a;
