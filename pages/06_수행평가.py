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
        # 윈도우 기본 맑은 고딕
        plt.rcParams["font.family"] = "Malgun Gothic"
    elif os_name == "Darwin":
        # 맥OS 기본 애플 고딕
        plt.rcParams["font.family"] = "AppleGothic"
    else:
        # Streamlit Cloud (Linux) 및 기타 환경
        # 리눅스 서버에 기본 탑재된 나눔 또는 고딕 계열 폰트 자동 검색
        available_fonts = [f.name for f in fm.fontManager.ttflist]
        
        # 서버에 설치된 한글 지원 가능 폰트 후보들
        ko_font_candidates = [
            "NanumGothic", "NanumMyeongjo", "Noto Sans CJK KR", 
            "Liberation Sans", "DejaVu Sans", "sans-serif"
        ]
        
        for font in ko_font_candidates:
            if font in available_fonts:
                plt.rcParams["font.family"] = font
                break
                
    plt.rcParams["axes.unicode_minus"] = False  # 마이너스 부호 깨짐 방지

# 한글 설정 함수 실행
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

# 사망자수 숫자형 변환 및 결측치 제거
df["사망자수"] = pd.to_numeric(df["사망자수"], errors="coerce")
df = df.dropna(subset=["사망자수"])

# ----------------------
# 4. 연령 선택 필터
# ----------------------
ages = sorted(df["연령대별"].unique())
selected_age = st.selectbox("연령대를 선택하세요", ages)

# 선택된 연령대 데이터 필터링 후 사망원인별 합산 및 정렬
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
    
    # 그래프 생성 및 배경색 설정
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("#f8f9fa")
    
    # 막대그래프 시각화
    bars = ax.bar(
        filtered["사망원인"],
        filtered["사망자수"],
        color="#4A90E2",  # 깔끔한 블루 톤
        edgecolor="none",
        width=0.6
    )
    
    # 막대 위에 숫자 표시 (데이터 라벨링)
    for bar in bars:
        height = bar.get_height()
        ax.annotate(
            f'{int(height):,}',
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 3),  # 위로 3포인트 띄움
            text
