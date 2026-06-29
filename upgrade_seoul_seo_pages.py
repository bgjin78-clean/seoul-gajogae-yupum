from pathlib import Path
from datetime import date
import random

BASE_DOMAIN = "https://www.seoul.gajogae-yupum.com"
PHONE = "010-4720-3895"
MAIN_BANNER = f"{BASE_DOMAIN}/images/main/main-banner.png"

MAIN_BEFORE = list(range(1, 31))
MAIN_PROCESS = list(range(1, 26))
MAIN_AFTER = [n for n in range(1, 31) if n != 21]
CASES_MAX = 100

districts = [
    ("강남구", "gangnam", "아파트, 오피스텔, 빌라 등 주거 형태가 다양해 현장 구조에 맞춰 정리 범위 확인이 중요합니다.", "대단지 아파트와 오피스텔 비율이 높아 엘리베이터 예약, 주차 가능 여부, 폐기물 반출 동선을 먼저 확인하면 작업이 수월합니다."),
    ("강동구", "gangdong", "아파트 단지와 빌라, 주택이 함께 있어 공간 형태별 정리 범위 확인이 필요합니다.", "강동·송파·광진 인접 지역으로 일정 조율이 유연하며 엘리베이터와 주차 여부가 작업 시간에 영향을 줄 수 있습니다."),
    ("강북구", "gangbuk", "아파트와 다세대주택, 빌라 현장이 섞여 있어 층수와 운반 동선 확인이 중요합니다.", "노원·도봉·성북과 인접해 일정 조율이 가능하며 폐기물 양에 따라 차량과 인력을 조율합니다."),
    ("강서구", "gangseo", "대단지 아파트와 주택가가 함께 있어 물품 양과 폐기물 반출 방식에 따라 작업 범위가 달라질 수 있습니다.", "마곡·화곡·등촌 등 권역별 주거 형태가 달라 현장 주소와 관리 규정을 먼저 확인하는 것이 좋습니다."),
    ("관악구", "gwanak", "대학가 인근 원룸, 빌라, 아파트 등 주거 형태가 다양해 현장 확인 후 맞춤 정리 계획이 필요합니다.", "신림·봉천 등 밀집 주거지는 층수, 엘리베이터, 주차 공간이 작업 난이도에 영향을 줄 수 있습니다."),
    ("광진구", "gwangjin", "아파트와 오피스텔, 빌라가 함께 있어 보관품 확인, 서류 분류, 폐기물 이동 동선이 비용에 영향을 주는 경우가 많습니다.", "건대·자양·구의 등 역세권 주거지는 주차와 엘리베이터 사용 여부를 사전에 확인하면 작업이 수월합니다."),
    ("구로구", "guro", "아파트와 다세대주택, 상가형 공간이 함께 있어 물품 양과 폐기물 양에 따라 작업 인원이 달라질 수 있습니다.", "구로·금천·양천 인접 지역과 함께 상담되는 경우가 있어 일정 조율을 유연하게 안내합니다."),
    ("금천구", "geumcheon", "아파트와 빌라, 상가 겸용 공간이 함께 있어 정리 범위와 폐기물 양을 확인한 뒤 인력과 차량을 조율합니다.", "가산·독산 등 산업·주거 혼합 지역은 차량 진입과 폐기물 반출 동선 확인이 중요합니다."),
    ("노원구", "nowon", "대단지 아파트와 주택, 빌라가 함께 있어 엘리베이터, 주차, 폐기물 반출 조건을 확인합니다.", "상계·중계·하계 등 넓은 권역으로 나뉘어 현장 위치와 작업 일정 조율이 중요합니다."),
    ("도봉구", "dobong", "아파트와 주택 현장이 섞여 있어 물품 양과 폐기물 양에 따라 작업 방식이 달라질 수 있습니다.", "노원·강북·성북과 인접해 경기 북부 권역 일정 조율이 가능합니다."),
    ("동대문구", "dongdaemun", "아파트와 빌라, 다세대주택 밀집 지역이 많아 주차 가능 여부와 운반 동선 확인이 중요합니다.", "회기·이문·장안 등 구역별 주거 환경이 달라 현장 구조와 이동 동선을 확인한 뒤 정리 일정을 안내합니다."),
    ("동작구", "dongjak", "아파트, 빌라, 주택 등 주거 형태가 다양해 보관품과 폐기품을 먼저 구분하는 상담이 중요합니다.", "노량진·사당·흑석 등 역세권 주거지는 엘리베이터와 관리 규정 확인이 작업 시간에 영향을 줄 수 있습니다."),
    ("마포구", "mapo", "아파트, 오피스텔, 빌라 비율이 높아 보관품 확인, 서류 분류, 폐기물 이동 동선이 비용에 영향을 주는 경우가 많습니다.", "공덕·상암·연남 등 권역별 주거 형태가 달라 현장별 정리 기준을 먼저 확인하는 것이 좋습니다."),
    ("서대문구", "seodaemun", "아파트와 빌라, 주택 현장이 함께 있어 층수, 엘리베이터 여부, 주차 공간이 작업 시간에 영향을 줄 수 있습니다.", "신촌·연희·북아현 등 주거 밀집 지역은 폐기물 반출 시간과 운반 동선을 사전에 확인합니다."),
    ("서초구", "seocho", "대단지 아파트와 오피스텔, 빌라가 함께 있어 현장 구조에 맞춰 정리 범위 확인이 중요합니다.", "반포·방배·잠원 등 고층 아파트는 엘리베이터 예약과 관리 규정 확인이 작업 범위에 영향을 줄 수 있습니다."),
    ("성동구", "seongdong", "아파트와 빌라, 재개발·재건축 지역이 함께 있어 현장 상황별 유품정리 상담이 필요합니다.", "성수·왕십리·금호 등 역세권 주거지는 주차와 이동 동선이 중요해 현장 주소를 먼저 확인합니다."),
    ("성북구", "seongbuk", "아파트, 빌라, 주택, 원룸 등 주거 형태가 다양해 공간 형태에 따라 정리 방식이 달라질 수 있습니다.", "안암·정릉·길음 등 구역별 주거 환경이 달라 물품 양과 폐기물 양을 확인한 뒤 안내합니다."),
    ("송파구", "songpa", "대단지 아파트와 오피스텔 비율이 높아 엘리베이터 예약, 주차 가능 여부, 폐기물 반출 동선을 먼저 확인하면 작업이 수월합니다.", "잠실·문정·가락 등 권역별 주거 형태가 달라 현장 확인 후 맞춤 정리 계획이 필요합니다."),
    ("양천구", "yangcheon", "아파트와 빌라, 다세대주택이 함께 있어 층수와 엘리베이터 여부를 확인한 뒤 작업 방식을 안내합니다.", "목동·신정·신월 등 대단지 아파트는 관리 규정과 엘리베이터 예약 여부를 먼저 확인하는 것이 좋습니다."),
    ("영등포구", "yeongdeungpo", "아파트, 오피스텔, 빌라 현장이 많아 빠른 일정 상담 요청이 많은 편입니다.", "여의도·당산·대림 등 권역별 주거·업무 지역이 섞여 있어 현장 상황별 정리 범위 확인이 필요합니다."),
    ("용산구", "yongsan", "아파트, 오피스텔, 빌라, 주택 등 주거 형태가 다양해 현장 구조와 관리 규정 확인이 필요합니다.", "한남·이태원·용문 등 지역별 주거 환경이 달라 보관품과 폐기품을 먼저 구분하는 상담이 중요합니다."),
    ("은평구", "eunpyeong", "아파트와 주택, 빌라가 함께 있어 공간 규모와 폐기물 양을 먼저 확인한 뒤 작업 범위를 안내합니다.", "불광·응암·녹번 등 구역별 주거 형태가 달라 엘리베이터, 주차, 폐기물 반출 조건을 확인합니다."),
    ("종로구", "jongno", "아파트, 빌라, 주택, 한옥 등 주거 형태가 다양해 현장별 정리 기준을 먼저 확인하는 것이 좋습니다.", "혜화·삼청·평창 등 구역별 주거 환경이 달라 운반 동선과 폐기물 반출 방식에 따라 작업 난이도가 달라집니다."),
    ("중구", "jung", "아파트, 오피스텔, 빌라, 주택 등 도심형 주거지가 많아 주차와 이동 동선 확인이 중요합니다.", "명동·을지로·회현 등 중심 상권 인근 주거지는 관리 규정과 엘리베이터 사용 여부를 먼저 확인합니다."),
    ("중랑구", "jungnang", "아파트와 빌라, 주택 현장이 함께 있어 물품 양과 폐기물 양에 따라 작업 인원이 달라질 수 있습니다.", "면목·상봉·중화 등 구역별 주거 환경이 달라 현장 확인 후 정리 순서를 정하는 방식으로 진행합니다."),
]

