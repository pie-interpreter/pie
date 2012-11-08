--FILE--
<?php
$a = false;
++$a;
echo ($a === false); //true
echo "=";
$a++;
echo ($a === false); //true
echo "=";
$a = true;
++$a;
echo ($a === true); //true
echo "=";
$a++;
echo ($a === true); //true
?>
--EXPECT--
1=1=1=1