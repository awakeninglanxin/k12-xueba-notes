# 生成工具（可复现）

## 模块

| 文件 | 职责 |
|---|---|
| `prepare_data.py` | 从零归档三类来源：ima 检索元数据、GitHub 开源知识图谱、学前指南 PDF / mini-classroom |
| `build_site.py` | 生成入口，只做调度 |
| `site_core.py` | 常量 / 数据加载 / 样式 / 页面骨架 / 工具函数 / 页面分工契约 |
| `site_mindmap.py` | 放射状 SVG 脑图 + 树状知识地图 |
| `site_pages.py` | 总入口 / 14 个精讲页 / 14 张思维导图页 / 来源页 |
| `site_notes.py` | 14 个完整笔记网页版 + 14 份 Markdown 归档 |

模块拆分遵守「单文件不超过 20 KB」的约定；`build_site.py` 与 4 个模块必须放在同一目录，运行时 Python 会自动把该目录加入 `sys.path`。

## 复现

```bash
python _生成工具/build_site.py
```

只读取 `资料库/` 中已归档的数据，可反复重跑，覆盖生成 **44 个 HTML**（1 总入口 + 14 精讲 + 14 思维导图 + 14 完整笔记 + 1 来源页）、`style.css` 与 14 份 Markdown 笔记。

从零重建数据时才需要：

```bash
python _生成工具/prepare_data.py
```

⚠️ `prepare_data.py` 依赖会话临时目录里的 ima 检索结果与下载好的 zip/PDF；重跑前请先重新检索 ima 并下载开源仓库，否则会沿用 `资料库/` 里已归档的数据。

## 页面分工契约（改动时务必遵守）

同一份实质正文只在一个页面出现，改代码时不要跨页复制：

| 页面 | 唯一负责的内容 |
|---|---|
| `grade-XX.html` | 知识结构统计表、学前发展目标全文、前 20 道基础自测 |
| `map-grade-XX.html` | 脑图、章节树、知识点名称索引（不含正文与题目） |
| `note-grade-XX.html` | 全部知识点正文、第 21~60 道进阶例题、ima 教辅清单 |

`split_questions()` 负责把 60 道例题拆成 20 / 40 两组；`prep_for()` 与 `RESOURCES` 负责把学前 4 页的先修知识点与启蒙资源切片，避免 4 页复制同一份内容。
