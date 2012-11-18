--FILE--
<?php
echo (null != null); //false
echo "=";
echo (null != 12); //true
echo "=";
echo (null != 0); //false
echo "=";
echo (null != "0"); //true
echo "=";
echo (null != ""); //false
echo "=";
echo (null != false); //false
echo "=";
echo (null != true); //true
?>
--EXPECT--
=1==1===1