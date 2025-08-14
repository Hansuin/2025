import streamlit as st
import random
from datetime import date

# 페이지 설정
st.set_page_config(page_title="운명 궁합 테스트", page_icon="🔮", layout="centered")

st.title("🔮 운명 궁합 테스트")
st.write("이름과 생일을 입력하면 당신과 상대방의 궁합을 확인해드립니다!")

# 사용자 입력
col1, col2 = st.columns(2)
with col1:
    my_name = st.text_input("당신의 이름", "")
    my_birthday = st.date_input("당신의 생일", value=date(2000, 1, 1))
with col2:
    partner_name = st.text_input("상대방 이름", "")
    partner_birthday = st.date_input("상대방 생일", value=date(2000, 1, 1))

# 궁합 설명 데이터
compat_desc = [
    "천생연분, 운명적인 인연 💖",
    "서로를 잘 이해하는 베스트 파트너 😊",
    "성향이 달라 자극을 주는 관계 ⚡",
    "서로에게 배우며 성장하는 관계 🌱",
    "노력하면 좋은 인연이 될 수 있어요 🌟"
]

# 궁합 계산 함수 (간단한 랜덤 기반)
def calculate_compatibility(name1, birth1, name2, birth2):
    seed_value = sum(ord(c) for c in (name1 + name2)) + birth1.year + birth2.year
    random.seed(seed_value)
    score = random.randint(50, 100)
    desc = random.choice(compat_desc)
    return score, desc

# 버튼 클릭 시 결과 표시
if st.button("궁합 보기"):
    if my_name and partner_name:
        score, desc = calculate_compatibility(my_name, my_birthday, partner_name, partner_birthday)
        st.subheader(f"{my_name} ❤️ {partner_name}")
        st.metric(label="궁합 점수", value=f"{score}점")
        st.write(desc)
        st.progress(score / 100)
    else:
        st.warning("이름을 모두 입력해주세요!")

