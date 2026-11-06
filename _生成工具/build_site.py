# -*- coding: utf-8 -*-
"""
生成「学霸笔记资料库」静态站点：
  总入口 index.html + 14 个年级子页 grade-01..14.html + style.css
  同时为每个年级产出一份完整 Markdown 笔记到 资料库/年级笔记/
内容来源：
  - GitHub 开源 cn-math-taxonomy（CC BY-NC 4.0）真实知识点 / 题库
  - 教育部《3-6岁儿童学习与发展指南》公开分龄目标
  - ima 个人知识库检索到的真实教辅目录元数据
"""
import html
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(r"E:\小学到高中学霸资料")
LIB = ROOT / "资料库"
OPEN = LIB / "开源数据"
NOTES = LIB / "年级笔记"
NOTES.mkdir(parents=True, exist_ok=True)

TOPICS = json.loads((OPEN / "topics.json").read_text(encoding="utf-8"))
QUESTIONS = json.loads((OPEN / "questions.json").read_text(encoding="utf-8"))
IMA_ALL = json.loads((LIB / "ima索引" / "ima资料目录.json").read_text(encoding="utf-8"))
IMA_ITEMS = IMA_ALL["条目"]

Q_BY_TOPIC = defaultdict(list)
for q in QUESTIONS:
    Q_BY_TOPIC[q.get("topicId", "")].append(q)

SUBJECT = {
    "cnm": "数学", "cnc": "语文", "cne": "英语", "cnp": "物理",
    "cns": "科学", "cnd": "道德与法治", "cnh": "历史", "cng": "地理",
    "cnb": "生物", "cnk": "化学",
}
SUBJECT_ORDER = ["数学", "语文", "英语", "科学", "道德与法治", "物理", "化学",
                 "生物", "历史", "地理"]

GRADES = [
    dict(n=1, slug="grade-01", name="幼儿0-3岁", stage="学前期", age="0–3 岁", tg=[], band=None,
         desc="亲子启蒙期。以感官、动作、语言与社会性发展为主，不适宜学科化训练。"),
    dict(n=2, slug="grade-02", name="小班", stage="学前期", age="3–4 岁", tg=[], band="3~4岁",
         desc="幼儿园小班，对应《3–6 岁儿童学习与发展指南》3~4 岁发展目标。"),
    dict(n=3, slug="grade-03", name="中班", stage="学前期", age="4–5 岁", tg=[], band="4~5岁",
         desc="幼儿园中班，对应指南 4~5 岁发展目标。"),
    dict(n=4, slug="grade-04", name="大班", stage="学前期", age="5–6 岁", tg=[], band="5~6岁",
         desc="幼儿园大班 / 幼小衔接，对应指南 5~6 岁发展目标。"),
    dict(n=5, slug="grade-05", name="一年级", stage="小学", age="6–7 岁", tg=[1], band=None, desc="小学起点：识字、拼音、20 以内加减与入学适应。"),
    dict(n=6, slug="grade-06", name="二年级", stage="小学", age="7–8 岁", tg=[2], band=None, desc="巩固字词与表内乘除，建立阅读与书写习惯。"),
    dict(n=7, slug="grade-07", name="三年级", stage="小学", age="8–9 岁", tg=[3], band=None, desc="英语起步、作文起步，数学进入多位数运算与分数初步。"),
    dict(n=8, slug="grade-08", name="四年级", stage="小学", age="9–10 岁", tg=[4], band=None, desc="从具象到抽象的关键转折：运算律、段落阅读、科学探究。"),
    dict(n=9, slug="grade-09", name="五年级", stage="小学", age="10–11 岁", tg=[5], band=None, desc="小数分数方程、说明文与记叙文阅读，为小升初打底。"),
    dict(n=10, slug="grade-10", name="六年级", stage="小学", age="11–12 岁", tg=[6], band=None, desc="小学总复习：比例、百分数、综合运用与初中先修衔接。"),
    dict(n=11, slug="grade-11", name="初一", stage="初中", age="12–13 岁", tg=[7], band=None, desc="七年级：有理数、整式、文言文起步，学科数量骤增。"),
    dict(n=12, slug="grade-12", name="初二", stage="初中", age="13–14 岁", tg=[8], band=None, desc="八年级：物理开课、几何证明与函数入门，分化最明显的一年。"),
    dict(n=13, slug="grade-13", name="初三", stage="初中", age="14–15 岁", tg=[9], band=None, desc="九年级：化学开课 + 中考总复习，知识体系收口。"),
    dict(n=14, slug="grade-14", name="高中", stage="高中", age="15–18 岁", tg=list(range(10, 17)), band=None,
         desc="高中必修与选择性必修：函数、导数、力学、电磁学、有机化学与高考综合。"),
]

