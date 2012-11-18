--FILE--
<?php
echo (1 != 0); //true
echo "=";
echo (333 != 333); //false
echo "=";
echo (0 != "a"); //false
echo "=";
echo (100 != "100"); //false
echo "=";
echo (100 != "1e2"); //false
echo "=";
echo (1 != "02"); //true
echo "=";
echo (-27 != "-0X1b"); //true
?>
--EXPECT--
1=====1=1