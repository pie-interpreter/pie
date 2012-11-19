--TEST--
Tests if redeclared function message is printed right
--FILE--
<?php
include("pie/test/coverage/errors/include_path/redeclared_function_test.php");
include("pie/test/coverage/errors/include_path/redeclared_function_test.php");
--EXPECT_ERROR--
PHP Fatal:  Cannot redeclare relative() (previously declared in%redeclared_function_test.php:4)%redeclared_function_test.php on line 2