# 教育部《3-6岁儿童学习与发展指南》公开分龄目标（据指南原文整理）
GUIDE = {
    "健康·动作发展": {
        "3~4岁": ["能沿地面直线或在较窄的低矮物体上走一段距离", "能双脚灵活交替上下楼梯",
                 "能身体平稳地双脚连续向前跳", "能双手向上抛球", "能双手抓杠悬空吊起 10 秒左右"],
        "4~5岁": ["能在较窄的低矮物体上平稳地走一段距离", "能以匍匐、膝盖悬空等多种方式钻爬",
                 "能助跑跨跳过一定距离或高度的物体", "能连续自抛自接球", "能双手抓杠悬空吊起 15 秒左右"],
        "5~6岁": ["能在斜坡、荡桥和有一定间隔的物体上较平稳地行走", "能以手脚并用方式安全地爬攀登架",
                 "能连续跳绳、连续拍球", "能躲避他人滚过来的球", "能双手抓杠悬空吊起 20 秒左右"],
    },
    "语言·表达与阅读": {
        "3~4岁": ["愿意在熟悉的人面前说话，能大方地与人打招呼", "能口齿清楚地说儿歌、童谣或复述简短故事",
                 "能听懂短小的儿歌或故事", "会看画面，说出图中有什么、发生了什么",
                 "经常主动要求成人讲故事、读图书"],
        "4~5岁": ["愿意与他人交谈，喜欢谈论自己感兴趣的话题", "能基本完整地讲述自己的所见所闻",
                 "能大体讲出所听故事的主要内容", "能根据连续画面大致说出故事情节",
                 "喜欢把听过的故事讲给别人听"],
        "5~6岁": ["愿意与他人讨论问题，敢在众人面前说话", "能有序、连贯、清楚地讲述一件事情",
                 "能说出所阅读作品的主要内容", "能根据画面线索猜想情节发展或续编故事",
                 "对看过的图书能说出自己的看法"],
    },
    "社会·人际交往": {
        "3~4岁": ["愿意和小朋友一起游戏", "愿意与熟悉的长辈一起活动",
                 "想加入同伴游戏时能友好地提出请求", "在成人指导下不争抢、不独霸玩具"],
        "4~5岁": ["喜欢和小朋友一起游戏，有经常一起玩的小伙伴", "会运用介绍自己、交换玩具等技巧加入游戏",
                 "对大家都喜欢的东西能轮流、分享", "活动时愿意接受同伴的意见和建议"],
        "5~6岁": ["有自己的好朋友，也喜欢结交新朋友", "有问题愿意向别人请教",
                 "活动时能与同伴分工合作，遇到困难一起克服", "与同伴发生冲突时能自己协商解决"],
    },
    "科学·数学认知": {
        "3~4岁": ["感知和发现周围物体的形状是多种多样的", "体验和发现生活中很多地方都用到数",
                 "能感知和区分大小、多少、高矮长短并会用相应词表示", "能通过一一对应比较两组物体的多少",
                 "能手口一致地点数 5 个以内物体并说出总数"],
        "4~5岁": ["在指导下感知有些事物可以用形状或数来描述", "能感知和区分粗细、厚薄、轻重",
                 "能通过数数比较两组物体的多少", "能通过实际操作理解数与数之间的关系（如 5 比 4 多 1）",
                 "会用数词描述事物的排列顺序和位置"],
        "5~6岁": ["能发现事物简单的排列规律并尝试创造新规律", "初步理解量的相对性",
                 "借助实际情境理解「加」和「减」的实际意义", "能通过实物操作进行 10 以内加减运算",
                 "能用简单记录表、统计图表示数量关系"],
    },
    "科学·探究与艺术表现": {
        "3~4岁": ["对感兴趣的事物能仔细观察，发现其明显特征", "能用笔涂涂画画",
                 "能熟练地用勺子吃饭", "能用剪刀沿直线剪，边线基本吻合", "喜欢听音乐或观看舞蹈、戏剧等表演"],
        "4~5岁": ["能对事物或现象进行观察比较，发现其相同与不同", "能沿边线较直地画出简单图形",
                 "会用筷子吃饭", "能沿轮廓线剪出由直线构成的简单图形", "能用绘画、手工制作表现观察到的事物"],
        "5~6岁": ["能通过观察、比较与分析发现并描述不同种类物体的特征",
                 "能用一定的方法验证自己的猜测", "能根据需要画出图形，线条基本平滑",
                 "能沿轮廓线剪出由曲线构成的简单图形", "能用多种工具、材料或不同表现手法表达自己的感受"],
    },
}

STAMP = datetime.now().strftime("%Y-%m-%d %H:%M")

