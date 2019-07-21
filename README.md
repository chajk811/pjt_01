# 1. 프로젝트 요약

영화진흥위원회의 api를 이용하여 요청을 보내고 응답받은 데이터 중에서 필요한 정보들을 가져와 cvs 파일로 작성하는 프로젝트이다.



# 2. 코딩 세부 설명

### <파일명 : 01.py> 



### 세부 요약 

최근 50주간 데이터 중에 박스오피스 TOP 10의 영화 대표코드, 영화명, 해당일 누적관객 수의 데이터를 수집합니다. 중복되는 영화는 없으며, 중복이 된다면 그 중에서 최대 누적관객수를 기록한다. 



### 코드 작성 순서

1. 키 값 발급 후 api key 발급
   - key 값은 노출의 위험이 있으므로 .env 파일에 저장 후  decouple의 config를 통해 호출한다.



2. 데이터를 dict 형식으로 저장

   - api 로 주간 박스오피스의 모든 정보를 불러온다. 그러기 위해서 url의 targetDt의 값을 바꿔주면서 돌려줘야함, for문을 사용해서  50번의 요청을 보낸다.

   
   
   - 요청페이지에서  requests.get(url)를 response 에 할당,  그 데이터를 .json()으로 dict 형식으로 정리 후 ranks 변수에 할당한다.



3. 뽑아온 데이터에서 필요한 정보만 새로운 dict에 저장

   - 그 안에서  대표코드, 영화명, 해당일 누적관객 수의 정보를 얻기 위해  ranks 1->10위 순차적으로 돌면서 movieCd를 key로하고 원하는 정보를 value로 갖는 딕셔너리를 추가해준다.

   

   - 단, 중복을 방지하기 위해 조건을 부여하고, 날짜가 점진적으로 작아지면서 제일 많은 누적관객수가 먼저 저장되므로 한 개의 영화당 최대 누적 관객수를 저장할 수 있다.



4. cvs 파일 생성





## <파일명 : 02.py> 



### 세부 요약 

위에서 수집한 영화 대표코드를 활용하여 상세 정보를 수집한다. 상세 정보로는 영화 대표코드, 영화명(국문), 영화명(영문), 관람등급, 개봉연도, 상영시간, 장르, 감독명 을 포함한다.



### 코드 작성 순서

1. 키 값 발급 후 api key 발급
   - key 값은 노출의 위험이 있으므로 .env 파일에 저장 후  decouple의 config를 통해 호출한다.



2. 영화 대표코드를 뽑아 오고 빈 딕셔너리(movies)에 key 값으로 저장
   - 추후 movie.csv 생성에 사용될 빈 딕셔너리를 생성한다.
   - 한 줄씩 영화 코드를 읽어오면서 빈 딕셔너리에 `{'영화 코드' : {}} `형태로 저장한다.  



3.  movies 를 돌면서 url 생성 후 요청

   -  ```python
     for movieCd in movies:
         key = config('KEY')
         base_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?'
         url = base_url + f'key={key}&movieCd={movieCd}'
     
         response = requests.get(url)
         response_dict = response.json()
         movie_info = response_dict['movieInfoResult']['movieInfo']
     ```

     요청한 url에서 위와 같은 코드로 원하는 정보에 도달하고, `movie_info`에 저장한다.

     

   - ```python
     geners_list = []
     for genre in movie_info.get('genres'):
         geners_list.append(genre.get('genreNm'))
     geners_str = '/'.join(geners_list)
     ```

     원하는 정보 중 장르는 여러 개인 경우가 있다. 이를 처리 해주기 위해 여러 딕셔너리로 나눠진 장르 정보를 list에 담고 `'/'.join()`을 사용해 하나의 스트링 값으로 변환해준다.

     

   - ```python
     watchGradeNm = movie_info.get('audits')[0].get('watchGradeNm') if movie_info.get('audits') else None
     director =  movie_info.get('directors')[0].get('peopleNm') if movie_info.get('directors') else None
     ```

     원하는 정보 중 관람등급과 영화감독은 값이 없거나 있으면 value가 리스트를 담고 있어 별도의 처리가 필요하다. 조건 표현식을 사용한다.

     

   - 원하는 정보를 담은 딕셔너리를 최종으로 사용될 movies에 저장한다.



4. cvs 파일 생성





## <파일명 : 03.py> 



### 세부 요약 

위에서 수집한 감독명을 활용하여 상세 정보를 수집한다. 상세 정보로는 감독 코드, 감독명, 감독명(영문), 필모리스트 을 포함한다.



### 코드 작성 순서

1. 키 값 발급 후 api key 발급
   - key 값은 노출의 위험이 있으므로 .env 파일에 저장 후  decouple의 config를 통해 호출한다.



2. 감독명을 뽑아 오고 빈 딕셔너리(directors)에 key 값으로 저장
   - 추후 director.csv 생성에 사용될 빈 딕셔너리를 생성한다.
   - 한 줄씩 영화 코드를 읽어오면서 빈 딕셔너리에 `{'감독명' : {}} `형태로 저장한다.  



3.  directors 를 돌면서 url 생성 후 요청

   - ```python
     for director in directors:
         key = config('KEY')
         base_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json?'
         url = base_url + f'key={key}&peopleNm={director}&itemPerPage=100'
     
         response = requests.get(url)
         response_dict = response.json()
         director_info = response_dict['peopleListResult']['peopleList']
     ```

     요청한 url에서 위와 같은 코드로 원하는 정보에 도달하고, `director_info`에 저장한다.

     

   - ```python
         for i in director_info:
             if i.get('repRoleNm') == '감독':
                 directors[director] = {
                 '감독코드': i.get('peopleCd'),
                 '감독명': director,
                 '감독명(영문)': i.get('peopleNmEn'),
                 '필모리스트': i.get('filmoNames')
                 }
     ```

     url로 요청 한 정보에서 totCnt에 동명이인 혹은 동일인물의 다른 분야의 수를 담고 있다. director_info에 그만큼의 이름에 맞는 딕셔너리가 저장된다. 따라서 director_info 딕셔너리 안의 요소를 돌면서 분야의 key 값이  '감독' 에 해당할 경우만 추가시켜준다.

     

4. cvs 파일 생성
