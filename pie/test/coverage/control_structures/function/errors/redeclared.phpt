--TEST--
Tests if redeclared function message is printed right
--FILE--
<?php

include("pie/test/coverage/control_structures/function/errors/redeclared.inc.php");
include("pie/test/coverage/control_structures/function/errors/redeclared.inc.php");
?>
--EXPECT_ERROR--
PHP Fatal:  Cannot redeclare foo() (previously declared in %redeclared.inc.php:2)in %redeclared.inc.php on line 2