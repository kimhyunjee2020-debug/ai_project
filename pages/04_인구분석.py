import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 페이지 설정
st.set_page_config(
    page_title="서울시 자치구별 연령대 인구 분석",
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
        continue

if df is None:
    st.error("CSV 파일을 읽을 수 없습니다.")
    st.stop()

# -----------------------------
# 데이터 확인
# -----------------------------
with st.expander("데이터 확인"):
    st.write("컬럼명")
    st.write(df.columns.tolist())
    st.dataframe(df.head())

# -----------------------------
# 첫 번째 컬럼을 행정구로 사용
# -----------------------------
district_col = df.columns[0]

# 숫자형 컬럼만 추출
numeric_cols = []

for col in df.columns:
    temp = pd.to_numeric(
        df[col].astype(str).str.replace(",", ""),
        errors="coerce"
    )

    if temp.notna().sum() > 0:
        numeric_cols.append(col)

# 총인구수 제외
if len(numeric_cols) > 1:
    age_columns = numeric_cols[1:]
else:
    age_columns = numeric_cols

# -----------------------------
# 행정구 선택
# -----------------------------
district = st.selectbox(
    "🏙️ 행정구 선택",
    df[district_col].astype(str).unique()
)

selected_row = df[df[district_col].astype(str) == district].iloc[0]

# -----------------------------
# 연령대 데이터 추출
# -----------------------------
ages = []
population = []

for col in age_columns:
    value = str(selected_row[col]).replace(",", "")

    try:
        value = float(value)

        ages.append(col)
        population.append(value)

    except:
        pass

if len(population) == 0:
    st.error("연령대 데이터를 찾을 수 없습니다.")
    st.stop()

# -----------------------------
# 그래프
# -----------------------------
fig, ax = plt.subplots(figsize=(12, 6))

fig.patch.set_facecolor("#f2f2f2")
ax.set_facecolor("#f2f2f2")

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
        f"{int(max(population)):,}명"
    )
