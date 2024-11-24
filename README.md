# 2024 Wx Hackerton PADA Team

## Docker 개발환경 구축 - 윈도우에 Linux 설치 (Home 버전 사용자)
``` bash
# 윈도우 하위시스템으로 Linux (Ubuntu) 설치
# 20241124 기준 Ubuntu 24.04.1 LTS 설치
wsl --install

# 설치 완료 후 재부팅 후 아래 명령어 실행
# 초기 아이디 및 패스워드 설정 필요 (자동으로 실행)
wsl

```

## 윈도우 - Linux 포트포워딩 설정 스크립트

``` powershell
$remoteport = bash.exe -c "ifconfig eth0 | grep 'inet '"
$found = $remoteport -match '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}';

if( $found ){
$remoteport = $matches[0];
} else{
echo "The Script Exited, the ip address of WSL 2 cannot be found";
exit;
}

#[Ports]
#All the ports you want to forward separated by coma
$ports=@(22,80,3306,10000,3000,5001,8080,443);

#[Static ip]
#You can change the addr to your ip config to listen to a specific address
$addr='0.0.0.0';
$ports_a = $ports -join ",";

#Remove Firewall Exception Rules
iex "Remove-NetFireWallRule -DisplayName 'WSL 2 Firewall Unlock' ";

#adding Exception Rules for inbound and outbound Rules
iex "New-NetFireWallRule -DisplayName 'WSL 2 Firewall Unlock' -Direction Outbound -LocalPort $ports_a -Action Allow -Protocol TCP";
iex "New-NetFireWallRule -DisplayName 'WSL 2 Firewall Unlock' -Direction Inbound -LocalPort $ports_a -Action Allow -Protocol TCP";

for( $i = 0; $i -lt $ports.length; $i++ ){
$port = $ports[$i];
iex "netsh interface portproxy delete v4tov4 listenport=$port listenaddress=$addr";
iex "netsh interface portproxy add v4tov4 listenport=$port listenaddress=$addr connectport=$port connectaddress=$remoteport";
}
```

## Docker 개발환경 구축 - 윈도우 하위 시스템에 설치된 Linux 에 Docker 설치 (WSL 명령어로 하위시스템 접근 후)

``` bash
# 패키지 업데이트
sudo apt update

# 필요 패키지 설치 (종속성)
sudo apt install apt-transport-https ca-certificates curl software-properties-common

# Docker 공식 GPG 키 추가
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# Docker APT 저장소 추가
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# 패키지 목록 업데이트
sudo apt update

# Docker 설치
sudo apt install docker-ce docker-ce-cli containerd.io

# Docker 설치 확인
sudo docker --version

# Docker 사용 권한을 현재 유저에게 부여
sudo usermod -aG docker $USER
exit

# exit 명령어로 로그아웃 후, 아래 명령어 실행
newgrp docker

# wxhack 이미지 PULL
docker pull emdas93/wxhack:0.0

# wxhack 컨테이너 실행
docker run --privileged -d -it --name wxhack -p 80:80 -p 443:443 -p 3306:3306 -p 3000:3000 -p 5001:5001 -p 27017:27017 -p 27018:27018 -p 27019:27019 -p 28017:28017 -v $(pwd):/workspace emdas93/wxhack:0.1 bash

# wxhack 터미널 확인
docker exec -it wxhack bash

# whoami로 현재 로그인 된 유저 계정 확인새로운 터미널로 로그인 되면 완료
whoami
root

```

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

# 경로 : 프로젝트 클론 후 web/ 이동하여 실행
cd web/

# PHP Laravel 패키지 설치
composer install
php artisan key:generate

# Front단 빌드
npm install

# Database 접속 (비밀번호 그냥 엔터)
mysql -uroot -p

# 유저 생성 SQL
###########################################################
create user 'wxhack'@'localhost' identified by 'qweQWE12!';
create user 'wxhack'@'127.0.0.1' identified by 'qweQWE12!';
create user 'wxhack'@'%' identified by 'qweQWE12!';
CREATE DATABASE wxhack CHARACTER SET utf8mb4;
grant all privileges on wxhack.* to 'wxhack'@'localhost';
grant all privileges on wxhack.* to 'wxhack'@'%';
flush privileges;
###########################################################

# Database Migrate
php artisan migrate

# 빌드 및 HMR서버 실행
npm run dev
```

## Wxhack Python Flask 초기 환경 설정 방법
``` bash

# 프로젝트 클론 후 api/ 이동하여 실행
cd api/

# 가상 환경 생성
python3 -m venv venv

# 가상 환경 실행 (실행시키면 명령줄 가장 왼쪽에 venv가 표시됨.)
source venv/bin/activate

# 가상 환경 종료 할 때 명령어 (참고)
deactivate

# 필요한 패키지 설치
pip install -r requirements.txt

# 필요한 패키지 백업
pip freeze > requirements.txt

# Flask 서버 실행
python main.py

```

## MySQL 테스트용 유저 및 데이터베이스 만들기

``` sql
create user 'wxhack'@'localhost' identified by 'qweQWE12!';
create user 'wxhack'@'127.0.0.1' identified by 'qweQWE12!';
create user 'wxhack'@'%' identified by 'qweQWE12!';
CREATE DATABASE wxhack CHARACTER SET utf8mb4;
grant all privileges on wxhack.* to 'wxhack'@'localhost';
grant all privileges on wxhack.* to 'wxhack'@'%';
flush privileges;
```

## wxhack 개발을 위한 dockerfile

``` dockerfile
# Base Image
# For MAC
FROM --platform=linux/x86_64 ubuntu:24.04

# For Window
# FROM ubuntu:24.04

LABEL maintainer="emdas93 <emdas93@gmail.com>"

# TimeZone 환경 변수 지정
ENV TZ Asia/Seoul

# TimeZone 설정    
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/lㄴㄴocaltime && echo $TZ > /etc/timezone

# /home/dev 폴더 생성
RUN mkdir /workspace

# Home Directory
WORKDIR /workspace

# APT UPDATE
RUN apt update

# SET LOCALE KOREAN
RUN apt install locales -y
RUN locale-gen ko_KR.UTF-8
ENV LC_ALL ko_KR.UTF-8

# Package
RUN apt install vim git tar gzip build-essential curl -y
RUN apt install fcgiwrap -y
RUN apt install zsh -y
RUN apt install net-tools -y
RUN apt install openssh-server -y
RUN apt install samba -y

# Nginx Setup
RUN apt install nginx -y
RUN apt install apache2-utils -y

# PHP Setup
RUN apt install php openssl php-common php php-cli php-json php-pdo php-mysql php-zip php-gd php-mbstring php-curl php-xml php-pear php-bcmath -y
RUN apt install php-fpm -y
RUN apt install composer -y

# MySQL Setup
RUN apt install mysql-server -y

# NodeJS Setup
RUN curl -sL https://deb.nodesource.com/setup_22.x -o nodesource_22_setup.sh && bash nodesource_22_setup.sh
RUN apt install nodejs -y
# RUN apt install npm -y

# HTTP Port
EXPOSE 80

# HTTPS Port
EXPOSE 443

# MySQL Port
EXPOSE 3306

# ETC Port
EXPOSE 8080
EXPOSE 8081
EXPOSE 8082
EXPOSE 8083

CMD [ "bash" ]
```