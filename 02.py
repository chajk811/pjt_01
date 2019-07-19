import csv
import requests
from pprint import pprint
from decouple import config
from datetime import datetime, timedelta

movies = {}
with open('boxoffice.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)

    # 읽어 오면서 movies의 빈 딕셔너리에 영화코드 저장
    for row in reader:
        movies[row['movieCd']] = {}

for movieCd in movies:
    key = config('KEY')
    base_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?'
    url = base_url + f'key={key}&movieCd={movieCd}'

    response = requests.get(url)
    response_dict = response.json()
    movie_info = response_dict['movieInfoResult']['movieInfo']

    # 딕셔너리의 여러개의 요소가 있는 경우를 고려하여
    # 장르의 경우 여러 딕셔너리의 value 값을 빈 리스트에 저장-> 리스트를 합쳐 하나의 스트링값으로 만듦
    # 빈 딕셔너리일 경우 조건문을 통해 None값 부여
    geners_list = []
    for genre in movie_info.get('genres'):
        geners_list.append(genre.get('genreNm'))
    geners_str = '/'.join(geners_list)

    watchGradeNm = movie_info.get('audits')[0].get('watchGradeNm') if movie_info.get('audits') else None
    director =  movie_info.get('directors')[0].get('peopleNm') if movie_info.get('directors') else None
    
    movies[movieCd] = {
            '영화코드': movieCd,
            '영화명(국문)': movie_info.get('movieNm'),
            '영화명(영문)': movie_info.get('movieNmEn'),
            '관람등급': watchGradeNm,
            '개봉연도': movie_info.get('openDt'),
            '상영시간': movie_info.get('showTm'),
            '장르': geners_str,
            '감독명': director,
            }

with open('movie.csv', 'w', newline='', encoding='utf-8') as f:
    fieldnames = ('영화코드', '영화명(국문)', '영화명(영문)', '관람등급', '개봉연도', '상영시간', '장르', '감독명')
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    for i in movies.values():
        writer.writerow(i)