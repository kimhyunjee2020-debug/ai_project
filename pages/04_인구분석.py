import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import matplotlib.font_manager as fm
import os
import urllib.request

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="서울시 연령대별 인구 분석",
    page_icon="📊",
    layout="wide"
)

st.title("📊 서울시 연령대별 인구 분석")

# -----------------------------
# 한글 폰트 설정 (Streamlit Cloud 대응)
# -----------------------------
font_path = "NanumGothic.ttf"

if not os.path.exists(font_path):
    urllib.request.urlretrieve(
        "https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Regular.ttf",
        font_path
    )

fontprop = fm.FontProperties(fname=font_path)

plt.rcParams["font.family"] = fontprop.get_name()
plt.rcParams["axes.unicode_minus"] = False

# -----------------------------
# CSV 읽기
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
# 연령대 컬럼 찾기
# -----------------------------
age_columns = [
    col for col in df.columns
    if (
        "0~9세" in str(col)
        or "10~19세" in str(col)
        or "20~29세" in str(col)
        or "30~39세" in str(col)
        or "40~49세" in str(col)
        or "50~59세" in str(col)
        or "60~69세" in str(col)
        or "70~79세" in str(col)
        or "80~89세" in str(col)
        or "90~99세" in str(col)
        or "100세 이상" in str(col)
    )
]

if len(age_columns) == 0:
    st.error("연령대 컬럼을 찾을 수 없습니다.")
    st.stop()

# -----------------------------
# 행정구 컬럼
# -----------------------------
district_col = df.columns[0]

# -----------------------------
# 연령대 선택
# -----------------------------
selected_age = st.selectbox(
    "👥 연령대를 선택하세요",
    age_columns
)

# -----------------------------
# 숫자 변환
# -----------------------------
temp_df = df[[district_col, selected_age]].copy()

temp_df[selected_age] = (
    temp_df[selected_age]
    .astype(str)
    .str.replace(",", "", regex=False)
)

temp_df[selected_age] = pd.to_numeric(
    temp_df[selected_age],
    errors="coerce"
)

temp_df = temp_df.dropna()

# 내림차순 정렬
temp_df = temp_df.sort_values(
    selected_age,
    ascending=False
)

# 상위 10개
top10 = temp_df.head(10)

# -----------------------------
# 그래프
# -----------------------------
fig, ax = plt.subplots(figsize=(12, 6))

fig.patch.set_facecolor("#f2f2f2")
ax.set_facecolor("#f2f2f2")

ax.plot(
    top10[district_col],
    top10[selected_age],
    color="black",
    linewidth=3,
    marker="o"
)

ax.set_title(
    f"{selected_age} 인구가 많은 자치구 TOP10",
    fontsize=18,
    fontproperties=fontprop
)

ax.set_xlabel(
    "자치구",
    fontproperties=fontprop
)

ax.set_ylabel(
    "인구수",
    fontproperties=fontprop
)

ax.yaxis.set_major_formatter(
    FuncFormatter(
        lambda x, p: format(int(x), ",")
    )
)

for label in ax.get_xticklabels():
    label.set_fontproperties(fontprop)

for label in ax.get_yticklabels():
    label.set_fontproperties(fontprop)

ax.grid(
    True,
    linestyle="--",
    alpha=0.4
)

plt.tight_layout()

st.pyplot(fig)

# -----------------------------
# 가장 많은 자치구
# -----------------------------
top_district = top10.iloc[0][district_col]
top_population = int(top10.iloc[0][selected_age])

st.subheader("🏆 가장 많은 자치구")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "자치구",
        top_district
    )

with col2:
    st.metric(
        "인구수",
        f"{top_population:,}명"
    )

# -----------------------------
# 데이터 보기
# -----------------------------
with st.expander("📋 데이터 보기"):
    st.dataframe(top10)
