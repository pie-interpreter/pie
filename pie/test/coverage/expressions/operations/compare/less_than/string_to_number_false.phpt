--FILE--
<?php
echo "51" < "Hello" . "51";
echo "=";
echo "51" < "55";
echo "=";
echo "51" < "45";
echo "=";
echo "51" . "Hello" < "Hello" . "51";
?>
--EXPECT--
1=1==1