nearby = {
    "강남구": ["서초구", "송파구", "광진구"],
    "강동구": ["송파구", "광진구", "성동구"],
    "강북구": ["노원구", "도봉구", "성북구"],
    "강서구": ["양천구", "마포구", "영등포구"],
    "관악구": ["동작구", "금천구", "구로구"],
    "광진구": ["성동구", "강동구", "송파구"],
    "구로구": ["금천구", "영등포구", "양천구"],
    "금천구": ["구로구", "관악구", "동작구"],
    "노원구": ["도봉구", "강북구", "성북구"],
    "도봉구": ["노원구", "강북구", "성북구"],
    "동대문구": ["성북구", "성동구", "중랑구"],
    "동작구": ["관악구", "영등포구", "서초구"],
    "마포구": ["서대문구", "용산구", "영등포구"],
    "서대문구": ["마포구", "은평구", "종로구"],
    "서초구": ["강남구", "동작구", "송파구"],
    "성동구": ["광진구", "동대문구", "용산구"],
    "성북구": ["강북구", "동대문구", "종로구"],
    "송파구": ["강남구", "강동구", "광진구"],
    "양천구": ["강서구", "구로구", "영등포구"],
    "영등포구": ["구로구", "동작구", "마포구"],
    "용산구": ["마포구", "성동구", "중구"],
    "은평구": ["서대문구", "종로구", "마포구"],
    "종로구": ["중구", "서대문구", "성북구"],
    "중구": ["종로구", "용산구", "성동구"],
    "중랑구": ["동대문구", "성북구", "노원구"],
}

