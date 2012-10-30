--FILE--
<?php
echo (true != false); //true
echo "=";
echo (true != true); //false
echo "=";
echo (false != false); //false
echo "=";
echo (false != true); //true
echo "=";
echo (true != "Hello"); //false
echo "=";
echo (true != 0); //true
echo "=";
echo (true != 12); //false
echo "=";
echo (false != ""); //false
echo "=";
echo (false != 0); //false
?>
--EXPECT--
1===1==1===