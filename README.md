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
