import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="서울시 연령대별 인구 분석",
    page_icon="📊",
    layout="wide"
)

st.title("📊 서울시 자치구별 연령대 인구 분석")

# -----------------------------
# 한글 설정
# -----------------------------
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

# -----------------------------
# CSV 불러오기
# -----------------------------
encodings = ["utf-8", "utf-8-sig", "cp949", "euc-kr"]

df = None

for enc in encodings:
    try:
        df = pd.read_csv("population.csv", encoding=enc)
        break
    except:
        pass

if df is None:
    st.error("CSV 파일을 읽을 수 없습니다.")
    st.stop()

# -----------------------------
# 행정구 컬럼
# -----------------------------
district_col = df.columns[0]

# -----------------------------
# 연령 컬럼만 추출
# (총인구수, 연령구간인구수 제외)
# -----------------------------
age_columns = []

for col in df.columns:
    col_str = str(col)

    if (
        "0~9세" in col_str
        or "10~19세" in col_str
        or "20~29세" in col_str
        or "30~39세" in col_str
        or "40~49세" in col_str
        or "50~59세" in col_str
        or "60~69세" in col_str
        or "70~79세" in col_str
        or "80~89세" in col_str
        or "90~99세" in col_str
        or "100세 이상" in col_str
    ):
        age_columns.append(col)

# -----------------------------
# 행정구 선택
# -----------------------------
district = st.selectbox(
    "🏙️ 행정구를 선택하세요",
    df[district_col]
)

selected_row = df[df[district_col] == district].iloc[0]

# -----------------------------
# 데이터 추출
# -----------------------------
ages = []
population = []

for col in age_columns:

    value = str(selected_row[col]).replace(",", "")

    try:
        value = int(float(value))

        ages.append(col)
        population.append(value)

    except:
        pass

# -----------------------------
# 그래프
# -----------------------------
fig, ax = plt.subplots(figsize=(12, 6))

# 배경색
fig.patch.set_facecolor("#f2f2f2")
ax.set_facecolor("#f2f2f2")

# 꺾은선 그래프
ax.plot(
    ages,
    population,
    color="black",
    linewidth=3,
    marker="o"
)

# 제목
ax.set_title(
    f"{district} 연령대별 인구수",
    fontsize=18,
    fontweight="bold"
)

# 축 제목
ax.set_xlabel("연령대")
ax.set_ylabel("인구수")

# 천 단위 콤마
ax.yaxis.set_major_formatter(
    FuncFormatter(lambda x, p: format(int(x), ","))
)

# 격자
ax.grid(
    True,
    linestyle="--",
    alpha=0.4
)

plt.xticks(rotation=0)
plt.tight_layout()

st.pyplot(fig)

# -----------------------------
# 최대 인구 연령대
# -----------------------------
if len(population) > 0:

    max_idx = population.index(max(population))

    st.subheader("📈 분석 결과")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "가장 많은 연령대",
            ages[max_idx]
        )

    with col2:
        st.metric(
            "인구수",
            f"{population[max_idx]:,}명"
        )
