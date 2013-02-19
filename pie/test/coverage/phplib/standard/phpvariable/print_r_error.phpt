--TEST--
Test for print_r() function in case when PHP Warning is generated

TODO: add array, object and resource support
--FILE--
<?php
echo "dummy string";
//$test = print_r
?>
--EXPECT--
dummy string