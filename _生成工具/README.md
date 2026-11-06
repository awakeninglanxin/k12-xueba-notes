# 生成工具（可复现）

- `prepare_data.py` —— 归档三类来源：ima 检索元数据、GitHub 开源知识图谱、学前指南 PDF / mini-classroom。
- `build_site.py` —— 生成 `index.html` + 14 个年级子页 + `style.css` + 14 份 Markdown 年级笔记。

## 复现

```bash
python _生成工具/prepare_data.py
python _生成工具/build_site.py
```

⚠️ `prepare_data.py` 依赖会话临时目录里的 ima 检索结果与下载好的 zip/PDF；
重跑前请先重新检索 ima 并下载开源仓库，否则会沿用 `资料库/` 里已归档的数据。
知识点与题库正文来自 `资料库/开源数据/`，`build_site.py` 可单独重跑。
