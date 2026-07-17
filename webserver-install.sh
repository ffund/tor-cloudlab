sudo apt-get update
sudo apt-get -y install apache2 libapache2-mod-php

sudo rm -f /var/www/html/index.html
sudo tee /var/www/html/index.php >/dev/null <<'PHP'
<?php
echo "Remote address: " . ($_SERVER['REMOTE_ADDR'] ?? '') . "\n";
echo "Forwarded for:  " . ($_SERVER['HTTP_X_FORWARDED_FOR'] ?? '') . "\n";
?>
PHP

sudo /etc/init.d/apache2 restart
