# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 페이지 설정
st.set_page_config(
    page_title="🌍 국가별 MBTI 분석",
    page_icon="📊",
    layout="wide"
)

# 제목
st.title("🌍 국가별 MBTI 비율 분석")
st.markdown("국가를 선택하면 MBTI 비율을 막대그래프로 보여줘요!")

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

df = load_data()

# 국가 선택
countries = sorted(df["Country"].unique())
selected_country = st.selectbox(
    "📌 국가를 선택하세요",
    countries
)

# 선택된 국가 데이터
country_data = df[df["Country"] == selected_country].iloc[0]

# MBTI 컬럼만 추출
mbti_types = [col for col in df.columns if col != "Country"]
values = country_data[mbti_types]

# 가장 높은 값 찾기
max_index = np.argmax(values)

# 색상 설정
colors = []

green_shades = [
    "#d8f3dc",
    "#b7e4c7",
    "#95d5b2",
    "#74c69d",
    "#52b788",
    "#40916c",
    "#2d6a4f",
    "#1b4332"
]

green_idx = 0

for i in range(len(values)):
    if i == max_index:
        colors.append("#ff1493")  # 핫핑크
    else:
        colors.append(green_shades[green_idx % len(green_shades)])
        green_idx += 1

# 그래프 생성
fig, ax = plt.subplots(figsize=(12, 6))

bars = ax.bar(
    mbti_types,
    values,
    color=colors
)

# 그래프 꾸미기
ax.set_title(
    f"{selected_country}의 MBTI 비율",
    fontsize=18,
    fontweight="bold"
)

ax.set_xlabel("MBTI 유형", fontsize=12)
ax.set_ylabel("비율", fontsize=12)

plt.xticks(rotation=45)

# 값 표시
for bar in bars:
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width()/2,
        height,
        f"{height:.2f}",
        ha='center',
        va='bottom',
        fontsize=9
    )

st.pyplot(fig)

# 최고 MBTI 표시
top_mbti = values.idxmax()
top_value = values.max()

st.success(
    f"💖 {selected_country}에서 가장 높은 MBTI는 "
    f"**{top_mbti}** ({top_value:.2%}) 입니다!"
)
