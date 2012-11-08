<?php
$i = 0;
$a = "hello";
while ($i < 1000000) {
    ++$i;
    ++$a;
}
echo $a;
?>