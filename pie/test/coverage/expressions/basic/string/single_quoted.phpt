--TEST--
Testing, that single-quoted string are parsed correctly and that
special symbols are correctly replaced
--FILE--
<?php
echo 'hello';
echo '=';
echo '\'hello\'';
echo '=';
echo 'hel\'lo';
echo '=';
echo '\h\e\l\l\o';
echo '=';
echo 'hel\\lo';
echo '=';
echo 'hel\\\lo';
echo '=';
echo 'hello\\';
echo '=';
echo 'привет';
?>
--EXPECT--
hello='hello'=hel'lo=\h\e\l\l\o=hel\lo=hel\\lo=hello\=привет
