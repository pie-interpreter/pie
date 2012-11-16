--TEST--
Test to see if all the float values are parsed more or less,
when var_dump will be implemented, we will be able to compare types
--FILE--
<?php
1.2;
1.0;
000000.2000;
1.;
.2;
-1.;
+.2;
1e1;
1e-2;
-1.2e2;
+1.23e2;
.2e-2;
?>