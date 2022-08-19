# Project-a
## 프로젝트 설명
사용자 인증 기능을 구현한 백엔드 웹 어플리케이션

### 최종 구현 범위
요구사항 4가지 모두 구현 완료

### 강조 부분
1. 전화번호 인증 방법은 **SMS 인증 메커니즘**을 예상하고 구현함
2. 로그인 식별정보는 **이메일**과 **비밀번호**로 정함
3. Client 인증 메커니즘으로 **JWT**를 사용함
4. **RESTful** 규약에 기반한 웹 어플리케이션을 개발함
5. **Annotation**, **Docstring**을 적극 사용함
6. **레이어드 아키텍쳐**에 집중함
7. **에러 핸들링**에 집중함

## 프로젝트 구현 스펙
### 언어
Python 3.10.4
### 웹 프레임워크
Flask 2.2.2
### Database
MySQL 8.0.29
### 테스트 프레임워크
Pytest 7.1.2
### 개발환경 OS
MacOS 12.2 (arm64)

## 프로젝트 로컬 실행 방법
0. Required
 - MySQL Server 설치
 - Python 3.10 설치
1. Github Import
```
% git clone https://github.com/mal-moo/project-a.git 
% cd project-a
```
2. Install Python Package
```
% pip install requirements.txt
```
3. MySQL Schema Import and Create User
```
% bash database_setting_cmd.sh
```
4. Run Web Application
```
% python run.py
```
6. Test API with cURL
```
% curl localhost:6000/
Hello, Project-a !
```