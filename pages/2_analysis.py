import streamlit as st
from main import icon
icon("🔍")

# 제목 크게 띄우기
st.set_page_config('Safari Bookings', '🦁', layout='wide')
st.markdown("<div style='font-size: 50px; font-weight: bold;'>Analysis</div>", unsafe_allow_html=True)
st.write('분석 공간')