slug_by_name = {name: slug for name, slug, *_ in districts}

case_items = [
    ("아파트", "대단지 아파트 유품정리", "보관할 물품 기준을 먼저 정한 뒤 서류와 사진, 귀중품을 확인하고 생활용품과 폐기물을 구분해 정리했습니다."),
    ("빌라·주택", "빌라 유품정리 및 폐기물 처리", "층수와 운반 동선을 확인한 뒤 가구와 생활폐기물을 분리하고, 마무리 단계에서 공간 상태를 다시 확인했습니다."),
    ("고독사청소", "고독사청소 포함 유품정리", "오염 범위와 악취 여부를 확인한 뒤 특수청소 필요 범위를 안내하고, 유품 분류와 폐기물 처리를 함께 진행했습니다."),
]

review_texts = [
    "중요 물품 기준을 먼저 정해 주셔서 가족과 상의하기 편했습니다. 정리 후 공간도 깔끔해졌습니다.",
    "물품이 많아 막막했는데 보관품과 폐기품을 구분해 주셔서 부담이 많이 줄었습니다.",
    "고독사청소가 필요한 상황이었는데 설명을 차근차근 해 주셔서 안심하고 맡길 수 있었습니다.",
    "서류와 사진, 귀중품을 따로 확인해 주셔서 큰 도움이 됐습니다. 일정 조율도 유연했습니다.",
    "폐기물처리까지 함께 상담할 수 있어서 한 번에 정리가 끝났습니다. 비용 안내도 명확했습니다.",
    "엘리베이터 사용이 어려운 현장이었는데 작업 순서를 잘 잡아 주셔서 무사히 마쳤습니다.",
]

faq_sets = [
    ("{name} 유품정리는 당일 상담이 가능한가요?", "예약 상황과 현장 위치에 따라 당일 상담 또는 빠른 일정 조율이 가능합니다."),
    ("{name} 고독사청소도 함께 가능한가요?", "가능합니다. 오염 범위와 악취, 소독 및 특수청소 필요 여부를 확인한 뒤 안내드립니다."),
    ("폐기물처리도 같이 신청할 수 있나요?", "가능합니다. 유품정리 과정에서 발생하는 생활폐기물과 가구, 잔짐까지 함께 상담 가능합니다."),
    ("가족이 현장에 꼭 있어야 하나요?", "중요 물품 기준을 정하기 위해 초기 상담 단계에서는 가족분과 협의하는 것이 좋습니다."),
    ("귀중품이나 서류는 어떻게 확인하나요?", "통장, 도장, 계약서, 사진, 귀금속 등은 별도로 확인해 가족분께 안내드립니다."),
]

