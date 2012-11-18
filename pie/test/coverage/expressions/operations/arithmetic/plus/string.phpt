--FILE--
<?php
echo "Hello" + "World";
echo "=\n";
echo 5 + "-10Hello";
echo "=\n";
echo 5 + "Hello";
echo "=\n";
echo "53" + "12";
echo "=\n";
echo "4.5" + 12;
echo "=\n";
echo "4.5" + "6.5";
?>
--EXPECT--
0=
-5=
5=
65=
16.5=
11
