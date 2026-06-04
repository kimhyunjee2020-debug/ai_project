import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from pathlib import Path

# --------------------
# 페이지 설정
# --------------------
st.set_page_config(
    page_title="서울 기온 분석",
    page_icon="🌡️",
    layout="wide"
)

# --------------------
# 한글 폰트 설정
# --------------------
font_path = Path("fonts/NanumGothic.ttf")

if font_path.exists():
    font_prop = fm.FontProperties(fname=str(font_path))
    plt.rcParams["font.family"] = font_prop.get_name()

plt.rcParams["axes.unicode_minus"] = False

# --------------------
# 데이터 불러오기
# --------------------
@st.cache_data
def load_data():

    try:
        df = pd.read_csv("seoul.csv", encoding="cp949")
    except:
        try:
            df = pd.read_csv("seoul.csv", encoding="utf-8")
        except:
            df = pd.read_csv("seoul.csv")

    df.columns = df.columns.str.strip()

    # 날짜 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"],
        errors="coerce"
    )

    df = df.dropna(subset=["날짜"])

    # 숫자형 변환
    df["최고기온(℃)"] = pd.to_numeric(
        df["최고기온(℃)"],
        errors="coerce"
    )

    df["최저기온(℃)"] = pd.to_numeric(
        df["최저기온(℃)"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["최고기온(℃)", "최저기온(℃)"]
    )

    df["연도"] = df["날짜"].dt.year
    df["월"] = df["날짜"].dt.month
    df["일"] = df["날짜"].dt.day

    return df

df = load_data()

# --------------------
# 제목
# --------------------
st.title("🌡️ 서울 기온 분석")

st.write(
    "월과 일을 선택하면 해당 날짜의 연도별 최고기온과 최저기온을 확인할 수 있습니다."
)

# --------------------
# 월 선택
# --------------------
month = st.selectbox(
    "월 선택",
    sorted(df["월"].unique())
)

# --------------------
# 일 선택
# --------------------
days = sorted(
    df[df["월"] == month]["일"].unique()
)

day = st.selectbox(
    "일 선택",
    days
)

# --------------------
# 데이터 필터링
# --------------------
selected_df = df[
    (df["월"] == month) &
    (df["일"] == day)
].copy()

selected_df = selected_df.sort_values("연도")

# --------------------
# 그래프
# --------------------
fig, ax = plt.subplots(
    figsize=(14, 6)
)

# 최고기온
ax.plot(
    selected_df["연도"],
    selected_df["최고기온(℃)"],
    color="red",
    linewidth=2,
    label="최고기온"
)

# 최저기온
ax.plot(
    selected_df["연도"],
    selected_df["최저기온(℃)"],
    color="blue",
    linewidth=2,
    label="최저기온"
)

ax.set_title(
    f"{month}월 {day}일 서울 기온 변화"
)

ax.set_xlabel("연도")
ax.set_ylabel("기온(℃)")

ax.legend()

ax.grid(
    True,
    alpha=0.3
)

plt.tight_layout()

st.pyplot(fig)

# --------------------
# 통계
# --------------------
col1, col2 = st.columns(2)

with col1:
    st.metric(
        "🔥 최고기온 최고값",
        f"{selected_df['최고기온(℃)'].max():.1f}℃"
    )

with col2:
    st.metric(
        "🥶 최저기온 최저값",
        f"{selected_df['최저기온(℃)'].min():.1f}℃"
    )

# --------------------
# 데이터 보기
# --------------------
with st.expander("데이터 보기"):
    st.dataframe(
        selected_df,
        use_container_width=True
    )
