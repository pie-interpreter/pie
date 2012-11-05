--FILE--
<?php ?>
<?php ;; ?>
<?php // hello ?>
<?php echo "hello"; ?>
<?php echo "hello" ?>
<?php echo "hello";;; ?>
<?php ;;"hello";;; ?>
<?php
if (true)
    echo 1;
else
    ?>123<?php
?>
--EXPECT--
hellohellohello1123
