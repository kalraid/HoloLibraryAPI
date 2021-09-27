# HoloLibraryAPI

홀로라이브의 유투브들을 라이브러리화 시켜서 
각종 기능을 붙여 놓으려는 목적을 가진 api 모음

마크다운 문법 설명 :

<a>https://heropy.blog/2017/09/30/markdown/
<a>https://gist.github.com/ihoneymon/652be052a0727ad59601
----------------------
1. 프로젝트 구조 설명

<pre>
HoloLibraryAPI
ㄴapp
 ㄴㄴ common      : 공통 구조 모듈
 ㄴㄴ config      : 설정 관련 모듈
 ㄴㄴ const       : 상수 모듈
 ㄴㄴ db          : DB 설정 관련 모듈
 ㄴㄴ middleware  : falcon 설정 관련 모듈
 ㄴㄴ module      : 외부 연동 모듈
 ㄴㄴ service     : 서비스 모듈
 ㄴㄴ store       : 전역 변수 모듈
 
ㄴexample         : 예제 파일

ㄴresources       : 리소스
ㄴapp.py          : 메인 실행 파일 
ㄴconfig.py       : 운영 환경 구분용 컨피그

ㄴtests           : 커버리지 + TDD 기반으로 테스트하는 파일 목적
</pre>

참고 링크 목록
>https://brunch.co.kr/@joypinkgom/55
> https://github.com/googleapis/google-api-python-client
> https://365kim.tistory.com/93
> https://velog.io/@bigsaigon333/Client-Side%EC%97%90%EC%84%9C-Youtube-API-Key-%EC%88%A8%EA%B8%B0%EA%B8%B0
> https://untitledtblog.tistory.com/169
> https://towardsdatascience.com/the-simplest-way-to-build-a-rest-api-with-falcon-and-python-3-10-application-in-spatial-geometry-c1ee305aed75
> https://developer.mozilla.org/ko/docs/Learn/Server-side/Django/Deployment#%EC%98%88%EC%A0%9C_locallibrary%EB%A5%BC_heroku%EC%97%90_%EC%84%A4%EC%B9%98%ED%95%98%EA%B8%B0
> https://falcon.readthedocs.io/en/stable/api/routing.html
> https://falcon.readthedocs.io/en/stable/api/websocket.html
> https://falcon.readthedocs.io/en/stable/user/quickstart.html#a-more-complex-example
> https://falcon.readthedocs.io/en/stable/user/quickstart.html#learning-by-example
> https://falcon.readthedocs.io/en/stable/api/api.html
> 

Falcon REST API with PostgreSQL
===============================
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/ziwon/falcon-rest-api)<!-- <a href="https://tracking.gitads.io/?repo=falcon-rest-api"> <img src="https://images.gitads.io/falcon-rest-api" alt="GitAds"/></a> -->

Simple REST API using Falcon web framework.

