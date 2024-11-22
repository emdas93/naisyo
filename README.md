# 2024 Wx Hackerton PADA Team

## Wxhack Web 초기 환경 설정 방법

- 테스트용 유저 및 데이터베이스 만들기

``` sql
create user 'wxhack'@'localhost' identified by 'qweQWE12!';
create user 'wxhack'@'127.0.0.1' identified by 'qweQWE12!';
create user 'wxhack'@'%' identified by 'qweQWE12!';
CREATE DATABASE wxhack CHARACTER SET utf8mb4;
grant all privileges on wxhack.* to 'wxhack'@'localhost';
grant all privileges on wxhack.* to 'wxhack'@'%';
flush privileges;
```
