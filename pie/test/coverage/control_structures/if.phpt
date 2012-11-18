--FILE--
<?php
if (true)
    echo 1;

if (true) {} else {}

if (false) {
    echo 2;
}

if (true)
    echo 1;
else
    echo 2;

if ($a = 3) { // assign expression in condition
    echo 1;
} else {
    echo 2;
}

if (false) {
    echo 1;
} else if (true) {
    echo 2;
}

if (false) {
    echo 1;
} else if (true) {
    echo 2;
} else {
    echo 3;
}

if (false) {
    echo 1;
} elseif ($a == 24) {
    echo 2;
}

if (false) {
    echo 1;
} elseif (true) {
    echo 2;
} else {
    echo 3;
}

if (true)
    if (false)
        echo 2;
    else
        echo 3;

if (true):
    echo 1;
endif;

if (false):
else:
endif;

if (false):
elseif (true):
else:
endif;

if (false):
    echo 1;
elseif (true):
    echo 2;
    echo 2;
else:
    echo 3;
endif;

if (true):
    if (false):
        echo 2;
    else:
        echo 3;
    endif;
endif;

if (true):
?>5<?php
endif;
?>
--EXPECT--
111222312235
