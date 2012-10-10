<?php
$contents = file_get_contents('test2.txt');
$tokens = token_get_all($contents);
    // var_dump($tokens);
foreach ($tokens as $token) {
    if (is_array($token)) {
        echo token_name($token[0]) . ': ' . $token[1] . "\n";
    } else {
        echo "STRING:" . $token . "\n";
    }
}
echo "a"
?>