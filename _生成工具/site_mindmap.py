# -*- coding: utf-8 -*-
"""思维导图生成：放射状 SVG 脑图 + 可折叠树状知识地图。

两者都只使用 topics.json 的真实 学科 / domain / chapter / name 层级，
脑图上只放「结构名称 + 数量」，知识点正文与题目一律不在脑图页重复出现。
"""
import math

from site_core import (COLORS, GUIDE, SUBJECT_ORDER, esc, structure)

W, H = 1240, 880
CX, CY = W / 2, H / 2
R1, R2 = 205, 382
FONT = "Microsoft YaHei,PingFang SC,Arial,sans-serif"


def short(s, n):
    s = str(s or "")
    return s if len(s) <= n else s[:n - 1] + "…"


def branches_for(g, ts):
    """返回 [(一级名, [(二级名, 数量), ...], 颜色, 一级总量), ...]"""
    out = []
    if ts:
        st = structure(ts)
        subs = [s for s in SUBJECT_ORDER + ["其他"] if st.get(s)]
        for i, sub in enumerate(subs):
            domains = st[sub]
            pairs = sorted(((d, sum(len(v) for v in chs.values()))
                            for d, chs in domains.items()), key=lambda x: -x[1])
            total = sum(n for _, n in pairs)
            # 每科最多 6 个分支，其余合并为一个「其他领域」节点
            if len(pairs) > 6:
                pairs = pairs[:5] + [("其他领域", sum(n for _, n in pairs[5:]))]
            out.append((sub, pairs, COLORS[i % len(COLORS)], total))
    else:
        for i, (domain, bands) in enumerate(GUIDE.items()):
            items = bands.get(g["band"], [])
            # 关键词索引：每条目标只取前 8 字，完整原文只在精讲页出现一次
            pairs = [(short(x, 8), 1) for x in items] or [("3 岁后参照指南", 1)]
            out.append((domain, pairs, COLORS[i % len(COLORS)], len(items)))
    return out


def radial_svg(g, branches, unit="个知识点", show_count=True,
               center_sub="知识思维导图"):
    """白底放射状脑图：中心=年级，内圈=学科/领域，外圈=知识领域/目标关键词"""
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
         f'width="{W}" height="{H}" role="img" aria-label="{esc(g["name"])} 思维导图">',
         f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
         f'<g font-family="{FONT}">']
    n = max(len(branches), 1)
    # 节点宽度按分支数自适应：分支越多，单个节点越窄，避免相邻节点重叠
    bw = min(168, max(96, 2 * R1 * math.sin(math.pi / n) * 0.88))
    max_chars = max(5, int(bw / 15))
    for i, (label, pairs, color, total) in enumerate(branches):
        a0 = -math.pi / 2 + 2 * math.pi * i / n
        x1, y1 = CX + R1 * math.cos(a0), CY + R1 * math.sin(a0)
        s.append(f'<line x1="{CX:.1f}" y1="{CY:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" '
                 f'stroke="{color}" stroke-width="2.4" opacity=".55"/>')
        spread = min(0.72, (2 * math.pi / n) * 0.44)
        m = max(len(pairs), 1)
        for j, (sub, cnt) in enumerate(pairs):
            a = a0 if m == 1 else a0 - spread + 2 * spread * j / (m - 1)
            x2, y2 = CX + R2 * math.cos(a), CY + R2 * math.sin(a)
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            qx, qy = CX + (mx - CX) * 1.10, CY + (my - CY) * 1.10
            s.append(f'<path d="M{x1:.1f} {y1:.1f} Q{qx:.1f} {qy:.1f} {x2:.1f} {y2:.1f}" '
                     f'fill="none" stroke="{color}" stroke-width="1.2" opacity=".45"/>')
            right = math.cos(a) >= 0
            anchor = "start" if right else "end"
            tx = x2 + (10 if right else -10)
            s.append(f'<circle cx="{x2:.1f}" cy="{y2:.1f}" r="3.6" fill="{color}"/>')
            suffix = f" · {cnt}" if show_count else ""
            s.append(f'<text x="{tx:.1f}" y="{y2 + 4:.1f}" text-anchor="{anchor}" '
                     f'font-size="14" fill="#333"><title>{esc(sub)}</title>'
                     f'{esc(short(sub, 12))}{suffix}</text>')
        bh = 46
        s.append(f'<rect x="{x1 - bw/2:.1f}" y="{y1 - bh/2:.1f}" width="{bw:.1f}" height="{bh}" '
                 f'rx="9" fill="#f7f9fd" stroke="{color}" stroke-width="1.8"/>')
        s.append(f'<text x="{x1:.1f}" y="{y1 - 3:.1f}" text-anchor="middle" '
                 f'font-size="16" font-weight="700" fill="#1c1c1c">'
                 f'{esc(short(label, max_chars))}</text>')
        s.append(f'<text x="{x1:.1f}" y="{y1 + 15:.1f}" text-anchor="middle" '
                 f'font-size="11" fill="#666">{total} {unit}</text>')

    s.append(f'<circle cx="{CX}" cy="{CY}" r="78" fill="#ffffff" stroke="#1552b8" stroke-width="2.6"/>')
    s.append(f'<text x="{CX}" y="{CY - 6}" text-anchor="middle" font-size="22" '
             f'font-weight="700" fill="#1c1c1c">{esc(g["name"])}</text>')
    s.append(f'<text x="{CX}" y="{CY + 20}" text-anchor="middle" font-size="13" '
             f'fill="#666">{esc(center_sub)}</text>')
    s.append('</g></svg>')
    return "".join(s)


