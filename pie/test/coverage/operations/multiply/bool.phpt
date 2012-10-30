--FILE--
<?php
echo 50 * true;
echo "=";
echo -14 * false;
echo "=";
echo true * true;
?>
--EXPECT--
50=0=1