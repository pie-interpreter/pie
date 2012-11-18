--FILE--
<?php
print 5; // simple expression
print "=";
print ("hello"); // expression in parenthesis
print "=";
print (5 + true); // complex expression
print "=";
echo print 5; // return value used in expression
?>
--EXPECT--
5=hello=6=51
