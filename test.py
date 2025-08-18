import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io, requests, textwrap

st.set_page_config(page_title="AI 밈 생성기", page_icon="🖼️", layout="centered")

st.title("😂 AI 밈 생성기")
st.caption("이미지를 업로드하거나 템플릿을 선택해 텍스트를 얹어 밈을 만들어보세요. 한글 폰트가 필요하면 폰트 파일(.ttf)도 업로드하세요!")

# -----------------------
# 템플릿 정의 (저작권/출처 확인된 링크 사용 권장)
# -----------------------
TEMPLATES = {
    "없음(내 이미지 사용)": None,
    "Drake Hotline Bling": "https://upload.wikimedia.org/wikipedia/commons/7/76/Drake_Hotline_Bling_meme_template.jpg",
    "Distracted Boyfriend": "https://upload.wikimedia.org/wikipedia/commons/8/89/Distracted_boyfriend_meme.jpg",
    "Two Buttons": "https://upload.wikimedia.org/wikipedia/commons/2/2f/Two_buttons_meme_template.jpg",
    "Change My Mind": "https://upload.wikimedia.org/wikipedia/commons/0/0e/Change_My_Mind_meme_template.jpg",
}

# -----------------------
# 사이드바: 입력 UI
# -----------------------
with st.sidebar:
    st.header("설정")
    template_name = st.selectbox("템플릿", list(TEMPLATES.keys()), index=1)
    uploaded = st.file_uploader("내 이미지 업로드 (선택)", type=["png","jpg","jpeg","webp"]) 
    font_file = st.file_uploader("한글 폰트(.ttf) 업로드 (선택)", type=["ttf","otf"]) 

    st.subheader("텍스트")
    top_text = st.text_area("상단 텍스트", "위 텍스트", height=80)
    bottom_text = st.text_area("하단 텍스트", "아래 텍스트", height=80)

    st.subheader("스타일")
    font_size = st.slider("폰트 크기", 16, 120, 48)
    stroke = st.slider("외곽선 두께", 0, 8, 3)
    padding = st.slider("여백(%)", 0, 10, 3)
    align = st.selectbox("정렬", ["center","left","right"], index=0)
    uppercase = st.checkbox("대문자(영문)로 변환", value=True)
    watermark = st.text_input("워터마크(선택)", "")

    st.subheader("고급")
    top_y = st.slider("상단 텍스트 위치(높이 %)", 0, 40, 8)
    bottom_y = st.slider("하단 텍스트 위치(높이 %)", 60, 100, 92)

# -----------------------
# 이미지 로드
# -----------------------
@st.cache_data(show_spinner=False)
def load_image_from_url(url: str) -> Image.Image:
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    return Image.open(io.BytesIO(r.content)).convert("RGB")

if uploaded is not None:
    base_img = Image.open(uploaded).convert("RGB")
elif template_name and TEMPLATES[template_name]:
    base_img = load_image_from_url(TEMPLATES[template_name])
else:
    st.info("템플릿을 선택하거나 이미지를 업로드하세요.")
    st.stop()

# -----------------------
# 폰트 로드
# -----------------------
@st.cache_resource(show_spinner=False)
def get_default_font(size: int) -> ImageFont.FreeTypeFont:
    # 시스템에 따라 한글 지원 폰트가 다를 수 있음. Noto 또는 DejaVu 우선 시도.
    candidates = [
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansKR-Regular.otf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for p in candidates:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()

if font_file is not None:
    try:
        font = ImageFont.truetype(io.BytesIO(font_file.read()), font_size)
    except Exception:
        st.warning("업로드한 폰트를 불러오지 못했습니다. 기본 폰트를 사용합니다.")
        font = get_default_font(font_size)
else:
    font = get_default_font(font_size)

# -----------------------
# 텍스트 렌더링 함수
# -----------------------

def draw_multiline_centered(draw: ImageDraw.Draw, text: str, xy, w, font, align="center", stroke=3):
    if not text:
        return
    if uppercase:
        text = text.upper()
    # 가로폭에 맞춰 줄바꿈
    # 대충 폭 기준으로 단어 단위 wrap
    words = text.split()
    lines = []
    if not words:
        return
    # 이진 탐색 없이 간단히 점진 wrap
    line = words[0]
    for word in words[1:]:
        if draw.textlength(line + " " + word, font=font) <= w:
            line += " " + word
        else:
            lines.append(line)
            line = word
    lines.append(line)

    total_h = sum(draw.textbbox((0,0), l, font=font)[3] for l in lines) + (len(lines)-1)*4
    x, y = xy
    cur_y = y
    for l in lines:
        bbox = draw.textbbox((0,0), l, font=font)
        line_w = bbox[2]
        if align == "center":
            tx = x + (w - line_w)//2
        elif align == "left":
            tx = x
        else:  # right
            tx = x + (w - line_w)
        draw.text((tx, cur_y), l, fill="white", font=font, stroke_width=stroke, stroke_fill="black")
        cur_y += bbox[3] + 4

img = base_img.copy()
draw = ImageDraw.Draw(img)
W, H = img.size
pad_px = int(W * (padding/100))

# 상단 텍스트
draw_multiline_centered(
    draw,
    top_text,
    (pad_px, int(H * (top_y/100))),
    W - pad_px*2,
    font,
    align=align,
    stroke=stroke,
)

# 하단 텍스트
draw_multiline_centered(
    draw,
    bottom_text,
    (pad_px, int(H * (bottom_y/100))),
    W - pad_px*2,
    font,
    align=align,
    stroke=stroke,
)

# 워터마크(오른쪽 아래)
if watermark:
    wm_font = ImageFont.truetype(font.path, max(14, font_size//3)) if hasattr(font, 'path') else get_default_font(max(14, font_size//3))
    wm_bbox = draw.textbbox((0,0), watermark, font=wm_font)
    wm_x = W - wm_bbox[2] - 8
    wm_y = H - wm_bbox[3] - 6
    draw.text((wm_x, wm_y), watermark, fill=(255,255,255,180), font=wm_font, stroke_width=2, stroke_fill=(0,0,0,120))

st.image(img, caption="미리보기", use_column_width=True)

# 다운로드
buf = io.BytesIO()
img.save(buf, format="PNG")
bytes_data = buf.getvalue()
st.download_button(
    label="📥 PNG 다운로드",
    data=bytes_data,
    file_name="meme.png",
    mime="image/png",
)

with st.expander("도움말 / 라이선스 주의"):
    st.markdown(
        """
        - 상업적 사용 시 템플릿 이미지의 라이선스를 반드시 확인하세요.
        - 한글이 깨질 경우, 사이드바에서 **한글 폰트(.ttf)** 를 업로드하세요 (예: NotoSansKR-Regular.ttf).
        - 텍스트가 너무 길면 자동 줄바꿈됩니다. 여백(%)과 위치 슬라이더로 미세 조정해보세요.
        - 멀티 패널 밈(예: Drake)도 상/하 텍스트만으로 간단 제작 가능합니다.
        """
    )

