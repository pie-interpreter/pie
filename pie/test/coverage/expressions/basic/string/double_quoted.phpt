--TEST--
Testing, that double-quoted string are parsed correctly and that
special symbols are correctly replaced
--FILE--
<?php
echo "hello";
echo "=";
echo "\"hello\"";
echo "=";
echo "hel\"lo";
echo "=";
echo "\hello";
echo "=";
echo "hel\\lo";
echo "=";
echo "hel\\\lo";
echo "=";
echo "hello\\";
echo "=";
echo "привет";
echo "=";
echo "he\nllo";
echo "=";
echo "he\xllo"; // invalid hex char
echo "=";
echo "he\xAllo"; // valid 1-symbol hex char
echo "=";
echo "he\x2Bllo"; // valid 2-symbol hex char
echo "=";
echo "he\x2BAllo"; // valid 2-symbol hex char, followed by valid symbol
echo "=";
echo "he\9llo"; // invalid oct char
echo "=";
echo "he\12llo"; // valid 2-symbol oct char
echo "=";
echo "he\136llo"; // valid 3-symbol oct char
echo "=";
echo "he\1366llo"; // valid 3-symbol oct char, followed by valid symbol
?>
--EXPECT--
hello="hello"=hel"lo=\hello=hel\lo=hel\\lo=hello\=привет=he
llo=he\xllo=he
llo=he+llo=he+Allo=he\9llo=he
llo=he^llo=he^6llo
