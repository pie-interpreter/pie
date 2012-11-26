--FILE--
<?php
$a = 10;
$b = & $a;
$c = & $b;
$c++;
echo $a . "=\n";
echo $b . "=\n";
++$c;
echo $a  . "=\n";
echo $b . "=\n";
--$c;
echo $a  . "=\n";
echo $b . "=\n";
$c--;
echo $a  . "=\n";
echo $b . "=";
--EXPECT--
11=
11=
12=
12=
11=
11=
10=
10=