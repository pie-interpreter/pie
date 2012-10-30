--FILE--
<?php
echo (true == false); //false
echo "==";
echo (true == true); //true
echo "==";
echo (false == false); //true
echo "==";
echo (true == true); //true
echo "==";
echo (true == "Hello"); //true
echo "==";
echo (true == 1); //true
echo "==";
echo (true == 12); //true
echo "==";
echo (false == ""); //true
echo "==";
echo (false == 0); //true
?>
--EXPECT--
==1==1==1==1==1==1==1==1