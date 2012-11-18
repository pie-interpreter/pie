--FILE--
<?php
echo (bool)false . "=\n";
echo (bool)true . "=\n";
echo (bool)null . "=\n";
echo (bool)1 . "=\n";
echo (bool)321 . "=\n";
echo (bool)-32 . "=\n";
echo (bool)"Hello" . "=\n";
echo (bool)"123Hello" . "=\n";
echo (bool)"123e1Hello" . "=\n";
echo (bool)"" . "=\n";
echo (bool)"0" . "=\n";
echo (bool)0 . "=\n";
echo (bool)-1 . "=\n";
echo (bool)"123.3e1Hello" . "=";
?>
--EXPECT--
=
1=
=
1=
1=
1=
1=
1=
1=
=
=
=
1=
1=