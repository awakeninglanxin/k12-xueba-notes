# -*- coding: utf-8 -*-
"""完整笔记生成：note-grade-XX.html 网页版 + 资料库/年级笔记/*.md 离线归档。

本模块是「知识点正文 + 进阶例题 + ima 教辅索引」的唯一出处，
精讲页与思维导图页不得复制这里的正文。
"""
from collections import defaultdict

from site_core import (GUIDE, GUIDE_PDF, MINI_BASE, RESOURCES, STAMP,
                       SUBJECT_ORDER, esc, mapbar, neighbors, page, prep_for,
                       size_txt, split_questions, subj_of, topic_block)


def md_clean(s):
    """Markdown 单元格/正文清洗：去掉换行与竖线，避免表格被切断"""
    return str(s or "").replace("\n", " ").replace("|", "\\|").strip()


def guide_shape_table():
    """0–3 岁笔记页专用：指南五大领域 × 三个年龄段的目标条数（统计，非正文）"""
    bands = ["3~4岁", "4~5岁", "5~6岁"]
    rows = ["| 发展领域 | 3~4 岁 | 4~5 岁 | 5~6 岁 |", "|---|---|---|---|"]
    for domain, b in GUIDE.items():
        rows.append(f"| {domain} | " + " | ".join(str(len(b.get(x, []))) for x in bands) + " |")
    return rows


