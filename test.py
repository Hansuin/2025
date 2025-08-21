import streamlit as st
import random

# 예시 단어 데이터 (실제로는 사전 API 연결 가능)
word_data = {
    "apple": {
        "pron": "ˈæp.əl",
        "meaning": "사과",
        "examples": [
            "I ate an **apple** this morning.",
            "She bought some fresh **apples** from the market."
        ]
    },
    "run": {
        "pron": "rʌn",
        "meaning": "달리다",
        "examples": [
            "I usually **run** in the park every morning.",
            "He can **run** faster than anyone in his class."
        ]
    },
    "book": {
        "pron": "bʊk",
        "meaning": "책",
        "examples": [
            "I borrowed a **book** from the library.",
            "She is reading a new **book** about history."
        ]
    },
}

# 페이지 설정
st.set_page_config(page_title="영어 단어 학습", page_icon="📚", layout="centered")

st.title("📚 영어 단어 학습 웹")
st.write("단어를 입력하면 발음, 뜻, 예문을 보여주고, 퀴즈로 확인 학습할 수 있습니다!")

# 단어 입력
word = st.text_input("학습할 영어 단어를 입력하세요", "").lower()

if word:
    if word in word_data:
        info = word_data[word]

        # 발음 / 뜻
        st.subheader(f"🔤 {word}")
        st.write(f"발음: /{info['pron']}/")
        st.write(f"뜻: {info['meaning']}")

        # 예문
        st.subheader("📖 예문")
        for ex in info["examples"]:
            st.write(ex)

        # 퀴즈
        st.subheader("📝 확인 학습")
        quiz_sentence = random.choice(info["examples"])
        quiz_sentence_blank = quiz_sentence.replace(f"**{word}**", "_____")

        st.write("다음 문장에서 빈칸에 들어갈 단어는?")
        st.write(quiz_sentence_blank)

        answer = st.text_input("정답 입력", "")

        if st.button("정답 확인"):
            if answer.strip().lower() == word:
                st.success("정답입니다! 🎉")
            else:
                st.error(f"오답입니다. 정답은 '{word}' 입니다.")
    else:
        st.warning("단어 데이터베이스에 없습니다. (확장 필요)")
