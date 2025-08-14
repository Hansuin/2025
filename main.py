import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="MBTI 직업 추천", page_icon="💼", layout="centered")

# 제목
st.title("💼 MBTI 기반 직업 추천")
st.write("MBTI를 선택하면 해당 성향에 맞는 직업을 추천해드립니다.")

# MBTI별 추천 직업 데이터
mbti_jobs = {
    "INTJ": [
        {"name": "데이터 분석가", "desc": "논리적이고 전략적인 분석 업무에 적합합니다.", "img": "https://via.placeholder.com/150"},
        {"name": "전략 기획자", "desc": "미래를 내다보고 장기 계획을 세우는 역할에 강점이 있습니다.", "img": "https://via.placeholder.com/150"},
        {"name": "연구원", "desc": "깊이 있는 탐구와 문제 해결 능력을 발휘할 수 있습니다.", "img": "https://via.placeholder.com/150"}
    ],
    "ENTP": [
        {"name": "창업가", "desc": "새로운 아이디어를 실행에 옮기고 도전을 즐깁니다.", "img": "https://via.placeholder.com/150"},
        {"name": "마케팅 전문가", "desc": "창의적 사고와 설득력이 필요한 분야입니다.", "img": "https://via.placeholder.com/150"},
        {"name": "광고 기획자", "desc": "다양한 캠페인을 기획하고 홍보 전략을 세웁니다.", "img": "https://via.placeholder.com/150"}
    ],
    "INFJ": [
        {"name": "상담가", "desc": "타인의 감정을 잘 이해하고 돕는 데 능숙합니다.", "img": "https://via.placeholder.com/150"},
        {"name": "작가", "desc": "깊이 있는 통찰과 감성을 글로 표현할 수 있습니다.", "img": "https://via.placeholder.com/150"},
        {"name": "심리학자", "desc": "사람의 마음과 행동을 연구하는 직업입니다.", "img": "https://via.placeholder.com/150"}
    ],
    "ESFP": [
        {"name": "배우", "desc": "무대와 사람들 앞에서 빛나는 에너지를 발휘합니다.", "img": "https://via.placeholder.com/150"},
        {"name": "이벤트 기획자", "desc": "다양한 행사와 파티를 기획하고 실행합니다.", "img": "https://via.placeholder.com/150"},
        {"name": "홍보 담당자", "desc": "대중과 소통하며 브랜드 이미지를 관리합니다.", "img": "https://via.placeholder.com/150"}
    ]
}

# MBTI 선택
mbti_list = list(mbti_jobs.keys())
selected_mbti = st.selectbox("당신의 MBTI를 선택하세요", mbti_list)

# 버튼 클릭 시 결과 표시
if st.button("추천 직업 보기"):
    st.subheader(f"{selected_mbti} 유형 추천 직업")
    for job in mbti_jobs[selected_mbti]:
        st.image(job["img"], width=150)
        st.markdown(f"**{job['name']}**")
        st.write(job["desc"])
        st.write("---")

