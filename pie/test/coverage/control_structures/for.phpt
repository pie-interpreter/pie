--FILE--
<?php
for ($i = 0; $i < 5; $i = $i + 1)
    echo $i;

for ($i = 0, $j = 5; $i < 5; $i = $i + 1, $j = $j - 1) {
    echo $j;
}
for ($i = 0, $j = 5; $j = $j - 1, false, $i < 5; $i = $i + 1) {
    echo $i;
}
for (;;) {
    echo "hello";
    break;
}
for ($i = 0; $i < 5; $i = $i + 1):
    echo $i;
endfor;
for (;;):
    echo "hello";
    break;
endfor;
for ($i = 0; $i < 5; $i = $i + 1):
endfor;
for ($i = 0; $i < 5; $i = $i + 1):?>1<?php endfor;
?>
--EXPECT--
012345432101234hello01234hello11111