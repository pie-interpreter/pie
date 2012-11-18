--FILE--
<?php
echo (5 % 3)."=\n";           // prints 2
echo (5 % -3)."=\n";          // prints 2
echo (-5 % 3)."=\n";          // prints -2
echo (-5 % -3)."=";         // prints -2
?>
--EXPECT--
2=
2=
-2=
-2=