Falcon is a high-performance Python framework for building cloud APIs, smart proxies, and app backends. More information can be found [here](https://github.com/falconry/falcon/).

Requirements
============
This project uses [virtualenv](https://virtualenv.pypa.io/en/stable/) as isolated Python environment for installation and running. Therefore, [virtualenv](https://virtualenv.pypa.io/en/stable/) must be installed. And you may need a related dependency library for a PostgreSQL database. See [install.sh](https://github.com/ziwon/falcon-rest-api/blob/master/install.sh) for details.


Installation
============

Install all the python module dependencies in requirements.txt

```
  ./install.sh
```

Start server

```
  ./bin/run.sh start
```

Deploy
=====
You need to set `APP_ENV` environment variables before deployment. You can set LIVE mode in Linux/Heroku as follows.

Linux
------
In Linux, just set `APP_ENV` to run in live mode.
```shell
export APP_ENV=live
./bin/run.sh start
```

Heroku
------
In Heroku, use the command `config:set`. (See [here](https://devcenter.heroku.com/articles/config-vars) for details)
```shell
heroku config:set APP_ENV=live
```

Usage
=====

Create an user
- Request
```shell
curl -XPOST http://localhost:5000/v1/users -H "Content-Type: application/json" -d '{
 "username": "test1",
 "email": "test1@gmail.com",
 "password": "test1234"
}'
```

- Response
```json
{
  "meta": {
    "code": 200,
    "message": "OK",
  },
  "data": null
}
```

Log in with email and password

- Request
```shell
curl -XGET http://localhost:5000/v1/users/self/login -H "Content-Type: application/json" -d '{
 "email": "test1@gmail.com",
 "password": "test1234"
}'
```

- Response
```json
{
  "meta": {
    "code": 200,
    "message": "OK"
  },
  "data": {
    "username": "test1",
    "token": "gAAAAABV-TpG0Gk6LhU5437VmJwZwgkyDG9Jj-UMtRZ-EtnuDOkb5sc0LPLeHNBL4FLsIkTsi91rdMjDYVKRQ8OWJuHNsb5rKw==",
    "email": "test1@gmail.com",
    "created": 1442396742,
    "sid": "3595073989",
    "modified": 1442396742
  }
}
```

Check the validation of requested data

- Request
```shell
curl -XPOST http://localhost:5000/v1/users -H "Content-Type: application/json" -d '{
 "username": "t",
 "email": "test1@gmail.c",
 "password": "123"
}'
```

- Response
```json
{
  "meta": {
    "code": 88,
    "message": "Invalid Parameter",
    "description": {
      "username": "min length is 4",
      "email": "value does not match regex '[a-zA-Z0-9._-]+@(?:[a-zA-Z0-9-]+\\.)+[a-zA-Z]{2,4}'",
      "password": [
        "value does not match regex '[0-9a-zA-Z]\\w{3,14}'",
        "min length is 8"
      ]
    }
  }
}
```

Get database rollback error in response for duplicated data

- Request
```shell
curl -XPOST http://localhost:5000/v1/users -H "Content-Type: application/json" -d '{
 "username": "test1",
 "email": "test1@gmail.com",
 "password": "test1234"
}'
```

- Response
```json
{
  "meta": {
    "code": 77,
    "message": "Database Rollback Error",
    "description": {
      "details": "(psycopg2.IntegrityError) duplicate key value violates unique constraint \"user_email_key\"\nDETAIL:  Key (email)=(test1@gmail.com) already exists.\n",
      "params": "{'username': 'test1', 'token': 'gAAAAABV-UCq_DneJyz4DTuE6Fuw68JU7BN6fLdxHHIlu42R99sjWFFonrw3eZx7nr7ioIFSa7Akk1nWgGNmY3myJzqqbpOsJw==', 'sid': '6716985526', 'email': 'test1@gmail.com', 'password': '$2a$12$KNlGvL1CP..6VNjqQ0pcjukj/fC88sc1Zpzi0uphIUlG5MjyAp2fS'}"
    }
  }
}
```

Get a collection of users with auth token

- Request
```shell
curl -XGET http://localhost:5000/v1/users/100 -H "Authorization: gAAAAABV6Cxtz2qbcgOOzcjjyoBXBxJbjxwY2cSPdJB4gta07ZQXUU5NQ2BWAFIxSZlnlCl7wAwLe0RtBECUuV96RX9iiU63BP7wI1RQW-G3a1zilI3FHss="
```

- Response
```json
{
  "meta": {
    "code": 200,
    "message": "OK"
  },
  "data": [
    {
      "username": "test1",
      "token": "gAAAAABV-UCAgRy-ee6t4YOLMW84tKr_eOiwgJO0QcAHL7yIxkf1fiMZfELkmJAPWnldptb3iQVzoZ2qJC6YlSioVDEUlLhG7w==",
      "sid": "2593953362",
      "modified": 1442398336,
      "email": "test1@gmail.com",
      "created": 1442398336
    },
    {
      "username": "test2",
      "token": "gAAAAABV-UCObi3qxcpb1XLV4GnCZKqt-5lDXX0YAOcME5bndZjjyzQWFRZKV1x54EzaY2-g5Bt47EE9-45UUooeiBM8QrpSjA==",
      "sid": "6952584295",
      "modified": 1442398350,
      "email": "test2@gmail.com",
      "created": 1442398350
    },
    {
      "username": "test3",
      "token": "gAAAAABV-UCccDCKuG28DbJrObEPUMV5eE-0sEg4jn57usBmIADJvkf3r5gP5F9rX5tSzcBhuBkDJwEJ1mIifEgnp5sxc3Z-pg==",
      "sid": "8972728004",
      "modified": 1442398364,
      "email": "test3@gmail.com",
      "created": 1442398364
    }
  ]
}
```
