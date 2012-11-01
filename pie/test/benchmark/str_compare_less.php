<?php
$i = 0;
$a = "hellofkdjalkfdjs";
$b = "hellofkdfalkfdjs";
$c = 1;
while ($i < 10000000) {
    if ($a < $b) {
        $c = 1;
    }
    ++$i;
}
echo $a;
?>