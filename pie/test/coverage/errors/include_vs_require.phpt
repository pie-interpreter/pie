--TEST--
Tests if no file inclusion message is printed right
--FILE--
<?php
include("no_include.php");
require("no_include.php");
--EXPECT_ERROR--
PHP Warning:  include(no_include.php): failed to open stream: No such file or directory%line 2
PHP Warning:  include(): Failed opening 'no_include.php' for inclusion (include_path='.:/usr/share/php:pie/test/coverage/constructs/include/include_path')%line 2
PHP Fatal:  require(no_include.php): failed to open stream: No such file or directory%line 3
PHP Fatal:  require(): Failed opening required 'no_include.php' for inclusion (include_path='.:/usr/share/php:pie/test/coverage/constructs/include/include_path')%line 3