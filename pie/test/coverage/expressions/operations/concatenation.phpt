--FILE--
<?php
echo "Hel" . "lo";
echo "=";
echo 5 . 5;
echo "=";
echo "Tes" . 55;
echo "=";
echo false . true;
echo "=";
echo true . 55;
echo "=";
echo "Less" . false;
?>
--EXPECT--
Hello=55=Tes55=1=155=Less