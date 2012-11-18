--FILE--
<?php
echo (string)false . "=\n";
echo (string)true . "=\n";
echo (string)null . "=\n";
echo (string)1 . "=\n";
echo (string)321 . "=\n";
echo (string)-32 . "=\n";
echo (string)"Hello" . "=";
?>
--EXPECT--
=
1=
=
1=
321=
-32=
Hello=