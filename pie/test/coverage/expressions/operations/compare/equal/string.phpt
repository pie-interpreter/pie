--FILE--
<?php
echo ("a" == 0); //true
echo "=";
echo ("Hello" == "Hello"); //true
echo "=";
echo ("Hello World" == "Hello World"); //true
echo "=";
echo ("1" == "01"); //true
echo "=";
echo ("100" == "1e2"); //true
echo "=";
echo ("26" == "0x1a"); //true
echo "=";
echo ("-100" == "-1e2"); //true
echo "=";
echo ("-100" == "-1e2A"); //false
echo "=";
echo (true == "0" . "0"); //true
echo "=";
echo (false == "0" . ""); //true
?>
--EXPECT--
1=1=1=1=1=1=1==1=1