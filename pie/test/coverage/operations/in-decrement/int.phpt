--FILE--
<?php
$a = 1;
echo ++$a;
echo "=";
echo $a++;
echo "=";
echo $a;
$b = 10;
echo "=";
echo --$b;
echo "=";
echo $b--;
echo "=";
echo $b;
?>
--EXPECT--
2=2=3=9=9=8