# MBTI 진로 추천 Streamlit 코드


import streamlit as st

st.set_page_config(page_title="MBTI 진로 추천", page_icon="✨")

st.title("✨ MBTI 진로 추천 서비스 ✨")
st.write("MBTI를 선택하면 어울리는 진로와 학과를 추천해줄게 😎")

mbti_data = {
    "INTJ": [
        {
            "job": "🧠 데이터 분석가",
            "major": "컴퓨터공학과, 통계학과",
            "personality": "논리적이고 분석적인 사람에게 잘 맞아!",
            "salary": "평균 연봉 약 5,000만원"
        },
        {
            "job": "📚 연구원",
            "major": "자연과학계열, 생명과학과",
            "personality": "혼자 깊게 탐구하는 걸 좋아하면 추천!",
            "salary": "평균 연봉 약 4,500만원"
        }
    ],

    "INTP": [
        {
            "job": "💻 프로그래머",
            "major": "소프트웨어학과, 컴퓨터공학과",
            "personality": "창의적이고 문제 해결을 좋아하는 성격에 딱!",
            "salary": "평균 연봉 약 5,200만원"
        },
        {
            "job": "🔬 과학자",
            "major": "물리학과, 화학과",
            "personality": "새로운 이론과 아이디어를 좋아하면 잘 맞아!",
            "salary": "평균 연봉 약 4,800만원"
        }
    ],

    "ENTJ": [
        {
            "job": "🏢 기업 CEO",
            "major": "경영학과, 경제학과",
            "personality": "리더십 강하고 목표 지향적인 사람 추천!",
            "salary": "평균 연봉 약 7,000만원"
        },
        {
            "job": "📈 마케팅 기획자",
            "major": "광고홍보학과, 경영학과",
            "personality": "전략 세우는 걸 좋아하면 잘 맞아 😎",
            "salary": "평균 연봉 약 4,600만원"
        }
    ],

    "ENTP": [
        {
            "job": "🎤 크리에이터",
            "major": "미디어학과, 방송연예과",
            "personality": "아이디어 많고 도전 좋아하면 추천!",
            "salary": "평균 연봉 약 4,000만원 이상"
        },
        {
            "job": "🚀 스타트업 창업가",
            "major": "경영학과, 창업학과",
            "personality": "새로운 걸 시도하는 걸 좋아하면 찰떡!",
            "salary": "수익 차이가 큰 편 💸"
        }
    ],

    "INFJ": [
        {
            "job": "🩺 상담사",
            "major": "심리학과, 상담학과",
            "personality": "공감 능력 좋고 배려심 많다면 추천!",
            "salary": "평균 연봉 약 4,200만원"
        },
        {
            "job": "✍️ 작가",
            "major": "문예창작과, 국문학과",
            "personality": "감수성이 풍부한 사람에게 잘 맞아 📖",
            "salary": "수입 차이가 큰 편"
        }
    ],

    "INFP": [
        {
            "job": "🎨 일러스트레이터",
            "major": "시각디자인과, 애니메이션학과",
            "personality": "상상력 풍부하고 감성적인 성격 추천!",
            "salary": "평균 연봉 약 3,800만원"
        },
        {
            "job": "🎵 음악 프로듀서",
            "major": "실용음악과",
            "personality": "예술 감각이 뛰어나면 잘 맞아 🎧",
            "salary": "수입 차이가 큰 편"
        }
    ],

    "ENFJ": [
        {
            "job": "👩‍🏫 교사",
            "major": "교육학과, 국어교육과",
            "personality": "사람 도와주는 걸 좋아하면 추천!",
            "salary": "평균 연봉 약 4,700만원"
        },
        {
            "job": "🤝 인사담당자",
            "major": "경영학과, 심리학과",
            "personality": "소통 능력이 뛰어난 사람에게 딱!",
            "salary": "평균 연봉 약 4,500만원"
        }
    ],

    "ENFP": [
        {
            "job": "📱 콘텐츠 기획자",
            "major": "미디어학과, 광고홍보학과",
            "personality": "트렌드에 민감하고 밝은 성격 추천 😆",
            "salary": "평균 연봉 약 4,300만원"
        },
        {
            "job": "✈️ 여행 기획자",
            "major": "관광학과",
            "personality": "활동적이고 자유로운 성격이면 잘 맞아!",
            "salary": "평균 연봉 약 3,900만원"
        }
    ],

    "ISTJ": [
        {
            "job": "🏛️ 공무원",
            "major": "행정학과, 법학과",
            "personality": "책임감 강하고 꼼꼼한 사람 추천!",
            "salary": "평균 연봉 약 4,500만원"
        },
        {
            "job": "📊 회계사",
            "major": "회계학과, 경영학과",
            "personality": "숫자 다루는 걸 좋아하면 잘 맞아 💡",
            "salary": "평균 연봉 약 6,000만원"
        }
    ],

    "ISFJ": [
        {
            "job": "🏥 간호사",
            "major": "간호학과",
            "personality": "배려심 많고 책임감 있는 사람 추천!",
            "salary": "평균 연봉 약 4,600만원"
        },
        {
            "job": "👶 유치원 교사",
            "major": "유아교육과",
            "personality": "아이들을 좋아하면 잘 맞아 😊",
            "salary": "평균 연봉 약 3,700만원"
        }
    ],

    "ESTJ": [
        {
            "job": "⚖️ 경찰관",
            "major": "경찰행정학과",
            "personality": "리더십 있고 정의감 강하면 추천!",
            "salary": "평균 연봉 약 5,000만원"
        },
        {
            "job": "🏦 은행원",
            "major": "금융학과, 경제학과",
            "personality": "체계적인 성격이면 잘 맞아 💰",
            "salary": "평균 연봉 약 5,200만원"
        }
    ],

    "ESFJ": [
        {
            "job": "💄 승무원",
            "major": "항공서비스학과",
            "personality": "친절하고 사람 만나는 걸 좋아하면 추천!",
            "salary": "평균 연봉 약 4,500만원"
        },
        {
            "job": "🎉 이벤트 플래너",
            "major": "관광경영학과, 이벤트학과",
            "personality": "활발하고 사교적인 성격 추천 😄",
            "salary": "평균 연봉 약 4,000만원"
        }
    ],

    "ISTP": [
        {
            "job": "🔧 자동차 엔지니어",
            "major": "기계공학과, 자동차공학과",
            "personality": "손으로 만드는 걸 좋아하면 추천!",
            "salary": "평균 연봉 약 5,500만원"
        },
        {
            "job": "🎮 게임 개발자",
            "major": "게임공학과, 소프트웨어학과",
            "personality": "문제 해결 능력이 뛰어난 사람에게 딱!",
            "salary": "평균 연봉 약 5,000만원"
        }
    ],

    "ISFP": [
        {
            "job": "📸 사진작가",
            "major": "사진영상학과",
            "personality": "감각적이고 자유로운 성격 추천!",
            "salary": "수입 차이가 큰 편"
        },
        {
            "job": "🧵 패션 디자이너",
            "major": "패션디자인학과",
            "personality": "예술 감각 뛰어나면 잘 맞아 👗",
            "salary": "평균 연봉 약 4,200만원"
        }
    ],

    "ESTP": [
        {
            "job": "🏀 스포츠 트레이너",
            "major": "체육학과",
            "personality": "활동적이고 에너지 넘치면 추천!",
            "salary": "평균 연봉 약 4,000만원"
        },
        {
            "job": "💼 영업 전문가",
            "major": "경영학과",
            "personality": "사람 설득하는 걸 잘하면 잘 맞아 😎",
            "salary": "평균 연봉 약 5,000만원"
        }
    ],

    "ESFP": [
        {
            "job": "🎬 배우",
            "major": "연극영화과",
            "personality": "끼 많고 표현력 좋은 사람 추천!",
            "salary": "수입 차이가 큰 편 🎭"
        },
        {
            "job": "🎤 방송인",
            "major": "방송연예과, 미디어학과",
            "personality": "사람들 앞에서 말하는 걸 좋아하면 딱!",
            "salary": "평균 연봉 약 4,500만원 이상"
        }
    ]
}

mbti = st.selectbox(
    "🧐 너의 MBTI를 선택해줘!",
    list(mbti_data.keys())
)

if st.button("✨ 진로 추천 보기 ✨"):
    st.subheader(f"💖 {mbti} 유형 추천 진로 💖")

    careers = mbti_data[mbti]

    for career in careers:
        st.markdown("---")
        st.markdown(f"## {career['job']}")
        st.write(f"🎓 추천 학과 : {career['major']}")
        st.write(f"🌟 잘 맞는 성격 : {career['personality']}")
        st.write(f"💰 평균 연봉 : {career['salary']}")

    st.success("✨ 미래의 멋진 모습을 응원할게! ✨")


