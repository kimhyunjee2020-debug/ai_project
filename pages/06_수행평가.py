import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------
# 페이지 설정
# -------------------
st.set_page_config(
    page_title="연령별 사망원인 분석",
    page_icon="📊",
    layout="wide"
)

# -------------------
# 한글 설정
# -------------------
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

st.title("📊 2024 연령별 사망원인 분석")
st.markdown("---")

# -------------------
# 데이터 불러오기
# -------------------
@st.cache_data
def load_data():

    df = pd.read_csv(
        "fffff.csv",
        encoding="cp949"
    )

    # 첫 번째 행이 실제 컬럼명
    new_cols = df.iloc[0]

    df = df[1:].copy()
    df.columns = new_cols

    return df

df = load_data()

# -------------------
# 컬럼명 지정
# -------------------
gender_col = "성별"
age_col = "연령대별"
rank_col = "사망원인 순위"
cause_col = "사망원인"
death_col = "사망자수(명)"

# -------------------
# 숫자 변환
# -------------------
df[death_col] = pd.to_numeric(
    df[death_col],
    errors="coerce"
)

df = df.dropna(subset=[death_col])

# -------------------
# 연령대 목록
# -------------------
age_list = sorted(df[age_col].unique())

selected_age = st.selectbox(
    "연령대를 선택하세요",
    age_list
)

# -------------------
# 데이터 필터링
# -------------------
filtered = df[df[age_col] == selected_age].copy()

# 사망자수 내림차순
filtered = filtered.sort_values(
    death_col,
    ascending=False
)

# -------------------
# 데이터 표
# -------------------
st.subheader(f"📋 {selected_age} 사망원인 순위")

st.dataframe(
    filtered[
        [rank_col, cause_col, death_col]
    ],
    use_container_width=True
)

# -------------------
# 그래프
# -------------------
st.subheader("📈 사망원인별 사망자 수")

fig, ax = plt.subplots(
    figsize=(14, 6)
)

# 배경 연회색
fig.patch.set_facecolor("#f2f2f2")
ax.set_facecolor("#f2f2f2")

# 검정색 꺾은선
ax.plot(
    filtered[cause_col],
    filtered[death_col],
    color="black",
    marker="o",
    linewidth=2
)

ax.set_title(
    f"{selected_age} 사망원인 분석"
)

ax.set_xlabel("사망원인")
ax.set_ylabel("사망자 수")

plt.xticks(rotation=70)
plt.tight_layout()

st.pyplot(fig)

# -------------------
# TOP5
# -------------------
st.subheader("🏆 TOP 5 사망원인")

top5 = filtered.head(5)

for i, row in enumerate(top5.itertuples(), start=1):
    st.write(
        f"{i}위 : {getattr(row, cause_col)} ({int(getattr(row, death_col)):,}명)"
    )

# -------------------
# 원본 데이터 보기
# -------------------
with st.expander("원본 데이터 보기"):
    st.dataframe(df)
