--FILE--
<?php
echo "51" < "51.3";
echo "=";
echo "46.7" < "4e2";
echo "=";
echo "1e2" < "444.3";
echo "=";
echo 444 < "444.3";
echo "=";
echo 4 < "4.46";
?>
--EXPECT--
1=1=1=1=1