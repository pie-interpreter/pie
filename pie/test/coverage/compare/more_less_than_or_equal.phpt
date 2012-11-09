--FILE--
<?php
echo (5 >= 5);
echo "=";
echo (6 >= 5);
echo "=";
echo (5 <= 5);
echo "=";
echo (5 <= 11);
echo "=";
echo (null <= "0"); //true
echo "=";
echo (null <= ""); //true
echo "=";
echo (null >= false); //true
echo "=";
echo (null >= true); //false
?>
--EXPECT--
1=1=1=1=1=1=1=