import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="서울 기온 분석",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 서울 기온 분석")

# -----------------------------
# 데이터 불러오기
# -----------------------------
@st.cache_data
def load_data():

    # 인코딩 자동 대응
    try:
        df = pd.read_csv("seoul.csv", encoding="cp949")
    except:
        df = pd.read_csv("seoul.csv", encoding="utf-8")

    # 컬럼명 공백 제거
    df.columns = df.columns.str.strip()

    # 날짜 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"],
        errors="coerce"
    )

    # 날짜 없는 행 제거
    df = df.dropna(subset=["날짜"])

    # 기온 컬럼 숫자로 변환
    df["최고기온(℃)"] = pd.to_numeric(
        df["최고기온(℃)"],
        errors="coerce"
    )

    df["최저기온(℃)"] = pd.to_numeric(
        df["최저기온(℃)"],
        errors="coerce"
    )

    return df

df = load_data()

# -----------------------------
# 연도 선택
# -----------------------------
years = sorted(
    df["날짜"].dt.year.unique()
)

selected_year = st.selectbox(
    "📅 연도 선택",
    years,
    index=len(years)-1
)

# -----------------------------
# 데이터 필터링
# -----------------------------
year_df = df[
    df["날짜"].dt.year == selected_year
].copy()

year_df = year_df.sort_values("날짜")

# x축용
year_df["월일"] = year_df["날짜"].dt.strftime("%m-%d")

# -----------------------------
# 그래프
# -----------------------------
st.subheader(
    f"📈 {selected_year}년 최고기온 · 최저기온 변화"
)

fig, ax = plt.subplots(figsize=(15, 6))

# 최고기온 (빨강)
ax.plot(
    year_df["월일"],
    year_df["최고기온(℃)"],
    color="red",
    linewidth=2,
    label="최고기온"
)

# 최저기온 (파랑)
ax.plot(
    year_df["월일"],
    year_df["최저기온(℃)"],
    color="blue",
    linewidth=2,
    label="최저기온"
)

ax.set_title(
    f"{selected_year}년 서울 기온 변화"
)

ax.set_xlabel("날짜")
ax.set_ylabel("기온(℃)")

# 범례
ax.legend()

# 격자
ax.grid(True, alpha=0.3)

# x축 간격 조절
tick_step = max(len(year_df)//12, 1)

ax.set_xticks(
    range(0, len(year_df), tick_step)
)

ax.set_xticklabels(
    year_df["월일"].iloc[::tick_step],
    rotation=45
)

plt.tight_layout()

st.pyplot(fig)

# -----------------------------
# 통계
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.metric(
        "🔥 최고기온",
        f"{year_df['최고기온(℃)'].max():.1f}℃"
    )

with col2:
    st.metric(
        "🥶 최저기온",
        f"{year_df['최저기온(℃)'].min():.1f}℃"
    )

# -----------------------------
# 데이터 보기
# -----------------------------
with st.expander("📋 데이터 보기"):
    st.dataframe(
        year_df,
        use_container_width=True
    )
