--FILE--
<?php
echo ("a" != 0); //false
echo "=";
echo ("Hello" != "Hello"); //false
echo "=";
echo ("Hello World" != "HelloWorld"); //true
echo "=";
echo ("1" != "01"); //false
echo "=";
echo ("27" != "0x1a"); //true
?>
--EXPECT--
==1==1