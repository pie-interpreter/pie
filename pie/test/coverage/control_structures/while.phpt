--FILE--
<?php
$i = 0;
while ($i < 5)
    $i = $i + 1;
echo $i;

$i = 0;
while ($i < 5) {
    $i = $i + 1;
    echo $i;
}

$i = 5;
while ($i = $i - 1);
echo $i;

$i = 0;
while ($i < 5):
    $i = $i + 1;
endwhile;
echo $i;

$i = 5;
while ($i = $i - 1): endwhile;
echo $i;

$i = 0;
while ($i < 5):
    $i = $i + 1;
    ?>Z<?php
endwhile;
?>
--EXPECT--
512345050ZZZZZ