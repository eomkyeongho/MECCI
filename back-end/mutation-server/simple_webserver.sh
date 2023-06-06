#!/bin/sh

echo "script start" >> /tmp/result

apt-get install apache2 php -y
git clone https://github.com/banago/simple-php-website.git
php -S 0.0.0.0:8080 -t /simple-php-website &