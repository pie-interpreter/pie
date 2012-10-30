--FILE--
<?php
echo (5 !== "5"); //true
echo "=";
echo (5 !== 5); //false
echo "=";
echo (5 === 5); //true
echo "=";
echo (5 !== 11); //true
echo "=";
echo "0" !== false; //true
echo "=";
echo "1" !== true; //true
echo "=";
echo "1" === false; //false
echo "=";
echo 1 !== true; //true
echo "=";
echo 0 === false; //false
?>
--EXPECT--
1==1=1=1=1==1=