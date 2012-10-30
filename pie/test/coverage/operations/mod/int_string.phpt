--FILE--
<?php
$a = false; //$a = 5 % "HelloWorld!";
echo "HelloWorld!" % 5;
echo "=";
echo "52HelloWorld!" % 5;
echo "=";
echo $a == false; //true
?>
--EXPECT--
0=2=1