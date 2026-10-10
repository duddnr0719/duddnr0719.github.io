#!/usr/bin/env python3
"""카테고리 안 글 순서(front matter `order`)를 제목의 장 번호로 매긴다.

- '3. 배열', '3-1. 프로세스', '10장-2 감성분석', '1-1 인터넷' → (3,0) (3,1) (10,2) (1,1)
- 장 번호가 없는 글은 같은 카테고리의 번호 글 뒤에 날짜순으로 붙는다
- 카테고리에 번호 글이 하나도 없으면 order 를 넣지 않는다 (목록은 최신순)

새 스터디 노트를 추가한 뒤 한 번 실행 : python3 scripts/assign_order.py
"""
import collections
import os
import re

POSTS = os.path.join(os.path.dirname(__file__), "..", "content", "posts")
NUM = re.compile(r"^\s*(\d+)\s*장?\s*(?:[-.]\s*(\d+))?")


def front(s):
    m = re.match(r"^(---\n.*?\n---\n)", s, re.S)
    return m.group(1) if m else ""


def field(fm, k):
    m = re.search(rf"^{k}:\s*(.*)$", fm, re.M)
    return m.group(1).strip() if m else ""


cats = collections.defaultdict(list)
for f in sorted(os.listdir(POSTS)):
    if not f.endswith(".md") or f.startswith("_"):
        continue
    p = os.path.join(POSTS, f)
    s = open(p, encoding="utf-8").read()
    fm = front(s)
    title = field(fm, "title").strip('"')
    cat = field(fm, "categories")
    m = NUM.match(title)
    key = (int(m.group(1)), int(m.group(2) or 0)) if m else None
    cats[cat].append((key, field(fm, "date"), p, s, fm))

changed = 0
for cat, items in cats.items():
    numbered = any(k for k, *_ in items)
    items.sort(key=lambda x: (x[0] is None, x[0] or (0, 0), x[1]))
    for i, (key, _, p, s, fm) in enumerate(items, 1):
        new_fm = re.sub(r"^order:.*\n", "", fm, flags=re.M)
        if numbered:
            # 닫는 '---' 바로 앞에 order 삽입 (여는 '---'는 앞에 개행이 없어서 첫 '\n---\n'이 닫는 줄)
            new_fm = new_fm.replace("\n---\n", f"\norder: {i}\n---\n", 1)
        if new_fm != fm:
            open(p, "w", encoding="utf-8").write(s.replace(fm, new_fm, 1))
            changed += 1
print(f"order 갱신 : {changed}개 파일")
