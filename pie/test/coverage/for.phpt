--FILE--
<?php
$a = 10;
for ($i = 0; $i < 10; $i = $i + 1) {
    $a = $a + 10;
}
echo $a;
?>
--EXPECT--
110