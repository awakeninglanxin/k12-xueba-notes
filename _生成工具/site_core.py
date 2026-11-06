# -*- coding: utf-8 -*-
"""站点共享层：常量、数据加载、样式、页面骨架与工具函数。

拆自原 build_site.py。所有页面生成模块都从这里取数据与工具，
保证 14 个年级用同一套口径，避免同一份内容在多处重复拼装。
"""
import html
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIB = ROOT / "资料库"
OPEN = LIB / "开源数据"
NOTES = LIB / "年级笔记"
NOTES.mkdir(parents=True, exist_ok=True)

TOPICS = json.loads((OPEN / "topics.json").read_text(encoding="utf-8"))
QUESTIONS = json.loads((OPEN / "questions.json").read_text(encoding="utf-8"))
IMA_ALL = json.loads((LIB / "ima索引" / "ima资料目录.json").read_text(encoding="utf-8"))
IMA_ITEMS = IMA_ALL["条目"]

Q_BY_TOPIC = defaultdict(list)
for _q in QUESTIONS:
    Q_BY_TOPIC[_q.get("topicId", "")].append(_q)

SUBJECT = {
    "cnm": "数学", "cnc": "语文", "cne": "英语", "cnp": "物理",
    "cns": "科学", "cnd": "道德与法治", "cnh": "历史", "cng": "地理",
    "cnb": "生物", "cnk": "化学",
}
SUBJECT_ORDER = ["数学", "语文", "英语", "科学", "道德与法治", "物理", "化学",
                 "生物", "历史", "地理"]
COLORS = ["#1552b8", "#1f7a52", "#a8641a", "#7a4fa3", "#b03a3a",
          "#1c7a8c", "#8a5a2b", "#4a5aa8", "#8a3f6a", "#4f7a2b"]

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