def map_stats(g, ts):
    if not ts:
        return dict(subjects=len(GUIDE), domains=len(GUIDE), chapters=0, topics=0,
                    goals=sum(len(b.get(g["band"], [])) for b in GUIDE.values()))
    st = structure(ts)
    domains = sum(len(d) for d in st.values())
    chapters = sum(len(ch) for d in st.values() for ch in d.values())
    return dict(subjects=len(st), domains=domains, chapters=chapters,
                topics=len(ts), goals=0)


def tree_html(g, ts):
    """可折叠树状思维导图：学科 → 领域 → 章节 → 知识点名称（仅名称，链接到笔记正文）"""
    b = ['<div class="tree">']
    if not ts:
        for i, (domain, bands) in enumerate(GUIDE.items(), 1):
            items = bands.get(g["band"], [])
            b.append(f'<details><summary>{esc(domain)} · {len(items)} 条分龄目标</summary>')
            if not items:
                b.append('<div class="leaf">0–3 岁不在指南覆盖范围，3 岁后参照下列领域目标</div>')
            for j, item in enumerate(items, 1):
                b.append(f'<div class="leaf"><a href="{g["slug"]}.html#d{i}-{j}">'
                         f'{esc(short(item, 20))}…（全文见精讲页）</a></div>')
            b.append('</details>')
        b.append('</div>')
        return "".join(b)

    st = structure(ts)
    for sub in SUBJECT_ORDER + ["其他"]:
        domains = st.get(sub)
        if not domains:
            continue
        n_sub = sum(len(v) for chs in domains.values() for v in chs.values())
        n_ch = sum(len(chs) for chs in domains.values())
        b.append(f'<details><summary><b>{esc(sub)}</b> · {n_sub} 个知识点 / '
                 f'{len(domains)} 个领域 / {n_ch} 章</summary>')
        for dom, chs in sorted(domains.items(), key=lambda x: -sum(len(v) for v in x[1].values())):
            n_dom = sum(len(v) for v in chs.values())
            b.append(f'<details><summary>{esc(dom)} · {n_dom} 个知识点 / {len(chs)} 章</summary>')
            for ch, items in chs.items():
                b.append(f'<details><summary title="{esc(ch)}">{esc(short(ch, 34))} '
                         f'· {len(items)} 个</summary>')
                for t in items:
                    b.append(f'<div class="leaf"><a href="note-{g["slug"]}.html#kp-{esc(t["id"])}">'
                             f'{esc(t["name"])}</a></div>')
                b.append('</details>')
            b.append('</details>')
        b.append('</details>')
    b.append('</div>')
    return "".join(b)
