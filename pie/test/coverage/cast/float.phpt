--FILE--
<?php
echo (float)false . "=\n";
echo (float)true . "=\n";
echo (float)null . "=\n";
echo (float)1 . "=\n";
echo (float)321 . "=\n";
echo (float)-32 . "=\n";
echo (float)"Hello" . "=\n";
echo (float)"123Hello" . "=\n";
echo (float)"123.321Hello" . "=\n";
echo (float)"123.32e1Hello" . "=";
?>
--EXPECT--
0.0=
1.0=
0.0=
1.0=
321.0=
-32.0=
0.0=
123.0=
123.321=
1233.2=