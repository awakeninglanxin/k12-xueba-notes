# -*- coding: utf-8 -*-
"""页面生成：总入口、14 个年级精讲页、14 个思维导图页、来源说明页。

页面分工（去重契约，勿在两页之间复制同一份正文）：
  grade-XX      知识结构总览 + 发展目标（学前）+ 20 道基础自测
  map-XX        放射状脑图 + 树状知识地图（只有结构名称，无正文、无题目）
  note-XX       全部知识点正文 + 40 道进阶例题 + ima 教辅索引
"""
from site_core import (GRADES, GUIDE, IMA_ITEMS, LIB, RESOURCES, STAMP,
                       SUBJECT_ORDER, esc, mapbar, neighbors, page,
                       split_questions, structure, subj_of)
from site_mindmap import branches_for, map_stats, radial_svg, tree_html


def build_grade_html(g, ts, qs, ima):
    basic, _ = split_questions(qs)
    st = structure(ts)
    active_subs = [s for s in SUBJECT_ORDER + ["其他"] if st.get(s)]
    stats = "".join(
        f'<div class="stat"><b>{v}</b><span>{k}</span></div>'
        for k, v in [("知识点", len(ts)), ("基础自测", len(basic)),
                     ("ima 教辅", len(ima)), ("学科", len(active_subs))])

    b = [f'<div class="hero"><h1>{esc(g["name"])} · 精讲页</h1>',
         f'<div class="meta">{esc(g["stage"])} · {esc(g["age"])} · 第 {g["n"]} / 14 站</div>',
         f'<p class="lead">{esc(g["desc"])}</p>',
         f'<div class="stats">{stats}</div>',
         mapbar(g, "精讲页"), '</div>']

    b += ['<div class="note"><b>本页与另外两页不重复</b>：本页只放「知识结构 + 基础自测」；'
          f'<a href="map-{g["slug"]}.html">思维导图</a>只放结构图与知识点名称索引；'
          f'<a href="note-{g["slug"]}.html">完整笔记</a>才放全部知识点正文、进阶例题与教辅索引。</div>']

    if g["n"] == 1:
        b += ['<div class="note"><b>关于 0–3 岁</b>：教育部《3–6 岁儿童学习与发展指南》自 3 岁起，'
              '本阶段不设学科知识点与刷题内容。请以儿保体检与医师评估为准，'
              '本站归档的指南 PDF 可用于了解 3 岁后的发展阶梯。</div>']
    elif g["band"]:
        b += ['<h2>发展目标 · ' + esc(g["band"]) + '</h2>',
              '<p style="color:#666;font-size:14px">以下为教育部《3–6 岁儿童学习与发展指南》分龄目标原文要点整理，'
              'PDF 原件已归档于 <code>资料库/学前指南/</code>。全文只在本页出现一次。</p>',
              '<div class="groups">']
        for i, (domain, bands) in enumerate(GUIDE.items(), 1):
            items = bands.get(g["band"], [])
            b.append(f'<div class="card"><h4>{esc(domain)}</h4>'
                     '<ul style="margin:0;padding-left:20px;font-size:14px">')
            for j, x in enumerate(items, 1):
                b.append(f'<li id="d{i}-{j}">{esc(x)}</li>')
            b.append('</ul></div>')
        b.append('</div>')

    if ts:
        b += ['<h2>知识结构总览</h2>',
              f'<p style="color:#666;font-size:14px">共 {len(ts)} 个知识点，按学科 / 领域 / 章节统计。'
              '本页不重复罗列知识点正文，需要逐条精讲请打开完整笔记；'
              '想先看整体脉络请打开思维导图。</p>',
              '<table><thead><tr><th>学科</th><th>领域数</th><th>章节数</th>'
              '<th>知识点数</th><th>领域构成</th></tr></thead><tbody>']
        for sub in active_subs:
            domains = st[sub]
            n_ch = sum(len(chs) for chs in domains.values())
            n_kp = sum(len(v) for chs in domains.values() for v in chs.values())
            dom_txt = "、".join(f"{esc(d)}({sum(len(v) for v in chs.values())})"
                               for d, chs in sorted(domains.items(),
                                                    key=lambda x: -sum(len(v) for v in x[1].values()))[:4])
            b.append(f'<tr><td><b>{esc(sub)}</b></td><td>{len(domains)}</td><td>{n_ch}</td>'
                     f'<td>{n_kp}</td><td>{dom_txt}</td></tr>')
        b += ['</tbody></table>',
              f'<p class="legend">思维导图：<a href="map-{g["slug"]}.html">'
              f'查看 {esc(g["name"])} 完整脑图与章节树 →</a></p>']

    if basic:
        b += ['<h2>基础自测 · 20 道</h2>',
              f'<p style="color:#666;font-size:14px">本页独有的 {len(basic)} 道入门题，'
              '点击展开答案与解析。其余 40 道进阶题在完整笔记页，两页题目不重复。</p>']
        for i, (t, q) in enumerate(basic, 1):
            b += ['<details class="q"><summary>' + f'{i}. {esc(q.get("prompt",""))}'
                  + f'　<span style="color:#888;font-size:12px">[{esc(subj_of(t))}·{esc(t.get("name",""))}]</span></summary>',
                  '<div class="ans"><b>答案：</b>' + esc(q.get("answer", ""))]
            if q.get("explanation"):
                b.append('<br><b>解析：</b>' + esc(q["explanation"]))
            b.append('</div></details>')

    if ima:
        b += ['<h2>ima 教辅索引</h2>',
              f'<p>本年级在老师 ima 知识库中共检索到 <b>{len(ima)}</b> 条真实教辅目录。'
              f'完整清单（含文件名、大小、所属文件夹）只在 '
              f'<a href="note-{g["slug"]}.html">完整笔记页</a>列出，本页不重复。</p>']

    b += ['<h2>本年级三页与归档文件</h2>',
          '<table><thead><tr><th>页面 / 文件</th><th>独有内容</th></tr></thead><tbody>',
          f'<tr><td><a href="{g["slug"]}.html">精讲页（本页）</a></td>'
          '<td>知识结构总览、发展目标（学前）、20 道基础自测</td></tr>',
          f'<tr><td><a href="map-{g["slug"]}.html">思维导图页</a></td>'
          '<td>放射状脑图 + 章节树 + 知识点名称索引（可跳转正文）</td></tr>',
          f'<tr><td><a href="note-{g["slug"]}.html">完整笔记页</a></td>'
          '<td>全部知识点正文、40 道进阶例题、ima 教辅索引</td></tr>',
          f'<tr><td><code>资料库/年级笔记/{esc(g["name"])}.md</code></td>'
          '<td>完整笔记的 Markdown 离线归档（便于打印与二次编辑）</td></tr>',
          f'<tr><td><a href="资料库/ima索引/{esc(g["name"])}.json">{esc(g["name"])}.json</a></td>'
          '<td>该年级 ima 资料目录元数据</td></tr>',
          '<tr><td><a href="sources.html">资料来源与许可（网页版）</a></td>'
          '<td>全部来源、许可与页面分工说明</td></tr>', '</tbody></table>']

    prevg, nextg = neighbors(g)
    b.append('<div class="nav"><span>')
    if prevg:
        b.append(f'← 上一站：<a href="{prevg["slug"]}.html">{esc(prevg["name"])}</a>')
    b.append('</span><span><a href="index.html">返回总入口</a>　')
    if nextg:
        b.append(f'下一站：<a href="{nextg["slug"]}.html">{esc(nextg["name"])}</a> →')
    b.append('</span></div>')
    crumb = f'<span class="crumb">/ <a href="index.html">总入口</a> / {esc(g["stage"])} / {esc(g["name"])}</span>'
    return page(esc(g["name"]) + " 精讲页", crumb, b)


