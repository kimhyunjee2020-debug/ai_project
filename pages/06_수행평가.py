import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

# --------------------
# 한글 설정
# --------------------
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# --------------------
# 페이지 설정
# --------------------
st.set_page_config(
    page_title="연령별 사망원인 분석",
    page_icon="📊",
    layout="wide"
)

st.title("📊 2024 연령별 사망원인 분석")
st.markdown("---")

# --------------------
# 데이터 불러오기
# --------------------
df = pd.read_csv("fffff.csv", encoding="utf-8")

# 컬럼명 공백 제거
df.columns = df.columns.str.strip()

# 숫자형 변환
df["사망자수"] = (
    df["사망자수"]
    .astype(str)
    .str.replace(",", "")
)

df["사망자수"] = pd.to_numeric(df["사망자수"], errors="coerce")

# 결측 제거
df = df.dropna(subset=["사망자수"])

# --------------------
# 연령대 선택
# --------------------
age_list = sorted(df["연령"].dropna().unique())

selected_age = st.selectbox(
    "연령대를 선택하세요",
    age_list
)

# --------------------
# 선택된 연령 데이터
# --------------------
age_df = df[df["연령"] == selected_age].copy()

# 높은 순 정렬
age_df = age_df.sort_values(
    by="사망자수",
    ascending=False
)

# --------------------
# 표 출력
# --------------------
st.subheader(f"📋 {selected_age} 사망원인 순위")

st.dataframe(
    age_df[["사망원인", "사망자수"]],
    use_container_width=True
)

# --------------------
# 그래프
# --------------------
st.subheader("📈 사망원인별 사망자 수")

fig, ax = plt.subplots(figsize=(14, 6))

# 배경 연한 회색
fig.patch.set_facecolor("#f2f2f2")
ax.set_facecolor("#f2f2f2")

# 검정색 꺾은선
ax.plot(
    age_df["사망원인"],
    age_df["사망자수"],
    color="black",
    linewidth=2,
    marker="o"
)

ax.set_xlabel("사망원인")
ax.set_ylabel("사망자 수")
ax.set_title(f"{selected_age} 사망원인 분석")

plt.xticks(rotation=75)
plt.tight_layout()

st.pyplot(fig)

# --------------------
# TOP5
# --------------------
st.subheader("🏆 TOP 5 사망원인")

top5 = age_df.head(5)

for i, row in enumerate(top5.itertuples(), start=1):
    st.write(
        f"{i}위 : {row.사망원인} ({int(row.사망자수):,}명)"
    )
