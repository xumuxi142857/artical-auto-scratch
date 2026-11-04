# 工作区约定

## 1. 这个仓库是什么

- 本地路径：`E:\01科研之路\a.有价值的文章`
- 远端仓库：https://github.com/xumuxi142857/artical-auto-scratch （GitHub，main 分支，公开）
- 用途：把每天收集的会议论文（正式版 PDF、arXiv 版、正文中文译文 md/docx、README、当日索引）同步到 GitHub 备份／分享。

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

- 论文目录结构：`<YYYY-MM-DD>\NN_会议年份_短标题\`，每篇固定含 `原文_*正式版.pdf`、`原文_arXiv*.pdf`（如有）、`翻译_正文中文.md`、`翻译_正文中文.docx`、`README.md`；当天另有 `00_今日索引_<日期>.md`。
- 工具脚本在 `_工具与原文提取\`：`extract.py`（PDF→txt）、`merge_parts.py`、`md2docx.py`（md→docx）、`sync_to_github.ps1`（同步）。
