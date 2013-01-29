--TEST--
Tests if undefined function message is printed right
--FILE--
<?php
test();
?>
--EXPECT_ERROR--
PHP Fatal error:  Call to undefined function test()% on line 2
PHP Stack trace:
PHP   1. {main}() %:0