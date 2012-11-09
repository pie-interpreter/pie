--FILE--
<?php
echo (int)false . "=\n";
echo (int)true . "=\n";
echo (int)null . "=\n";
echo (int)1 . "=\n";
echo (int)321 . "=\n";
echo (int)-32 . "=\n";
echo (int)"Hello" . "=\n";
echo (int)"123Hello" . "=\n";
echo (int)"123e1Hello" . "=\n";
echo (int)"123.3e1Hello" . "=";
?>
--EXPECT--
0=
1=
0=
1=
321=
-32=
0=
123=
123=
123=