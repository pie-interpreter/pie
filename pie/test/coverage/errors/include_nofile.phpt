--TEST--
Tests if no file inclusion message is printed right
--FILE--
<?php
include("no_include.php");
include("../still_no_include.php");
?>
--EXPECT_ERROR--
PHP Warning:  include(no_include.php): failed to open stream: No such file or directory%line 2
PHP Stack trace:
PHP   1. {main}() %:0
PHP Warning:  include(): Failed opening 'no_include.php' for inclusion (include_path='.:/usr/share/php:pie/test/coverage/constructs/include/include_path%line 2
PHP Stack trace:
PHP   1. {main}() %:0
PHP Warning:  include(../still_no_include.php): failed to open stream: No such file or directory%line 3
PHP Stack trace:
PHP   1. {main}() %:0
