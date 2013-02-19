--DOC--
Test for boolval() function.
http://www.php.net/manual/en/function.boolval.php

TODO: add array and object support
--FILE--
<?php
echo '0:        '.(boolval(0) ? 'true' : 'false')."\n";
echo '42:       '.(boolval(42) ? 'true' : 'false')."\n";
echo '0.0:      '.(boolval(0.0) ? 'true' : 'false')."\n";
echo '4.2:      '.(boolval(4.2) ? 'true' : 'false')."\n";
echo '"":       '.(boolval("") ? 'true' : 'false')."\n";
echo '"string": '.(boolval("string") ? 'true' : 'false')."\n";
//echo '[1, 2]:   '.(boolval([1, 2]) ? 'true' : 'false')."\n";
//echo '[]:       '.(boolval([]) ? 'true' : 'false')."\n";
//echo 'stdClass: '.(boolval(new stdClass) ? 'true' : 'false')."\n";
?>
--EXPECT--
0:        false
42:       true
0.0:      false
4.2:      true
"":       false
"string": true