def build_note_html(g, ts, qs, ima):
    _, advanced = split_questions(qs)
    b = [f'<div class="hero"><h1>{esc(g["name"])} · 完整学霸笔记</h1>',
         f'<div class="meta">{esc(g["stage"])} · {esc(g["age"])} · '
         f'知识点 {len(ts)} 个 / 进阶例题 {len(advanced)} 道 / ima 教辅索引 {len(ima)} 条</div>',
         '<p class="lead">本页是该年级<b>知识点正文、进阶例题与教辅索引</b>的唯一出处：'
         '全部知识点的描述、掌握标准与自测题，加上与精讲页基础自测不重复的进阶题。'
         '同名 Markdown 版本归档于 <code>资料库/年级笔记/</code>，便于本地打印与二次编辑。</p>',
         mapbar(g, "完整笔记"), '</div>']

    if not ts:
        # 学前：发展目标全文只留在精讲页，这里放资源与幼小衔接（按阶段切片，4 页互不重复）
        b += ['<h2>本阶段启蒙资源（按年龄段递进）</h2>',
              '<p style="color:#666;font-size:14px">4 个学前页分配不同的资源与先修知识点，'
              '不复制同一份清单；发展指南分龄目标正文请到'
              f'<a href="{g["slug"]}.html">精讲页</a>查看。</p>', '<div class="groups">']
        for title, url, desc in RESOURCES[g["n"]]:
            link = (f'<a href="{url}">{esc(title)}</a>' if url
                    else f'{esc(title)}　<code>{GUIDE_PDF}</code>')
            b.append(f'<div class="card"><h4>{link}</h4>'
                     f'<div style="font-size:14px;color:#444">{esc(desc)}</div></div>')
        b.append('</div>')

        if g["n"] == 1:
            b += ['<h2>相邻年龄段 · 指南结构概览</h2>',
                  '<p style="color:#666;font-size:14px">0–3 岁不在《3–6 岁儿童学习与发展指南》覆盖范围，'
                  '此处只列该指南的领域与分龄目标条数，便于了解 3 岁之后的发展阶梯；'
                  '目标原文在后续 3 个年级的精讲页，不在本页复制。</p>',
                  '<table><thead><tr><th>发展领域</th><th>3~4 岁</th><th>4~5 岁</th><th>5~6 岁</th>'
                  '</tr></thead><tbody>']
            for domain, bands in GUIDE.items():
                b.append(f'<tr><td>{esc(domain)}</td>' + "".join(
                    f'<td>{len(bands.get(x, []))} 条</td>' for x in ["3~4岁", "4~5岁", "5~6岁"])
                    + '</tr>')
            b.append('</tbody></table>')

        prep = prep_for(g)
        if prep:
            b += ['<h2>幼小衔接 · 一年级先修知识点（名称索引）</h2>',
                  '<p style="color:#666;font-size:14px">取自开源知识图谱一年级真实数据。'
                  '4 个学前页按年龄段各取不同片段，逐段递进、互不重复；'
                  '这里只列<b>名称</b>并链接到一年级完整笔记的对应正文，'
                  '不复制知识点描述，避免跨年级内容重复。学前期不建议提前刷题。</p>',
                  '<div class="tree">']
            for t in prep:
                b.append(f'<div class="leaf"><a href="note-grade-05.html#kp-{esc(t["id"])}">'
                         f'{esc(t["name"])}</a>'
                         f'<span style="color:#888;font-size:12px"> · {esc(t.get("chapter",""))}</span></div>')
            b.append('</div>')

    if ts:
        by = defaultdict(list)
        for t in ts:
            by[subj_of(t)].append(t)
        b += ['<h2>知识点精讲（全量正文）</h2>',
              f'<p style="color:#666;font-size:14px">共 {len(ts)} 个知识点，含描述、掌握标准与自测题。'
              '脑图页的章节树可通过锚点直接跳到这里的对应条目。</p>']
        for sub in SUBJECT_ORDER + ["其他"]:
            group = by.get(sub, [])
            if not group:
                continue
            b += [f'<h3>{esc(sub)}　<span style="font-weight:400;font-size:13px;color:#888">'
                  f'{len(group)} 个知识点</span></h3>', '<div class="groups">']
            for i in range(0, len(group), 4):
                b.append('<div class="card">')
                for t in group[i:i + 4]:
                    b.append(topic_block(t))
                b.append('</div>')
            b.append('</div>')

    if advanced:
        b += ['<h2>进阶例题与解析</h2>',
              f'<p style="color:#666;font-size:14px">本页独有 {len(advanced)} 道，'
              f'与<a href="{g["slug"]}.html">精讲页</a>的 20 道基础自测题零重复。</p>']
        for i, (t, q) in enumerate(advanced, 1):
            b += ['<details class="q"><summary>' + f'{i}. {esc(q.get("prompt",""))}'
                  + f'　<span style="color:#888;font-size:12px">[{esc(subj_of(t))}·{esc(t.get("name",""))}]</span></summary>',
                  '<div class="ans"><b>答案：</b>' + esc(q.get("answer", ""))]
            if q.get("explanation"):
                b.append('<br><b>解析：</b>' + esc(q["explanation"]))
            b.append('</div></details>')

    if ima:
        b += ['<h2>ima 教辅原件索引（完整清单）</h2>',
              '<div class="note">仅元数据，原件请在 ima 客户端打开。'
              '本清单只在完整笔记页出现一次，精讲页与脑图页不重复。</div>',
              '<table><thead><tr><th>资料名</th><th>类型</th><th>大小</th><th>文件夹</th></tr></thead><tbody>']
        for i in ima[:40]:
            b.append('<tr><td>' + esc(i["title"]) + '</td><td>' + esc(i["type"]) + '</td><td>'
                     + size_txt(i["size_bytes"]) + '</td><td>' + esc(i["folder"]) + '</td></tr>')
        b.append('</tbody></table>')

    prevg, nextg = neighbors(g)
    b += ['<div class="nav"><span>']
    if prevg:
        b.append(f'← <a href="note-{prevg["slug"]}.html">{esc(prevg["name"])} 完整笔记</a>')
    b.append('</span><span><a href="index.html">总入口</a>　')
    if nextg:
        b.append(f'<a href="note-{nextg["slug"]}.html">{esc(nextg["name"])} 完整笔记</a> →')
    b.append('</span></div>')
    crumb = (f'<span class="crumb">/ <a href="index.html">总入口</a> / '
             f'<a href="{g["slug"]}.html">{esc(g["name"])}</a> / 完整笔记</span>')
    return page(esc(g["name"]) + " 完整笔记", crumb, b)


