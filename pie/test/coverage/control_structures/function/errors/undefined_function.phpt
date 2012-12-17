--TEST--
Tests if undefined function message is printed right
--FILE--
<?php
test();
--EXPECT_ERROR--
PHP Fatal:  Call to undefined function test()%line 2
