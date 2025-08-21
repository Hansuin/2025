import streamlit as st
from openai import OpenAI

# ✅ OpenAI 클라이언트 초기화 (secrets.toml에서 API 키 불러오기)
# .streamlit/secrets.toml 파일 안에 아래처럼 작성하세요:
# OPENAI_API_KEY = "sk-본인_API키"
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---------------- 페이지 기본 설정 ----------------
st.set_page_config(page_title="AI 언어 학습 도우미", page_icon="📘", layout="centered")

st.title("📘 AI 언어 학습 도우미")
st.write("영어 단어나 문장을 입력하면 예문, 해석, 퀴즈를 제공합니다!")

# ---------------- 사용자 입력 ----------------
user_input = st.text_area("학습하고 싶은 영어 단어나 문장을 입력하세요:")

# ---------------- 학습 버튼 ----------------
if st.button("학습하기"):
    if user_input.strip() == "":
        st.warning("단어나 문장을 입력해주세요!")
    else:
        with st.spinner("학습 자료를 생성 중입니다..."):
            try:
                prompt = f"""
                사용자가 입력한 영어 단어나 문장을 학습할 수 있도록 다음을 생성해줘:
                1. 한국어 뜻
                2. 영어 예문 3개 (자연스럽게)
                3. 각 예문의 한국어 해석
                4. 간단한 빈칸 맞추기 퀴즈 2개 (정답 포함)
                입력: {user_input}
                """

                response = client.chat.completions.create(
                    model="gpt-4o-mini",  # 빠르고 저렴한 모델
                    messages=[
                        {"role": "system", "content": "당신은 영어 학습 도우미입니다."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7
                )

                result = response.choices[0].message.content
                st.subheader("✨ 학습 자료")
                st.write(result)

            except Exception as e:
                st.error("학습 자료 생성 중 오류가 발생했습니다. API 키를 확인해주세요.")
                st.exception(e)

# ---------------- 추가 안내 ----------------
st.markdown("---")
st.info("Tip: 짧은 문장을 입력하면 예문과 퀴즈가 더 깔끔하게 생성됩니다!")

