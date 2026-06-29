from pathlib import Path
import re
import random

# 사용법:
# 1) 이 파일을 seoul-gajogae-yupum 폴더 안에 넣기
# 2) 같은 폴더 안에 최종 확정된 gangnam.html 이 있어야 함
# 3) VS Code 터미널에서 실행:
#    python create_seoul_pages_from_gangnam.py

BASE_DOMAIN = "https://www.seoul.gajogae-yupum.com"
PHONE = "010-4720-3895"

districts = [
    ("강남구", "gangnam"),
    ("강동구", "gangdong"),
    ("강북구", "gangbuk"),
    ("강서구", "gangseo"),
    ("관악구", "gwanak"),
    ("광진구", "gwangjin"),
    ("구로구", "guro"),
    ("금천구", "geumcheon"),
    ("노원구", "nowon"),
    ("도봉구", "dobong"),
    ("동대문구", "dongdaemun"),
    ("동작구", "dongjak"),
    ("마포구", "mapo"),
    ("서대문구", "seodaemun"),
    ("서초구", "seocho"),
    ("성동구", "seongdong"),
    ("성북구", "seongbuk"),
    ("송파구", "songpa"),
    ("양천구", "yangcheon"),
    ("영등포구", "yeongdeungpo"),
    ("용산구", "yongsan"),
    ("은평구", "eunpyeong"),
    ("종로구", "jongno"),
    ("중구", "jung"),
    ("중랑구", "jungnang"),
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

slug_by_name = dict(districts)

MAIN_BEFORE = list(range(1, 31))
MAIN_PROCESS = list(range(1, 26))
MAIN_AFTER = [n for n in range(1, 31) if n != 21]


def pick_main_gallery(idx, count=4):
    rng = random.Random(1000 + idx)
    return (
        rng.sample(MAIN_BEFORE, count),
        rng.sample(MAIN_PROCESS, count),
        rng.sample(MAIN_AFTER, count),
    )

def two(n: int) -> str:
    return f"{n:02d}"


def three(n: int) -> str:
    return f"{n:03d}"

def build_nearby_links(region_name: str) -> str:
    links = []
    for name in nearby.get(region_name, []):
        slug = slug_by_name[name]
        links.append(f'          <a href="{slug}.html">{name} 유품정리</a>')
    links.append('          <a href="/">서울 유품정리 메인</a>')
    return "\n".join(links)

def replace_canonical_and_urls(html: str, slug: str) -> str:
    html = re.sub(r'<link rel="canonical" href="[^"]+">', f'<link rel="canonical" href="{BASE_DOMAIN}/{slug}.html">', html)
    html = re.sub(r'<meta property="og:url" content="[^"]+">', f'<meta property="og:url" content="{BASE_DOMAIN}/{slug}.html">', html)
    html = re.sub(r'"url":"https://www\.seoul\.gajogae-yupum\.com/[^"]*"', f'"url":"{BASE_DOMAIN}/{slug}.html"', html)
    return html

def replace_area_links_block(html: str, region_name: str) -> str:
    section_match = re.search(r'<section id="areas".*?</section>', html, flags=re.S)
    if not section_match:
        return html
    section = section_match.group(0)
    replacement = '<div class="areaLinks">\n' + build_nearby_links(region_name) + '\n        </div>'
    section2 = re.sub(r'<div class="areaLinks">\s*.*?\s*</div>', replacement, section, flags=re.S)
    return html[:section_match.start()] + section2 + html[section_match.end():]

def replace_photos(html: str, region_name: str, idx: int) -> str:
    before_nums, process_nums, after_nums = pick_main_gallery(idx)

    before_imgs = "\n".join(
        f'            <img src="images/main/before-{two(n)}.jpg" alt="{region_name} 유품정리 작업 전 사진 {i+1}">'
        for i, n in enumerate(before_nums)
    )
    process_imgs = "\n".join(
        f'            <img src="images/main/process-{two(n)}.jpg" alt="{region_name} 유품정리 작업 중 사진 {i+1}">'
        for i, n in enumerate(process_nums)
    )
    after_imgs = "\n".join(
        f'            <img src="images/main/after-{two(n)}.jpg" alt="{region_name} 유품정리 작업 후 사진 {i+1}">'
        for i, n in enumerate(after_nums)
    )

    gallery_pattern = r'<div class="gallery">\s*.*?\s*</div>'
    galleries = list(re.finditer(gallery_pattern, html, flags=re.S))
    if len(galleries) >= 3:
        blocks = [before_imgs, process_imgs, after_imgs]
        offset = 0
        for g, block in zip(galleries[:3], blocks):
            start, end = g.start() + offset, g.end() + offset
            new_block = '<div class="gallery">\n' + block + '\n          </div>'
            html = html[:start] + new_block + html[end:]
            offset += len(new_block) - (end - start)
    return html

def make_page(template: str, region_name: str, slug: str, idx: int) -> str:
    html = template.replace("강남구", region_name)
    html = replace_canonical_and_urls(html, slug)

    html = re.sub(
        r'<title>.*?</title>',
        f'<title>{region_name} 유품정리 고독사청소 특수청소 | 가족애유품정리</title>',
        html,
        flags=re.S
    )
    html = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{region_name} 유품정리, 고독사청소, 특수청소 상담. {region_name} 아파트, 오피스텔, 빌라, 주택 유품정리와 폐기물처리 상담을 안내드립니다. 가족애유품정리 {PHONE}">',
        html
    )
    html = replace_area_links_block(html, region_name)
    html = replace_photos(html, region_name, idx)
    return html

def main():
    root = Path(".")
    template_path = root / "gangnam.html"
    if not template_path.exists():
        raise FileNotFoundError("gangnam.html 파일이 없습니다. 이 스크립트를 seoul-gajogae-yupum 폴더 안에서 실행하세요.")

    template = template_path.read_text(encoding="utf-8")
    created = []

    for idx, (name, slug) in enumerate(districts):
        if name == "강남구":
            continue
        html = make_page(template, name, slug, idx)
        out = root / f"{slug}.html"
        out.write_text(html, encoding="utf-8")
        created.append(out.name)

    print("서울 24개 구 페이지 생성 완료")
    for filename in created:
        print("-", filename)

if __name__ == "__main__":
    main()
