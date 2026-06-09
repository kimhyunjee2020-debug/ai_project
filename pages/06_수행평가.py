import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# 페이지 설정
# =========================
st.set_page_config(
    page_title="연령별 사망원인 분석",
    page_icon="📊",
    layout="wide"
)

# =========================
# 한글 설정
# =========================
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

st.title("📊 2024 연령별 사망원인 분석")
st.markdown("---")

# =========================
# 데이터 읽기
# =========================
@st.cache_data
def load_data():

    # 인코딩 자동 시도
    for enc in ["cp949", "euc-kr", "utf-8"]:
        try:
            df = pd.read_csv(
                "fffff.csv",
                encoding=enc,
                sep=None,
                engine="python"
            )
            return df
        except:
            pass

    return None

df = load_data()

if df is None:
    st.error("CSV 파일을 읽을 수 없습니다.")
    st.stop()

# =========================
# 컬럼 확인
# =========================
st.write("데이터 미리보기")
st.dataframe(df.head())

# =========================
# 실제 컬럼명 찾기
# =========================
columns = list(df.columns)

age_col = None
cause_col = None
death_col = None

for col in columns:

    if "연령" in str(col):
        age_col = col

    if "사망원인" in str(col):
        cause_col = col

    if "사망자" in str(col):
        death_col = col

if age_col is None:
    st.error("연령 컬럼을 찾을 수 없습니다.")
    st.write(columns)
    st.stop()

if cause_col is None:
    st.error("사망원인 컬럼을 찾을 수 없습니다.")
    st.write(columns)
    st.stop()

if death_col is None:
    st.error("사망자수 컬럼을 찾을 수 없습니다.")
    st.write(columns)
    st.stop()

# =========================
# 숫자 변환
# =========================
df[death_col] = (
    df[death_col]
    .astype(str)
    .str.replace(",", "", regex=False)
)

df[death_col] = pd.to_numeric(
    df[death_col],
    errors="coerce"
)

df = df.dropna(subset=[death_col])

# =========================
# 연령 선택
# =========================
age_list = sorted(df[age_col].dropna().unique())

selected_age = st.selectbox(
    "연령대를 선택하세요",
    age_list
)

# =========================
# 필터링
# =========================
filtered = df[
    df[age_col] == selected_age
].copy()

filtered = filtered.sort_values(
    by=death_col,
    ascending=False
)

# =========================
# 표
# =========================
st.subheader(f"📋 {selected_age} 사망원인 순위")

st.dataframe(
    filtered[[cause_col, death_col]],
    use_container_width=True
)

# =========================
# 그래프
# =========================
st.subheader("📈 사망원인별 사망자 수")

fig, ax = plt.subplots(figsize=(14, 6))

fig.patch.set_facecolor("#f2f2f2")
ax.set_facecolor("#f2f2f2")

ax.plot(
    filtered[cause_col],
    filtered[death_col],
    color="black",
    marker="o",
    linewidth=2
)

ax.set_title(f"{selected_age} 사망원인 분석")
ax.set_xlabel("사망원인")
ax.set_ylabel("사망자 수")

plt.xticks(rotation=70)
plt.tight_layout()

st.pyplot(fig)

# =========================
# TOP5
# =========================
st.subheader("🏆 TOP 5 사망원인")

top5 = filtered.head(5)

for idx, row in top5.iterrows():
    st.write(
        f"{len(top5.loc[:idx])}위 : {row[cause_col]} ({int(row[death_col]):,}명)"
    )
