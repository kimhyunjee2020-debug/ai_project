import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 페이지 설정
st.set_page_config(
    page_title="서울시 연령대별 인구 분석",
    page_icon="📊",
    layout="wide"
)

st.title("📊 서울시 자치구별 연령대 인구 분석")

# 데이터 불러오기
df = pd.read_csv("population.csv", encoding="utf-8")

# 자치구 컬럼명
district_col = df.columns[0]

# 연령대 컬럼
age_columns = df.columns[2:]

# 자치구 선택
district = st.selectbox(
    "행정구(자치구)를 선택하세요",
    df[district_col]
)

# 선택된 데이터
selected = df[df[district_col] == district].iloc[0]

# 연령대와 인구수
ages = age_columns
population = [selected[col] for col in age_columns]

# 그래프 생성
fig, ax = plt.subplots(figsize=(12, 6))

# 배경색
ax.set_facecolor("#f2f2f2")
fig.patch.set_facecolor("#f2f2f2")

# 꺾은선 그래프
ax.plot(
    ages,
    population,
    color="black",
    linewidth=2,
    marker="o"
)

# 제목
ax.set_title(
    f"{district} 연령대별 인구수",
    fontsize=16,
    fontweight="bold"
)

# 축 이름
ax.set_xlabel("연령대")
ax.set_ylabel("인구수")

# 격자
ax.grid(True, linestyle="--", alpha=0.4)

# 글자 회전
plt.xticks(rotation=45)

st.pyplot(fig)

# 데이터 보기
with st.expander("📋 데이터 보기"):
    st.dataframe(df)
