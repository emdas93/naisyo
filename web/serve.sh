#!/bin/sh

echo "Nginx 실행"
service nginx stop
service nginx start

echo "php8.3-fpm 실행"
service php8.3-fpm stop
service php8.3-fpm start

echo "MySQL 실행"
service mysql stop
service mysql start
