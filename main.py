import streamlit as st
import folium
import pymysql
import json
import pandas as pd
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
from streamlit_option_menu import option_menu
from _query import db_conn, total_tour, big_five_options, tours_by_animals

# 레이아웃 넓게 보기
st.set_page_config('Safari Bookings', '🦁', layout='wide')

# streamlit 갤러리에서 가져온 icon 크게 띄우기
def icon(emoji: str):
    """Shows an emoji as a Notion-style page icon."""
    st.write(
        f'<span style="font-size: 90px; line-height: 1">{emoji}</span>',
        unsafe_allow_html=True,
    )
icon("🧭")

# 제목 크게 띄우기
st.markdown("<div style='font-size: 50px; font-weight: bold;'>Safari Bookings</div>", unsafe_allow_html=True)

# 함수 import -> db 연결
conn = db_conn()

# big 5 설명
st.markdown("<h4><b>Big Five 동물이란?</b></h4>", unsafe_allow_html=True)
st.markdown("<h5><div style='font-weight: lighter;'>아프리카에 가면 반드시 봐야할 동물로 <b>🐘 코끼리, 🦁 사자, 🐃 버팔로, 🦏 코뿔소, 🐆 표범</b>을 의미한다.</h5></h5></div>", unsafe_allow_html=True)