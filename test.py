import streamlit as st
import openai

# 🔑 OpenAI API 키 설정 (환경변수나 secrets.toml 사용 권장)
openai.api_key = "YOUR_API_KEY"

st.set_page_config(page_title="AI 추천 서비스", page_icon="🎬", layout="centered")

st.title("🎯 AI 기반 추천 서비스")
st.write("원하는 취향을 입력하면 AI가 맞춤 추천을 해드립니다!")

# ---------------- 사용자 입력 ----------------
category = st.selectbox(
    "추천받고 싶은 카테고리를 선택하세요",
    ["영화", "책", "음악"]
)

preference = st.text_area(
    f"어떤 {category}을(를) 원하시나요? (예: 스릴러 영화, 자기계발서, 잔잔한 재즈 음악)"
)

# ---------------- 추천 버튼 ----------------
if st.button("추천 받기"):
    if preference.strip() == "":
        st.warning("취향을 입력해주세요!")
    else:
        with st.spinner("추천을 생성 중입니다..."):
            prompt = f"사용자의 취향에 맞는 {category} 5개를 추천해줘. 각 항목은 간단한 설명과 함께 제공해."
            
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",  # 속도/비용 고려
                messages=[
                    {"role": "system", "content": "당신은 추천 전문가입니다."},
                    {"role": "user", "content": f"{prompt}\n취향: {preference}"}
                ],
                temperature=0.7
            )

            result = response.choices[0].message["content"]
            st.subheader("✨ 추천 결과")
            st.write(result)

# ---------------- 추가 기능 ----------------
st.markdown("---")
st.info("Tip: 추천받은 결과를 저장하거나 카테고리를 바꿔가며 여러 번 시도해 보세요!")

