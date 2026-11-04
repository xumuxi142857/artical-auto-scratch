# 每日自动任务（无人值守）

这套文件让“每天找 3 篇 CCF-A/B 会议论文 → 下载正式版 PDF → 翻译正文 → 建目录写索引”在**不用打开 DeepSeek Harness 窗口**的情况下，由 Windows 任务计划程序每天定时跑一遍。

> **状态（2026-11-05 更新）**：计划任务 `DSH-Daily-Papers` **已按要求取消并删除**，当前没有任何定时触发。以下内容保留作“按需手动跑”的说明——需要时执行下面的手动命令即可，或直接在工作区里叫我做。

## 文件

| 文件 | 作用 |
| --- | --- |
| `daily_task.md` | **任务说明书**。每次运行时 agent 读它、按要求干活。想改标准（会议范围、篇数、输出格式）改这里，不用动脚本。 |
| `run_daily.ps1` | 启动器。设置权限模式、切到工作目录、调 `dsh headless`，日志写进 `logs\`。 |
| `smoke_task.md` | 冒烟测试任务（只写一个 probe 文件），用来验证链路是否通。 |
| `logs\` | 每次运行的完整日志（`YYYY-MM-DD.log`）与 agent 写的运行报告（`YYYY-MM-DD-report.md`）。 |

## 它怎么跑

```
Windows 任务计划程序（每天 08:30）
  └─ powershell -File _automation\run_daily.ps1
       └─ DSH_PERMISSION_MODE=danger-full-access
            └─ dsh headless "读 _automation/daily_task.md 并照做"
                 └─ 产出：2026-11-05\01_... 等文件夹 + 00_今日索引_2026-11-05.md
```

要点：`headless` 是 DSH 自带的一次性模式（答完一个任务就退出，不启 GUI）。它默认用**只读/需审批**的权限，无人值守会卡在审批上，所以启动器强制 `DSH_PERMISSION_MODE=danger-full-access`（全盘可写、不再询问）。

## 常用操作

手动跑一次（不等到点）：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "E:\01科研之路\a.有价值的文章\_automation\run_daily.ps1"
```

只跑冒烟测试：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "E:\01科研之路\a.有价值的文章\_automation\run_daily.ps1" -TaskFile "E:\01科研之路\a.有价值的文章\_automation\smoke_task.md"
```

看计划任务状态：

```powershell
schtasks /Query /TN "DSH-Daily-Papers" /V /FO LIST
```

立刻触发计划任务：

```powershell
schtasks /Run /TN "DSH-Daily-Papers"
```

改时间（例如改到 07:30）：

```powershell
schtasks /Change /TN "DSH-Daily-Papers" /ST 07:30
```

删除计划任务：

```powershell
schtasks /Delete /TN "DSH-Daily-Papers" /F
```

## 排查

- 没产出：先看 `logs\<日期>.log`，最后一行 `run finished ... exit=N`。
- `ACCOUNT_SIGN_IN_REQUIRED`：说明账号凭据没被读到——检查 `C:\Users\32531\.dsh\profiles\headless\cordis.patch.yml` 里 `authorization` / `credentials` / `deepseek-account` 三个条目仍是 `disabled: false`。
- 工具调用被拒（权限）：检查启动器里的 `DSH_PERMISSION_MODE`。
- 下载卡住：agent 会被要求在 `daily_task.md` 的约束下改用 `curl.exe` 分块下载；必要时手动补下。

## 已知限制

- 任务只在**用户登录状态**下运行（任务计划程序默认如此），电脑关机/休眠时不会跑；错过就等下一次，不会自动补跑多天。
- 一次运行可能 20–60 分钟（搜索 + 下载 + 三篇长文翻译），期间不要关机。
- 每天会消耗一次完整 agent 会话的 token（相当于你手动让我做一遍）。
