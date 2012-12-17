--FILE--
<?php
function foo() {
    function bar() {
        echo "bar";
    }
    echo "foo";
}
foo();
bar();
?>
--EXPECT--
foobar