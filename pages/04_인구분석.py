import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------
# 페이지 설정
# -------------------
st.set_page_config(
    page_title="서울시 인구 분석",
    page_icon="📊",
    layout="wide"
)

st.title("📊 서울시 자치구별 연령대 인구 분석")

# -------------------
# CSV 불러오기
# -------------------
encodings = ["utf-8", "utf-8-sig", "cp949", "euc-kr"]

df = None

for enc in encodings:
    try:
        df = pd.read_csv("population.csv", encoding=enc)
        break
    except:
        continue

if df is None:
    st.error("population.csv 파일을 읽을 수 없습니다.")
    st.stop()

# -------------------
# 컬럼 설정
# -------------------
district_col = df.columns[0]

# 연령대 컬럼만 추출
age_columns = [
    col for col in df.columns
    if any(age in str(col) for age in [
        "0~9",
        "10~19",
        "20~29",
        "30~39",
        "40~49",
        "50~59",
        "60~69",
        "70~79",
        "80~89",
        "90~99",
        "100"
    ])
]

if len(age_columns) == 0:
    st.error("연령대 컬럼을 찾을 수 없습니다.")
    st.write(df.columns.tolist())
    st.stop()

# 숫자형 변환
for col in age_columns:
    df[col] = pd.to_numeric(
        df[col].astype(str).str.replace(",", ""),
        errors="coerce"
    )

# -------------------
# 탭 생성
# -------------------
tab1, tab2 = st.tabs([
    "🏙️ 행정구별 연령 분석",
    "👥 연령대별 행정구 분석"
])

# =====================================================
# TAB1
# 행정구 선택 → 연령대별 인구
# =====================================================
with tab1:

    st.subheader("🏙️ 행정구 선택")

    district = st.selectbox(
        "행정구를 선택하세요",
        df[district_col].unique()
    )

    row = df[df[district_col] == district].iloc[0]

    chart_df = pd.DataFrame({
        "연령대": age_columns,
        "인구수": [row[col] for col in age_columns]
    })

    fig = px.line(
        chart_df,
        x="연령대",
        y="인구수",
        markers=True
    )

    fig.update_layout(
        title=f"{district} 연령대별 인구수",
        plot_bgcolor="#f2f2f2",
        paper_bgcolor="#f2f2f2",
        font=dict(color="black"),
        height=600
    )

    fig.update_traces(
        line=dict(color="black", width=4)
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# TAB2
# 연령대 선택 → 행정구별 인구
# =====================================================
with tab2:

    st.subheader("👥 연령대 선택")

    selected_age = st.selectbox(
        "연령대를 선택하세요",
        age_columns
    )

    chart_df = df[[district_col, selected_age]].copy()

    chart_df = chart_df.sort_values(
        selected_age,
        ascending=False
    )

    fig = px.bar(
        chart_df,
        x=district_col,
        y=selected_age
    )

    fig.update_layout(
        title=f"{selected_age} 인구수 비교",
        plot_bgcolor="#f2f2f2",
        paper_bgcolor="#f2f2f2",
        font=dict(color="black"),
        height=600
    )

    fig.update_traces(
        marker_color="black"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    top_district = chart_df.iloc[0][district_col]
    top_population = int(chart_df.iloc[0][selected_age])

    st.success(
        f"🏆 {selected_age} 인구가 가장 많은 자치구: "
        f"{top_district} ({top_population:,}명)"
    )
