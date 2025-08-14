import streamlit as st

# 페이지 설정
st.set_page_config(page_title="MBTI 궁합 테스트", page_icon="💖", layout="centered")

st.title("💖 MBTI 궁합 테스트")
st.write("당신과 상대방의 MBTI를 선택하고 궁합을 확인하세요!")

# MBTI 목록
mbti_types = [
    "ISTJ", "ISFJ", "INFJ", "INTJ",
    "ISTP", "ISFP", "INFP", "INTP",
    "ESTP", "ESFP", "ENFP", "ENTP",
    "ESTJ", "ESFJ", "ENFJ", "ENTJ"
]

# 예시 궁합 데이터 (일부)
compatibility_data = {
    ("ENFP", "INFJ"): {"score": 95, "desc": "서로의 장점을 잘 보완하는 이상적인 관계입니다."},
    ("INTJ", "ENTP"): {"score": 90, "desc": "지적 호기심이 맞아 떨어져 대화가 즐겁습니다."},
    ("ISFJ", "ESFP"): {"score": 88, "desc": "서로의 부족함을 채워주는 좋은 짝입니다."},
    ("ESTJ", "ISTJ"): {"score": 70, "desc": "가치관은 비슷하지만 다소 고집이 부딪칠 수 있습니다."},
}

# MBTI 선택
col1, col2 = st.columns(2)
with col1:
    my_mbti = st.selectbox("나의 MBTI", mbti_types, index=mbti_types.index("ENFP"))
with col2:
    partner_mbti = st.selectbox("상대방 MBTI", mbti_types, index=mbti_types.index("INFJ"))

# 궁합 보기 버튼
if st.button("궁합 보기"):
    # 키 만들기 (양방향 동일 처리)
    pair = (my_mbti, partner_mbti)
    reverse_pair = (partner_mbti, my_mbti)

    if pair in compatibility_data:
        result = compatibility_data[pair]
    elif reverse_pair in compatibility_data:
        result = compatibility_data[reverse_pair]
    else:
        # 데이터 없을 때 기본 결과
        result = {"score": 75, "desc": "무난한 관계이지만 서로 노력에 따라 달라집니다."}

    # 결과 출력
    st.subheader(f"{my_mbti} ❤️ {partner_mbti} 궁합 점수: {result['score']}점")
    st.write(result["desc"])
    st.progress(result["score"] / 100)


