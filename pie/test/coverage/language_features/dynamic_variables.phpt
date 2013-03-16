--FILE--
<?php
$a = 'hello';
$$a = 'world';
echo $a . ' ' . $$a;
echo "\n";
echo ${'hel' . 'lo'};

// TODO uncomment, when arrays are ready:
// $e = 42;
// echo $$a[1];
// echo ${$a[1]};
// echo ${$a}[1];
?>
--EXPECT--
hello world
world