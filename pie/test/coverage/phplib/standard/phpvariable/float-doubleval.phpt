--DOC--
Test for floatval() and doubleval() functions

http://www.php.net/manual/en/function.doubleval.php
http://www.php.net/manual/en/function.floatval.php

TODO: add array/object support
--FILE--
<?php
$var = '122.34343The';
$float_value_of_var = floatval($var);
echo $float_value_of_var; // 122.34343
?>
--EXPECT--
122.34343