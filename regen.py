#!/usr/bin/env python3
import json, os, re

home=os.path.expanduser("~"); os.chdir(f"{home}/blog")
trees=json.load(open("/tmp/notion_trees.json"))
cm=json.load(open("/tmp/notion_children_map.json"))
rows=json.load(open("/tmp/study_notes_full2.json"))

def local_img(url):
    m=re.search(r'com/([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})',url)
    if not m: return None
    cand=m.group(1).replace("-","")
    for e in [".png",".jpg",".jpeg",".gif",".webp",".pdf"]:
        if os.path.exists(f"static/images/{cand}{e}"):
            return f"/images/{cand}{e}"
    return None

def get_children(bid):
    return cm.get(bid,[])

def rich_md(rich):
    out=[]
    for x in rich:
        t=x.get("plain_text","")
        a=x.get("annotations",{})
        if a.get("code"): t=f"`{t}`"
        if a.get("bold") and a.get("italic"): t=f"***{t}***"
        elif a.get("bold"): t=f"**{t}**"
        elif a.get("italic"): t=f"*{t}*"
        if a.get("strikethrough"): t=f"~~{t}~~"
        if x.get("href") and not t.startswith("!"):
            t=f"[{t}]({x['href']})"
        out.append(t)
    return "".join(out)

def detect_code(s):
    if "func(" in s: return "python"
    if "#include <" in s or "int main" in s: return "c"
    if "public static void main" in s: return "java"
    if "kubectl" in s or "apiVersion" in s: return "yaml"
    if "docker" in s or "FROM " in s: return "docker"
    return ""

def child_block_md(b):
    if not b.get("has_children"): return ""
    parts=[]
    for c in get_children(b["id"]):
        md=block_md(c)
        if md: parts.append(md)
    return "\n".join(parts)

def block_md(b):
    t=b.get("type")
    if t is None: return ""
    v=b.get(t) or {}
    if t in ("heading_1","heading_2","heading_3"):
        lv=int(t[-1])
        txt=rich_md(v.get("rich_text",[]))
        head=(f"{'#'*lv} {txt}" if txt else f"{'#'*lv} {b.get('id','')[:8]}")
        kids=child_block_md(b)
        return head+("\n"+kids if kids else "")
    if t=="paragraph":
        txt=rich_md(v.get("rich_text",[]))
        kids=child_block_md(b)
        return (txt+"\n"+kids).strip()
    if t in ("bulleted_list_item","to_do"):
        chk="x" if (t=="to_do" and v.get("checked")) else " "
        txt=rich_md(v.get("rich_text",[]))
        base=f"- [{chk}] {txt}" if t=="to_do" else f"- {txt}"
        if b.get("has_children"):
            parts=[]
            for c in get_children(b["id"]):
                md=block_md(c)
                if md: parts.append("\n".join("  "+l for l in md.splitlines()))
            return base+"\n"+"\n".join(parts)
        return base
    if t=="code":
        raw="".join(x.get("plain_text","") for x in v.get("rich_text",[]))
        return f"```{detect_code(raw)}\n{raw.rstrip()}\n```"
    if t in ("image","video","embed","file","pdf"):
        url=""
        fobj=v.get("file") or {}
        eobj=v.get("external") or {}
        url=fobj.get("url") or eobj.get("url") or ""
        loc=local_img(url) if url else None
        cap=""
        for c in v.get("caption",[])[:2]:
            cap+=c.get("plain_text","")
        if loc: return f"![{cap}]({loc})"
        return f"![{cap}]({url})" if url else ""
    if t=="divider": return "---"
    if t=="quote":
        txt=rich_md(v.get("rich_text",[]))
        kids=child_block_md(b)
        q=f"> {txt}"
        return q+("\n"+kids if kids else "")
    if t=="callout":
        txt=rich_md(v.get("rich_text",[]))
        kids=get_children(b["id"])
        for c in kids:
            txt+= "\n"+block_md(c)
        return f"> {txt}"
    if t=="numbered_list_item":
        txt=rich_md(v.get("rich_text",[]))
        base=f"1. {txt}"
        if b.get("has_children"):
            parts=[]
            for c in get_children(b["id"]):
                md=block_md(c)
                if md: parts.append("\n".join("  "+l for l in md.splitlines()))
            return base+"\n"+"\n".join(parts)
        return base
    if t in ("column_list","column","toggle","child_page","child_database","child_block","table","table_row","link_preview","bookmark","equation","synced_block","table_view"):
        kids=get_children(b["id"])
        if not kids: return ""
        parts=[]
        for c in kids:
            md=block_md(c)
            if md: parts.append(md)
        if t=="column_list":
            return "<columns>\n"+ "\n".join(f'<column ratio="100">{p}</column>' for p in parts) + "\n</columns>"
        if t=="toggle":
            summary=rich_md(v.get("rich_text",[]))
            return f"- **{summary}**\n"+"\n".join(p for p in parts)
        if t=="numbered_list_item":
            txt=rich_md(v.get("rich_text",[]))
            return f"1. {txt}"+"\n"+"\n".join(parts)
        return "\n".join(parts)
    if t in ("paragraph","empty"):
        return ""
    return ""

def page_md(blocks):
    parts=[]
    for b in blocks:
        md=block_md(b)
        if md: parts.append(md)
    # collapse 3+ blank lines
    txt="\n".join(parts)
    txt=re.sub(r'\n{3,}','\n\n',txt)
    return txt.strip()+"\n"

import glob, datetime, re as _re
imgmap=json.load(open("/tmp/img_mapping.json"))
changed=0
for f in sorted(glob.glob("content/posts/*.md")):
    m=re.search(r'^title: "(.+)"$',open(f,encoding="utf-8").read(),re.M)
    if not m or m.group(1).strip()=="스터디 노트": continue
    t=m.group(1).strip()
    match=[r for r in rows if (r.get("Title") or "").strip()==t]
    if not match:
        print("NO NOTION MATCH:",t); continue
    r=match[0]
    body=page_md(trees[r["id"]])
    refs=list(imgmap.get(t,[]))
    body=_re.sub(r'!\[[^\]]*\]\(https://prod-files-secure[^)]+\)',
                 lambda m: f"![]({refs.pop(0)})" if refs else m.group(0), body)
    txt=open(f,encoding="utf-8").read()
    m2=re.match(r'^(---\n.*?\n---\n)',txt,re.S)
    pre=m2.group(1)
    if txt[len(pre):].strip() != body:
        open(f,"w",encoding="utf-8").write(f"{pre}\n{body}")
        changed+=1
        print(f"regen: {t} -> {len(body)}ch")
print("changed:",changed)

