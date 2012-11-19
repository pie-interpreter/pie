<?php
$a = 10;
echo $a . "=\n";
function test() {
    include_once("examples/test1.php");
}
echo $a . "=\n";
echo test() . "=";
