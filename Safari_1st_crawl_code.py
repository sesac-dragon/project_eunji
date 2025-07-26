import requests
import re
import json
from bs4 import BeautifulSoup

res = requests.get(f'https://www.safaribookings.com/tours/page/1',
                   headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Whale/4.32.315.22 Safari/537.36',
                            'cookie': 'v=1.0.313; _ga=GA1.1.762332180.1752736610; CookieConsent={stamp:%27smOAvwHrouD3ERr0LAClV08CPzvUWzHxlHpL7bgMN48vygQuEMsBgw==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27explicit%27%2Cver:1%2Cutc:1752736611021%2Cregion:%27kr%27}; _gcl_au=1.1.1437524738.1752736611; _fbp=fb.1.1752736613392.535065786467195256; vsd=%7B%22cc%22%3A%22KR%22%2C%22cn%22%3A%22South%20Korea%22%2C%22ci%22%3A114%2C%22cp%22%3A%22%2B82%22%2C%22c%22%3A%22Asia%22%2C%22cg%22%3A0%2C%22ri%22%3A7%2C%22ip%22%3A%22211.34.202.232%22%2C%22d%22%3A2%2C%22cur%22%3A%22KRW%22%7D; laravel_session=rNYT1LO549F7Tu2fLIYwNovHOxQpTQrXlLfBgk5i; hpp=8%2C7%2C0; list_location=%2Ftours%3Fcur%3Dkrw%7C%7C%2Ftours%3Ffilter%3Dall%26cur%3Dkrw; _ga_D6DBBH8PKF=GS2.1.s1753160001$o11$g1$t1753161456$j59$l0$h0; _uetsid=b56e8e40662611f0b28a21bd6cad6003; _uetvid=02ee75c062de11f098f641fe3c03548d; prf=%7B%22sd%22%3A%22%22%2C%22sf%22%3A1%2C%22ta%22%3A2%2C%22tc%22%3A0%2C%22tca%22%3A%22%22%2C%22td%22%3Afalse%2C%22up%22%3A%2220250722141738%22%7D; XSRF-TOKEN=eyJpdiI6IlNLdlN4SlBNWWRQMVF3Z1JVQXpZc0E9PSIsInZhbHVlIjoiWFNHU1B2a0pUZFdFYzNKNHVNYktsYTVwZVoxb25tc2NqMytKbVAyQzhCUUxaVVhDTW1aY1pLb0V4TWhmaENVdldZY0ZoRkgrWnRNQk1rcEorZ3RYSVVVYmlQYW9CRlhTSDZua0dlM1BqN015anZJblhoTnNJR2tKT1oySkIwSEIiLCJtYWMiOiIzMDNlN2E0OWU0ZWE4MDcwMDA4ZTFmY2M4NzJhYmI4NjM2Nzc4YTg5Y2M5MGJhZmRkNmFmYmViNzVlZDY2M2RjIiwidGFnIjoiIn0%3D'
                   })

soup = BeautifulSoup(res.text, 'html.parser')

total_count = int(soup.select_one('b.itemcount')['data-count'])

quo = total_count // 20
mod = total_count % 20

if mod >= 1:
    total_page = quo + 1
else:
    total_page = quo

total = 0

result= []

# 페이지 반복 -> 사파리 투어 목록 크롤링
for page in range(1, total_page+1):
    res = requests.get(f'https://www.safaribookings.com/tours/page/{page}',
                   headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Whale/4.32.315.22 Safari/537.36',
                            'cookie': 'v=1.0.313; _ga=GA1.1.762332180.1752736610; CookieConsent={stamp:%27smOAvwHrouD3ERr0LAClV08CPzvUWzHxlHpL7bgMN48vygQuEMsBgw==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27explicit%27%2Cver:1%2Cutc:1752736611021%2Cregion:%27kr%27}; _gcl_au=1.1.1437524738.1752736611; _fbp=fb.1.1752736613392.535065786467195256; vsd=%7B%22cc%22%3A%22KR%22%2C%22cn%22%3A%22South%20Korea%22%2C%22ci%22%3A114%2C%22cp%22%3A%22%2B82%22%2C%22c%22%3A%22Asia%22%2C%22cg%22%3A0%2C%22ri%22%3A7%2C%22ip%22%3A%22211.34.202.232%22%2C%22d%22%3A2%2C%22cur%22%3A%22KRW%22%7D; laravel_session=rNYT1LO549F7Tu2fLIYwNovHOxQpTQrXlLfBgk5i; hpp=8%2C7%2C0; list_location=%2Ftours%3Fcur%3Dkrw%7C%7C%2Ftours%3Ffilter%3Dall%26cur%3Dkrw; _ga_D6DBBH8PKF=GS2.1.s1753160001$o11$g1$t1753161456$j59$l0$h0; _uetsid=b56e8e40662611f0b28a21bd6cad6003; _uetvid=02ee75c062de11f098f641fe3c03548d; prf=%7B%22sd%22%3A%22%22%2C%22sf%22%3A1%2C%22ta%22%3A2%2C%22tc%22%3A0%2C%22tca%22%3A%22%22%2C%22td%22%3Afalse%2C%22up%22%3A%2220250722141738%22%7D; XSRF-TOKEN=eyJpdiI6IlNLdlN4SlBNWWRQMVF3Z1JVQXpZc0E9PSIsInZhbHVlIjoiWFNHU1B2a0pUZFdFYzNKNHVNYktsYTVwZVoxb25tc2NqMytKbVAyQzhCUUxaVVhDTW1aY1pLb0V4TWhmaENVdldZY0ZoRkgrWnRNQk1rcEorZ3RYSVVVYmlQYW9CRlhTSDZua0dlM1BqN015anZJblhoTnNJR2tKT1oySkIwSEIiLCJtYWMiOiIzMDNlN2E0OWU0ZWE4MDcwMDA4ZTFmY2M4NzJhYmI4NjM2Nzc4YTg5Y2M5MGJhZmRkNmFmYmViNzVlZDY2M2RjIiwidGFnIjoiIn0%3D'
                   })
    
    soup = BeautifulSoup(res.text, 'html.parser')

    feeds = soup.select('li[class*="col"]')

    total += len(feeds)

    print(f'현재 페이지: {page}')
    print(soup.title.text)
    print(f'{page}페이지 투어 개수: {len(feeds)}')
    print(f'누적 투어 개수: {total}')

    len(result)
    
    # 투어 목록에서 id, 투어명, 나라, 일수, 가격, 상세 투어 url 수집
    for feed in feeds:
        item_tag = feed.select_one('a.list__item')
        p_tag = feed.select_one('p.price b') or feed.select_one('p.price')
        title_tag = feed.select_one('h2.serif.tourtitle')
        desc_tag = feed.select_one('p.desc b') or feed.select_one('p.desc')

        if not item_tag or not p_tag or not title_tag or not desc_tag:
            continue
        
        p_text = p_tag.text
        title_text = title_tag.text.strip()

        search_days = re.search(r'(\d+)\s*-\s*Day', title_text)
        if search_days != None:
            Tour_days = int(search_days.group(1))
        elif '½' in title_text:
            Tour_days = 1
        else:
            Tour_days = None

        temp = {
        'Tour_ID':item_tag.attrs['data-id'],
        'Tour_title': item_tag.attrs['title'],
        'Tour_country': desc_tag.text.strip(':'),
        'Tour_days': Tour_days,
        'Tour_price': int(re.sub(r'[\D]+', '', p_text)),
        'Tour_URL': item_tag.attrs['href']}
        result.append(temp)
    

with open('safari_tour_1st_crawl.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)