--DOC--
Test for gettype() function
http://www.php.net/manual/en/function.gettype.php

TODO: add array, object and resource support
--FILE--
<?php
echo gettype(true) . "\n";
echo gettype(0) . "\n";
echo gettype(1.2) . "\n";
echo gettype("string") . "\n";
echo gettype(null);
?>
--EXPECT--
boolean
integer
double
string
NULL