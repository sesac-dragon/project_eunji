import pymysql
import streamlit as st
import pandas as pd
from datetime import timedelta

# ttl -> 정해진 시간 동안 캐시 저장

# @st.cache_resource(ttl=timedelta(hours=12))
def db_conn():
    envs = dict([l.strip().split('=') for l in open('.env', 'r').readlines()])
    db_config = {}
    for k, v in envs.items():
        if 'DB' not in k:
            continue
        k = k.split('_')[1].lower()
        if k == 'port':
            v = int(v)
        db_config[k]=v
    return pymysql.connect(**db_config)

@st.cache_data(ttl=timedelta(hours=12))
def total_tour(_conn):
    query = 'select count(*) as count from tours'
    df = pd.read_sql(query, _conn)
    return df['count'][0]

@st.cache_data(ttl=timedelta(hours=12))
def big_five_options(_conn):
    query = """
    select distinct big_five_animal
    from location_big_five
    where big_five_animal is not null
    order by big_five_animal
    """
    df = pd.read_sql(query, _conn)
    return list(df['big_five_animal'])

# 선택된 동물을 포함하는 투어 목록
@st.cache_data(ttl=timedelta(hours=12))
def tours_by_animals(_conn, selected_animals):
    if not selected_animals:
        return pd.DataFrame()

    # 동물 이름에 '' 붙임
    name_change_animals = []
    for a in selected_animals:
        name = "'" + a + "'"
        name_change_animals.append(name)

    # ,로 연결
    sql_format_animals = ",".join(name_change_animals)

    query = f"""
    select t.tour_id, t.title, t.country, t.price, t.tour_days,
    l.latitude, l.longitude, l.location_name, lbf.big_five_animal
    from tours as t
    join locations as l
    on t.tour_id = l.tour_id
    join location_big_five as lbf
    on l.location_id = lbf.location_id
    where t.price is not null
    and t.tour_days is not null
    and l.latitude is not null
    and l.longitude is not null
    and lbf.big_five_animal in ({sql_format_animals})
    """

    df = pd.read_sql(query, _conn)
    
    # 투어 아이디 같은 애들끼리 묶고, 거기 속한 동물명 갯수 뽑음(중복 없이), 인덱스 다시 리셋함.
    # 각 투어 몇개 동물 포함되는지 확인 가능
    counts = (df.groupby('tour_id')['big_five_animal'].nunique()
    .reset_index(name='match_count')
    )
    # 모든 동물 포함된 투어만 매치
    matched_tour_id = counts[counts['match_count'] == len(selected_animals)]['tour_id']
    filtered = df[df['tour_id'].isin(matched_tour_id)]

    def join_animals(animal_list):
        return ', '.join(sorted(animal_list))
    
    # 같은 투어끼리 묶기, 그 중 동물만(유니크)
    tour_group_animal = (
        filtered.groupby(['tour_id', 'title', 'country', 'price', 'tour_days', 'latitude', 'longitude', 'location_name'])['big_five_animal'].unique().apply(join_animals).reset_index(name='available_animals'))
    
    return tour_group_animal.drop_duplicates(subset='tour_id')

# @st.cache_data(ttl=timedelta(hours=12))
# def get_country_stats(conn):
#     query = """
#     select t.country,
#         count(distinct t.tour_id) as tour_count,
#         min(t.price) as min_price,
#         max(t.price) as max_price,
#         avg(t.price) as avg_price
#     from tours t
#     join locations l on t.tour_id = l.tour_id
#     where t.price is not null
#     and l.latitude is not null
#     and l.longitude is not null
#     group by t.country
#     order by tour_count desc
#     """
#     df = pd.read_sql(query, conn)
#     return df

