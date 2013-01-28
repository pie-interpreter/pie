--FILE--
<?php
$a = (array)false;
$a = (array)true ;
$a = (array)null ;
$a = (array)1 ;
$a = (array)321 ;
$a = (array)-32 ;
$a = (array)"Hello" ;
$a = (array)"123Hello" ;
$a = (array)"123e1Hello" ;
$a = (array)"123.3e1Hello";
?>
--EXPECT--
0=
1=
0=
1=
321=
-32=
0=
123=
123=
123=