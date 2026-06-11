import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="사망원인 통계 대시보드", layout="wide")

st.title("📊 연령대별 사망원인 순위 데이터 분석")
st.caption("제공된 사망원인 통계 데이터를 기반으로 시각화한 대시보드입니다.")

# 데이터 불러오기 함수
@st.cache_data
def load_data():
    # CSV 파일을 읽어옵니다.
    df = pd.read_csv("hhhh.csv")
    
    # 헤더 중복 행 제거 (데이터 내부에 컬럼명이 한 번 더 들어가 있는 경우 처리)
    df = df[df['성별'] != '성별']
    
    # 숫자형 데이터 변환 및 결측치 처리
    df['사망자수(명)'] = pd.to_numeric(df['사망자수(명)'].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
    df['사망률(십만명당)'] = pd.to_numeric(df['사망률(십만명당)'].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
    
    return df

try:
    df = load_data()

    # 사이드바 1: 성별 선택
    gender_list = sorted(df['성별'].unique())
    # '계'를 기본값으로 설정하기 위한 인덱스 찾기
    default_gender_idx = gender_list.index('계') if '계' in gender_list else 0
    selected_gender = st.sidebar.selectbox("👤 성별을 선택하세요", gender_list, index=default_gender_idx)

    # 사이드바 2: 연령대 선택
    # 선택된 성별의 데이터만 먼저 필터링
    df_gender = df[df['성별'] == selected_gender]
    age_list = df_gender['연령대별'].unique().tolist()
    
    # '전체'를 기본값으로 설정하기 위한 인덱스 찾기
    default_age_idx = age_list.index('전체') if '전체' in age_list else 0
    selected_age = st.sidebar.selectbox("🎂 연령대를 선택하세요", age_list, index=default_age_idx)

    # 최종 필터링 데이터
    filtered_df = df_gender[df_gender['연령대별'] == selected_age]

    # 조건 2: 사망원인이 높은 것(사망자수 내림차순)을 왼쪽에서 오른쪽으로 정렬
    filtered_df = filtered_df.sort_values(by='사망자수(명)', ascending=False)

    # 화면 레이아웃 구성
    st.subheader(f"📌 선택된 조건: [{selected_gender}] - [{selected_age}]")
    
    if not filtered_df.empty:
        # 데이터프레임 시각화 변환 (차트용 데이터 생성)
        # 꺾은선 그래프는 순서가 중요하므로 인덱스를 '사망원인'으로 지정
        chart_data = filtered_df.set_index('사망원인')[['사망자수(명)']]
        
        # 조건 3: 디자인 커스텀 (연한 회색 바탕, 검정색 꺾은선)
        # 스트림릿 내장 차트의 색상 매개변수(color)를 블랙('#000000')으로 지정합니다.
        st.markdown(
            """
            <style>
            /* 차트가 들어가는 컨테이너 영역의 배경을 연한 회색으로 변경 */
            [data-testid="stDataFrame_Native"], [data-testid="stArrowVegaLiteChart"] {
                background-color: #f0f2f6;
                padding: 15px;
                border-radius: 10px;
            }
            </style>
            """, 
            unsafe_allow_html=True
        )
        
        # 꺾은선 차트 출력 (한글 절대 깨지지 않음)
        st.write("📈 사망원인별 사망자수 추이 (왼쪽이 가장 높은 원인)")
        st.line_chart(chart_data, color="#000000")
        
        # 상세 데이터 테이블 출력
        st.write("📋 상세 데이터 목록")
        st.dataframe(
            filtered_df[['사망원인 순위', '사망원인', '사망자수(명)', '사망률(십만명당)']], 
            use_container_width=True,
            hide_index=True
        )
    else:
        st.warning("선택한 조건에 해당하는 데이터가 존재하지 않습니다.")

except FileNotFoundError:
    st.error("❌ `hhhh.csv` 파일을 찾을 수 없습니다. GitHub 저장소에 데이터 파일이 올바르게 업로드되었는지 확인해주세요.")
