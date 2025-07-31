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

# country_options = tour_country_list()
# selected_country = st.sidebar.selectbox('나라를 선택하세요.', ['나라 선택'] + country_options)

# with st.sidebar:
#     st.header("🗺️ Map Settings")

#     location = st.text_input("Location address", value="Praça Ferreira do Amaral, Macau")

#     radius = st.slider("Radius (meter)", min_value=100, max_value=1500, value=1500)

#     theme = st.selectbox("Color theme", ["Auburn", "Jungle", "Desert", "Ocean"])

#     map_style = st.selectbox("Customize map style", ["Standard", "Satellite", "Dark", "Minimal"])

#     submit = st.button("Submit")

# # ---- 본문 영역 ----
# st.title("Safari Bookings Dashboard")

# if submit:
#     st.success(f"📍 Address: {location}\n📏 Radius: {radius}m\n🎨 Theme: {theme}\n🗺️ Map Style: {map_style}")



# with st.sidebar:
#     st.markdown("""
#         <div style="border: 1px solid #ccc; border-radius: 12px; padding: 20px;">
#     """, unsafe_allow_html=True)

#     st.text_input("Prompt")
#     st.text_area("Negative Prompt")
#     st.button("Submit")

#     st.markdown("</div>", unsafe_allow_html=True)

# st.markdown(
#     """
#     <style>
#         section[data-testid="stSidebar"] {
#             width: 500px !important; # Set the width to your desired value
#         }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# # Example sidebar content
# st.sidebar.header("This is the sidebar")
# st.sidebar.text("This is some text in the sidebar")

# # Example main content
# st.header("This is the Main Content Area")
# st.text("This is some text in the main content area")

# st.set_page_config(page_title="Sidebar Demo", layout="wide")

# with st.sidebar:
#     # 상단 강조 박스 (Streamlit v1.26)
#     st.markdown("""
#         <div style='
#             background-color: #e5e7eb;
#             padding: 10px 15px;
#             border-radius: 10px;
#             font-weight: bold;
#             margin-bottom: 15px;
#         '>
#         🎈 Streamlit v1.26
#         </div>
#     """, unsafe_allow_html=True)

#     # 데모 1: 체크박스 스타일 링크 (사실은 마크다운 텍스트)
#     st.markdown("✅ **st.status demo**", unsafe_allow_html=True)

#     # 데모 2: 일반 텍스트 링크
#     st.markdown("🦜 LangChain demo", unsafe_allow_html=True)

# tabs = st.tabs(["📊 Dashboard", "🔍 Analysis"])

# tab1, tab2 = st.tabs(["📊 Dashboard", "🔍 Analysis"])

# with tab1:
#     st.title("📊 Safari Booking Dashboard")
#     st.write("대시보드 영역입니다.")
#     # 예: st.metric, st.dataframe 등

# with tab2:
#     st.title("🔍 Deep Analysis")
#     st.write("분석 영역입니다.")
#     # 예: st.line_chart, st.altair_chart 등
