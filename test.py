import streamlit as st
import random
from PIL import Image
import requests
from io import BytesIO
File "/mount/src/2025/test.py", line 28, in <module>
    img = Image.open(BytesIO(response.content))
File "/home/adminuser/venv/lib/python3.13/site-packages/PIL/Image.py", line 3580, in open
    raise UnidentifiedImageError(msg)

st.set_page_config(page_title="가상 동물 키우기", page_icon="🐾", layout="centered")

st.title("🐾 가상 동물 키우기")

st.write("원하는 동물을 선택해서 키워보세요!")

# 동물 이미지 URL
animal_images = {
    "강아지": "https://cdn.pixabay.com/photo/2016/02/19/11/53/dog-1209621_1280.png",
    "고양이": "https://cdn.pixabay.com/photo/2017/11/09/21/41/cat-2934720_1280.png",
    "햄스터": "https://cdn.pixabay.com/photo/2020/04/06/16/34/hamster-5009129_1280.png",
    "카피바라": "https://cdn.pixabay.com/photo/2022/05/25/16/36/capybara-7221134_1280.png",
    "도마뱀": "https://cdn.pixabay.com/photo/2016/11/22/19/04/iguana-1852792_1280.jpg",
}

animal_choice = st.selectbox("키우고 싶은 동물을 선택하세요", list(animal_images.keys()))

# 선택된 동물 이미지 표시
if animal_choice:
    url = animal_images[animal_choice]
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    st.image(img, caption=f"{animal_choice}와 함께 놀아요!", use_column_width=True)

    st.subheader(f"{animal_choice} 상태")
    hunger = random.randint(0, 100)
    happiness = random.randint(0, 100)

    st.write(f"🍖 배고픔: {hunger}%")
    st.write(f"😊 행복도: {happiness}%")

    if st.button("밥 주기"):
        st.success(f"{animal_choice}가(이) 맛있게 밥을 먹었어요!")
    if st.button("놀아주기"):
        st.info(f"{animal_choice}가(이) 즐겁게 놀고 있어요!")

st.caption("© 재미용 가상 동물 키우기 · 이미지 출처: pixabay")

