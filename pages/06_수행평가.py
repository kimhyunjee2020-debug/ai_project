import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# ----------------------
# 한글 폰트 등록
# ----------------------
font_path = "NanumGothic.ttf"

fm.fontManager.addfont(font_path)
font_name = fm.FontProperties(fname=font_path).get_name()

plt.rcParams["font.family"] = font_name
plt.rcParams["axes.unicode_minus"] = False

# ----------------------
# 페이지 설정
# ----------------------
st.set_page_config(
    page_title="연령별 사망원인 분석",
    page_icon="📊",
    layout="wide"
)

st.title("📊 2024 연령별 사망원인 분석")

# ----------------------
# 데이터 읽기
# ----------------------
df = pd.read_csv("fffff.csv", encoding="cp949")

df.columns = [
    "성별",
    "연령대별",
    "사망원인순위",
    "사망원인",
    "사망자수",
    "사망률"
]

df["사망자수"] = pd.to_numeric(
    df["사망자수"],
    errors="coerce"
)

df = df.dropna(subset=["사망자수"])

# ----------------------
# 연령 선택
# ----------------------
ages = sorted(df["연령대별"].unique())

selected_age = st.selectbox(
    "연령대를 선택하세요",
    ages
)

# ----------------------
# 필터링
# ----------------------
filtered = df[
    df["연령대별"] == selected_age
].copy()

filtered = filtered.sort_values(
    "사망자수",
    ascending=False
)

# ----------------------
# 표
# ----------------------
st.dataframe(
    filtered[["사망원인", "사망자수"]],
    use_container_width=True
)

# ----------------------
# 그래프
# ----------------------
fig, ax = plt.subplots(figsize=(14, 7))

fig.patch.set_facecolor("#f2f2f2")
ax.set_facecolor("#f2f2f2")

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
