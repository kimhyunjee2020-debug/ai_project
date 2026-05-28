# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# -----------------------------------
# 페이지 설정
# -----------------------------------
st.set_page_config(
    page_title="🌍 MBTI 세계 분석",
    page_icon="📊",
    layout="wide"
)

# -----------------------------------
# 제목
# -----------------------------------
st.title("🌍 MBTI 세계 분석")
st.markdown("국가별 MBTI 비율과 MBTI TOP10 국가를 확인해보세요!")

# -----------------------------------
# 데이터 불러오기
# -----------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("countriesMBTI_16types.csv")

df = load_data()

# MBTI 컬럼 추출
mbti_types = [col for col in df.columns if col != "Country"]

# -----------------------------------
# 탭 생성
# -----------------------------------
tab1, tab2 = st.tabs([
    "🌎 국가별 MBTI 분석",
    "🏆 MBTI TOP10 국가"
])

# ==================================================
# TAB 1 : 국가별 MBTI 비율
# ==================================================
with tab1:

    st.header("🌎 국가별 MBTI 비율")

    # 국가 선택
    countries = sorted(df["Country"].unique())

    selected_country = st.selectbox(
        "📌 국가를 선택하세요",
        countries
    )

    # -----------------------------------
    # 선택 국가 데이터
    # -----------------------------------
    country_data = df[df["Country"] == selected_country].iloc[0]

    # MBTI 데이터만 추출
    values = country_data[mbti_types]

    # -----------------------------------
    # 🔥 높은 비율 순으로 정렬
    # -----------------------------------
    sorted_values = values.sort_values(
        ascending=False
    )

    sorted_mbti = sorted_values.index
    sorted_scores = sorted_values.values

    # -----------------------------------
    # 색상 설정
    # 1등 = 핫핑크
    # 나머지 = 초록 그라데이션
    # -----------------------------------
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

    colors = []

    green_idx = 0

    for i in range(len(sorted_scores)):

        if i == 0:
            colors.append("#ff1493")  # 핫핑크
        else:
            colors.append(
                green_shades[
                    green_idx % len(green_shades)
                ]
            )
            green_idx += 1

    # -----------------------------------
    # 그래프 생성
    # -----------------------------------
    fig1, ax1 = plt.subplots(
        figsize=(12, 6)
    )

    bars = ax1.bar(
        sorted_mbti,
        sorted_scores,
        color=colors
    )

    # 제목
    ax1.set_title(
        f"{selected_country}의 MBTI 비율",
        fontsize=18,
        fontweight="bold"
    )

    # 축 이름
    ax1.set_xlabel("MBTI 유형")
    ax1.set_ylabel("비율")

    # x축 회전
    plt.xticks(rotation=45)

    # -----------------------------------
    # 값 표시
    # -----------------------------------
    for bar in bars:

        height = bar.get_height()

        ax1.text(
            bar.get_x() + bar.get_width()/2,
            height,
            f"{height:.2%}",
            ha='center',
            va='bottom',
            fontsize=9
        )

    # Streamlit 출력
    st.pyplot(fig1)

    # -----------------------------------
    # 최고 MBTI 표시
    # -----------------------------------
    top_mbti = sorted_mbti[0]
    top_value = sorted_scores[0]

    st.success(
        f"💖 {selected_country}에서 가장 높은 MBTI는 "
        f"**{top_mbti}** ({top_value:.2%}) 입니다!"
    )

# ==================================================
# TAB 2 : MBTI별 국가 TOP10
# ==================================================
with tab2:

    st.header("🏆 MBTI 유형별 국가 TOP10")

    # MBTI 선택
    selected_mbti = st.selectbox(
        "📌 MBTI 유형 선택",
        mbti_types
    )

    # -----------------------------------
    # TOP10 국가 추출
    # -----------------------------------
    top10 = (
        df[["Country", selected_mbti]]
        .sort_values(
            by=selected_mbti,
            ascending=False
        )
        .head(10)
    )

    # -----------------------------------
    # 색상 설정
    # -----------------------------------
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

    colors2 = ["#ff1493"]

    for i in range(9):
        colors2.append(
            green_gradient[i]
        )

    # -----------------------------------
    # 그래프 생성
    # -----------------------------------
    fig2, ax2 = plt.subplots(
        figsize=(12, 6)
    )

    bars2 = ax2.bar(
        top10["Country"],
        top10[selected_mbti],
        color=colors2
    )

    # 제목
    ax2.set_title(
        f"🏆 {selected_mbti} 비율이 높은 국가 TOP10",
        fontsize=18,
        fontweight="bold"
    )

    # 축 이름
    ax2.set_xlabel("국가")
    ax2.set_ylabel("비율")

    # x축 회전
    plt.xticks(rotation=30)

    # -----------------------------------
    # 값 표시
    # -----------------------------------
    for bar in bars2:

        height = bar.get_height()

        ax2.text(
            bar.get_x() + bar.get_width()/2,
            height,
            f"{height:.2%}",
            ha='center',
            va='bottom',
            fontsize=10,
            fontweight='bold'
        )

    # Streamlit 출력
    st.pyplot(fig2)

    # -----------------------------------
    # 순위표
    # -----------------------------------
    st.subheader("📋 TOP10 순위")

    rank_df = top10.copy()

    rank_df.insert(
        0,
        "순위",
        range(1, 11)
    )

    rank_df.columns = [
        "순위",
        "국가",
        "비율"
    ]

    st.dataframe(
        rank_df,
        use_container_width=True
    )

    # -----------------------------------
    # 1위 국가 표시
    # -----------------------------------
    top_country = top10.iloc[0]["Country"]
    top_value2 = top10.iloc[0][selected_mbti]

    st.success(
        f"💖 {selected_mbti} 비율 1위 국가는 "
        f"**{top_country}** 입니다! ({top_value2:.2%})"
    )
