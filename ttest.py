import streamlit as st
from datetime import date, datetime
from dataclasses import dataclass
from typing import Optional, Tuple

st.set_page_config(page_title="정밀 사주 궁합 & 오늘의 연애운", page_icon="💘", layout="centered")

# -----------------------------
# 기본 데이터 (천간/지지/오행)
# -----------------------------
STEMS = ["갑","을","병","정","무","기","경","신","임","계"]
BRANCHES = ["자","축","인","묘","진","사","오","미","신","유","술","해"]
STEM_ELEMENT = {
    "갑":"목","을":"목",
    "병":"화","정":"화",
    "무":"토","기":"토",
    "경":"금","신":"금",
    "임":"수","계":"수",
}
BRANCH_ELEMENT_PRIMARY = {
    "자":"수","축":"토","인":"목","묘":"목","진":"토","사":"화",
    "오":"화","미":"토","신":"금","유":"금","술":"토","해":"수",
}
FIVE_GEN = {
    ("목","화"): 15,
    ("화","토"): 15,
    ("토","금"): 15,
    ("금","수"): 15,
    ("수","목"): 15,
}
FIVE_CTRL = {
    ("목","토"): -15,
    ("토","수"): -15,
    ("수","화"): -15,
    ("화","금"): -15,
    ("금","목"): -15,
}

TRINE_GROUPS = [
    {"신","자","진"},
    {"인","오","술"},
    {"해","묘","미"},
    {"사","유","축"},
]
LiuHe = {
    ("자","축"), ("인","해"), ("묘","술"), ("진","유"), ("사","신"), ("오","미"),
}
Chong = {
    frozenset(("자","오")), frozenset(("축","미")), frozenset(("인","신")),
    frozenset(("묘","유")), frozenset(("진","술")), frozenset(("사","해")),
}

@dataclass
class Person:
    name: str
    birth: date
    sex: str
    year_stem: Optional[str] = None
    year_branch: Optional[str] = None
    year_element: Optional[str] = None
    month_branch: Optional[str] = None
    day_branch: Optional[str] = None
    hour_branch: Optional[str] = None

def approx_year_pillar(g: date) -> Tuple[str, str]:
    y = g.year
    if (g.month, g.day) < (2, 4):
        y -= 1
    stem = STEMS[(y - 4) % 10]
    branch = BRANCHES[(y - 4) % 12]
    return stem, branch

