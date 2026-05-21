import streamlit as st
import folium
from streamlit_folium import st_folium

# 페이지 설정
st.set_page_config(
    page_title="서울 관광지 TOP10",
    page_icon="🗺️",
    layout="wide"
)

st.title("🗺️ 외국인들이 좋아하는 서울 관광지 TOP10")
st.markdown("폴리움(Folium) 지도로 서울의 인기 관광지를 확인해보세요!")

# 관광지 데이터
tour_places = [
    {
        "name": "경복궁",
        "location": [37.5796, 126.9770],
        "description": "조선 시대의 대표 궁궐"
    },
    {
        "name": "북촌한옥마을",
        "location": [37.5826, 126.9830],
        "description": "전통 한옥이 모여 있는 마을"
    },
    {
        "name": "명동",
        "location": [37.5636, 126.9827],
        "description": "쇼핑과 먹거리의 중심지"
    },
    {
        "name": "N서울타워",
        "location": [37.5512, 126.9882],
        "description": "서울 야경 명소"
    },
    {
        "name": "홍대거리",
        "location": [37.5563, 126.9220],
        "description": "젊음과 예술의 거리"
    },
    {
        "name": "인사동",
        "location": [37.5740, 126.9865],
        "description": "전통 문화와 공예 거리"
    },
    {
        "name": "롯데월드타워",
        "location": [37.5131, 127.1025],
        "description": "서울의 초고층 랜드마크"
    },
    {
        "name": "광장시장",
        "location": [37.5704, 126.9998],
        "description": "전통 음식 시장"
    },
    {
        "name": "동대문디자인플라자(DDP)",
        "location": [37.5665, 127.0092],
        "description": "현대적인 디자인 명소"
    },
    {
        "name": "한강공원",
        "location": [37.5207, 126.9395],
        "description": "서울 시민들의 휴식 공간"
    }
]

# 서울 중심 좌표
seoul_center = [37.5665, 126.9780]

# 지도 생성
m = folium.Map(
    location=seoul_center,
    zoom_start=11,
    tiles="CartoDB positron"
)

# 관광지 마커 추가
for place in tour_places:
    folium.Marker(
        location=place["location"],
        popup=f"""
        <b>{place['name']}</b><br>
        {place['description']}
        """,
        tooltip=place["name"],
        icon=folium.Icon(
            color="blue",
            icon="star"
        )
    ).add_to(m)

# 지도 출력
st.subheader("📍 서울 관광지 지도")

st_folium(
    m,
    width=1400,
    height=700
)

# 관광지 목록 출력
st.subheader("📖 관광지 설명")

for idx, place in enumerate(tour_places, start=1):
    st.markdown(
        f"""
        ### {idx}. {place['name']}
        - {place['description']}
        """
    )
