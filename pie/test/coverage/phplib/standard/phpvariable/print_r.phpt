--TEST--
Test for print_r() function
http://www.php.net/manual/en/function.print-r.php

ATTENTION: turn off automatic trim of whitespaces on file save otherwise
    after saving test could start failing!!!!


TODO: add array, object and resource support
--FILE--
<?php
$a = 1;
$test = print_r($a);
echo "=\n";
echo $test . "=\n";
print_r(321);
echo "=\n";
print_r(1.32);
echo "=\n";
print_r(false);
echo "=\n";
print_r(true);
echo "=\n";
print_r(null);
echo "=\n";
print_r("string");
echo "=\n";
print_r("1.3");
echo "=\n";
echo "+++++\n";
// array
print_r(array());
print_r(array(1,2.32,"test", null, false));
print_r(array(3,3,array(4, 3 => "test", "6" => "value")));
echo "+++++\n";
//redirect output
$a = print_r(12, 1);
echo $a . "=\n";
$a = print_r(12, 1.32);
echo $a . "=\n";
$a = print_r(12, true);
echo $a . "=\n";
$a = print_r(12, "1");
echo $a . "=\n";
?>
--EXPECT--
1=
1=
321=
1.32=
=
1=
=
string=
1.3=
+++++
Array
(
)
Array
(
    [0] => 1
    [1] => 2.32
    [2] => test
    [3] => 
    [4] => 
)
Array
(
    [0] => 3
    [1] => 3
    [2] => Array
        (
            [0] => 4
            [3] => test
            [6] => value
        )

)
+++++
12=
12=
12=
12=