CSS = """* { box-sizing: border-box; }
body { margin:0; background:#fff; color:#1c1c1c; font:16px/1.75 -apple-system,"Microsoft YaHei","PingFang SC",Arial,sans-serif; }
a { color:#1552b8; text-decoration:none; }
a:hover { text-decoration:underline; }
.wrap { max-width:1080px; margin:0 auto; padding:0 24px 80px; }
header.top { border-bottom:1px solid #e8e8e8; background:#fff; }
.top .wrap { padding-top:18px; padding-bottom:18px; display:flex; align-items:center; gap:18px; flex-wrap:wrap; }
.brand { font-size:19px; font-weight:700; color:#111; }
.brand small { font-weight:400; color:#777; font-size:13px; margin-left:8px; }
.crumb { color:#666; font-size:14px; }
.crumb a { margin:0 4px; }
.hero { padding:38px 0 22px; border-bottom:1px solid #eee; margin-bottom:28px; }
.hero h1 { font-size:34px; margin:0 0 8px; letter-spacing:1px; }
.hero .meta { color:#666; font-size:14px; }
.hero p.lead { margin:14px 0 0; color:#333; max-width:820px; }
.stats { display:flex; gap:12px; flex-wrap:wrap; margin-top:20px; }
.stat { border:1px solid #e3e8f2; background:#f7f9fd; border-radius:8px; padding:10px 16px; min-width:120px; }
.stat b { display:block; font-size:22px; color:#1552b8; line-height:1.3; }
.stat span { font-size:12px; color:#666; }
h2 { font-size:21px; margin:38px 0 14px; padding-bottom:8px; border-bottom:2px solid #eee; }
h3 { font-size:17px; margin:26px 0 10px; color:#223; }
.groups { display:grid; grid-template-columns:repeat(auto-fill,minmax(300px,1fr)); gap:18px; }
.card { border:1px solid #e5e5e5; border-radius:8px; padding:16px 18px; background:#fff; }
.card h4 { margin:0 0 10px; font-size:16px; color:#1552b8; }
.kp { border-left:3px solid #dbe6fb; padding:6px 0 6px 12px; margin:10px 0; }
.kp b { display:block; font-size:15px; }
.kp .ch { color:#888; font-size:12px; }
.kp .ds { color:#444; font-size:14px; margin-top:3px; }
.kp .mc { color:#555; font-size:13px; margin-top:4px; }
.kp .dq { color:#7a4a00; background:#fff8ea; border-radius:4px; padding:5px 8px; font-size:13px; margin-top:6px; }
details.q { border:1px solid #e8e8e8; border-radius:6px; padding:9px 13px; margin:8px 0; background:#fcfcfc; }
details.q summary { cursor:pointer; font-size:15px; }
details.q .ans { margin-top:8px; padding-top:8px; border-top:1px dashed #ddd; font-size:14px; color:#333; }
details.q .ans b { color:#0a7a3d; }
table { border-collapse:collapse; width:100%; font-size:14px; }
th,td { border:1px solid #e2e2e2; padding:8px 10px; text-align:left; vertical-align:top; }
th { background:#f6f8fc; }
code { background:#f3f3f3; padding:1px 5px; border-radius:3px; font-size:13px; word-break:break-all; }
.grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(210px,1fr)); gap:14px; }
.gcard { border:1px solid #e3e8f2; border-radius:8px; padding:16px; background:#fff; display:block; color:#1c1c1c; }
.gcard:hover { border-color:#1552b8; text-decoration:none; box-shadow:0 2px 10px rgba(21,82,184,.10); }
.gcard .nm { font-size:19px; font-weight:700; }
.gcard .st { color:#1552b8; font-size:12px; }
.gcard .num { color:#666; font-size:13px; margin-top:8px; }
.stage { margin:30px 0 12px; font-size:16px; font-weight:700; border-left:4px solid #1552b8; padding-left:10px; }
.nav { display:flex; justify-content:space-between; gap:12px; margin:34px 0 10px; padding-top:18px; border-top:1px solid #eee; font-size:14px; }
footer { color:#777; font-size:13px; border-top:1px solid #eee; margin-top:30px; padding-top:18px; }
.note { background:#fff8f2; border-left:4px solid #e8792b; padding:12px 16px; font-size:14px; margin:16px 0; border-radius:4px; }
.search { padding:9px 13px; border:1px solid #ccc; border-radius:6px; width:280px; font-size:14px; }
"""

