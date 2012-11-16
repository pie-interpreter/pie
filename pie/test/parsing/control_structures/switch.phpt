--FILE--
<?php

$a = 2;
switch ($a) {
    case 1:
        echo "1";
        break;
    case 2:
        echo "2";
        break;
    case 3:
        echo "3";
        break;
}
echo "\n";

$a = "hello";
switch ($a) {
    case "hello":
        echo "1";
        break;
    case "bye":
        echo "2";
        break;
    case "see you":
        echo "3";
        break;
}
echo "\n";

$a = "12";
switch ($a) {
    case "12":
        echo "1";
        break;
    case 12:
        echo "2";
        break;
    case 0:
        echo "3";
        break;
}
echo "\n";

$a = 2;
switch ($a) {
    case 1:
        echo "1";
        break;
    case 2:
        break;
    case 3:
        echo "3";
        break;
}
echo "\n";

$a = 2;
switch (++$a) {
    case 1:
        echo "1";
        break;
    case 2:
        echo "2";
        break;
    case 3:
        echo "3";
        break;
}
echo "\n";

$a = 5;
switch ($a) {
    case 1:
        echo "1";
        break;
    case 2:
        echo "2";
        break;
    case 3:
        echo "3";
        break;
    default:
        echo "4";
}
echo "\n";

$a = 3;
switch ($a) {
    default:
        echo "4";
        break;
    case 1:
        echo "1";
        break;
    case 2:
        echo "2";
        break;
    case 3:
        echo "3";
        break;
}
echo "\n";

$a = 5;
switch ($a) {
    case 1:
        echo "1";
        break;
    default:
        echo "4";
    case 2:
        echo "2";
        break;
    case 3:
        echo "3";
        break;
}
echo "\n";

$a = 1;
switch ($a) {
    case 1:
        echo "1";
    case 2:
        echo "2";
        break;
    case 3:
        echo "3";
        break;
}
echo "\n";

$a = 2;
switch ($a) {
    case 1:
        echo "1";
        break;
    case 2:
    case 3:
        echo "3";
        break;
}
echo "\n";

$a = 2;
switch ($a) {
    case 1:
        echo "1";
        break;
    case 2:
        echo "2";
        continue;
    case 3:
        echo "3";
        break;
}
echo "\n";

do {
    $a = 2;
    switch ($a) {
        case 1:
            echo "1";
            break;
        case 2:
            echo "2";
            break 2;
        case 3:
            echo "3";
            break;
    }
    echo "hello";
} while(false);
echo "\n";

$a = 2;
switch ($a):
    case 1:
        echo "1";
        break;
    case 2:
        echo "2";
        break;
    case 3:
        echo "3";
        break;
endswitch;
echo "\n";

$a = 3;
switch ($a) {
    case 1;
        echo "1";
        break;
    case 2;
        echo "2";
        continue;
    case 3;
        echo "3";
        break;
}
echo "\n";

$a = 3;
$b = 0;
switch ($a) {
    case ++$b;
        echo "wrong";
        break;
    case ++$b;
        echo "wrong";
        break;
    case ++$b;
        echo $b;
        break;
}
echo "\n";

$a = 2;
switch ($a) {
    case 1: {
        echo "1";
        break;
    }
    case 2: {
        echo "2";
        break;
    }
    case 3: {
        echo "3";
        break;
    }
}
switch ($a) {
}
?>
--EXPECT--
2
1
1

3
4
3
42
12
3
2
2
2
3
3
2
