import csv
import requests
from pprint import pprint
from decouple import config
from datetime import datetime, timedelta

directors = {}

with open('movie.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)

    for row in reader:
        directors[row['감독명']] = {}
    pprint(directors)

# 영화인 코드 peopleCd, 영화인명 peopleNm, 분야 repRoleNm, 필모리스트 filmoNames


# for director in directors:
key = config('KEY')
movieCd = 20192689
base_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json?key='
url = base_url + f'key={key}&movieCd={movieCd}'