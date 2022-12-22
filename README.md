# pay-here

간단한 가계부 과제
> 본 API를 사용하기에 앞서 환경설정 파일을 생성하여 DB_USER, DB_PASSWORD, SECRET_KEY를 작성해야 합니다

## 사용 기술
- Django
- DjangoRestFramework
- DjangoRestFramework-simplejwt
- python-dotenv
- Mysql 5.7

## DB 구조
![화면 캡처 2022-12-22 232858](https://user-images.githubusercontent.com/77658870/209155905-7c55f4de-0ab5-4bb7-a1b7-b4bc213c0228.png)

## API 정리
1. 회원 기능
    1. 회원가입
> url : members/signup   

      - 사용자는 이메일과 비밀번호를 통해 회원가입을 할 수 있다
      - 비밀번호는 django에서 제공하는 hash 기능을 통해 암호화를 거쳤다
    2. 로그인
> url : members/login   

      - 가입된 정보를 토대로 로그인을 한다
      - 로그인에 성공하면 jwt 토큰을 헤더에 추가하여 발급한다
    3. 로그아웃
> url : members/logout

      - request의 jwt 토큰을 blacklist에 추가하여 만료시켜 로그아웃을 구현하였다
    4. jwt 토큰 재발급
> url : auth/refresh/

      - drf-simplejwt에서 제공하는 TokenRefreshView를 사용
    
2. 가계부 기능
    1. 가계부 작성
> url : account-books

    2. 가계부 복제
> url : account-books/<int:pk>   

      - pk에 해당하는 가계부 내역을 복제한다
      - description에 '-copy'를 추가하여 복사본임을 명시했다
    3. 가계부 수정
> url : account-books/<int:pk>   

    4. 가계부 삭제
> url : account-books/<int:pk>   

    5. 가계부 상세 내용 확인
> url : account-books/<int:pk>   

    6. 가계부 리스트 확인
> url : account-books/list

      - jwt 토큰으로 사용자가 작성한 가계부의 리스트를 출력할 수 있다
      - query parameter로 year, month, day를 추가하여 원하는 년/월/일에 대한 가계부 내역으로 필터링 할 수 있다
3. URL 기능
    1. 단축 URL 생성
> url : short

      - 특정 가계부 상세 내용에 대한 url을 단축 url로 변경한다
      - 가계부의 pk(auto_increment)로 유일성을 보장받으며 base62 변환을 사용하였다
      - 현재 시간 + 6시간으로 만료시간을 설정했다
    2. 단축 URL 접근 (에러 미해결)
> url : short/<str:encoded>

      - 단축 url을 HTTP GET으로 접근한다
      - 해당 url에 대해 expired 속성을 확인하고 만료가 되었을 경우 삭제 후 404_NOT_FOUND를 반환한다
      - 현재 django global setting으로 IS_AUTHENTICATION 을 적용하여 redirect 시 권한 에러가 발생






