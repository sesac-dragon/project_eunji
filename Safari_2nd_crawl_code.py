import requests
import re
import time
import json
from bs4 import BeautifulSoup
import os
import multiprocessing.pool as pool

big5 = ['Lion', 'Leopard', 'Elephant', 'Buffalo', 'White Rhino', 'Black Rhino']
valid = ['Abundant', 'Common', 'Occasional', 'Rare']

def tour_url(tour):
    url = tour['Tour_URL']
    time.sleep(0.5)

    res = requests.get(url,
                headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Whale/4.32.315.22 Safari/537.36',
                        'cookie': 'v=1.0.313; _ga=GA1.1.762332180.1752736610; CookieConsent={stamp:%27smOAvwHrouD3ERr0LAClV08CPzvUWzHxlHpL7bgMN48vygQuEMsBgw==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27explicit%27%2Cver:1%2Cutc:1752736611021%2Cregion:%27kr%27}; _gcl_au=1.1.1437524738.1752736611; _fbp=fb.1.1752736613392.535065786467195256; vsd=%7B%22cc%22%3A%22KR%22%2C%22cn%22%3A%22South%20Korea%22%2C%22ci%22%3A114%2C%22cp%22%3A%22%2B82%22%2C%22c%22%3A%22Asia%22%2C%22cg%22%3A0%2C%22ri%22%3A7%2C%22ip%22%3A%22211.34.202.232%22%2C%22d%22%3A2%2C%22cur%22%3A%22KRW%22%7D; laravel_session=rNYT1LO549F7Tu2fLIYwNovHOxQpTQrXlLfBgk5i; hpp=8%2C7%2C0; list_location=%2Ftours%3Fcur%3Dkrw%7C%7C%2Ftours%3Ffilter%3Dall%26cur%3Dkrw; _ga_D6DBBH8PKF=GS2.1.s1753160001$o11$g1$t1753161456$j59$l0$h0; _uetsid=b56e8e40662611f0b28a21bd6cad6003; _uetvid=02ee75c062de11f098f641fe3c03548d; prf=%7B%22sd%22%3A%22%22%2C%22sf%22%3A1%2C%22ta%22%3A2%2C%22tc%22%3A0%2C%22tca%22%3A%22%22%2C%22td%22%3Afalse%2C%22up%22%3A%2220250722141738%22%7D; XSRF-TOKEN=eyJpdiI6IlNLdlN4SlBNWWRQMVF3Z1JVQXpZc0E9PSIsInZhbHVlIjoiWFNHU1B2a0pUZFdFYzNKNHVNYktsYTVwZVoxb25tc2NqMytKbVAyQzhCUUxaVVhDTW1aY1pLb0V4TWhmaENVdldZY0ZoRkgrWnRNQk1rcEorZ3RYSVVVYmlQYW9CRlhTSDZua0dlM1BqN015anZJblhoTnNJR2tKT1oySkIwSEIiLCJtYWMiOiIzMDNlN2E0OWU0ZWE4MDcwMDA4ZTFmY2M4NzJhYmI4NjM2Nzc4YTg5Y2M5MGJhZmRkNmFmYmViNzVlZDY2M2RjIiwidGFnIjoiIn0%3D'
                })
    if res.status_code != 200:
        raise Exception(f"Tour_ID: {tour['Tour_ID']}, Request 상태: {res.status_code}")
    return BeautifulSoup(res.text, 'html.parser') 

def tour_days(soup):
    days_tag = soup.select('tr.last td strong')

    if len(days_tag) > 0:
        day_text = days_tag[0].text
        days = re.findall(r'\d+', day_text)
        if len(days) > 0:
            return int(days[0])
        else:
            return None
    else:
        return None

