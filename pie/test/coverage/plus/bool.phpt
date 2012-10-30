--FILE--
<?php
echo false + true;
echo "Done.";
echo true + true;
echo "Done.";
echo false + false;
echo "Done.";
?>
--EXPECT--
1Done.2Done.0Done.