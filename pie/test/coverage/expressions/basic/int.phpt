--FILE--
<?php
echo 0;
echo "=";
echo -12;
echo "=";
echo +0123;
echo "=";
echo -0b0101;
echo "=";
echo +0xAF;
?>
--EXPECT--
0=-12=83=-5=175
