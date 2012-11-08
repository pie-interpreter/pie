--FILE--
<?php
$a = "Hello";
echo ++$a;
echo "=";
echo $a++;
echo "=";
echo $a;
$b = "H";
echo "=";
echo --$b;
echo "=";
echo $b--;
echo "=";
echo $b;
echo "=";
$c = "Z";
echo $c;
echo "=";
echo ++$c;
echo "=";
$c = "z";
echo $c;
echo "=";
echo ++$c;
$c = "";
echo "=";
echo ++$c;
echo "=";
echo ++$c;
echo ($c === "1"); //true
$c = "";
echo "=";
echo --$c;
echo "=";
echo ($c === -1); //true;
echo "=";
$c = "10";
echo ++$c;
$c = "10";
echo "=";
echo --$c;
$c = "0";
echo "=";
echo --$c;
$d = "-1e2";
echo "=";
echo --$d;
$e = "hellz";
echo "=";
echo ++$e;
$w = "zzz";
echo "=";
echo ++$w;
$z = "9";
echo "=";
echo ++$z;
$a = 'ф';
echo "=";
echo ++$a;
$a = "z{z";
echo "=";
echo ++$a;
$a = "A109";
echo "=";
echo ++$a;
?>
--EXPECT--
Hellp=Hellp=Hellq=H=H=H=Z=AA=z=aa=1=2=-1=1=11=9=-1=-101=helma=aaaa=10=ф=z{a=A110