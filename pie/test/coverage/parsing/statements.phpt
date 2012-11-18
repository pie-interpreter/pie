--FILE--
<?php
echo 1;
echo 2;
;;;
if (true) {
    echo 3;
};
{
    echo 4;
    echo 5;
}
{
    echo 6;
    echo 7;
    {
        echo 8;
    }
}
if (true) {{
        echo 9;
}}
if (false)
    echo "not here";
    echo 10;
?>
--EXPECT--
12345678910