BACKLINKS = '''<section id="backlinks" class="backlinkSection areaBox"><div class="container"><h2 class="sectionTitle">가족애 관련 서비스 바로가기</h2><p class="sectionLead">서울·경기 지역 유품정리와 폐기물처리 상담 사이트입니다.</p><div class="backlinkGrid">
          <a href="https://www.seoul.gajogae-yupum.com/" target="_blank" rel="noopener"><strong>서울유품정리</strong><span>서울 전지역 유품정리 · 고독사청소 상담</span></a>
          <a href="https://www.seoul.gajogae-waste.com/" target="_blank" rel="noopener"><strong>서울폐기물처리</strong><span>서울 전지역 폐기물처리 · 가정폐기물 상담</span></a>
          <a href="https://www.gyeonggi.gajogae-yupum.com/" target="_blank" rel="noopener"><strong>경기유품정리</strong><span>경기도 유품정리 · 특수청소 상담</span></a>
          <a href="https://www.gyeonggi.gajogae-waste.com/" target="_blank" rel="noopener"><strong>경기폐기물처리</strong><span>경기도 폐기물처리 · 이사폐기물 상담</span></a>
        </div></div></section>'''


def two(n):
    return f"{n:02d}"


def three(n):
    return f"{n:03d}"


def pick_main_gallery(idx, count=4):
    rng = random.Random(1000 + idx)
    return (
        rng.sample(MAIN_BEFORE, count),
        rng.sample(MAIN_PROCESS, count),
        rng.sample(MAIN_AFTER, count),
    )


def pick_case_images(idx, count=3):
    rng = random.Random(3000 + idx)
    pool = list(range(1, CASES_MAX + 1))
    return rng.sample(pool, count)


def gallery_imgs(nums, folder, prefix, name, phase):
    return "\n".join(
        f'            <img src="images/{folder}/{prefix}-{three(n) if folder == "cases" else two(n)}.jpg" alt="{name} 유품정리 {phase} 사진 {i + 1}">'
        for i, n in enumerate(nums)
    )


def case_grid_html(name, idx):
    imgs = pick_case_images(idx)
    cards = []
    for i, (label, title, desc) in enumerate(case_items):
        cards.append(
            f'''          <article class="caseCard">
            <img src="images/cases/before-{three(imgs[i])}.jpg" alt="{name} {label} 유품정리 작업 전">
            <div><span class="caseLabel">{name} · {label}</span><h3>{title}</h3><p>{desc}</p></div>
          </article>'''
        )
    return "\n".join(cards)


def review_grid_html(name, idx):
    rng = random.Random(4000 + idx)
    picks = rng.sample(review_texts, 3)
    cards = []
    for text in picks:
        cards.append(
            f'''          <article class="reviewCard"><div class="reviewStars">★★★★★</div><p>{text}</p><strong>{name} 고객님</strong></article>'''
        )
    return "\n".join(cards)


def area_links_html(name):
    items = []
    for n in nearby.get(name, [])[:3]:
        items.append(f'          <a href="{slug_by_name[n]}.html">{n} 유품정리</a>')
    items.append('          <a href="/">서울 유품정리 메인</a>')
    return "\n".join(items)


def faq_html(name, start):
    selected = [faq_sets[(start + i) % len(faq_sets)] for i in range(5)]
    return "\n".join(
        f'        <details{" open" if i == 0 else ""}><summary>{q.format(name=name)}</summary><p>{a}</p></details>'
        for i, (q, a) in enumerate(selected)
    )


