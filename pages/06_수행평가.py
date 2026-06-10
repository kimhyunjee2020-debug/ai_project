import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import platform

# ----------------------
# 1. 시스템 기본 폰트를 활용한 한글 설정 (다운로드 없음)
# ----------------------
def set_korean_font():
    os_name = platform.system()
    
    if os_name == "Windows":
        plt.rcParams["font.family"] = "Malgun Gothic"
    elif os_name == "Darwin":
        plt.rcParams["font.family"] = "AppleGothic"
    else:
        # Streamlit Cloud (Linux) 환경 대응
        available_fonts = [f.name for f in fm.fontManager.ttflist]
        ko_font_candidates = [
            "NanumGothic", "NanumMyeongjo", "Noto Sans CJK KR", 
            "Liberation Sans", "DejaVu Sans", "sans-serif"
        ]
        for font in ko_font_candidates:
            if font in available_fonts:
                plt.rcParams["font.family"] = font
                break
                
    plt.rcParams["axes.unicode_minus"] = False

# 한글 설정 적용
set_korean_font()

# ----------------------
# 2. 페이지 설정
# ----------------------
st.set_page_config(
    page_title="연령별 사망원인 분석",
    page_icon="📊",
    layout="wide"
)

st.title("📊 2024 연령별 사망원인 분석")

# ----------------------
# 3. 데이터 읽기 및 전처리
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

# 숫자형 변환 및 결측치 제거
df["사망자수"] = pd.to_numeric(df["사망자수"], errors="coerce")
df = df.dropna(subset=["사망자수"])

# ----------------------
# 4. 연령 선택 필터
# ----------------------
ages = sorted(df["연령대별"].unique())
selected_age = st.selectbox("연령대를 선택하세요", ages)

# 데이터 필터링 및 합산/정렬
filtered = df[df["연령대별"] == selected_age].copy()
filtered = filtered.groupby("사망원인", as_index=False)["사망자수"].sum()
filtered = filtered.sort_values("사망자수", ascending=False)

# ----------------------
# 5. 화면 레이아웃 분할 (표 & 그래프)
# ----------------------
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📋 데이터 상세")
    st.dataframe(
        filtered[["사망원인", "사망자수"]],
        use_container_width=True,
        hide_index=True
    )

with col2:
    st.subheader("📈 시각화 차트")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("#f8f9fa")
    
    # 막대그래프 시각화
    bars = ax.bar(
        filtered["사망원인"],
        filtered["사망자수"],
        color="#4A90E2",
        edgecolor="none",
        width=0.6
    )
    
    # 막대 위에 숫자 표시
    for bar in bars:
        height = bar.get_height()
        ax.annotate(
            f"{int(height):,}",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9
        )
    
    # 축 및 제목 설정
    ax.set_title(f"[{selected_age}] 주요 사망원인 순위", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("사망원인", fontsize=11, labelpad=10)
    ax.set_ylabel("사망자 수 (명)", fontsize=11, labelpad=10)
    
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    
    st.pyplot(fig)
