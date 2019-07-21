import csv
import requests
from pprint import pprint
from decouple import config
from datetime import datetime, timedelta

# 제일 마지막에 csv 파일 생성에 사용될 빈 딕셔너리 생성
result = {} 

# url의 targetDt를 변경하며 50회 반복하며 url요청
for i in range(50):
    key = config('KEY')
    targetDt = datetime(2019, 7, 13) - timedelta(weeks=i)
    targetDt = targetDt.strftime("%Y%m%d")
    base_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json?'
    url = base_url + f'key={key}&targetDt={targetDt}'
    
    # 한 주간 1-10위까지의 데이터를 dict형식으로 ranks에 할당
    response = requests.get(url)
    response_dict = response.json()
    ranks = response_dict['boxOfficeResult']['weeklyBoxOfficeList']

    # 한 주에 1위부터 10까지 돌면서 하나의 순위에서 원하는 정보를 찾기 위한 과정
    for i in range(len(ranks)):
        movieNm = ranks[i]['movieNm']
        movieCd = ranks[i]['movieCd']
        audiAcc = ranks[i]['audiAcc']
        # 해당 정보를 뽑고 빈 딕셔너리에 저장, 단 없던 요소를 넣어주기 위한 과정
        if movieCd not in result:
            result[movieCd] = {
                'movieCd': movieCd,
                'movieNm': movieNm,
                'audiAcc': audiAcc
                }
    
# csv생성
with open('boxoffice.csv', 'w', newline='', encoding='utf-8') as f:
    fieldnames = ('movieNm', 'movieCd', 'audiAcc')
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    for i in result.values():
        writer.writerow(i)