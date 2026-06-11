import streamlit as st
import pandas as pd

# 페이지 설정 (반드시 최상단에 위치해야 합니다)
st.set_page_config(page_title="사망원인 통계 대시보드", layout="wide")

st.title("📊 연령대별 사망원인 순위 데이터 분석")
st.caption("제공된 사망원인 통계 데이터를 기반으로 시각화한 대시보드입니다.")

# 데이터 불러오기 함수 (인코딩 에러 해결 버전)
@st.cache_data
def load_data():
    csv_file = "hhhh.csv"
    
    # 1단계: 가장 흔한 한국어 엑셀 인코딩인 cp949로 시도
    try:
        df = pd.read_csv(csv_file, encoding="cp949")
    except UnicodeDecodeError:
        # 2단계: 실패 시 대체 한국어 인코딩인 euc-kr로 시도
        try:
            df = pd.read_csv(csv_file, encoding="euc-kr")
        except UnicodeDecodeError:
            # 3단계: 둘 다 안 될 경우 일반 utf-8로 시도
            df = pd.read_csv(csv_file, encoding="utf-8")
    
    # 헤더 중복 행 제거 (데이터 내부에 컬럼명이 한 번 더 들어가 있는 경우 처리)
    df = df[df['성별'] != '성별']
    
    # 숫자형 데이터 변환 및 결측치 처리 (쉼표 제거 후 숫자로 변환)
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

    # 조건: 사망원인이 높은 것(사망자수 내림차순)을 왼쪽에서 오른쪽으로 정렬
    filtered_df = filtered_df.sort_values(by='사망자수(명)', ascending=False)

    # 화면 레이아웃 구성
    st.subheader(f"📌 선택된 조건: [{selected_gender}] - [{selected_age}]")
    
    if not filtered_df.empty:
        # 꺾은선 그래프는 순서가 중요하므로 인덱스를 '사망원인'으로 지정
        chart_data = filtered_df.set_index('사망원인')[['사망자수(명)']]
        
        # 조건: 디자인 커스텀 (연한 회색 바탕, 검정색 꺾은선)
        st.markdown(
            """
            <style>
            /* 차트 및 데이터프레임 컨테이너 배경을 연한 회색으로 변경 */
            [data-testid="stDataFrame_Native"], [data-testid="stArrowVegaLiteChart"] {
                background-color: #f0f2f6;
                padding: 15px;
                border-radius: 10px;
            }
            </style>
            """, 
            unsafe_allow_html=True
        )
        
        # 꺾은선 차트 출력 (브라우저 내장 폰트를 써서 한글 절대 깨지지 않음)
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
except Exception as e:
    st.error(f"❌ 데이터를 처리하는 과정에서 오류가 발생했습니다: {e}")
