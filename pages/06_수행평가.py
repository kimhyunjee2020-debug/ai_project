import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib

# =====================
# 페이지 설정
# =====================
st.set_page_config(
    page_title="연령별 사망원인 분석",
    page_icon="📊",
    layout="wide"
)

st.title("📊 2024 연령별 사망원인 분석")

# =====================
# 데이터 불러오기
# =====================
@st.cache_data
def load_data():

    for enc in ["cp949", "euc-kr", "utf-8"]:
        try:
            return pd.read_csv("fffff.csv", encoding=enc)
        except:
            continue

    return None

df = load_data()

if df is None:
    st.error("CSV 파일을 읽을 수 없습니다.")
    st.stop()

# =====================
# 컬럼명 변경
# =====================
df.columns = [
    "성별",
    "연령대별",
    "사망원인순위",
    "사망원인",
    "사망자수",
    "사망률"
]

# =====================
# 숫자형 변환
# =====================
df["사망자수"] = pd.to_numeric(
    df["사망자수"],
    errors="coerce"
)

df = df.dropna(subset=["사망자수"])

# =====================
# 연령대 선택
# =====================
age_list = sorted(df["연령대별"].unique())

selected_age = st.selectbox(
    "연령대를 선택하세요",
    age_list
)

# =====================
# 필터링
# =====================
filtered = df[df["연령대별"] == selected_age].copy()

filtered = filtered.sort_values(
    by="사망자수",
    ascending=False
)

# =====================
# 표 출력
# =====================
st.subheader(f"📋 {selected_age} 사망원인 순위")

st.dataframe(
    filtered[["사망원인", "사망자수"]],
    use_container_width=True
)

# =====================
# 그래프
# =====================
st.subheader("📈 사망원인별 사망자 수")

fig, ax = plt.subplots(figsize=(15, 7))

# 배경 연회색
fig.patch.set_facecolor("#f2f2f2")
ax.set_facecolor("#f2f2f2")

# 검정색 꺾은선
ax.plot(
    filtered["사망원인"],
    filtered["사망자수"],
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

# =====================
# TOP5
# =====================
st.subheader("🏆 TOP 5 사망원인")

top5 = filtered.head(5)

for i, (_, row) in enumerate(top5.iterrows(), start=1):
    st.write(
        f"{i}위 : {row['사망원인']} ({int(row['사망자수']):,}명)"
    )
