# -*- coding: utf-8 -*-
"""「学霸笔记资料库」站点生成入口（可复现）。

拆分后的模块：
  site_core.py     常量 / 数据 / 样式 / 页面骨架 / 工具
  site_mindmap.py  放射状 SVG 脑图 + 树状知识地图
  site_pages.py    总入口 / 精讲页 / 思维导图页 / 来源页
  site_notes.py    完整笔记网页版 + Markdown 归档

运行：python _生成工具/build_site.py
只读 资料库/ 中已归档的数据，可反复重跑，覆盖生成 44 个 HTML、style.css 与 14 份 Markdown。
"""
from site_core import (CSS, GRADES, NOTES, ROOT, grade_questions, grade_topics,
                       ima_for)
from site_notes import build_note_html, build_note_md
from site_pages import (build_grade_html, build_index, build_map_html,
                        build_sources_html)


def main():
    (ROOT / "style.css").write_text(CSS, encoding="utf-8")
    counts = {}
    for g in GRADES:
        ts = grade_topics(g)
        qs = grade_questions(ts, 60)
        ima = ima_for(g["name"])
        counts[g["name"]] = (len(ts), len(qs), len(ima))
        (NOTES / f"{g['name']}.md").write_text(
            build_note_md(g, ts, qs, ima), encoding="utf-8")
        (ROOT / f"{g['slug']}.html").write_text(
            build_grade_html(g, ts, qs, ima), encoding="utf-8")
        (ROOT / f"map-{g['slug']}.html").write_text(
            build_map_html(g, ts), encoding="utf-8")
        (ROOT / f"note-{g['slug']}.html").write_text(
            build_note_html(g, ts, qs, ima), encoding="utf-8")
        print(f'{g["slug"]:<10} {g["name"]:<8} 知识点 {len(ts):>4}  '
              f'例题 {len(qs):>3}  教辅 {len(ima):>3}  三页已生成')
    (ROOT / "index.html").write_text(build_index(counts), encoding="utf-8")
    (ROOT / "sources.html").write_text(build_sources_html(), encoding="utf-8")
    print("index.html + sources.html 已生成；共 44 个 HTML 页面")


if __name__ == "__main__":
    main()
