import csv
import requests
from pprint import pprint
from decouple import config
from datetime import datetime, timedelta

# 제일 마지막에 csv 파일 생성에 사용될 빈 딕셔너리 생성 
directors = {}

# movie.csv에서 '감독명'을 읽어와 키값으로 direcors에 추가
with open('movie.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)

    for row in reader:
        directors[row['감독명']] = {}

# 감독명을 바꿔가면서 url 생성 후 요청
for director in directors:
    key = config('KEY')
    base_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json?'
    url = base_url + f'key={key}&peopleNm={director}&itemPerPage=100'

    response = requests.get(url)
    response_dict = response.json()
    director_info = response_dict['peopleListResult']['peopleList']
    
    # url로 요청 한 정보에서 totCnt에 동명이인 혹은 동일인물의 다른 분야의 수를 담고 있음.
    # director_info에 그만큼의 이름에 맞는 딕셔너리가 나옴.
    # 따라서 딕셔너리 안의 요소를 돌면서 '감독'에 해당할 경우만 추가시켜준다.
    for i in director_info:
        if i.get('repRoleNm') == '감독':
            directors[director] = {
            '감독코드': i.get('peopleCd'),
            '감독명': director,
            '감독명(영문)': i.get('peopleNmEn'),
            '필모리스트': i.get('filmoNames')
            }

# 생성된 directors로 csv파일 생성
with open('director.csv', 'w', newline='', encoding='utf-8') as f:
    fieldnames = ('감독코드', '감독명', '감독명(영문)', '필모리스트')
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    for i in directors.values():
        writer.writerow(i)