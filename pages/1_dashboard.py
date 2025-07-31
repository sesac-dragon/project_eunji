import streamlit as st
import pymysql
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
from datetime import timedelta
from main import icon
from _query import db_conn, total_tour, big_five_options, tours_by_animals

# icon("🗺️")

# 제목 크게 띄우기
# st.markdown("<div style='font-size: 50px; font-weight: bold;'>Dashboard</div>", unsafe_allow_html=True)
st.set_page_config('Safari Bookings', '🦁', layout='wide')
conn = db_conn()


col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.markdown(
        "<h1 style='text-align: center;'>🦁Safari Bookings Dashboard</h1>",
        unsafe_allow_html=True
    )

    total_count = total_tour(conn)
    st.markdown(
        f"<h6 style='text-align: right;'>총 등록된 투어 수</h6>"
        f"<h6 style='text-align: right;'>{total_count:,}개</h6>",
        unsafe_allow_html=True
    )

    # 1단계: 동물 선택으로 시작 (더 직관적!)
    st.markdown("---")
    
    # # 필터 박스 스타일링
    # st.markdown("""
    # <style>
    # .main-filter-container {
    #     border: 3px solid #ff6b6b;
    #     border-radius: 20px;
    #     padding: 30px;
    #     margin: 20px 0;
    #     background: linear-gradient(135deg, #fff5f5, #ffe8e8);
    #     box-shadow: 0 4px 8px rgba(255,107,107,0.2);
    # }
    # .filter-header {
    #     font-size: 28px;
    #     font-weight: bold;
    #     color: #d63031;
    #     margin-bottom: 25px;
    #     text-align: center;
    # }
    # .secondary-filter-container {
    #     border: 2px solid #74b9ff;
    #     border-radius: 15px;
    #     padding: 25px;
    #     margin: 20px 0;
    #     background: linear-gradient(135deg, #f8fcff, #e8f4ff);
    #     box-shadow: 0 2px 4px rgba(116,185,255,0.2);
    # }
    # .secondary-header {
    #     font-size: 22px;
    #     font-weight: bold;
    #     color: #0984e3;
    #     margin-bottom: 20px;
    #     text-align: center;
    # }
    # </style>
    # """, unsafe_allow_html=True)
    
    # 메인 필터 컨테이너
    st.markdown('<div class="main-filter-container">', unsafe_allow_html=True)
    st.markdown('<div class="filter-header">🐾 보고싶은 동물을 선택해주세요!</div>', unsafe_allow_html=True)
    
    # Big Five 동물 선택
    big_five_options = big_five_options(conn)
    
    # 동물별 아이콘 매핑
    animal_icons = {
        'Lion': '🦁',
        'Leopard': '🐆', 
        'Elephant': '🐘',
        'White Rhino': '🦏',
        'Black Rhino': '🦏',
        'Buffalo': '🐃'
    }

    
    # 동물 옵션에 아이콘 추가
    animal_display = []
    for animal in big_five_options:
        icon = animal_icons.get(animal, '🦁')  # 기본 아이콘
        animal_display.append(f"{icon} {animal}")
    
    
    selected_animals_display = st.multiselect(
        "Big Five 동물 선택 (복수 선택 가능)",
        options=animal_display,
        default=[],
    )
    
    # 실제 동물명 추출
    selected_animals = []
    for display_name in selected_animals_display:
        # 아이콘 제거하고 동물명만 추출
        animal_name = display_name.split(' ', 1)[1] if ' ' in display_name else display_name
        selected_animals.append(animal_name)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 동물이 선택되었을 때만 다음 단계 표시
    if selected_animals:
        tours_df = tours_by_animals(conn, selected_animals)
        
        if not tours_df.empty:
            st.success(f"**{', '.join([animal_icons.get(a, '🦒') + ' ' + a for a in selected_animals])}** 관찰 가능한 **{len(tours_df):,}개 투어** 탐색!")
            
            # 2단계: 세부 필터링
            st.markdown('<div class="secondary-filter-container">', unsafe_allow_html=True)
            st.markdown('<div class="secondary-header">세부 조건 설정</div>', unsafe_allow_html=True)
            
            # 세부 필터 옵션들
            filter_col1, filter_col2= st.columns(2)
            
            with filter_col1:
                # 국가 필터 (추출된 국가들만)
                available_countries = sorted(tours_df['country'].str.split('&|,').explode().str.strip().unique())
                selected_countries = st.multiselect(
                    "🌍 희망 국가 (복수 선택 가능)",
                    options=available_countries,
                    default=[],
                )
            
            with filter_col2:
                # 투어 일수
                min_days = int(tours_df['tour_days'].min())
                max_days = int(tours_df['tour_days'].max())
                duration_range = st.slider(
                    "📅 여행 기간 (일)",
                    min_value=min_days,
                    max_value=max_days,
                    value=(min_days, max_days),
                    step=1,
                )

            # with filter_col3:
            #     # 가격 범위
            #     min_price = int(tours_df['price'].min())
            #     max_price = int(tours_df['price'].max())
            #     price_range = st.slider(
            #         "💰 가격 범위 (KRW):",
            #         min_value=min_price,
            #         max_value=max_price,
            #         value=(min_price, max_price),
            #         step=100,
            #     )
            
            
            # 필터 적용
            filtered_df = tours_df.copy()
            
            # 가격 필터
            # filtered_df = filtered_df[
            #     (filtered_df['price'] >= price_range[0]) & 
            #     (filtered_df['price'] <= price_range[1])
            # ]
            
            # 일수 필터
            filtered_df = filtered_df[
                (filtered_df['tour_days'] >= duration_range[0]) & 
                (filtered_df['tour_days'] <= duration_range[1])
            ]
            
            # 국가 필터
            if selected_countries:
                country_filter = pd.Series([False] * len(filtered_df), index=filtered_df.index)
                for country in selected_countries:
                    country_filter |= filtered_df['country'].str.contains(country, na=False)
                filtered_df = filtered_df[country_filter]
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 결과 표시
            if len(filtered_df) > 0:
                st.markdown(f"### 🗺️ 필터링 결과: **총 {len(filtered_df):,}개 투어**")
                
                animal_map = (filtered_df.groupby('location_name')['available_animals'].first().to_dict())
    
                unique_locations = filtered_df.drop_duplicates(subset=['location_name'])
                unique_locations['all_animals'] = unique_locations['location_name'].map(animal_map)
                
                # 지도 생성
                m = folium.Map(location=[2, 25], zoom_start=3)
                marker_cluster = MarkerCluster().add_to(m)

                for _, row in unique_locations.iterrows():
                    popup_text = f"""
                    <h5><b>📍 {row['location_name']}</b><br></h5>
                    🐾 관측 가능 동물: {row.get('all_animals', '정보 없음')}<br>
                    """
                    
                    folium.Marker(
                        [row['latitude'], row['longitude']],
                        tooltip=row['location_name'],
                        popup=folium.Popup(popup_text, max_width=350)
                    ).add_to(marker_cluster)
                st_folium(m, width=800, height=600)


                # m = folium.Map(location=[2, 25], zoom_start=3)

                # # 1. 좌표 기준으로 그룹화해서 투어 개수 계산
                # location_group = (
                #     filtered_df
                #     .groupby(['latitude', 'longitude'])
                #     .size()
                #     .reset_index(name='tour_count')
                # )

                # # 2. folium.Circle로 시각화 (tour_count를 반영해 반지름 조절)
                # for _, row in location_group.iterrows():
                #     count = row['tour_count']
                #     folium.Circle(
                #         location=[row['latitude'], row['longitude']],
                #         radius=max(2000, min(count*3000, 30000)),
                #         color="#4AFF3D",
                #         fill=True,
                #         fill_color="#93FF98",
                #         fill_opacity=0.2,
                #         popup=f"📍 {row['tour_count']}개 투어"
                #     ).add_to(m)

                

                # 선택한 동물 모두 포함된 투어만 필터링
                filtered_df = filtered_df[
                    filtered_df['available_animals'].apply(
                        lambda animals: all(animal in animals.split(', ') for animal in selected_animals)
                    )
                ]

                # 투어 목록 테이블
                st.subheader("📋 투어 상세 목록")
                display_df = filtered_df[['title', 'country', 'price', 'tour_days', 'available_animals']].copy()
                display_df.columns = ['투어명', '국가', '가격', '기간(일)', '볼 수 있는 동물']
                display_df['가격'] = display_df['가격'].apply(lambda x: f"{x:,}원")
                st.dataframe(display_df, use_container_width=True, height=400)
                
            else:
                st.warning("선택한 조건에 맞는 투어가 없습니다.")
        
        else:
            st.info(f"선택한 동물들({', '.join(selected_animals)})을 모두 볼 수 있는 투어를 찾을 수 없습니다.")
    
    # else:
        # 동물이 선택되지 않았을 때 - 인기 국가 정보 표시
        # st.info("👆 위에서 보고싶은 동물을 선택해주세요!")
        
        # # 국가별 통계 미리보기
        # with st.expander("🌍 인기 여행지 미리보기", expanded=False):
        #     country_stats = get_country_stats()
        #     if not country_stats.empty:
        #         st.subheader("투어가 많은 국가 TOP 10")
        #         top_countries = country_stats.head(10)
                
        #         for idx, row in top_countries.iterrows():
        #             col1, col2, col3 = st.columns([2, 1, 1])
        #             with col1:
        #                 st.write(f"**{row['country']}**")
        #             with col2:
        #                 st.write(f"🎯 {row['tour_count']}개 투어")
        #             with col3:
        #                 st.write(f"💰 {row['avg_price']:,.0f}원 (평균)")