def build_map_html(g, ts):
    ms = map_stats(g, ts)
    br = branches_for(g, ts)
    unit = "条目标" if not ts else "个知识点"
    svg = radial_svg(g, br, unit=unit, show_count=bool(ts),
                     center_sub="知识思维导图" if ts else "发展领域导图")
    items = [("一级分支", ms["subjects"]), ("二级分支", ms["domains"]),
             ("章节", ms["chapters"]), ("知识点", ms["topics"])] if ts else [
             ("发展领域", ms["subjects"]), ("分龄目标", ms["goals"]), ("指南领域", 5), ("启蒙资源", len(RESOURCES[g["n"]]))]
    stats = "".join(f'<div class="stat"><b>{v}</b><span>{k}</span></div>' for k, v in items)

    lead = ('<p class="lead">放射状脑图给出学科 / 领域的整体脉络，下方章节树可逐级展开到每一个知识点；'
            '点击知识点名称会跳到完整笔记页的对应正文。本页只有结构名称与数量，不含知识点正文与题目。</p>'
            if ts else
            '<p class="lead">放射状脑图按《3–6 岁儿童学习与发展指南》五大领域组织，'
            '下方领域树可展开到每条分龄目标的关键词；点击会跳到精讲页的对应原文。'
            '本页只有结构名称与关键词索引，不含目标全文与题目。</p>')
    b = [f'<div class="hero"><h1>{esc(g["name"])} · 思维导图</h1>',
         f'<div class="meta">{esc(g["stage"])} · {esc(g["age"])} · 第 {g["n"]} / 14 站</div>',
         lead,
         f'<div class="stats">{stats}</div>',
         mapbar(g, "思维导图"), '</div>']

    b += ['<h2>放射状脑图</h2>',
          '<div class="mindmap">' + svg + '</div>',
          '<p class="legend">中心为年级；内圈为' + ('学科（含该科知识点总数）' if ts else '发展领域（含分龄目标数）')
          + '，外圈为' + ('知识领域（含知识点数）' if ts else '分龄目标关键词（仅前 8 字索引）')
          + '。颜色仅用于区分分支，全图白底黑字，可横向滚动或缩放查看。'
          + ('' if ts else ' 学前脑图外圈只取每条目标前 8 字作索引，完整原文只在精讲页出现一次。')
          + '</p>',
          ('<p class="legend">数据来自 <code>topics.json</code> 的 '
           '<code>subject / domain / chapter / name</code> 真实字段，未人工编造节点。</p>'
           if ts else
           '<p class="legend">节点来自教育部《3–6 岁儿童学习与发展指南》五大领域及分龄目标，'
           '未人工编造节点。</p>')]

    tree_hint = ('<p style="color:#666;font-size:14px">逐级点击展开。'
                 '这一层只列知识点<b>名称</b>作为导航，正文与掌握标准在完整笔记页，避免重复。</p>'
                 if ts else
                 '<p style="color:#666;font-size:14px">逐级点击展开。'
                 '这一层只列分龄目标的<b>前 20 字关键词</b>作为导航，'
                 '完整原文在精讲页，避免重复。</p>')
    b += ['<h2>树状思维导图 · ' + ('章节与知识点索引' if ts else '领域与目标索引') + '</h2>',
          tree_hint, tree_html(g, ts)]

    if not ts:
        b += ['<div class="note">学前期不属于义务教育，没有学科知识点与题库，'
              '因此脑图按《3–6 岁儿童学习与发展指南》五大领域组织，'
              '分龄目标正文请到本年级精讲页查看（本页不复制）。</div>']

    prevg, nextg = neighbors(g)
    b.append('<div class="nav"><span>')
    if prevg:
        b.append(f'← 上一站脑图：<a href="map-{prevg["slug"]}.html">{esc(prevg["name"])}</a>')
    b.append('</span><span><a href="index.html">返回总入口</a>　')
    if nextg:
        b.append(f'下一站脑图：<a href="map-{nextg["slug"]}.html">{esc(nextg["name"])}</a> →')
    b.append('</span></div>')
    crumb = (f'<span class="crumb">/ <a href="index.html">总入口</a> / '
             f'<a href="{g["slug"]}.html">{esc(g["name"])}</a> / 思维导图</span>')
    return page(esc(g["name"]) + " 思维导图", crumb, b)


