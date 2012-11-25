--FILE--
<?php
echo "Hel" . "lo" . "=\n";
echo 5 . 5 . "=\n";
echo "Tes" . 55 . "=\n";
echo false . true . "=\n";
echo true . 55 . "=\n";
echo "Less" . false . "=\n";
$a = "test";
$b = & $a;
echo $b . $b . "=";
?>
--EXPECT--
Hello=
55=
Tes55=
1=
155=
Less=
testtest=