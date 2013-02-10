--DOC--
Test for is_*() functions set
http://www.php.net/manual/en/function.is-array.php
http://www.php.net/manual/en/function.is-bool.php
http://www.php.net/manual/en/function.is-callable.php
http://www.php.net/manual/en/function.is-double.php
http://www.php.net/manual/en/function.is-float.php
http://www.php.net/manual/en/function.is-int.php
http://www.php.net/manual/en/function.is-integer.php
http://www.php.net/manual/en/function.is-long.php
http://www.php.net/manual/en/function.is-null.php
http://www.php.net/manual/en/function.is-numeric.php
http://www.php.net/manual/en/function.is-object.php
http://www.php.net/manual/en/function.is-real.php
http://www.php.net/manual/en/function.is-resource.php
http://www.php.net/manual/en/function.is-scalar.php
http://www.php.net/manual/en/function.is-string.php

TODO: add array, callable, resouce and object support
--FILE--
<?php
//echo is_array()
echo is_bool(1) . "=\n";
echo is_bool(true) . "=\n";
//echo is_callable
echo is_double("str") . "=\n";
echo is_double(1.3) . "=\n";
echo is_float(null) . "=\n";
echo is_float(1.3) . "=\n";
echo is_int("str") . "=\n";
echo is_int(1) . "=\n";
echo is_integer(false) . "=\n";
echo is_integer(31234123) . "=\n";
echo is_long(1.3) . "=\n";
echo is_long(31234123) . "=\n";
echo is_null(1.3) . "=\n";
echo is_null(null) . "=\n";
//echo is_numeric
//echo is_object
echo is_real(null) . "=\n";
echo is_real(1.3) . "=\n";
//echo is_resource
echo is_scalar(false) . "=\n";
echo is_scalar(31234123) . "=\n";
echo is_scalar("1.3") . "=\n";
echo is_scalar(1.3) . "=\n";
echo is_scalar(null) . "=\n";
echo is_string(null) . "=\n";
echo is_string("1.3") . "=\n";

--EXPECT--
=
1=
=
1=
=
1=
=
1=
=
1=
=
1=
=
1=
=
1=
1=
1=
1=
1=
=
=
1=