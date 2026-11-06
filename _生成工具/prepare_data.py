# -*- coding: utf-8 -*-
"""
准备阶段：把三类真实来源归档到 E:\\小学到高中学霸资料\\资料库
  1) ima 知识库检索结果 -> 真实资料目录索引（元数据）
  2) GitHub 开源 cn-math-taxonomy（CC BY-NC 4.0）-> 知识点/题库/课标
  3) 教育部《3-6岁儿童学习与发展指南》PDF + mini-classroom（MIT）
"""
import json
import re
import shutil
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(r"E:\小学到高中学霸资料")
LIB = ROOT / "资料库"
IMA_DIR = LIB / "ima索引"
OPEN_DIR = LIB / "开源数据"
PRE_DIR = LIB / "学前指南"
for d in (IMA_DIR, OPEN_DIR, PRE_DIR):
    d.mkdir(parents=True, exist_ok=True)

TMP = Path(tempfile.gettempdir())
TR = Path(r"C:\Users\ThinkPad\.workbuddy\projects\c-Users-ThinkPad-WorkBuddy-2026-11-06-15-27-56"
          r"\bd1e6efa-d9fe-4c5d-9d3d-90e8c79cdc38\tool-results")

GRADES = [
    ("幼儿0-3岁", "学前期", ["0-3", "0～3", "0—3", "托班", "早教", "婴幼儿"]),
    ("小班", "学前期", ["小班"]),
    ("中班", "学前期", ["中班"]),
    ("大班", "学前期", ["大班", "幼小衔接", "学前班"]),
    ("一年级", "小学", ["一年级", "1年级", "奥数1年级"]),
    ("二年级", "小学", ["二年级", "2年级", "奥数2年级"]),
    ("三年级", "小学", ["三年级", "3年级", "奥数3年级"]),
    ("四年级", "小学", ["四年级", "4年级", "奥数4年级"]),
    ("五年级", "小学", ["五年级", "5年级", "奥数5年级"]),
    ("六年级", "小学", ["六年级", "6年级", "奥数6年级"]),
    ("初一", "初中", ["初一", "七年级", "7年级", "七上", "七下"]),
    ("初二", "初中", ["初二", "八年级", "8年级", "八上", "八下"]),
    ("初三", "初中", ["初三", "九年级", "9年级", "中考"]),
    ("高中", "高中", ["高中", "高考", "高一", "高二", "高三", "必修", "选择性必修", "状元笔记"]),
]


def classify(title, folder=""):
    text = title + " " + folder
    hits = []
    for name, stage, pats in GRADES:
        if any(p in text for p in pats):
            hits.append(name)
    # 学段通用资料分发到该学段每个年级（如「初中数学学霸笔记」「小学学霸笔记-语文」）
    if not hits:
        if "初中" in text:
            hits = ["初一", "初二", "初三"]
        elif "小学" in text:
            hits = ["一年级", "二年级", "三年级", "四年级", "五年级", "六年级"]
    return hits


