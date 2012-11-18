--FILE--
<?php
echo (null > null); //false
echo "=";
echo (null > 1); //false
echo "=";
echo (null > 0); //false
echo "=";
echo (null > "0"); //false
echo "=";
echo (null > ""); //false
echo "=";
echo (null > false); //false
echo "=";
echo (null > true); //false
?>
--EXPECT--
======