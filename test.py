import streamlit as st
import random

st.set_page_config(page_title="가상 동물 키우기", page_icon="🐾")

# 세션 상태 초기화
if "pet" not in st.session_state:
    st.session_state.pet = None
    st.session_state.hunger = 50
    st.session_state.happiness = 50
    st.session_state.level = 1

# 동물 이미지 매핑
pet_images = {
    "강아지 🐕": "https://cdn.pixabay.com/photo/2016/02/19/11/53/dog-1209621_1280.png",
    "고양이 🐈": "https://cdn.pixabay.com/photo/2017/01/06/19/15/cat-1956597_1280.png",
    "토끼 🐇": "https://cdn.pixabay.com/photo/2018/01/15/07/51/rabbit-3089962_1280.png",
    "햄스터 🐹": "https://cdn.pixabay.com/photo/2017/09/05/18/42/hamster-2716986_1280.png",
    "카피바라 🦦": "https://cdn.pixabay.com/photo/2022/03/21/11/05/capybara-7083607_1280.png",
    "도마뱀 🦎": "https://cdn.pixabay.com/photo/2018/06/14/13/21/lizard-3474913_1280.png"
}

st.title("🐾 가상 동물 키우기 게임 🐾")

# 동물 선택
if st.session_state.pet is None:
    st.subheader("당신의 첫 번째 동물을 선택하세요!")
    choice = st.radio(
        "어떤 동물을 키울까요?",
        list(pet_images.keys())
    )
    if st.button("선택하기"):
        st.session_state.pet = choice
        st.success(f"{choice}를(을) 입양했습니다! 잘 키워주세요 ❤️")
else:
    st.subheader(f"내 동물: {st.session_state.pet}")
    
    # 동물 이미지 출력
    st.image(pet_images[st.session_state.pet], width=250)

    st.write(f"레벨: {st.session_state.level}")
    st.progress(st.session_state.happiness / 100)
    st.caption(f"행복도: {st.session_state.happiness}")
    st.progress(st.session_state.hunger / 100)
    st.caption(f"배고픔: {st.session_state.hunger}")

    # 행동 버튼
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🍖 먹이 주기"):
            st.session_state.hunger = max(0, st.session_state.hunger - 20)
            st.session_state.happiness += 5
    with col2:
        if st.button("🎾 놀아주기"):
            st.session_state.happiness = min(100, st.session_state.happiness + 20)
            st.session_state.hunger += 10
    with col3:
        if st.button("💤 쉬게 하기"):
            st.session_state.hunger += 5
            st.session_state.happiness = max(0, st.session_state.happiness - 5)

    # 랜덤 이벤트
    if random.random() < 0.2:  # 20% 확률 이벤트
        st.warning("🌟 동물이 특별한 행동을 했습니다! 행복도가 +10")
        st.session_state.happiness = min(100, st.session_state.happiness + 10)

    # 레벨업 조건
    if st.session_state.happiness >= 80 and st.session_state.hunger <= 20:
        st.session_state.level += 1
        st.session_state.happiness = 50
        st.session_state.hunger = 50
        st.success("🎉 레벨 업! 동물이 더 건강하게 성장했습니다!")

    # 상태 체크
    if st.session_state.hunger >= 100:
        st.error("😢 동물이 너무 배고파서 쓰러졌습니다... 다시 시작하세요.")
        st.session_state.pet = None
        st.session_state.hunger = 50
        st.session_state.happiness = 50
        st.session_state.level = 1