def build_ima_index():
    files = sorted(TR.glob("mcp-ima-mcp-search_knowledge-*.txt"))
    items, seen = [], set()
    for f in files:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        for x in data.get("searched_knowledge_list", []):
            k = x.get("knowledge", {})
            mid = k.get("media_id", "")
            if not mid or mid in seen:
                continue
            seen.add(mid)
            title = k.get("title", "")
            folder = x.get("parent_folder_name", "") or ""
            items.append({
                "title": title,
                "media_id": mid,
                "type": (k.get("media_type_info") or {}).get("name", ""),
                "size_bytes": int(k.get("file_size") or 0),
                "folder": folder,
                "intro": (k.get("introduction") or "")[:600],
                "highlight": re.sub(r"</?em>", "", x.get("highlight_content") or "")[:500],
                "grades": classify(title, folder),
            })
    out = {
        "来源": "ima 个人知识库（订阅库）检索结果元数据，非文件原件",
        "说明": "ima MCP 的 FetchMediaContent 对订阅库返回 220030「该文件获取失败」，"
                "因此只能归档标题/大小/目录摘录等元数据；PDF 原件请在 ima 客户端内查看。",
        "涉及知识库": ["小初高资料库&Ai智能备考", "初中全科状元/学霸笔记"],
        "条目总数": len(items),
        "条目": items,
    }
    (IMA_DIR / "ima资料目录.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    # 按年级拆出子索引
    by_grade = {}
    for name, stage, _ in GRADES:
        by_grade[name] = [i for i in items if name in i["grades"]]
        (IMA_DIR / f"{name}.json").write_text(
            json.dumps({"年级": name, "学段": stage, "条目数": len(by_grade[name]),
                        "条目": by_grade[name]}, ensure_ascii=False, indent=2), encoding="utf-8")
    print("ima 元数据:", len(items), "条，分年级:", {k: len(v) for k, v in by_grade.items()})
    return items, by_grade


def copy_open_data():
    src = TMP / "taxonomy" / "cn-math-taxonomy-main"
    keep = ["data/topics.json", "data/questions.json", "data/dependencies.json",
            "data/cn-curriculum-standards.json", "LICENSE", "README.md"]
    for rel in keep:
        p = src / rel
        if p.exists():
            shutil.copy2(p, OPEN_DIR / p.name)
    # 按年级的题库批次
    qb = src / "data" / "_qbatches"
    if qb.exists():
        dst = OPEN_DIR / "题库分年级"
        dst.mkdir(exist_ok=True)
        for p in qb.glob("*.json"):
            shutil.copy2(p, dst / p.name)
    # mini-classroom（MIT）
    mz = TMP / "mini.zip"
    if mz.exists():
        with zipfile.ZipFile(mz) as z:
            z.extractall(OPEN_DIR / "mini-classroom")
    print("开源数据归档:", len(list(OPEN_DIR.rglob("*"))), "项")


def copy_pre_guide():
    p = TMP / "guide36.pdf"
    if not p.exists():
        return
    dst = PRE_DIR / "3-6岁儿童学习与发展指南.pdf"
    shutil.copy2(p, dst)
    print("学前指南 PDF:", dst.stat().st_size, "B")


def write_sources(ima_items):
    lines = [
        "# 资料来源与许可",
        "",
        "本目录所有内容均来自可公开获取或老师本人 ima 账号内可见的资料。",
        "",
        "## 一、ima 知识库（资料目录索引）",
        "",
        f"- 已索引真实条目 **{len(ima_items)}** 条，见 `ima索引/ima资料目录.json` 及各年级子索引。",
        "- 涉及知识库：`小初高资料库&Ai智能备考`(2055 条)、`初中全科状元/学霸笔记`(30 条) 等订阅库。",
        "- ⚠️ ima MCP 的正文接口对订阅库返回 `220030 该文件获取失败`，**PDF 原件与全文无法导出**；"
        "这里只归档标题、文件大小、所属学科文件夹和目录摘录。原件请在 ima 客户端打开。",
        "",
        "## 二、GitHub 开源 `xiaoyang111222/cn-math-taxonomy`（知识点与题库正文）",
        "",
        "- 地址：https://github.com/xiaoyang111222/cn-math-taxonomy",
        "- 许可：**CC BY-NC 4.0**（个人学习/教学/研究免费，**禁止商用**，需署名）。",
        "- 内容：3297 个知识点（含年级、章节、掌握标准、诊断题）、13335 道题（含答案解析）、课标条目、先修依赖。",
        "- 本目录 `开源数据/` 保存原始 JSON；14 份年级笔记由这些真实数据按年级抽取生成，未虚构题目。",
        "- 覆盖：数学 1–9 年级及高中必修/选必、语文 1–9 年级、英语 3 年级至高中、物理 8 年级起、"
        "科学/道法 1–6 年级、历史/地理/生物/化学 7–9 年级。",
        "",
        "## 三、教育部《3–6 岁儿童学习与发展指南》",
        "",
        "- 来源：联合国儿童基金会中国站公开 PDF https://www.unicef.cn/media/8456/file/",
        "- 原件：`学前指南/3-6岁儿童学习与发展指南.pdf`（26.7 MB）",
        "- 用于学前期 4 个页面（幼儿0-3岁 / 小班 / 中班 / 大班）的分龄发展目标。",
        "- 说明：学前期不属于义务教育，不存在「学霸笔记」类教辅，这几个页面是权威发展指南 + 启蒙资源索引。",
        "",
        "## 四、GitHub 开源 `JeetChan/mini-classroom`（MIT）",
        "",
        "- 地址：https://github.com/JeetChan/mini-classroom",
        "- 许可：MIT。内容：小学 1–2 年级数学 23 个知识点、语文 6 大模块、基础英语 30 单元，纯静态可离线打开。",
        "- 归档于 `开源数据/mini-classroom/`。",
        "",
        "## 版权提醒",
        "",
        "CC BY-NC 4.0 内容仅限个人学习、教学与研究，不得用于付费课程、售卖或机构收费服务；"
        "ima 内的教辅 PDF 版权归原作者/出版社，请仅在个人学习范围内使用。",
        "",
    ]
    (LIB / "资料来源与许可.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    items, _ = build_ima_index()
    copy_open_data()
    copy_pre_guide()
    write_sources(items)
    print("准备完成 ->", LIB)
