import streamlit as st
from openai import OpenAI

# ✅ OpenAI 클라이언트 초기화 (secrets.toml에서 API 키 불러오기)
# .streamlit/secrets.toml 파일 안에 아래처럼 작성하세요:
# OPENAI_API_KEY = "sk-본인_API키"
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---------------- 페이지 기본 설정 ----------------
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
            try:
                prompt = f"사용자의 취향에 맞는 {category} 5개를 추천해줘. 각 항목은 간단한 설명과 함께 제공해."

                response = client.chat.completions.create(
                    model="gpt-4o-mini",  # 빠르고 저렴한 모델
                    messages=[
                        {"role": "system", "content": "당신은 추천 전문가입니다."},
                        {"role": "user", "content": f"{prompt}\n취향: {preference}"}
                    ],
                    temperature=0.7
                )

                result = response.choices[0].message.content
                st.subheader("✨ 추천 결과")
                st.write(result)

            except Exception as e:
                st.error("추천 생성 중 오류가 발생했습니다. API 키를 확인해주세요.")
                st.exception(e)

# ---------------- 추가 안내 ----------------
st.markdown("---")
st.info("Tip: 카테고리를 바꿔가며 여러 번 시도해 보세요!")