MINI_BASE = "资料库/开源数据/mini-classroom/mini-classroom-main/"
GUIDE_PDF = "资料库/学前指南/3-6岁儿童学习与发展指南.pdf"
# 学前 4 页的启蒙资源按年龄段递进分配，避免 4 页复制同一份清单
RESOURCES = {
    1: [("教育部《3–6 岁儿童学习与发展指南》PDF", None, "26.7 MB；了解 3 岁之后的发展阶梯，原件请在资源管理器打开")],
    2: [("小学语文一年级站 · 绘本 / 识字 / 古诗", MINI_BASE + "chinese-grade1-site/index.html", "6 大模块，适合 3–4 岁亲子共读"),
        ("指南 PDF · 3~4 岁段", None, "本页发展目标对应的公开原件")],
    3: [("小学数学 1–2 年级互动站", MINI_BASE + "math-grade1-2-workshop/index.html", "23 个数感与运算知识点，可离线打开"),
        ("小学语文一年级站", MINI_BASE + "chinese-grade1-site/index.html", "延续小班阶段的共读与识字")],
    4: [("基础英语工坊 · 30 单元", MINI_BASE + "basic-english-workshop/index.html", "幼小衔接英语启蒙"),
        ("基础英语 850 词", MINI_BASE + "basic-english-site/index.html", "高频词卡与句式"),
        ("小学数学 1–2 年级互动站", MINI_BASE + "math-grade1-2-workshop/index.html", "入学前数感预热")],
}
# 一年级先修知识点按 4 个学前阶段切片，每页不同、互不重复
PREP = [t for t in TOPICS if t.get("grade") == 1 and t["id"].startswith(("cnm", "cnc"))][:6]

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
.gcard .links { margin-top:10px; display:flex; gap:10px; flex-wrap:wrap; font-size:13px; }
.gcard .links a { border-bottom:1px dotted #9db6e8; }
.stage { margin:30px 0 12px; font-size:16px; font-weight:700; border-left:4px solid #1552b8; padding-left:10px; }
.nav { display:flex; justify-content:space-between; gap:12px; margin:34px 0 10px; padding-top:18px; border-top:1px solid #eee; font-size:14px; }
footer { color:#777; font-size:13px; border-top:1px solid #eee; margin-top:30px; padding-top:18px; }
.note { background:#fff8f2; border-left:4px solid #e8792b; padding:12px 16px; font-size:14px; margin:16px 0; border-radius:4px; }
.search { padding:9px 13px; border:1px solid #ccc; border-radius:6px; width:280px; font-size:14px; }
.mapbar { display:flex; gap:10px; flex-wrap:wrap; margin:16px 0 6px; }
.mapbar a { border:1px solid #d9e2f5; background:#f7f9fd; border-radius:6px; padding:6px 12px; font-size:14px; }
.mapbar a.on { border-color:#1552b8; color:#1552b8; font-weight:700; }
.mindmap { border:1px solid #e3e8f2; border-radius:10px; background:#fff; padding:10px; overflow:auto; }
.mindmap svg { display:block; margin:0 auto; max-width:100%; height:auto; }
.tree details { margin:6px 0 6px 12px; border-left:2px solid #e3e8f2; padding-left:14px; }
.tree > details { margin-left:0; }
.tree summary { cursor:pointer; font-size:15px; padding:2px 0; }
.tree .leaf { color:#444; font-size:13px; margin:3px 0 3px 18px; }
.tree .leaf a { color:#333; }
.legend { color:#777; font-size:13px; margin:8px 0 0; }
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
    return SUBJECT.get(t["id"].split("_")[0], "其他")


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


def structure(ts):
    """学科 → 领域 → 章节 → 知识点列表，脑图与结构表共用的唯一数据口径"""
    d = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for t in ts:
        d[subj_of(t)][t.get("domain") or "其他"][t.get("chapter") or "其他"].append(t)
    return d


def split_questions(qs):
    """页面分工：前 20 道给精讲页做基础自测，其余给完整笔记页，保证零重复"""
    return qs[:20], qs[20:]


def prep_for(g):
    """学前 4 页的一年级先修知识点切片，每页不同"""
    if g["n"] == 1:
        return []
    i = g["n"] - 2
    return PREP[i * 2:i * 2 + 2]


def topic_block(t, with_q=True, anchor=True):
    mc = t.get("mastery_criteria") or []
    dq = t.get("diagnostic_question") or {}
    aid = f' id="kp-{esc(t["id"])}"' if anchor else ""
    s = f'<div class="kp"{aid}><b>{esc(t.get("name"))}</b>'
    if t.get("chapter"):
        s += f'<div class="ch">{esc(t["chapter"])}</div>'
    if t.get("description"):
        s += f'<div class="ds">{esc(t["description"])}</div>'
    if mc:
        s += '<div class="mc">掌握标准：' + esc("；".join(mc[:3])) + '</div>'
    if with_q and dq.get("question"):
        s += f'<div class="dq">自测：{esc(dq["question"])}　答：{esc(dq.get("answer",""))}</div>'
    return s + "</div>"


def page(title, crumb, body):
    """统一渲染：先填占位符，再返回完整 HTML（不做全局 {{}} 替换）"""
    return (PAGE.replace("__TITLE__", esc(title))
                .replace("__CRUMB__", crumb)
                .replace("__BODY__", "\n".join(body) if isinstance(body, list) else body)
                .replace("__STAMP__", STAMP))


def mapbar(g, active):
    """每页顶部的四向导航：精讲 / 脑图 / 完整笔记 / 总入口"""
    items = [(f'{g["slug"]}.html', "精讲页"), (f'map-{g["slug"]}.html', "思维导图"),
             (f'note-{g["slug"]}.html', "完整笔记"), ("index.html", "总入口")]
    parts = []
    for u, k in items:
        on = ' class="on"' if k == active else ""
        parts.append(f'<a href="{u}"{on}>{k}</a>')
    return '<div class="mapbar">' + "".join(parts) + '</div>'


def neighbors(g):
    return (GRADES[g["n"] - 2] if g["n"] > 1 else None,
            GRADES[g["n"]] if g["n"] < len(GRADES) else None)