def build_note_md(g, ts, qs, ima):
    """完整年级笔记 Markdown（离线归档，与 note-grade-XX.html 同一份笔记的另一种格式）"""
    _, advanced = split_questions(qs)
    L = [f"# {g['name']} · 学霸笔记（完整版）", "",
         f"- 学段：{g['stage']}　|　年龄段：{g['age']}　|　生成时间：{STAMP}",
         f"- 知识点：{len(ts)} 个　|　进阶例题：{len(advanced)} 道　|　ima 教辅索引：{len(ima)} 条", "",
         "> 知识点、掌握标准、自测题与例题解析均来自 GitHub 开源项目 "
         "`xiaoyang111222/cn-math-taxonomy`（CC BY-NC 4.0），按年级抽取，未改写题目内容。", "",
         "> 本文件是 `note-" + g["slug"] + ".html` 的 Markdown 离线归档。站内页面分工："
         "精讲页放结构统计与 20 道基础自测，思维导图页放脑图与章节树，"
         "知识点正文与进阶例题只在本文件 / 完整笔记页出现一次。", ""]

    if not ts:
        L += ["## 本阶段启蒙资源（按年龄段递进）", ""]
        for title, url, desc in RESOURCES[g["n"]]:
            if url:
                L.append(f"- **{md_clean(title)}**：`{url}` —— {md_clean(desc)}")
            else:
                L.append(f"- **{md_clean(title)}**：`{GUIDE_PDF}` —— {md_clean(desc)}")
        L.append("")
        if g["n"] == 1:
            L += ["## 相邻年龄段 · 指南结构概览", "",
                  "0–3 岁不在《3–6 岁儿童学习与发展指南》覆盖范围；下表只列领域与分龄目标条数。", ""]
            L += guide_shape_table() + [""]
        prep = prep_for(g)
        if prep:
            L += ["## 幼小衔接 · 一年级先修知识点（名称索引）", "",
                  "> 取自开源知识图谱一年级真实数据；4 个学前页各取不同片段，互不重复。"
                  "这里只列名称，正文见 `note-grade-05.html`，避免跨年级复制。", ""]
            for t in prep:
                L.append(f"- {md_clean(t.get('name',''))}（章节：{md_clean(t.get('chapter',''))}）")
            L.append("")

    if ts:
        L += ["## 知识点精讲（按学科）", ""]
        by = defaultdict(list)
        for t in ts:
            by[subj_of(t)].append(t)
        for sub in SUBJECT_ORDER + ["其他"]:
            group = by.get(sub, [])
            if not group:
                continue
            L += [f"### {sub}（{len(group)} 个知识点）", ""]
            for t in group:
                L.append(f"#### {md_clean(t.get('name',''))}")
                if t.get("chapter"):
                    L.append(f"*章节：{md_clean(t['chapter'])}*")
                if t.get("description"):
                    L += ["", md_clean(t["description"])]
                mc = t.get("mastery_criteria") or []
                if mc:
                    L += ["", "**掌握标准**", ""] + [f"- {md_clean(x)}" for x in mc]
                dq = t.get("diagnostic_question") or {}
                if dq.get("question"):
                    L += ["", f"**自测**：{md_clean(dq['question'])}　**答**：{md_clean(dq.get('answer',''))}"]
                L.append("")

    if advanced:
        L += ["## 进阶例题与解析", "",
              "> 与精讲页的 20 道基础自测题零重复。", ""]
        for i, (t, q) in enumerate(advanced, 1):
            L += [f"### {i}. {md_clean(q.get('prompt',''))}", "",
                  f"- 所属知识点：{md_clean(t.get('name',''))}（{subj_of(t)}）",
                  f"- **答案**：{md_clean(q.get('answer',''))}"]
            if q.get("explanation"):
                L.append(f"- **解析**：{md_clean(q['explanation'])}")
            L.append("")

    if ima:
        L += ["## ima 知识库 · 本年级教辅原件索引", "",
              "> 仅元数据：ima MCP 对订阅库不提供正文/原件下载（返回 220030）。原件请在 ima 客户端打开。", "",
              "| 资料名 | 类型 | 大小 | 所属文件夹 |", "|---|---|---|---|"]
        for i in ima[:40]:
            L.append(f"| {md_clean(i['title'])} | {md_clean(i['type'])} | "
                     f"{size_txt(i['size_bytes'])} | {md_clean(i['folder'])} |")
        L.append("")

    return "\n".join(L)