PAGE = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__ · 学霸笔记资料库</title>
<link rel="stylesheet" href="style.css"></head><body>
<header class="top"><div class="wrap">
<a class="brand" href="index.html">📚 学霸笔记资料库</a><span class="brand small" style="font-weight:400;color:#777;font-size:13px">幼儿0-3岁 → 高中 · 14 个年级</span>
<span class="crumb">__CRUMB__</span>
</div></header>
<div class="wrap">
__BODY__
<footer>
资料来源：GitHub 开源 <a href="https://github.com/xiaoyang111222/cn-math-taxonomy">cn-math-taxonomy</a>（CC BY-NC 4.0，个人学习/教学免费，禁止商用）·
教育部《3–6 岁儿童学习与发展指南》· ima 个人知识库目录元数据。<br>
ima 内教辅 PDF 版权归原作者，仅归档目录信息；本页知识点与题目均取自开源项目真实数据，未虚构。生成时间：__STAMP__。
</footer>
</div></body></html>"""


def esc(s):
    return html.escape(str(s or "").strip())


def subj_of(t):
    pre = t["id"].split("_")[0]
    return SUBJECT.get(pre, "其他")


def size_txt(n):
    if not n:
        return "—"
    return f"{n/1048576:.1f} MB" if n >= 1048576 else f"{n/1024:.0f} KB"


def grade_topics(g):
    if not g["tg"]:
        return []
    return [t for t in TOPICS if t.get("grade") in g["tg"]]


def grade_questions(ts, limit=60):
    out = []
    for t in ts:
        for q in Q_BY_TOPIC.get(t["id"], [])[:2]:
            out.append((t, q))
            if len(out) >= limit:
                return out
    return out


def ima_for(name):
    return [i for i in IMA_ITEMS if name in i.get("grades", [])]


def topic_block(t, with_q=True):
    mc = t.get("mastery_criteria") or []
    dq = t.get("diagnostic_question") or {}
    s = f'<div class="kp"><b>{esc(t.get("name"))}</b>'
    if t.get("chapter"):
        s += f'<div class="ch">{esc(t["chapter"])}</div>'
    if t.get("description"):
        s += f'<div class="ds">{esc(t["description"])}</div>'
    if mc:
        s += '<div class="mc">掌握标准：' + esc("；".join(mc[:3])) + '</div>'
    if with_q and dq.get("question"):
        s += f'<div class="dq">自测：{esc(dq["question"])}　答：{esc(dq.get("answer",""))}</div>'
    return s + "</div>"


def build_note_md(g, ts, qs, ima):
    """完整年级笔记 Markdown（归档用，内容全量）"""
    L = [f"# {g['name']} · 学霸笔记", "",
         f"- 学段：{g['stage']}　|　年龄段：{g['age']}　|　生成时间：{STAMP}",
         f"- 知识点：{len(ts)} 个　|　例题：{len(qs)} 道　|　ima 教辅索引：{len(ima)} 条", "",
         "> 知识点、掌握标准、自测题与例题解析均来自 GitHub 开源项目 "
         "`xiaoyang111222/cn-math-taxonomy`（CC BY-NC 4.0），按年级抽取，未改写题目内容。", ""]

    if g["band"] is None and g["n"] == 1:
        L += ["## 说明", "",
              "0–3 岁不在《3–6 岁儿童学习与发展指南》的覆盖范围内（该指南自 3 岁起）。",
              "此阶段属亲子启蒙期，请以国家儿童保健体检与儿保医师评估为准，",
              "不适宜进行学科化训练或「学霸笔记」式刷题。", "",
              "可参照的公开材料：", "",
              "- 本站归档《3–6 岁儿童学习与发展指南》PDF（相邻年龄段，用于了解后续发展阶梯）",
              "- `开源数据/mini-classroom/` 中的基础英语与数学启蒙站点（MIT）", "",
              "启蒙方向建议：亲子共读、儿歌与韵律、感官与精细动作游戏、稳定的生活作息与语言互动。", ""]
    elif g["band"]:
        L += ["## 发展目标（教育部《3–6 岁儿童学习与发展指南》分龄要点）", ""]
        for domain, bands in GUIDE.items():
            L += [f"### {domain} · {g['band']}", ""]
            for x in bands.get(g["band"], []):
                L.append(f"- {x}")
            L.append("")
        L += ["原件：`资料库/学前指南/3-6岁儿童学习与发展指南.pdf`（26.7 MB，联合国儿童基金会中国站公开版）。", ""]

    if g["stage"] == "学前期":
        base = "资料库/开源数据/mini-classroom/mini-classroom-main/"
        L += ["## 已归档启蒙资源（可离线打开）", "",
              "- `资料库/学前指南/3-6岁儿童学习与发展指南.pdf` —— 教育部指南公开 PDF（26.7 MB）",
              f"- `{base}math-grade1-2-workshop/index.html` —— 小学数学 1–2 年级 23 个知识点",
              f"- `{base}chinese-grade1-site/index.html` —— 小学语文一年级 6 大模块",
              f"- `{base}basic-english-workshop/index.html` —— 基础英语工坊 30 单元",
              f"- `{base}basic-english-site/index.html` —— 基础英语 850 词",
              "",
              "以上 mini-classroom 为 MIT 许可开源项目，纯静态、无需联网。", "",
              "## 幼小衔接：一年级先修知识点预览", "",
              "> 取自开源知识图谱一年级真实数据，仅供了解后续学习阶梯；学前期不建议提前刷题。", ""]
        for t in [x for x in TOPICS
                  if x.get("grade") == 1 and x["id"].startswith(("cnm", "cnc"))][:8]:
            L.append(f"- **{t.get('name','')}**：{t.get('description','')}")
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
                L.append(f"#### {t.get('name','')}")
                if t.get("chapter"):
                    L.append(f"*章节：{t['chapter']}*")
                if t.get("description"):
                    L.append("")
                    L.append(t["description"])
                mc = t.get("mastery_criteria") or []
                if mc:
                    L += ["", "**掌握标准**", ""] + [f"- {x}" for x in mc]
                dq = t.get("diagnostic_question") or {}
                if dq.get("question"):
                    L += ["", f"**自测**：{dq['question']}　**答**：{dq.get('answer','')}"]
                L.append("")

    if qs:
        L += ["## 典型例题与解析", ""]
        for i, (t, q) in enumerate(qs, 1):
            L += [f"### {i}. {q.get('prompt','')}", "",
                  f"- 所属知识点：{t.get('name','')}（{subj_of(t)}）",
                  f"- **答案**：{q.get('answer','')}"]
            if q.get("explanation"):
                L.append(f"- **解析**：{q['explanation']}")
            L.append("")

    if ima:
        L += ["## ima 知识库 · 本年级教辅原件索引", "",
              "> 仅元数据：ima MCP 对订阅库不提供正文/原件下载（返回 220030）。原件请在 ima 客户端打开。", "",
              "| 资料名 | 类型 | 大小 | 所属文件夹 |", "|---|---|---|---|"]
        for i in ima[:40]:
            L.append(f"| {i['title']} | {i['type']} | {size_txt(i['size_bytes'])} | {i['folder']} |")
        L.append("")

    return "\n".join(L)


def build_grade_html(g, ts, qs, ima):
    by = defaultdict(list)
    for t in ts:
        by[subj_of(t)].append(t)

    stats = "".join(
        f'<div class="stat"><b>{v}</b><span>{k}</span></div>'
        for k, v in [("知识点", len(ts)), ("例题", len(qs)), ("ima 教辅", len(ima)),
                     ("学科", len([s for s in by if by[s]]))]
    )

    b = [f'<div class="hero"><h1>{esc(g["name"])}</h1>',
         f'<div class="meta">{esc(g["stage"])} · {esc(g["age"])} · 第 {g["n"]} / 14 站</div>',
         f'<p class="lead">{esc(g["desc"])}</p>',
         f'<div class="stats">{stats}</div></div>']

    if g["n"] == 1:
        b += ['<div class="note"><b>关于 0–3 岁</b>：教育部《3–6 岁儿童学习与发展指南》自 3 岁起，'
              '本阶段不设学科知识点与刷题内容。请以儿保体检与医师评估为准，'
              '本站归档的指南 PDF 可用于了解 3 岁后的发展阶梯。</div>']
    elif g["band"]:
        b += ['<h2>发展目标 · ' + esc(g["band"]) + '</h2>',
              '<p style="color:#666;font-size:14px">以下为教育部《3–6 岁儿童学习与发展指南》分龄目标原文要点整理，'
              'PDF 原件已归档于 <code>资料库/学前指南/</code>。</p>', '<div class="groups">']
        for domain, bands in GUIDE.items():
            items = bands.get(g["band"], [])
            b.append(f'<div class="card"><h4>{esc(domain)}</h4><ul style="margin:0;padding-left:20px;font-size:14px">')
            b += [f'<li>{esc(x)}</li>' for x in items]
            b.append('</ul></div>')
        b.append('</div>')

    if g["stage"] == "学前期":
        g1 = [t for t in TOPICS
              if t.get("grade") == 1 and t["id"].startswith(("cnm", "cnc"))][:6]
        base = "资料库/开源数据/mini-classroom/mini-classroom-main/"
        b += ['<h2>启蒙资源与幼小衔接</h2>', '<div class="groups">',
              '<div class="card"><h4>已归档 · 可离线直接打开</h4>',
              '<ul style="margin:0;padding-left:20px;font-size:14px">',
              '<li><code>资料库/学前指南/3-6岁儿童学习与发展指南.pdf</code>'
              '（26.7 MB，权威分龄目标；PDF 请在资源管理器打开）</li>',
              f'<li><a href="{base}math-grade1-2-workshop/index.html">小学数学 1–2 年级互动站</a>（23 个知识点，MIT）</li>',
              f'<li><a href="{base}chinese-grade1-site/index.html">小学语文一年级站</a>（6 大模块，MIT）</li>',
              f'<li><a href="{base}basic-english-workshop/index.html">基础英语工坊</a>（30 单元，MIT）</li>',
              f'<li><a href="{base}basic-english-site/index.html">基础英语 850 词</a>（MIT）</li>',
              '</ul></div>',
              '<div class="card"><h4>下一站：一年级先修知识点预览</h4>',
              '<p style="color:#777;font-size:13px">取自开源知识图谱一年级真实数据，'
              '仅供了解后续学习阶梯，学前期不建议提前刷题。</p>']
        for t in g1:
            b.append(topic_block(t, with_q=False))
        b.append('</div></div>')

    if ts:
        b += ['<h2>学霸笔记 · 知识点精讲</h2>',
              f'<p style="color:#666;font-size:14px">共 {len(ts)} 个知识点，按学科分组。'
              '页面展示每科前 8 个，<b>完整笔记见本页底部归档的 Markdown 文件</b>。</p>']
        for sub in SUBJECT_ORDER + ["其他"]:
            group = by.get(sub, [])
            if not group:
                continue
            b += [f'<h3>{esc(sub)}　<span style="font-weight:400;font-size:13px;color:#888">{len(group)} 个知识点</span></h3>',
                  '<div class="groups">']
            for chunk_i in range(0, min(len(group), 8), 4):
                b.append('<div class="card">')
                for t in group[chunk_i:chunk_i + 4]:
                    b.append(topic_block(t))
                b.append('</div>')
            b.append('</div>')

    if qs:
        b += ['<h2>典型例题与解析</h2>',
              f'<p style="color:#666;font-size:14px">从开源题库按本年级知识点抽取 {len(qs)} 道，'
              '点击展开答案与解析。</p>']
        for i, (t, q) in enumerate(qs[:20], 1):
            b += ['<details class="q"><summary>' + f'{i}. {esc(q.get("prompt",""))}'
                  + f'　<span style="color:#888;font-size:12px">[{esc(subj_of(t))}·{esc(t.get("name",""))}]</span></summary>',
                  '<div class="ans"><b>答案：</b>' + esc(q.get("answer", ""))]
            if q.get("explanation"):
                b.append('<br><b>解析：</b>' + esc(q["explanation"]))
            b.append('</div></details>')

    if ima:
        b += ['<h2>ima 知识库 · 本年级教辅原件索引</h2>',
              '<div class="note">以下为老师 ima 账号内可检索到的真实教辅文件目录（共 '
              + str(len(ima)) + ' 条，展示前 12 条）。'
              'ima 连接器对订阅库不提供正文/原件下载（返回 220030），'
              '因此这里只归档<strong>文件名、大小、所属学科文件夹与目录摘录</strong>；'
              'PDF 原件请在 ima 客户端内打开。</div>',
              '<table><thead><tr><th>资料名</th><th>类型</th><th>大小</th><th>所属文件夹 / 目录摘录</th></tr></thead><tbody>']
        for i in ima[:12]:
            snippet = (i.get("intro") or i.get("highlight") or "").replace("\n", " ")[:110]
            b.append('<tr><td>' + esc(i["title"]) + '</td><td>' + esc(i["type"]) + '</td><td>'
                     + size_txt(i["size_bytes"]) + '</td><td>' + esc(i["folder"])
                     + '<br><span style="color:#888;font-size:12px">' + esc(snippet) + '</span></td></tr>')
        b.append('</tbody></table>')

    b += ['<h2>本年级归档文件</h2>', '<table><thead><tr><th>文件</th><th>说明</th></tr></thead><tbody>',
          f'<tr><td><a href="note-{g["slug"]}.html">完整笔记 · 网页版</a></td>'
          f'<td>全部 {len(ts)} 个知识点 + {len(qs)} 道例题解析 + 教辅索引，点击直接阅读</td></tr>',
          f'<tr><td><code>资料库/年级笔记/{esc(g["name"])}.md</code></td>'
          '<td>同内容 Markdown 归档（预览面板不提供 .md，请在资源管理器打开）</td></tr>',
          f'<tr><td><a href="资料库/ima索引/{esc(g["name"])}.json">{esc(g["name"])}.json</a></td>'
          '<td>该年级 ima 资料目录元数据</td></tr>',
          '<tr><td><a href="资料库/开源数据/topics.json">开源数据/topics.json</a></td>'
          '<td>3297 个知识点原始数据（CC BY-NC 4.0）</td></tr>',
          '<tr><td><a href="sources.html">资料来源与许可（网页版）</a></td>'
          '<td>全部来源、许可与版权说明</td></tr>', '</tbody></table>']

    prevg = GRADES[g["n"] - 2] if g["n"] > 1 else None
    nextg = GRADES[g["n"]] if g["n"] < len(GRADES) else None
    b.append('<div class="nav"><span>')
    if prevg:
        b.append(f'← 上一站：<a href="{prevg["slug"]}.html">{esc(prevg["name"])}</a>')
    b.append('</span><span><a href="index.html">返回总入口</a>　')
    if nextg:
        b.append(f'下一站：<a href="{nextg["slug"]}.html">{esc(nextg["name"])}</a> →')
    b.append('</span></div>')

    crumb = f'<span class="crumb">/ <a href="index.html">总入口</a> / {esc(g["stage"])} / {esc(g["name"])}</span>'
    return (PAGE.replace("__TITLE__", esc(g["name"]))
                .replace("__CRUMB__", crumb)
                .replace("__BODY__", "\n".join(b))
                .replace("__STAMP__", STAMP))


def build_note_html(g, ts, qs, ima):
    """完整年级笔记的 HTML 版（预览面板可打开；.md 仅作本地归档）"""
    b = [f'<div class="hero"><h1>{esc(g["name"])} · 完整学霸笔记</h1>',
         f'<div class="meta">{esc(g["stage"])} · {esc(g["age"])} · '
         f'知识点 {len(ts)} 个 / 例题 {len(qs)} 道 / ima 教辅索引 {len(ima)} 条</div>',
         '<p class="lead">本页为该年级全量笔记：知识点精讲、掌握标准、自测题、例题解析与教辅索引。'
         '同名 Markdown 版本归档于 <code>资料库/年级笔记/</code>，便于本地打印与二次编辑。</p>',
         f'<div class="nav" style="margin-top:18px;border:0;padding:0">'
         f'<span><a href="{g["slug"]}.html">← 返回 {esc(g["name"])} 精讲页</a></span>'
         f'<span><a href="index.html">总入口</a></span></div></div>']

    if g["n"] == 1:
        b += ['<div class="note"><b>关于 0–3 岁</b>：此阶段不在《3–6 岁儿童学习与发展指南》覆盖范围，'
              '不设学科知识点与刷题内容，请以儿保体检与医师评估为准。</div>']
    if g["band"]:
        b += [f'<h2>发展目标 · {esc(g["band"])}</h2>', '<div class="groups">']
        for domain, bands in GUIDE.items():
            b.append(f'<div class="card"><h4>{esc(domain)}</h4><ul style="margin:0;padding-left:20px;font-size:14px">')
            b += [f'<li>{esc(x)}</li>' for x in bands.get(g["band"], [])]
            b.append('</ul></div>')
        b.append('</div>')

    if ts:
        by = defaultdict(list)
        for t in ts:
            by[subj_of(t)].append(t)
        b += ['<h2>知识点精讲（全量）</h2>']
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

    if qs:
        b += ['<h2>例题与解析（全量）</h2>']
        for i, (t, q) in enumerate(qs, 1):
            b += ['<details class="q"><summary>' + f'{i}. {esc(q.get("prompt",""))}'
                  + f'　<span style="color:#888;font-size:12px">[{esc(subj_of(t))}·{esc(t.get("name",""))}]</span></summary>',
                  '<div class="ans"><b>答案：</b>' + esc(q.get("answer", ""))]
            if q.get("explanation"):
                b.append('<br><b>解析：</b>' + esc(q["explanation"]))
            b.append('</div></details>')

    if ima:
        b += ['<h2>ima 教辅原件索引</h2>',
              '<div class="note">仅元数据，原件请在 ima 客户端打开。</div>',
              '<table><thead><tr><th>资料名</th><th>类型</th><th>大小</th><th>文件夹</th></tr></thead><tbody>']
        for i in ima[:40]:
            b.append('<tr><td>' + esc(i["title"]) + '</td><td>' + esc(i["type"]) + '</td><td>'
                     + size_txt(i["size_bytes"]) + '</td><td>' + esc(i["folder"]) + '</td></tr>')
        b.append('</tbody></table>')

    b += ['<div class="nav"><span><a href="index.html">← 总入口</a></span>'
          f'<span><a href="{g["slug"]}.html">{esc(g["name"])} 精讲页 →</a></span></div>']
    crumb = (f'<span class="crumb">/ <a href="index.html">总入口</a> / '
             f'<a href="{g["slug"]}.html">{esc(g["name"])}</a> / 完整笔记</span>')
    return (PAGE.replace("__TITLE__", esc(g["name"]) + " 完整笔记")
                .replace("__CRUMB__", crumb)
                .replace("__BODY__", "\n".join(b))
                .replace("__STAMP__", STAMP))


def build_sources_html():
    b = ['<div class="hero"><h1>资料来源与许可</h1>',
         '<p class="lead">本目录所有内容均来自可公开获取的资料，或老师本人 ima 账号内可见的资料目录。</p></div>',
         '<h2>来源一览</h2>',
         '<table><thead><tr><th>来源</th><th>内容</th><th>许可 / 限制</th></tr></thead><tbody>',
         '<tr><td>GitHub <a href="https://github.com/xiaoyang111222/cn-math-taxonomy">cn-math-taxonomy</a></td>'
         '<td>3297 知识点、13335 道题、课标、先修依赖；14 份年级笔记由此按年级抽取</td>'
         '<td><b>CC BY-NC 4.0</b>：个人学习/教学/研究免费，禁止商用，需署名</td></tr>',
         f'<tr><td>ima 个人知识库</td><td>{len(IMA_ITEMS)} 条真实教辅目录（课堂笔记、学霸笔记、状元笔记等）</td>'
         '<td>仅元数据：<code>FetchMediaContent</code> 对订阅库返回 220030，PDF 原件需在 ima 客户端查看</td></tr>',
         '<tr><td>教育部《3–6 岁儿童学习与发展指南》</td>'
         '<td>学前 4 页分龄目标；PDF 原件 26.7 MB 已归档</td><td>公开文件</td></tr>',
         '<tr><td>GitHub <a href="https://github.com/JeetChan/mini-classroom">mini-classroom</a></td>'
         '<td>小学 1–2 年级数学 / 语文 / 基础英语互动站点，纯静态可离线打开</td><td>MIT</td></tr>',
         '</tbody></table>',
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
    return (PAGE.replace("__TITLE__", "资料来源与许可")
                .replace("__CRUMB__", '<span class="crumb">/ <a href="index.html">总入口</a> / 来源与许可</span>')
                .replace("__BODY__", "\n".join(b))
                .replace("__STAMP__", STAMP))


def build_index(counts):
    total_kp = sum(c[0] for c in counts.values())
    total_q = sum(c[1] for c in counts.values())
    total_lib = sum(1 for _ in (LIB / "开源数据").rglob("*") if _.is_file())
    b = ['<div class="hero"><h1>📚 学霸笔记资料库</h1>',
         '<div class="meta">幼儿 0–3 岁 → 小班 / 中班 / 大班 → 小学 1–6 年级 → 初中 3 年 → 高中，共 14 个年级子站</div>',
         '<p class="lead">每个年级一个独立子网页：按学科整理<strong>真实知识点、掌握标准、自测题与例题解析</strong>，'
         '并附老师 ima 知识库里对应年级的教辅原件索引。内容取自开源知识图谱与教育部公开指南，不是空链接目录。</p>',
         '<div class="stats">'
         + "".join(f'<div class="stat"><b>{v}</b><span>{k}</span></div>' for k, v in
                   [("年级子站", 14), ("知识点", total_kp), ("例题", total_q),
                    ("ima 教辅索引", len(IMA_ITEMS)), ("归档文件", total_lib)])
         + '</div></div>',
         '<div class="note"><b>先说清楚来源</b>：核心知识点与题目来自 GitHub 开源 '
         '<a href="https://github.com/xiaoyang111222/cn-math-taxonomy">cn-math-taxonomy</a>'
         '（3297 个知识点、13335 道题，CC BY-NC 4.0，仅供个人学习/教学，禁止商用）；'
         '学前 4 页依据教育部《3–6 岁儿童学习与发展指南》分龄目标；'
         '「ima 教辅索引」是老师知识库内的真实文件目录——ima 接口不允许导出订阅库的 PDF 原件，'
         '所以那部分是元数据索引，原件请在 ima 客户端打开。</div>',
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
            b.append(f'<a class="gcard" href="{g["slug"]}.html" data-k="{esc(g["name"]+g["stage"]+g["age"])}">'
                     f'<div class="st">{esc(g["stage"])} · {esc(g["age"])}</div>'
                     f'<div class="nm">{esc(g["name"])}</div>'
                     f'<div class="num">{numtxt}</div></a>')
        b.append('</div>')

    b += ['<h2>资料来源与归档结构</h2>',
          '<table><thead><tr><th>来源</th><th>内容</th><th>许可 / 限制</th></tr></thead><tbody>',
          '<tr><td>GitHub <code>cn-math-taxonomy</code></td><td>3297 知识点、13335 道题、课标、先修依赖，'
          '按年级抽取生成 14 份笔记</td><td>CC BY-NC 4.0，个人学习/教学免费，<b>禁止商用</b></td></tr>',
          '<tr><td>教育部《3–6 岁儿童学习与发展指南》</td><td>学前 4 页分龄目标；PDF 原件 26.7 MB 已归档</td><td>公开文件</td></tr>',
          '<tr><td>ima 个人知识库</td><td>' + str(len(IMA_ITEMS)) + ' 条真实教辅目录（'
          '小学 1–6 年级课堂笔记、学霸笔记、中考/高考状元笔记等）</td>'
          '<td>仅元数据；PDF 原件需在 ima 客户端查看</td></tr>',
          '<tr><td>GitHub <code>mini-classroom</code></td><td>小学 1–2 年级数学 / 语文 / 基础英语互动站点</td>'
          '<td>MIT，可离线打开</td></tr>', '</tbody></table>',
          '<h3>目录</h3>', '<table><thead><tr><th>路径</th><th>说明</th></tr></thead><tbody>',
          '<tr><td><code>index.html</code> + <code>grade-01.html … grade-14.html</code></td><td>总入口与 14 个年级子页（同目录平铺，互链可靠）</td></tr>',
          '<tr><td><code>资料库/年级笔记/</code></td><td>14 份完整 Markdown 年级笔记</td></tr>',
          '<tr><td><code>资料库/ima索引/</code></td><td>总目录 JSON + 14 个年级子索引</td></tr>',
          '<tr><td><code>资料库/开源数据/</code></td><td>原始知识点 / 题库 / 课标 JSON、LICENSE、mini-classroom</td></tr>',
          '<tr><td><code>资料库/学前指南/</code></td><td>《3–6 岁儿童学习与发展指南》PDF</td></tr>',
          '<tr><td><a href="sources.html">sources.html</a>　/　<code>资料库/资料来源与许可.md</code></td>'
          '<td>完整来源、许可与版权说明（网页版可直接打开）</td></tr>', '</tbody></table>',
          '<h2>使用建议</h2>',
          '<p>① 从总入口选年级 → ② 看「知识点精讲」按学科过一遍掌握标准 → ③ 用「典型例题」自测，'
          '点击展开对答案与解析 → ④ 需要完整版打开该年级 Markdown 笔记 → '
          '⑤ ima 索引里的教辅原件，可在 ima 客户端按文件名搜索后阅读。</p>',
          '<p style="color:#777;font-size:13px">生成时间：' + STAMP + '。所有同目录页面可离线双击打开；'
          '若浏览器阻止本地 <code>.md</code> 打开，直接看子页内已内嵌的完整要点即可。</p>',
          '<script>function flt(){var v=document.getElementById("q").value.trim();'
          'document.querySelectorAll(".gcard").forEach(function(a){'
          'a.style.display=(!v||a.dataset.k.indexOf(v)>=0)?"":"none";});}</script>']

    return (PAGE.replace("__TITLE__", "总入口")
                .replace("__CRUMB__", '<span class="crumb">/ 总入口</span>')
                .replace("__BODY__", "\n".join(b))
                .replace("__STAMP__", STAMP))


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
        (ROOT / f"note-{g['slug']}.html").write_text(
            build_note_html(g, ts, qs, ima), encoding="utf-8")
        print(f"{g['slug']}.html  {g['name']:<8} 知识点 {len(ts):>4}  例题 {len(qs):>3}  ima {len(ima):>3}")
    (ROOT / "index.html").write_text(build_index(counts), encoding="utf-8")
    (ROOT / "sources.html").write_text(build_sources_html(), encoding="utf-8")
    print("index.html 总入口 + sources.html + 14 份完整笔记网页版 已生成")


if __name__ == "__main__":
    main()
