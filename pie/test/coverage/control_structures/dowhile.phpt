--FILE--
<?php
$i = 0;
do
    $i = $i + 1;
while ($i < 5);
echo $i;

$i = 0;
do {
    $i = $i + 1;
    echo $i;
} while ($i < 5);

$i = 5;
do {
} while ($i = $i - 1);
echo $i;

do {
    echo "hello";
} while (false);
?>
--EXPECT--
5123450hello