def build_index(counts):
    total_kp = sum(c[0] for c in counts.values())
    total_q = sum(c[1] for c in counts.values())
    total_lib = sum(1 for _ in (LIB / "开源数据").rglob("*") if _.is_file())
    b = ['<div class="hero"><h1>📚 学霸笔记资料库</h1>',
         '<div class="meta">幼儿 0–3 岁 → 小班 / 中班 / 大班 → 小学 1–6 年级 → 初中 3 年 → 高中，共 14 个年级</div>',
         '<p class="lead">每个年级三个页面：<strong>精讲页（结构 + 基础自测）、思维导图（脑图 + 章节树）、'
         '完整笔记（全部知识点正文 + 进阶例题）</strong>。三页内容互不重复，均取自真实公开数据。</p>',
         '<div class="stats">'
         + "".join(f'<div class="stat"><b>{v}</b><span>{k}</span></div>' for k, v in
                   [("年级", 14), ("网页", 44), ("思维导图", 14), ("知识点", total_kp),
                    ("例题", total_q), ("ima 教辅索引", len(IMA_ITEMS)), ("归档文件", total_lib)])
         + '</div></div>',
         '<div class="note"><b>先说清楚来源</b>：核心知识点与题目来自 GitHub 开源 '
         '<a href="https://github.com/xiaoyang111222/cn-math-taxonomy">cn-math-taxonomy</a>'
         '（CC BY-NC 4.0，仅供个人学习/教学，禁止商用）；学前 4 页依据教育部公开指南；'
         '「ima 教辅索引」是老师知识库内的真实文件目录（仅元数据）。'
         '完整许可、来源与页面分工见 <a href="sources.html">资料来源与许可</a>。</div>',
         '<h2>按学段选择年级</h2>',
         '<input class="search" id="q" placeholder="输入年级或关键词过滤…" oninput="flt()">']

    stages = [("学前期", "3–6 岁 · 发展指南与启蒙"), ("小学", "1–6 年级 · 语数英科学道法"),
              ("初中", "7–9 年级 · 全科 + 中考"), ("高中", "必修与选择性必修 · 高考")]
    for stage, sub in stages:
        b += [f'<div class="stage">{stage}　<span style="font-weight:400;color:#777;font-size:13px">{sub}</span></div>',
              '<div class="grid">']
        for g in GRADES:
            if g["stage"] != stage:
                continue
            kp, qs, ima = counts[g["name"]]
            numtxt = (f'知识点 {kp} · 例题 {qs} · 教辅 {ima}') if kp else '5 领域发展要点 · 启蒙资源 · 幼小衔接'
            b.append(f'<div class="gcard" data-k="{esc(g["name"]+g["stage"]+g["age"])}">'
                     f'<div class="st">{esc(g["stage"])} · {esc(g["age"])}</div>'
                     f'<div class="nm"><a href="{g["slug"]}.html">{esc(g["name"])}</a></div>'
                     f'<div class="num">{numtxt}</div>'
                     f'<div class="links">'
                     f'<a href="{g["slug"]}.html">精讲</a>'
                     f'<a href="map-{g["slug"]}.html">脑图</a>'
                     f'<a href="note-{g["slug"]}.html">完整笔记</a>'
                     f'</div></div>')
        b.append('</div>')

    b += ['<h2>三页分工 · 内容不重复</h2>',
          '<table><thead><tr><th>页面</th><th>独有内容</th><th>刻意不放的内容</th></tr></thead><tbody>',
          '<tr><td><code>grade-XX.html</code> 精讲页</td>'
          '<td>知识结构总览（学科/领域/章节统计）、学前发展目标全文、20 道基础自测</td>'
          '<td>知识点正文、进阶例题、教辅清单</td></tr>',
          '<tr><td><code>map-grade-XX.html</code> 思维导图</td>'
          '<td>放射状 SVG 脑图、章节树、知识点名称索引（可跳转正文）</td>'
          '<td>知识点正文、题目、教辅清单</td></tr>',
          '<tr><td><code>note-grade-XX.html</code> 完整笔记</td>'
          '<td>全部知识点精讲 + 掌握标准 + 自测题、40 道进阶例题、ima 教辅索引</td>'
          '<td>基础自测 20 道、发展目标全文、结构统计表</td></tr>',
          '</tbody></table>',
          '<p class="legend">注：<code>资料库/年级笔记/*.md</code> 是完整笔记网页版的 Markdown 离线归档，'
          '属同一份笔记的另一种格式，供本地打印与二次编辑；站内各 HTML 页面之间无正文重复。</p>',
          '<h2>目录</h2>', '<table><thead><tr><th>路径</th><th>说明</th></tr></thead><tbody>',
          '<tr><td><code>index.html</code> + <code>grade-XX.html</code> + '
          '<code>map-grade-XX.html</code> + <code>note-grade-XX.html</code></td>'
          '<td>总入口 + 14×3 个年级页面（同目录平铺，互链可靠）</td></tr>',
          '<tr><td><code>资料库/年级笔记/</code></td><td>14 份完整 Markdown 笔记</td></tr>',
          '<tr><td><code>资料库/ima索引/</code></td><td>总目录 JSON + 14 个年级子索引</td></tr>',
          '<tr><td><code>资料库/开源数据/</code></td><td>原始知识点 / 题库 / 课标 JSON、LICENSE、mini-classroom</td></tr>',
          '<tr><td><code>资料库/学前指南/</code></td><td>《3–6 岁儿童学习与发展指南》PDF</td></tr>',
          '<tr><td><a href="sources.html">sources.html</a></td>'
          '<td>完整来源、许可、页面分工与版权说明</td></tr>', '</tbody></table>',
          '<h2>使用建议</h2>',
          '<p>① 从总入口选年级 → ② 先打开<b>思维导图</b>建立整体框架 → '
          '③ 在<b>精讲页</b>看结构统计并用 20 道基础题自测 → '
          '④ 到<b>完整笔记页</b>逐条精讲并做 40 道进阶题 → '
          '⑤ ima 索引里的教辅原件，在 ima 客户端按文件名搜索阅读。</p>',
          '<p style="color:#777;font-size:13px">生成时间：' + STAMP + '。所有同目录页面可离线双击打开。</p>',
          '<script>function flt(){var v=document.getElementById("q").value.trim();'
          'document.querySelectorAll(".gcard").forEach(function(a){'
          'a.style.display=(!v||a.dataset.k.indexOf(v)>=0)?"":"none";});}</script>']
    return page("总入口", '<span class="crumb">/ 总入口</span>', b)