def make_page(name, slug, feature, cost_note, idx):
    before_nums, process_nums, after_nums = pick_main_gallery(idx)
    before = "\n".join(
        f'            <img src="images/main/before-{two(n)}.jpg" alt="{name} 유품정리 작업 전 사진 {i + 1}">'
        for i, n in enumerate(before_nums)
    )
    process = "\n".join(
        f'            <img src="images/main/process-{two(n)}.jpg" alt="{name} 유품정리 작업 중 사진 {i + 1}">'
        for i, n in enumerate(process_nums)
    )
    after = "\n".join(
        f'            <img src="images/main/after-{two(n)}.jpg" alt="{name} 유품정리 작업 후 사진 {i + 1}">'
        for i, n in enumerate(after_nums)
    )
    url = f"{BASE_DOMAIN}/{slug}.html"
    return f'''<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{name} 유품정리 고독사청소 특수청소 | 가족애유품정리</title>
  <meta name="description" content="{name} 유품정리, 고독사청소, 특수청소 상담. {feature} 유품정리와 폐기물처리 상담을 안내드립니다. 가족애유품정리 {PHONE}">
  <link rel="canonical" href="{url}">
  <meta property="og:title" content="{name} 유품정리 | 가족애유품정리"><meta property="og:description" content="{name} 유품정리, 고독사청소, 특수청소, 폐기물처리 상담. 가족의 마음으로 정리합니다."><meta property="og:type" content="website"><meta property="og:url" content="{url}"><meta property="og:image" content="{MAIN_BANNER}">
  <meta name="twitter:card" content="summary_large_image"><link rel="icon" href="/images/main/favicon.png"><link rel="stylesheet" href="style.css"><script src="https://cdn.jsdelivr.net/npm/@emailjs/browser@4/dist/email.min.js"></script>
  <script type="application/ld+json">{{"@context":"https://schema.org","@type":"LocalBusiness","name":"가족애유품정리 {name}","url":"{url}","telephone":"{PHONE}","image":"{MAIN_BANNER}","areaServed":"서울특별시 {name}","priceRange":"유품정리 25만원부터, 고독사청소 80만원부터, 폐기물처리 1톤 기준 25만원부터","description":"{name} 유품정리, 고독사청소, 특수청소, 폐기물처리 상담"}}</script>
</head>
<body>
<header class="topbar"><div class="container nav"><a class="logo" href="/">가족애<span>유품정리</span></a><nav class="navlinks"><a href="/#service">주요업무</a><a href="/#price">비용안내</a><a href="#process">업무절차</a><a href="#photos">작업사진</a><a href="#areas">지역안내</a><a href="#consult">상담접수</a></nav><a class="call" href="tel:{PHONE}">{PHONE}</a></div></header>
<main>
<section class="hero"><div class="container heroInner"><div class="eyebrow">서울 {name} 유품정리 · 고독사청소 · 특수청소</div><h1>{name} 유품정리<br>가족의 마음으로 정리합니다</h1><p>{feature} 현장 상황에 맞춰 유품 분류와 중요 물품 확인, 폐기물 정리, 공간 정돈까지 안내드립니다.</p><div class="heroBtns"><a class="btn primary" href="tel:{PHONE}">전화상담 {PHONE}</a><a class="btn secondary" href="#consult">상담접수</a></div><div class="heroBadges"><span>{name} 방문 상담</span><span>365일 상담 가능</span><span>유품정리 · 고독사청소</span></div></div></section>
<section class="trustSection"><div class="container"><div class="grid3"><div class="card trustCard"><strong>{name} 현장 맞춤 정리</strong><p>{cost_note}</p></div><div class="card trustCard"><strong>중요 물품 확인</strong><p>서류, 통장, 도장, 사진, 귀중품 등 확인이 필요한 물품을 별도로 분류합니다.</p></div><div class="card trustCard"><strong>폐기물처리 상담</strong><p>생활폐기물과 가구, 잔짐까지 함께 상담 가능합니다.</p></div></div></div></section>
<section id="service"><div class="container"><h2 class="sectionTitle">{name} 유품정리 주요업무</h2><p class="sectionLead">현장 상황에 따라 유품정리, 고독사청소, 특수청소, 폐기물처리를 함께 안내합니다.</p><div class="grid4"><div class="card"><h3>유품정리</h3><p>남겨진 생활용품과 의류, 서류, 사진, 귀중품을 가족과 협의하며 분류합니다.</p></div><div class="card"><h3>고독사청소</h3><p>오염과 악취가 있는 공간은 일반 정리와 별도로 특수청소 필요 여부를 확인합니다.</p></div><div class="card"><h3>특수청소</h3><p>장기간 방치, 오염, 악취 등 일반 정리로 어려운 현장을 확인 후 안내합니다.</p></div><div class="card"><h3>폐기물처리</h3><p>가구, 가전, 생활폐기물, 잔짐 등 현장에서 발생한 폐기물 처리를 상담합니다.</p></div></div></div></section>
<section id="price" class="areaBox"><div class="container"><h2 class="sectionTitle">{name} 유품정리 비용 안내</h2><p class="sectionLead">표시 금액은 기본 안내 금액이며, 정확한 비용은 현장 확인 후 작업 범위에 따라 안내드립니다.</p><div class="priceGrid"><div class="priceCard"><span class="priceLabel">유품정리</span><strong>25만원부터</strong><p>중요 물품 확인, 생활용품 분류, 폐기물 분류, 공간 정리 상담</p></div><div class="priceCard featured"><span class="priceLabel">고독사청소</span><strong>80만원부터</strong><p>오염 범위 확인, 악취·위생 문제, 특수청소 필요 여부에 따라 안내</p></div><div class="priceCard"><span class="priceLabel">폐기물처리</span><strong>25만원부터</strong><p>1톤 1대 기준. 폐기물 양, 운반 거리, 층수에 따라 변동 가능</p></div></div><div class="notice priceNotice">현장 구조와 물품 양에 따라 비용이 달라질 수 있습니다.</div></div></section>
<section id="cost-factor"><div class="container"><h2 class="sectionTitle">{name} 유품정리 비용에 영향을 미치는 요소</h2><p class="sectionLead">{cost_note}</p><div class="grid3"><div class="card"><h3>물품 양</h3><p>보관품과 폐기품의 양이 많을수록 작업 시간과 인력이 달라집니다.</p></div><div class="card"><h3>층수와 동선</h3><p>엘리베이터 여부, 주차 위치, 운반 동선에 따라 작업 난이도가 달라집니다.</p></div><div class="card"><h3>폐기물 양</h3><p>가구, 가전, 생활폐기물의 양과 종류에 따라 처리 비용이 달라질 수 있습니다.</p></div><div class="card"><h3>특수청소 여부</h3><p>오염, 악취, 장기간 방치가 있는 경우 추가 작업이 필요할 수 있습니다.</p></div><div class="card"><h3>작업 인원</h3><p>공간 규모와 희망 일정에 따라 투입 인원과 차량 수가 달라질 수 있습니다.</p></div><div class="card"><h3>일정 조율</h3><p>당일 상담이나 급한 일정은 현장 위치와 예약 상황에 따라 안내드립니다.</p></div></div></div></section>
<section id="process" class="areaBox"><div class="container"><h2 class="sectionTitle">{name} 유품정리 업무절차</h2><p class="sectionLead">상담부터 마무리 확인까지 가족과 협의하며 단계별로 진행합니다.</p><div class="processGrid"><div class="card processCard"><div class="processHead"><span>1</span><h3>상담 접수</h3></div><p>주소, 공간 형태, 정리 범위, 희망 일정을 확인합니다.</p></div><div class="card processCard"><div class="processHead"><span>2</span><h3>현장 확인</h3></div><p>물품 양, 층수, 엘리베이터 여부를 확인합니다.</p></div><div class="card processCard"><div class="processHead"><span>3</span><h3>중요품 분류</h3></div><p>서류, 통장, 사진, 귀중품 등을 분류합니다.</p></div><div class="card processCard"><div class="processHead"><span>4</span><h3>유품정리</h3></div><p>보관품, 확인품, 폐기품을 구분합니다.</p></div><div class="card processCard"><div class="processHead"><span>5</span><h3>마무리 확인</h3></div><p>정리 후 공간 상태를 확인합니다.</p></div></div></div></section>
<section id="photos"><div class="container"><h2 class="sectionTitle">{name} 유품정리 작업사진</h2><p class="sectionLead">작업 전·중·후 사진을 구분해 현장 정리 흐름을 확인할 수 있도록 구성했습니다.</p><div class="photoBlock"><h3>작업 전</h3><div class="gallery">
{before}
          </div></div><div class="photoBlock"><h3>작업 중</h3><div class="gallery">
{process}
          </div></div><div class="photoBlock"><h3>작업 후</h3><div class="gallery">
{after}
          </div></div></div></section>
<section id="case" class="areaBox"><div class="container"><h2 class="sectionTitle">{name} 유품정리 작업사례</h2><p class="sectionLead">{name} 현장 유형별 유품정리 작업 사례입니다.</p><div class="caseGrid">
{case_grid_html(name, idx)}
        </div></div></section>
<section id="reviews" class="reviewSection"><div class="container"><h2 class="sectionTitle">{name} 유품정리 고객후기</h2><p class="sectionLead">{name}에서 진행된 유품정리 상담과 작업 후기입니다.</p><div class="reviewGrid">
{review_grid_html(name, idx)}
        </div></div></section>
<section id="areas" class="areaBox"><div class="container"><h2 class="sectionTitle">{name} 인근 지역 유품정리 바로가기</h2><p class="sectionLead">{name} 외에도 서울 주요 지역 유품정리 상담을 함께 안내합니다.</p><div class="areaLinks">
{area_links_html(name)}
        </div></div></section>
<section class="faq" id="faq"><div class="container"><h2 class="sectionTitle">{name} 유품정리 자주 묻는 질문</h2>
{faq_html(name, idx)}
      </div></section>
<section id="consult"><div class="container"><div class="formWrap"><h2 class="sectionTitle">{name} 유품정리 상담접수</h2><p class="sectionLead">{name} 현장 상황과 주소를 남겨주시면 방문 가능 일정과 정리 범위를 확인해 안내드립니다.</p><form class="consultForm"><input type="hidden" name="title" value="[가족애유품정리 서울] {name} 상담접수"><input type="hidden" name="site_name" value="가족애유품정리 서울"><input type="hidden" name="region" value="{name}"><div class="formGrid"><div class="field"><label>성함</label><input name="name" placeholder="예: 홍길동" autocomplete="name"></div><div class="field"><label>연락처</label><input name="phone" placeholder="예: 010-0000-0000" autocomplete="tel"></div><div class="field"><label>요청 서비스</label><select name="service"><option value="유품정리">유품정리</option><option value="고독사청소">고독사청소</option><option value="특수청소">특수청소</option><option value="폐기물처리 상담">폐기물처리 상담</option></select></div><div class="field"><label>현장 주소</label><input name="address" placeholder="예: 서울 {name} ○○동 / 아파트·주택 등"></div><div class="field full"><label>상담 내용</label><textarea name="message" placeholder="정리할 공간, 엘리베이터 여부, 폐기물 양, 희망 일정 등을 남겨주세요."></textarea></div></div><label class="agree"><input type="checkbox" name="agree"> 상담 안내를 위한 개인정보 수집 및 이용에 동의합니다.</label><button type="submit" class="btn submitBtn">상담 접수하기</button><div class="status" aria-live="polite"></div></form></div></div></section>
{BACKLINKS}
<section class="bottomCta"><div class="container ctaInner"><div><span>{name} 유품정리 상담</span><h2>가족의 마음으로 조심스럽게 정리하겠습니다</h2><p>유품정리 · 고독사청소 · 특수청소 · 폐기물처리 상담</p></div><a class="btn primary" href="tel:{PHONE}">{PHONE} 전화상담</a></div></section>
</main><footer class="footer"><div class="container"><strong>가족애유품정리 {name}</strong><p>상담전화 {PHONE}</p><p>유품정리 · 고독사청소 · 특수청소 · 폐기물처리 상담</p></div></footer><div class="mobileQuick"><a href="tel:{PHONE}">전화상담</a><a href="#consult">상담접수</a></div><script src="script.js"></script></body></html>'''


