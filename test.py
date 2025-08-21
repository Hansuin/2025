import streamlit as st
import requests
import random

# 페이지 설정
st.set_page_config(page_title="영어 단어 학습", page_icon="📚", layout="centered")

st.title("📚 영어 단어 학습 (모든 단어 지원)")
st.write("단어를 입력하면 발음, 뜻, 예문을 보여주고, 퀴즈로 확인 학습할 수 있습니다!")

# 단어 입력
word = st.text_input("학습할 영어 단어를 입력하세요", "").lower()

if word:
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    res = requests.get(url)

    if res.status_code == 200:
        data = res.json()[0]

        # 발음
        phonetic = data.get("phonetic", "발음 없음")

        # 뜻
        meanings = data["meanings"]
        meaning_list = []
        for m in meanings:
            for d in m["definitions"]:
                meaning_list.append(d["definition"])
        meaning = meaning_list[0] if meaning_list else "뜻 없음"

        # 예문 (없으면 기본 문장 생성)
        examples = [d.get("example") for m in meanings for d in m["definitions"] if "example" in d]
        example = examples[0] if examples else f"I like to use the word **{word}** in a sentence."

        # 출력
        st.subheader(f"🔤 {word}")
        st.write(f"발음: /{phonetic}/")
        st.write(f"뜻: {meaning}")

        st.subheader("📖 예문")
        st.write(example)

        # 퀴즈
        st.subheader("📝 확인 학습")
        quiz_sentence = example.replace(word, "_____") if word in example else f"I like to study _____ every day."
        st.write(quiz_sentence)

        answer = st.text_input("정답 입력", "")

        if st.button("정답 확인"):
            if answer.strip().lower() == word:
                st.success("정답입니다! 🎉")
            else:
                st.error(f"오답입니다. 정답은 '{word}' 입니다.")
    else:
        st.error("❌ 단어를 찾을 수 없습니다. 다시 입력해주세요.")