def approx_other_pillars(g: date) -> Tuple[str,str,str]:
    # 간단히 월지/일지/시지 추정 (정밀하지 않음)
    month_branch = BRANCHES[(g.month+1) % 12]
    day_branch = BRANCHES[(g.toordinal()) % 12]
    hour_branch = BRANCHES[((g.hour if isinstance(g, datetime) else 12)//2) % 12]
    return month_branch, day_branch, hour_branch

def five_relation_score(e1: str, e2: str) -> int:
    if (e1, e2) in FIVE_GEN:
        return FIVE_GEN[(e1, e2)]
    if (e2, e1) in FIVE_GEN:
        return FIVE_GEN[(e2, e1)]
    if (e1, e2) in FIVE_CTRL:
        return FIVE_CTRL[(e1, e2)]
    if (e2, e1) in FIVE_CTRL:
        return FIVE_CTRL[(e2, e1)]
    return 0

def branch_relation_score(b1: str, b2: str) -> int:
    score = 0
    for grp in TRINE_GROUPS:
        if b1 in grp and b2 in grp:
            score += 20
    if (b1, b2) in LiuHe or (b2, b1) in LiuHe:
        score += 12
    if frozenset((b1, b2)) in Chong:
        score -= 18
    return score

def compatibility_score(p1: Person, p2: Person) -> Tuple[int, dict]:
    details = {}
    e1 = STEM_ELEMENT.get(p1.year_stem, "")
    e2 = STEM_ELEMENT.get(p2.year_stem, "")
    elem_score = five_relation_score(e1, e2)
    details["오행(연간)"] = elem_score

    br_score = branch_relation_score(p1.year_branch, p2.year_branch)
    details["지지(연지)"] = br_score

    if e1 and e2 and e1 == e2:
        details["같은 오행 보정"] = 5
    else:
        details["같은 오행 보정"] = 0

    total = max(0, min(100, 50 + elem_score + br_score + details["같은 오행 보정"]))
    return total, details

WEEKDAY_BOOST = {0: 1, 1: 2, 2: 3, 3: 2, 4: 1, 5: 5, 6: 4}
MONTH_BRANCH = {
    1:"축", 2:"인", 3:"묘", 4:"진", 5:"사", 6:"오",
    7:"미", 8:"신", 9:"유", 10:"술", 11:"해", 12:"자"
}

def today_love_score(user: Person, today: date) -> Tuple[int, str]:
    t_branch = MONTH_BRANCH[today.month]
    base = 60
    base += branch_relation_score(user.year_branch, t_branch)
    base += WEEKDAY_BOOST[today.weekday()]
    base = max(0, min(100, base))

    if base >= 80:
        msg = "매우 좋은 흐름! 오늘은 적극적인 표현이 통합니다."
    elif base >= 65:
        msg = "무난하게 괜찮은 날. 대화 비중을 조금 더 늘려보세요."
    elif base >= 50:
        msg = "보통의 운세. 약속은 가볍게, 분위기는 편안하게."
    else:
        msg = "조심스러운 날. 오해가 생기기 쉬워요."
    return base, msg

def interpret_pillar(stem: str, branch: str, pillar_name: str="연주") -> str:
    elem = STEM_ELEMENT.get(stem, "")
    interp = f"당신의 {pillar_name}는 {stem}{branch}로, 오행은 {elem}에 속합니다. "
    if elem == "목":
        interp += "성장과 발전을 중시하며, 배움과 확장을 추구합니다."
    elif elem == "화":
        interp += "열정과 활력이 강하며, 표현력과 추진력이 돋보입니다."
    elif elem == "토":
        interp += "안정과 균형을 중시하며, 신뢰와 책임감이 강합니다."
    elif elem == "금":
        interp += "결단력과 의지가 강하며, 원칙과 정의를 중요시합니다."
    elif elem == "수":
        interp += "지혜롭고 유연하며, 적응력과 통찰력이 뛰어납니다."
    return interp

st.title("💘 사주 궁합 & 오늘의 연애운")

mode = st.radio("모드 선택", ["궁합 보기", "개인 사주 보기"])

colA, colB = st.columns(2)

def person_form(key_prefix: str) -> Person:
    with st.form(key=f"form_{key_prefix}"):
        name = st.text_input("이름", key=f"name_{key_prefix}")
        birth = st.date_input("생년월일", value=date(2000,1,1), key=f"birth_{key_prefix}")
        sex = st.selectbox("성별", ["남","여"], key=f"sex_{key_prefix}")
        submitted = st.form_submit_button("등록")

    p = Person(name=name or key_prefix, birth=birth, sex=sex)
    ys, yb = approx_year_pillar(birth)
    p.year_stem, p.year_branch = ys, yb
    p.year_element = STEM_ELEMENT[ys]
    mb, db, hb = approx_other_pillars(datetime.combine(birth, datetime.min.time()))
    p.month_branch, p.day_branch, p.hour_branch = mb, db, hb
    return p

if mode == "궁합 보기":
    with colA:
        st.subheader("A 상대")
        A = person_form("A")
    with colB:
        st.subheader("B 상대")
        B = person_form("B")

    if A and B and A.name and B.name:
        st.subheader("🔮 궁합 결과")
        score, detail = compatibility_score(A, B)
        st.metric(label="궁합 점수(0~100)", value=score)
        st.write(f"A 연주: {A.year_stem}{A.year_branch} (오행: {A.year_element})")
        st.write(f"B 연주: {B.year_stem}{B.year_branch} (오행: {B.year_element})")
        for k, v in detail.items():
            st.write(f"- {k}: {v:+d}")

        st.subheader("❤️ 오늘의 연애운")
        today = date.today()
        loveA, msgA = today_love_score(A, today)
        loveB, msgB = today_love_score(B, today)
        st.metric(f"{A.name} 오늘의 연애운", loveA)
        st.write(msgA)
        st.metric(f"{B.name} 오늘의 연애운", loveB)
        st.write(msgB)

elif mode == "개인 사주 보기":
    person = person_form("개인")
    if person and person.name:
        st.subheader(f"🔮 {person.name}님의 개인 사주")
        st.write(f"연주: {person.year_stem}{person.year_branch} (오행: {person.year_element})")
        st.write(interpret_pillar(person.year_stem, person.year_branch, "연주"))
        st.write(f"월지: {person.month_branch}")
        st.write(f"일지: {person.day_branch}")
        st.write(f"시지: {person.hour_branch}")
        st.write(interpret_pillar(person.year_stem, person.month_branch, "월주"))
        st.write(interpret_pillar(person.year_stem, person.day_branch, "일주"))
        st.write(interpret_pillar(person.year_stem, person.hour_branch, "시주"))

        today = date.today()
        love, msg = today_love_score(person, today)
        st.metric(f"오늘의 연애운", love)
        st.write(msg)

st.caption("© 사주 궁합 & 개인 사주 데모 · 교육/엔터테인먼트 용도")
