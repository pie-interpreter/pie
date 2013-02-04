--FILE--
<?php
if (true) {
    function foo() {
        echo "1";
    }
} else {
    function foo($a) {
        echo "2";
    }
}
foo();
?>
--EXPECT--
1