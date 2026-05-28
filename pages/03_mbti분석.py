# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="🌍 MBTI 국가 순위",
    page_icon="📊",
    layout="wide"
)

st.title("🌍 MBTI 유형별 국가 TOP10")
st.markdown("원하는 MBTI를 선택하면 비율이 높은 나라 TOP10을 보여줘요!")

# -----------------------------
# 데이터 불러오기
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_csv("countriesMBTI_16types.csv")

df = load_data()

# MBTI 컬럼
mbti_types = [col for col in df.columns if col != "Country"]

# -----------------------------
# MBTI 선택
# -----------------------------
selected_mbti = st.selectbox(
    "📌 MBTI 유형 선택",
    mbti_types
)

# -----------------------------
# TOP10 국가 추출
# -----------------------------
top10 = (
    df[["Country", selected_mbti]]
    .sort_values(by=selected_mbti, ascending=False)
    .head(10)
)

# -----------------------------
# 그래프 색상 설정
# 1위 = 핫핑크
# 나머지 = 초록 그라데이션
# -----------------------------
green_gradient = [
    "#d8f3dc",
    "#b7e4c7",
    "#95d5b2",
    "#74c69d",
    "#52b788",
    "#40916c",
    "#2d6a4f",
    "#1b4332",
    "#081c15"
]

colors = ["#ff1493"]  # 1위 핫핑크

for i in range(9):
    colors.append(green_gradient[i])

# -----------------------------
# 그래프 생성
# -----------------------------
fig, ax = plt.subplots(figsize=(12, 6))

bars = ax.bar(
    top10["Country"],
    top10[selected_mbti],
    color=colors
)

# 제목
ax.set_title(
    f"🏆 {selected_mbti} 비율이 높은 국가 TOP10",
    fontsize=18,
    fontweight="bold"
)

# 축 이름
ax.set_xlabel("국가", fontsize=12)
ax.set_ylabel("비율", fontsize=12)

# x축 회전
plt.xticks(rotation=30)

# 값 표시
for i, bar in enumerate(bars):
    height = bar.get_height()

    ax.text(
        bar.get_x() + bar.get_width()/2,
        height,
        f"{height:.2%}",
        ha='center',
        va='bottom',
        fontsize=10,
        fontweight='bold'
    )

# Streamlit 출력
st.pyplot(fig)

# -----------------------------
# 순위 표
# -----------------------------
st.subheader("📋 TOP10 순위")

rank_df = top10.copy()
rank_df.insert(0, "순위", range(1, 11))

rank_df.columns = ["순위", "국가", "비율"]

st.dataframe(
    rank_df,
    use_container_width=True
)

# -----------------------------
# 1위 국가 강조
# -----------------------------
top_country = top10.iloc[0]["Country"]
top_value = top10.iloc[0][selected_mbti]

st.success(
    f"💖 {selected_mbti} 비율 1위 국가는 "
    f"**{top_country}** 입니다! ({top_value:.2%})"
)