def tour_location_details(soup):
    location_details = []

    tr_tag = soup.select('div.tour__route-list-inner tr')

    for tr in tr_tag:
        td = tr.select('td')

        if len(td) < 2: # td 1개 -> 나라명
            continue

        day_info = td[0].text.strip()
        location_text = td[1].text.strip()

        if 'Day' in day_info:
            num = re.findall(r'\d+', day_info)
            if len(num) == 2: # ex) Day 2-3 -> ['2', '3'] -> 3-2+1=2일
                days = int(num[1])-int(num[0])+1
            elif len(num) == 1: # ex) Day 1 -> ['1']
                days = 1
            else:
                continue
        elif day_info in ['Start', 'End']: # 반일 투어 -> Start (Day 1), End (Day 1)만 있음
            strong_tag = td[1].select_one('strong')

            if strong_tag != None:
                day_text = strong_tag.text
                num = re.findall(r'\d+', day_text)
                if len(num) == 2:
                    days = int(num[1])-int(num[0]) +1
                elif len(num) == 1:
                    days = 1
                else:
                    days = 1
            else:
                days = 1
        else:
            continue

        a_tag = td[1].select_one('a')

        if a_tag != None:
            name = re.sub(r'\s*\(Day.*?\)', '', a_tag.text).strip()
            link = a_tag['href']
        else:
            name = re.sub(r'\s*\(Day.*?\)', '', location_text).strip()
            link = ''

        location_details.append({'location_name': name, 'days': days, 'link': link})
    return location_details

def tour_start_end(soup):
    td_tag = soup.select('div.tour__route-list-inner tr td')

    if len(td_tag) >= 3:
        start = re.sub(r'\s*\(Day.*?\)', '', td_tag[2].text).strip()
        end = re.sub(r'\s*\(Day.*?\)', '', td_tag[-1].text).strip()
    else:
        start = ''
        end = ''
    return start, end

def tour_location_merge(location_details):
    location_merge = []
    for loca in location_details:
        if len(location_merge) > 0 and location_merge[-1]['location_name'] == loca['location_name']:
            location_merge[-1]['days'] += loca['days']
        else:
            location_merge.append(loca)
    location_details = location_merge
    return location_merge

def tour_style_type(soup):
    style_list = ['Luxury+ tour', 'Luxury tour', 'Mid-range tour', 'Budget tour',
                'Budget camping', 'Day tour', '1/2 Day tour', 'Participation camping', 'Mid-range camping']

    type_list = ['Private tour', 'Shared tour', 'Self-drive tour', 'Guided self-drive']

    style = soup.select('h4')[0].text.strip()

    if style in style_list:
        Tour_style = style
    else:
        Tour_style = ''

    type = soup.select('h4')[1].text.strip()

    if type in type_list:
        Tour_type = type
    else:
        Tour_type = ''
    return Tour_style, Tour_type
    
def tour_operator(soup):
    operator_tag = soup.select_one('div.operator__info dl dd strong')

    if operator_tag != None:
        return operator_tag.text.strip()
    else:
        return ''

def tour_activities(soup):
    activities = []
    acti_tag = soup.select('div.tour__content__block.tour__content__block--activities.avoid-break-p > ul > li:nth-child(1) > span')

    for act in acti_tag:
        acti = act.text.replace('Activities: ', '').strip()

        if '&' in acti:
            acti = acti.replace(' &', ',')

        for a in acti.split(','):
            a = a.strip()

            if len(a) > 0:
                activities.append(a)
    return activities

