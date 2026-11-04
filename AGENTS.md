# 工作区约定

## 1. 这个仓库是什么

- 本地路径：`E:\01科研之路\a.有价值的文章`
- 远端仓库：https://github.com/xumuxi142857/artical-auto-scratch （GitHub，main 分支，公开）
- 用途：把每天收集的会议论文（原文 PDF 一份、正文中文译文 Word、README、当日索引）同步到 GitHub 备份／分享。

## 2. 硬性约定：每次更新文件夹都要同步

**只要在工作区里新增或修改了论文相关内容（新日期文件夹、新论文、更新索引、修 README 等），必须立刻提交并推送**，不要等用户提醒。

一条命令搞定：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "_工具与原文提取\sync_to_github.ps1" -Message "论文: 2026-11-05 三篇（ICML/AAAI/ACL）"
```

或手动：

```powershell
& "C:\Program Files\Git\cmd\git.exe" -C "E:\01科研之路\a.有价值的文章" add -A
& "C:\Program Files\Git\cmd\git.exe" -C "E:\01科研之路\a.有价值的文章" commit -m "论文: ..."
& "C:\Program Files\Git\cmd\git.exe" -C "E:\01科研之路\a.有价值的文章" push origin main
```

提交信息格式：`论文: <日期> <篇数>篇（会议列表）`；杂项用 `chore:` 前缀。

## 3. 环境事实

- 这台机器原本没有 git；2026-11-05 通过 `winget install Git.Git` 装了 **Git 2.56.0.4**，可执行文件在 `C:\Program Files\Git\cmd\git.exe`（不在 PATH 里，要写全路径）。
- 推送凭据已可用（首次 `push` 直接成功，未再要求登录）；如果哪天报 `Authentication failed`，需要重新配一个 Personal Access Token。
- 仓库默认分支 `main`，已设 `origin` 与上游跟踪。

## 4. 不纳入版本管理的东西

`.gitignore` 里排除了：`_automation/logs/`（运行日志，含内部推理输出）、`_automation/smoke/`（冒烟测试残留）、`*.tmp`、`Thumbs.db`、`Desktop.ini`。

## 5. 其它

- 论文目录结构：`<YYYY-MM-DD>\NN_会议年份_短标题\`，**每篇只放 3 个文件**：
  1. `原文_*.pdf` —— **只存一个 PDF**：能拿到会议正式版就存正式版（`原文_<会议年份>正式版.pdf`，引用以它为准），拿不到就存 arXiv 版（`原文_arXiv<id>.pdf`）。不要再同时存两个版本。
  2. `翻译_正文中文.docx` —— **译文只交 Word**。生成时可以临时用 Markdown 走 `md2docx.py`，但**交付前必须删掉 .md 与 part*.md**，文件夹里不留 Markdown。
  3. `README.md` —— 会议/CCF/出版信息/链接/贡献/关键数字/阅读建议/BibTeX。
  当天另有 `00_今日索引_<日期>.md`（这个 .md 要保留，它是索引不是译文）。
- 工具脚本在 `_工具与原文提取\`：`extract.py`（PDF→txt）、`merge_parts.py`、`md2docx.py`（md→docx）、`sync_to_github.ps1`（同步）。
