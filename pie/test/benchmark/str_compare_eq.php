<?php
$i = 0;
$a = "hellofkdjalkfdjs";
$b = "hellofkdjalkfdjs";
$c = 1;
while ($i < 1000000) {
    if ($a == $b) {
        $c = 1;
    }
    ++$i;
}
echo $a;
?>