def tour_animals(tour):
    for location in tour['Tour_location_details']:
        loca_url = location['link']

        if loca_url == '':
            location['animals'] = []
            continue

        wildlife_url = loca_url + '/wildlife'

        time.sleep(0.6)

        res = requests.get(wildlife_url,
                headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Whale/4.32.315.22 Safari/537.36',
                        'cookie': 'v=1.0.313; _ga=GA1.1.762332180.1752736610; CookieConsent={stamp:%27smOAvwHrouD3ERr0LAClV08CPzvUWzHxlHpL7bgMN48vygQuEMsBgw==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27explicit%27%2Cver:1%2Cutc:1752736611021%2Cregion:%27kr%27}; _gcl_au=1.1.1437524738.1752736611; _fbp=fb.1.1752736613392.535065786467195256; vsd=%7B%22cc%22%3A%22KR%22%2C%22cn%22%3A%22South%20Korea%22%2C%22ci%22%3A114%2C%22cp%22%3A%22%2B82%22%2C%22c%22%3A%22Asia%22%2C%22cg%22%3A0%2C%22ri%22%3A7%2C%22ip%22%3A%22211.34.202.232%22%2C%22d%22%3A2%2C%22cur%22%3A%22KRW%22%7D; laravel_session=rNYT1LO549F7Tu2fLIYwNovHOxQpTQrXlLfBgk5i; hpp=8%2C7%2C0; list_location=%2Ftours%3Fcur%3Dkrw%7C%7C%2Ftours%3Ffilter%3Dall%26cur%3Dkrw; _ga_D6DBBH8PKF=GS2.1.s1753160001$o11$g1$t1753161456$j59$l0$h0; _uetsid=b56e8e40662611f0b28a21bd6cad6003; _uetvid=02ee75c062de11f098f641fe3c03548d; prf=%7B%22sd%22%3A%22%22%2C%22sf%22%3A1%2C%22ta%22%3A2%2C%22tc%22%3A0%2C%22tca%22%3A%22%22%2C%22td%22%3Afalse%2C%22up%22%3A%2220250722141738%22%7D; XSRF-TOKEN=eyJpdiI6IlNLdlN4SlBNWWRQMVF3Z1JVQXpZc0E9PSIsInZhbHVlIjoiWFNHU1B2a0pUZFdFYzNKNHVNYktsYTVwZVoxb25tc2NqMytKbVAyQzhCUUxaVVhDTW1aY1pLb0V4TWhmaENVdldZY0ZoRkgrWnRNQk1rcEorZ3RYSVVVYmlQYW9CRlhTSDZua0dlM1BqN015anZJblhoTnNJR2tKT1oySkIwSEIiLCJtYWMiOiIzMDNlN2E0OWU0ZWE4MDcwMDA4ZTFmY2M4NzJhYmI4NjM2Nzc4YTg5Y2M5MGJhZmRkNmFmYmViNzVlZDY2M2RjIiwidGFnIjoiIn0%3D'
                })
        
        soup = BeautifulSoup(res.text, 'html.parser')
        
        figure_tags = soup.find_all('figure')

        animal_list = []

        for figure in figure_tags:
            temp_lines = figure.text.strip().split('\n')
            lines = []

            for l in temp_lines:
                line = l.strip()
                if line != '':
                    lines.append(line)

            if len(lines) >= 2:  # lines[0], lines[1] 있나 체크
                if lines[0] in big5 and lines[1] in valid:
                    animal_list.append(lines[0])
        location['animals'] = list(set(animal_list))

def file_save(tour):
    file_name = f"safari_crawler_2차_수정/{tour['Tour_ID']}.json"
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(tour, f, ensure_ascii=False, indent=2)
    print(f"Tour_ID: {tour['Tour_ID']} 파일 저장 완료")

def Safari_Bookings(tour):
    try:
        soup = tour_url(tour)

        tour['Tour_days'] = tour_days(soup)

        location_details = tour_location_details(soup)
        start, end = tour_start_end(soup)
        location_details = tour_location_merge(location_details)

        if len(location_details) >= 3:
            idx0 = location_details[0]['location_name'].strip()
            idx1 = location_details[-1]['location_name'].strip()
            if idx0 == start.strip() and idx1 == end.strip():
                location_details = location_details[1:-1]
        
        if len(location_details) == 1 and start.strip() == end.strip()\
            and location_details[0]['location_name'] == start.strip()\
            and location_details[0]['location_name'] == end.strip()\
            and tour['Tour_days'] == 1:
            location_details[0]['days'] = 1
        
        tour['Tour_location_details'] = location_details
        tour['Tour_start'] = start
        tour['Tour_End'] = end

        style, type = tour_style_type(soup)
        tour['Tour_style'] = style
        tour['Tour_type'] = type

        tour['Tour_operator'] = tour_operator(soup)

        tour['Tour_activity'] = tour_activities(soup)

        tour_animals(tour)

        file_save(tour)

        file_count = len(os.listdir('safari_crawler_2차_수정'))
        print(f'현재까지 {file_count}개 완료')
        
        return tour
    
    except Exception as e:
        print(f"오류, Tour_ID: {tour.get('Tour_ID')}, 이유: {e}")
        return {'fail': tour.get('Tour_ID')}

if __name__ == '__main__':
    with open('safari_tour_1st_crawl.json', 'r', encoding='utf-8') as f:
        result = json.load(f)

    # area = result[0:100]

    data_check = []
    file_list = set(os.listdir('safari_crawler_2차_수정'))
    for tour in result:
        file_name = f"{tour['Tour_ID']}.json"
        if file_name not in file_list:
            data_check.append(tour)

    print(f'총 {len(data_check)}개 저장 시작')

    fail = []
    with pool.Pool(4) as p:
        data_result = p.map(Safari_Bookings, data_check)

    for d in data_result:
        if isinstance(d, dict) and 'fail' in d:
            fail.append(d['fail'])

    print('2차 크롤링 완료')
    print(f'실패 Tour_ID: {fail}, 개수: {len(fail)}개')