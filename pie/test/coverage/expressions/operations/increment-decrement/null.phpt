--FILE--
<?php
$a = null;
echo (++$a);
echo "=";
$a = null;
echo ($a--);
echo "=";
echo $a;
echo "=";
echo (--$a);
?>
--EXPECT--
1===