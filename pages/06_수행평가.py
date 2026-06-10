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
# 데이터 읽기 및 전처리
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
# 사이드바 또는 상단 필터
# ----------------------
ages = sorted(df["연령대별"].unique())
selected_age = st.selectbox("연령대를 선택하세요", ages)

# ----------------------
# 데이터 필터링 (전체 성별 합산 등의 처리가 필요할 수 있어 그룹화 추가)
# ----------------------
# 데이터에 '남성', '여성'이 나뉘어 있다면 합산해주는 것이 그래프 그릴 때 정확합니다.
filtered = df[df["연령대별"] == selected_age].copy()

# 사망원인별로 합산 후 내림차순 정렬
filtered = filtered.groupby("사망원인", as_index=False)["사망자수"].sum()
filtered = filtered.sort_values("사망자수", ascending=False)

# 상위 10개만 보기 (원인이 너무 많으면 그래프가 복잡해지므로 선택 사항)
# filtered = filtered.head(10)

# ----------------------
# 레이아웃 분할 (표와 그래프를 나란히 배치)
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
    
    # 그래프 생성 (선 그래프에서 세련된 막대그래프로 변경)
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 깔끔한 배경색 설정을 위해 흰색 또는 투명으로 지정
    fig.patch.set_facecolor("white")
    ax.set_facecolor("#f8f9fa")
    
    # 막대그래프 그리기
    bars = ax.bar(
        filtered["사망원인"],
        filtered["사망자수"],
        color="#4A90E2",  # 차분한 블루 톤
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
            textcoords="offset points",
            ha='center',
            va='bottom',
            fontsize=9
        )
    
    ax.set_title(f"[{selected_age}] 주요 사망원인 순위", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("사망원인", fontsize=11, labelpad=10)
    ax.set_ylabel("사망자 수 (명)", fontsize=11, labelpad=10)
    
    # 테두리 정리 (위쪽, 오른쪽 선 없애기)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.xticks(rotation=45, ha='right')  # 회전각을 45도로 조절해 가독성 향상
    plt.tight_layout()
    
    st.pyplot(fig)
