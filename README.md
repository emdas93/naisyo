# 2024 Wx Hackerton PADA Team

## Wxhack Web 초기 환경 설정 방법

- 초기 필요 라이브러리 및 모듈 인스톨
``` bash
# Nginx
service nginx restart

# MySQL
service mysql restart

# PHP-FPM
service php8.3-fpm stop
service php8.3-fpm start

cd web
# PHP Laravel 패키지 설치
composer install
php artisan key:generate

# Front단 빌드
npm install

# 빌드 및 HMR서버 실행
npm run dev
```

- MySQL 테스트용 유저 및 데이터베이스 만들기

``` sql
create user 'wxhack'@'localhost' identified by 'qweQWE12!';
create user 'wxhack'@'127.0.0.1' identified by 'qweQWE12!';
create user 'wxhack'@'%' identified by 'qweQWE12!';
CREATE DATABASE wxhack CHARACTER SET utf8mb4;
grant all privileges on wxhack.* to 'wxhack'@'localhost';
grant all privileges on wxhack.* to 'wxhack'@'%';
flush privileges;
```