def main():
    root = Path(".")
    for idx, (name, slug, feature, cost_note) in enumerate(districts):
        (root / f"{slug}.html").write_text(make_page(name, slug, feature, cost_note, idx), encoding="utf-8")

    urls = [f"{BASE_DOMAIN}/"] + [f"{BASE_DOMAIN}/{slug}.html" for _, slug, *_ in districts]
    today = date.today().isoformat()
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        sitemap += f"  <url><loc>{u}</loc><lastmod>{today}</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>\n"
    sitemap += "</urlset>\n"
    (root / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    (root / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE_DOMAIN}/sitemap.xml\n", encoding="utf-8")

    rss = f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
<title>가족애유품정리 서울</title>
<link>{BASE_DOMAIN}</link>
<description>서울 유품정리, 고독사청소, 특수청소 상담 안내</description>
<language>ko-KR</language>
<lastBuildDate>{today}</lastBuildDate>
<item>
<title>서울 유품정리 메인</title>
<link>{BASE_DOMAIN}/</link>
<description>서울 전지역 유품정리 상담 안내</description>
<pubDate>{today}</pubDate>
</item>
'''
    for name, slug, *_ in districts:
        rss += f'''<item>
<title>{name} 유품정리</title>
<link>{BASE_DOMAIN}/{slug}.html</link>
<description>{name} 유품정리 상담 안내</description>
<pubDate>{today}</pubDate>
</item>
'''
    rss += "</channel>\n</rss>\n"
    (root / "rss.xml").write_text(rss, encoding="utf-8")

    print("서울 25개 구 페이지 생성 완료 (메인과 동일 형식)")
    print("sitemap.xml / robots.txt / rss.xml 갱신 완료")


if __name__ == "__main__":
    main()
