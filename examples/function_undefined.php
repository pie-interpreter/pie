<?php
function test2($n) {
    return test1($n);
}

function test($n) {
    return test2($n + 5);
}
echo test(5);
?>