def build_sources_html():
    b = ['<div class="hero"><h1>资料来源、许可与页面分工</h1>',
         '<p class="lead">本目录所有内容均来自可公开获取的资料，或老师本人 ima 账号内可见的资料目录。</p></div>',
         '<h2>来源一览</h2>',
         '<table><thead><tr><th>来源</th><th>内容</th><th>许可 / 限制</th></tr></thead><tbody>',
         '<tr><td>GitHub <a href="https://github.com/xiaoyang111222/cn-math-taxonomy">cn-math-taxonomy</a></td>'
         '<td>3297 知识点、13335 道题、课标、先修依赖；14 份年级笔记由此按年级抽取</td>'
         '<td><b>CC BY-NC 4.0</b>：个人学习/教学/研究免费，禁止商用，需署名</td></tr>',
         f'<tr><td>ima 个人知识库</td><td>{len(IMA_ITEMS)} 条真实教辅目录（课堂笔记、学霸笔记、状元笔记等）</td>'
         '<td>仅元数据：<code>FetchMediaContent</code> 对订阅库返回 220030，PDF 原件需在 ima 客户端查看</td></tr>',
         '<tr><td>教育部《3–6 岁儿童学习与发展指南》</td>'
         '<td>学前 4 页分龄目标与脑图骨架；PDF 原件 26.7 MB 已归档</td><td>公开文件</td></tr>',
         '<tr><td>GitHub <a href="https://github.com/JeetChan/mini-classroom">mini-classroom</a></td>'
         '<td>小学 1–2 年级数学 / 语文 / 基础英语互动站点，纯静态可离线打开</td><td>MIT</td></tr>',
         '</tbody></table>',
         '<h2>页面分工与去重设计</h2>',
         '<p>14 个年级各有 3 个页面，共 44 个 HTML（含总入口与来源页）。'
         '同一份实质正文只在其中一个页面出现，其它页面只放导航链接或结构名称：</p>',
         '<table><thead><tr><th>页面</th><th>独有内容</th><th>刻意不放</th></tr></thead><tbody>',
         '<tr><td>精讲页 <code>grade-XX.html</code></td>'
         '<td>知识结构统计表、学前发展目标全文、基础自测 20 道、三页导航</td>'
         '<td>知识点正文、进阶例题、教辅清单、脑图</td></tr>',
         '<tr><td>思维导图 <code>map-grade-XX.html</code></td>'
         '<td>放射状 SVG 脑图、章节树、知识点名称索引（锚点跳转）</td>'
         '<td>知识点正文、题目、教辅清单、发展目标全文</td></tr>',
         '<tr><td>完整笔记 <code>note-grade-XX.html</code></td>'
         '<td>全部知识点正文 + 掌握标准 + 自测题、进阶例题 40 道、ima 教辅清单</td>'
         '<td>基础自测 20 道、发展目标全文、结构统计表</td></tr>',
         '</tbody></table>',
         '<div class="note"><b>三类刻意处理过的重复</b>：'
         '① 精讲页原有「每科前 8 个知识点精讲」与笔记页全量正文重复 → 精讲页改为结构统计表；'
         '② 精讲页 20 道题与笔记页 60 道题重复 → 题目按 20 / 40 拆开，两页零交集；'
         '③ 学前 4 页共用同一组 6 个「一年级先修」知识点 → 按小班 / 中班 / 大班各 2 个切片，'
         '且发展目标全文只留在精讲页。<br>'
         '另外，脑图页只列知识点<b>名称</b>作为导航，不复制正文；'
         '总入口的来源表已精简为一句话并指向本页。'
         '<code>资料库/年级笔记/*.md</code> 是完整笔记的 Markdown 归档（同一份笔记的另一种格式），'
         '不属于站内页面重复。</div>',
         '<h2>本地归档位置</h2>',
         '<table><thead><tr><th>路径</th><th>说明</th></tr></thead><tbody>',
         '<tr><td><code>资料库/年级笔记/</code></td><td>14 份完整 Markdown 笔记</td></tr>',
         '<tr><td><code>资料库/ima索引/</code></td><td>总目录 JSON + 14 个年级子索引</td></tr>',
         '<tr><td><code>资料库/开源数据/</code></td><td>原始知识点 / 题库 / 课标 JSON、LICENSE、mini-classroom</td></tr>',
         '<tr><td><code>资料库/学前指南/3-6岁儿童学习与发展指南.pdf</code></td><td>指南 PDF 原件</td></tr>',
         '<tr><td><code>资料库/资料来源与许可.md</code></td><td>本页的 Markdown 版本</td></tr>',
         '</tbody></table>',
         '<div class="note"><b>版权提醒</b>：CC BY-NC 4.0 内容仅限个人学习、教学与研究，'
         '不得用于付费课程、售卖或机构收费服务；ima 内教辅 PDF 版权归原作者/出版社，'
         '请仅在个人学习范围内使用。</div>',
         '<div class="nav"><span><a href="index.html">← 返回总入口</a></span><span></span></div>']
    return page("资料来源与许可",
                '<span class="crumb">/ <a href="index.html">总入口</a> / 来源与许可</span>', b)
