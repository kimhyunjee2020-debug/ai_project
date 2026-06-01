import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 페이지 설정
st.set_page_config(
    page_title="서울시 자치구별 인구 분석",
    page_icon="📊",
    layout="wide"
)

st.title("📊 서울시 자치구별 연령대 인구 분석")

# -----------------------------
# CSV 불러오기 (인코딩 자동 처리)
# -----------------------------
encodings = ["utf-8", "utf-8-sig", "cp949", "euc-kr"]

df = None

for enc in encodings:
    try:
        df = pd.read_csv("population.csv", encoding=enc)
        st.success(f"파일 로드 성공 (인코딩: {enc})")
        break
    except:
        pass

if df is None:
    st.error("CSV 파일을 읽을 수 없습니다.")
    st.stop()

# -----------------------------
# 데이터 확인
# -----------------------------
st.subheader("📋 원본 데이터")
st.dataframe(df)

# 첫 번째 컬럼 = 행정구
district_col = df.columns[0]

# 두 번째 컬럼이 총인구수라고 가정
# 세 번째 컬럼부터 연령대 데이터
age_columns = df.columns[2:]

# -----------------------------
# 행정구 선택
# -----------------------------
district = st.selectbox(
    "🏙️ 행정구를 선택하세요",
    df[district_col]
)

selected_row = df[df[district_col] == district].iloc[0]

# 연령대 인구수
ages = age_columns
population = [selected_row[col] for col in age_columns]

# 숫자형 변환
population = pd.to_numeric(population, errors="coerce")

# -----------------------------
# 그래프
# -----------------------------
fig, ax = plt.subplots(figsize=(12, 6))

# 배경색
fig.patch.set_facecolor("#f0f0f0")
ax.set_facecolor("#f0f0f0")

# 꺾은선 그래프
ax.plot(
    ages,
    population,
    color="black",
    linewidth=3,
    marker="o"
)

ax.set_title(
    f"{district} 연령대별 인구수",
    fontsize=18,
    fontweight="bold"
)

ax.set_xlabel("연령대")
ax.set_ylabel("인구수")

ax.grid(
    True,
    linestyle="--",
    alpha=0.4
)

plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig)

# -----------------------------
# 통계
# -----------------------------
st.subheader("📈 요약 통계")

max_age = ages[population.argmax()]
max_pop = int(population.max())

st.metric(
    "가장 많은 연령대",
    max_age,
    f"{max_pop:,}명"
)
