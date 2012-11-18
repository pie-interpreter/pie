--FILE--
<?php
echo (null == null); //true
echo "=";
echo (null == 1); //false
echo "=";
echo (null == 0); //true
echo "=";
echo (null == "0"); //false
echo "=";
echo (null == ""); //true
echo "=";
echo (null == false); //true
echo "=";
echo (null == true); //false
?>
--EXPECT--
1==1==1=1=