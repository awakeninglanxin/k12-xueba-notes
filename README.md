# K-12 学霸笔记站点

**GitHub 仓库：** https://github.com/awakeninglanxin/k12-xueba-notes

**在线浏览：** https://awakeninglanxin.github.io/k12-xueba-notes/

按 14 个年级（幼儿 0-3 岁 → 小班 / 中班 / 大班 → 小学一至六年级 → 初一 / 初二 / 初三 → 高中）组织的静态学习资料站点。全部内容取自真实公开数据源与 ima 知识库检索结果，**未编造知识点或题目**。

- **30 个 HTML 页面**：1 个总入口 + 14 个年级精讲页 + 14 个完整笔记页 + 1 个来源说明页
- **3297 个知识点**（含年级、章节、描述、掌握标准、诊断题）
- **13335 道带解析题目**，每个年级抽取 60 道例题
- **339 条 ima 教辅目录索引**，按年级拆分
- 白底黑字、纯静态、无外部依赖，可完全离线使用

## 一、快速开始

| 方式 | 操作 |
|---|---|
| 在线 | 打开 https://awakeninglanxin.github.io/k12-xueba-notes/ |
| 本地双击 | 直接打开根目录 `index.html`（页内链接均为相对路径） |
| 本地服务 | `python -m http.server 8000` 后访问 `http://localhost:8000` |

> 根目录 `.nojekyll` 用于关闭 Jekyll 处理，保证 `_生成工具/` 等下划线目录与中文路径在静态服务下可正常访问。线上由 `.github/workflows/pages.yml` 通过 GitHub Actions 部署，每次推送到 `main` 自动更新站点。

## 二、站点结构

| 路径 | 说明 |
|---|---|
| `index.html` | 总入口，按 4 个学段分 14 张年级卡片，带搜索框 |
| `grade-01.html` … `grade-14.html` | 年级精讲页：分学科知识点、20 道可折叠答案的例题、教辅索引、上下年级导航 |
| `note-grade-01.html` … `note-grade-14.html` | 完整笔记页：该年级全部知识点 + 60 道例题解析全量展开 |
| `sources.html` | 资料来源、许可与版权说明的网页版 |
| `style.css` | 全站唯一样式表 |
| `资料库/年级笔记/` | 14 份 Markdown 版年级笔记，便于二次编辑 |
| `资料库/ima索引/` | 14 份年级教辅目录 + 汇总 JSON（仅元数据，无正文） |
| `资料库/开源数据/` | 开源知识图谱原始 JSON、LICENSE 原文、题库分年级、mini-classroom 站点 |
| `资料库/学前指南/` | 教育部《3–6 岁儿童学习与发展指南》PDF 原件 |
| `_生成工具/` | `prepare_data.py`（数据归档）与 `build_site.py`（站点生成） |

## 三、14 个年级与 ima 教辅索引

| 学段 | 年级 | 精讲页 | 完整笔记 | ima 索引条数 |
|---|---|---|---|---:|
| 学前 | 幼儿 0-3 岁 | `grade-01.html` | `note-grade-01.html` | 0 |
| 学前 | 小班 | `grade-02.html` | `note-grade-02.html` | 0 |
| 学前 | 中班 | `grade-03.html` | `note-grade-03.html` | 0 |
| 学前 | 大班 | `grade-04.html` | `note-grade-04.html` | 0 |
| 小学 | 一年级 | `grade-05.html` | `note-grade-05.html` | 66 |
| 小学 | 二年级 | `grade-06.html` | `note-grade-06.html` | 53 |
| 小学 | 三年级 | `grade-07.html` | `note-grade-07.html` | 36 |
| 小学 | 四年级 | `grade-08.html` | `note-grade-08.html` | 30 |
| 小学 | 五年级 | `grade-09.html` | `note-grade-09.html` | 27 |
| 小学 | 六年级 | `grade-10.html` | `note-grade-10.html` | 73 |
| 初中 | 初一 | `grade-11.html` | `note-grade-11.html` | 38 |
| 初中 | 初二 | `grade-12.html` | `note-grade-12.html` | 40 |
| 初中 | 初三 | `grade-13.html` | `note-grade-13.html` | 49 |
| 高中 | 高中（必修 + 选必） | `grade-14.html` | `note-grade-14.html` | 48 |

学前 4 页内容取自教育部《3–6 岁儿童学习与发展指南》五大领域分龄目标 + 启蒙资源 + 一年级先修预览。学前期不属于义务教育，不存在「学霸笔记」类教辅。

## 四、数据来源

| 来源 | 本仓库内容 | 数量 | 许可 |
|---|---|---:|---|
| [xiaoyang111222/cn-math-taxonomy](https://github.com/xiaoyang111222/cn-math-taxonomy) | 知识点、例题解析、课标、先修依赖原始 JSON | 3297 知识点 / 13335 题 | **CC BY-NC 4.0** |
| [JeetChan/mini-classroom](https://github.com/JeetChan/mini-classroom) | 小学 1-2 年级数学、语文一年级、基础英语互动站点 | 4 个子站点 | MIT |
| [UNICEF 中国 · 教育部《3–6 岁儿童学习与发展指南》](https://www.unicef.cn/media/8456/file/) | PDF 原件 | 26.7 MB | 公开文件 |
| ima 知识库（订阅库检索） | 教辅目录元数据（标题、大小、所属文件夹） | 339 条 | 版权归原作者 |

知识点与例题正文全部来自 `开源数据/topics.json` 与 `questions.json`，由 `build_site.py` 按年级抽取生成，未虚构题目。

## 五、本地复现

```bash
python _生成工具/build_site.py
```

`build_site.py` 只读取 `资料库/` 中已归档的数据，可单独重跑，会重新生成全部 30 个页面、样式表与 14 份 Markdown 笔记。

`prepare_data.py` 负责从零归档三类来源，重跑前需要：重新通过 ima MCP 检索并保存结果、下载开源仓库 zip 与学前指南 PDF。详见 `_生成工具/README.md`。

## 六、许可与版权声明

- **`资料库/开源数据/` 内的知识点与题库数据采用 CC BY-NC 4.0**，原文见 `资料库/开源数据/LICENSE`。允许个人学习、教学、研究与非商业分享，**须署名、不得商用**。已按要求标注原作者与原仓库地址。
- **`资料库/开源数据/mini-classroom/` 采用 MIT**，原文见该目录内 `LICENSE`。
- **教育部指南 PDF** 为公开发布文件，此处仅作学习归档。
- **ima 索引仅为文件名、大小与目录结构的元数据**，不含任何教辅正文。教辅版权归原作者 / 出版社，请仅在个人学习范围内使用，原件请在 ima 客户端打开。
- 本仓库为**个人学习用途的资料聚合**，不用于任何付费课程、售卖或机构收费服务。若权利人认为某部分内容不宜公开，可提出，将及时移除或改为私有仓库。

## 七、已知限制

1. ima MCP 的 `FetchMediaContent` 对订阅知识库一律返回 `220030 该文件获取失败`，因此 PDF 原件与全文无法导出，本仓库只保留目录索引。
2. 部分本地预览面板不提供 `.md` / `.pdf` 的在线渲染，因此每份笔记额外生成了 HTML 网页版；Markdown 与 PDF 保留在 `资料库/` 供本地使用（GitHub Pages 上这两类文件均可直接访问）。
3. 知识点覆盖以数学为主，兼有语文、英语、物理、化学、科学、道法、历史、地理、生物；各科覆盖年级不同，详见各年级页面。
