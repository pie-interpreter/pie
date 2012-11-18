--TEST--
Test to see if all the float values are parsed more or less,
when var_dump will be implemented, we will be able to compare types
--FILE--
<?php
echo 1.2;
echo "=";
echo 1.0;
echo "=";
echo 000000.2000;
echo "=";
echo 1.;
echo "=";
echo .2;
echo "=";
echo -1.;
echo "=";
echo +.2;
echo "=";
echo 1e1;
echo "=";
echo 1e-2;
echo "=";
echo -1.2e2;
echo "=";
echo +1.23e2;
echo "=";
echo .2e-2;
?>
--EXPECT--
1.2=1=0.2=1=0.2=-1=0.2=10=0.01=-120=123=0.002
