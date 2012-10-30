--FILE--
<?php
echo (1 == 0); //false
echo "==";
echo (333 == 333); //true
echo "==";
echo (0 == "a"); //true
echo "==";
echo (100 == "100"); //true
echo "==";
echo (100 == "1e2"); //true
echo "==";
echo (1 == "01"); //true
echo "==";
echo (26 == "0X1A"); //true
echo "==";
echo (26 == "0X1A"); //true
echo "==";
echo (26 == "0X1a"); //true
echo "==";
echo (27 == "0X1b"); //true
echo "==";
echo (27 == "027"); //true
echo "==";
echo (27 == "0027"); //true
echo "==";
echo (1 == "1eA"); //true
echo "==";
echo (27 == "0X1b"); //true
?>
--EXPECT--
==1==1==1==1==1==1==1==1==1==1==1==1