# 05 | AAAI 2026（CCF-A）| RecToM：对话推荐系统里的机器心智理论基准

> **英文标题**：RecToM: A Benchmark for Evaluating Machine Theory of Mind in LLM-based Conversational Recommender Systems
> **中文译名**：RecToM：面向基于 LLM 的对话推荐系统机器心智理论评测基准

| 项目 | 内容 |
|---|---|
| 会议 | **AAAI-26**（第 40 届 AAAI 人工智能会议，2026-01-20~27，Singapore） |
| CCF 等级 | **CCF-A**（人工智能） |
| 出版信息 | *Proceedings of the AAAI Conference on Artificial Intelligence*, Vol. 40, No. 37, pp. **31636–31644**；DOI: **10.1609/aaai.v40i37.40430**；2026-03-14 出版 |
| 分会场 | AAAI Technical Track on Natural Language Processing II |
| 作者 | Mengfan Li$^{1*}$, Xuanhua Shi$^{1\dagger}$, Yang Deng$^{2}$（\*工作完成于 SMU 访问期间，$\dagger$通讯作者） |
| 单位 | $^{1}$ 华中科技大学（大数据技术与系统国家工程研究中心、服务计算技术与系统实验室、集群与网格计算实验室）；$^{2}$ 新加坡管理大学（SMU） |
| 官方页面 | https://ojs.aaai.org/index.php/AAAI/article/view/40430 |
| 官方 PDF | https://ojs.aaai.org/index.php/AAAI/article/view/40430/44391 |
| arXiv | https://arxiv.org/abs/2511.22275 |
| 代码/数据 | https://github.com/CGCL-codes/RecToM |
| 主题标签 | 心智理论 ToM · 对话推荐系统 CRS · 基准 benchmark · 心理状态推断 · 行为预测 · 谄媚偏差 |

## 一句话概括

第一个面向**对话推荐系统**、由人工标注的机器心智理论基准：用 336 段真实电影推荐对话构造 **20,524 个 QA**，把 ToM 拆成“认知推断（欲望/信念/意图）”与“行为预测（策略预测/有效性判断）”两个维度；5 个主流 LLM 在细粒度意图上平均只有 27.74%，判断任务上还出现严重的“Yes 谄媚”（约 93% 预测为“是”），远低于人类。

## 为什么今天推荐它（与三个关键词的对应）

- **ToM 的“真实对话 + 应用域”评测**：不同于 Sally-Anne 式合成故事，它用 REDIAL 真实推荐对话，且同时评“理解对方心理状态”与“用心理状态指导下一步策略”，比只做信念问答的基准更接近真实交互。
- **补足现有基准的盲区**：现有 ToM 基准多为通用叙事或任务导向对话，RecToM 首次系统评估 CRS 中**不对称角色**（推荐者 vs 寻求者）、**分层意图**、**多维信念**与**并发欲望**。
- **对 LLM 心智推理的诊断价值**：给出“多选比单选难”“细粒度意图是瓶颈”“CoT 收益有限”“判断任务存在系统性肯定偏差”四条可操作的结论，适合作为新方法的评测集。

## 核心贡献

1. **首个 CRS 场景的 ToM 基准**：基于 REDIAL 构造 336 段对话、4,583 轮、20,524 个 QA、10 类问题，覆盖 253 段“先拒后接受”的满意对话与 83 段“未接受”的不满意对话；三名受过 ToM 训练的博士生标注，Fleiss's K = 0.79。
2. **双维评估框架**：**认知推断**（欲望、信念、意图归因）与**行为预测**（下一策略预测、策略有效性判断），对应“理解心理状态”与“用心理状态指导行动”两类能力。
3. **四项 CRS 特化设计**：多选策略（一句话多意图）、多粒度意图（推荐者 10 类 / 寻求者 16 类细粒度，及对应粗粒度）、多维信念（建议/看过/喜欢）、多并发欲望（对每部电影独立评估）。
4. **系统性实证**：5 个 LLM（DeepSeek-v3、GPT-4o、GPT-4o-mini、Gemini 2.5 Flash-Lite、Claude 3.5 Haiku）× 零样本/CoT 两种提示，给出主结果、判断偏差与细粒度错误分析。
5. **可复现资源**：数据、评测代码与标注公开在 GitHub。

## 主要结果（原文口径）

- **总体**：模型平均（10 列）为细粒度意图 27.74%（推荐者）/28.20%（寻求者）、粗粒度意图 41.13%/55.77%、信念 68.72%、欲望 86.35%、预测 20.54%/30.59%、判断 34.84%/34.53%；人类对应为 64.32/59.92、86.31/82.74、96.84、98.25、87.44/85.18、96.37/97.23。
- **最佳单点**：DeepSeek-v3+CoT 的推荐者信念 **79.46%**；DeepSeek-v3 的寻求者细粒度意图 **33.20%**；GPT-4o 的寻求者粗粒度意图 **64.22%**、欲望 **92.27%**、寻求者预测 **49.23%**。
- **多选 vs 单选**：多选（斜体列）平均仅 27.74%（推荐者细粒度意图），而单选信念 68.72%、欲望 86.35%，差距近 40 个点。
- **粒度差距**：GPT-4o 寻求者粗粒度 64.22% → 细粒度 28.84%；DeepSeek-v3 推荐者 44.26% → 29.71%。
- **判断偏差**：全体平均“Yes”预测率约 **93.37%**，FPR 约 **93.28%**，“No”召回仅约 **7.22%**；多数模型判断准确率低于 50% 随机基线。
- **CoT**：多数设置仅边际变化，甚至下降（如 GPT-4o 寻求者粗粒度 64.22% → 54.10%）。

## 阅读建议

- **先看 §3（RECTOM Benchmark）**：Overview 的四个研究问题、Data Collection 的 REDIAL 筛选与标注流程，以及表 1–3 的数据规模。
- **再看 Cognitive Inference / Behavioral Prediction 两节**：把“欲望—信念—意图”与“预测—判断”的构念定义、问题模板（表 2）对应起来。
- **重点看表 4 与表 5**：表 4 的主结果按角色×粒度拆分；表 5 的 Prediction Bias/FPR/Recall 是“谄媚偏差”的直接证据。
- **最后看 In-depth Analysis**：Fine2Coarse 分析解释了“细粒度差不是方向错，而是同粗类内分不清”，对改进评测/训练很有用。
- **注意**：原文表 5 推荐者 Gemini 2.5 一行的 FPR 97.23 与 Recall 12.77 之和为 110，按定义应互补为 100，疑为原文笔误；译文照录并在译注说明。

## 文件说明

- `原文_AAAI2026正式版.pdf`：AAAI-26 正式出版版（9 页，pp. 31636–31644，含 DOI 与官方排版）
- `原文_arXiv2511.22275.pdf`：arXiv 预印版（便于检索/复制；正式版与预印版数值以正式版为准）
- `翻译_正文中文.md`：正文全文中文翻译（标题 → 结论/致谢，含表 1–5、图 1–3 说明；不含参考文献）
- `翻译_正文中文.docx`：同一译文的 Word 版
- `README.md`：本导读

## BibTeX

```bibtex
@inproceedings{li2026rectom,
  title     = {RecToM: A Benchmark for Evaluating Machine Theory of Mind in LLM-based Conversational Recommender Systems},
  author    = {Li, Mengfan and Shi, Xuanhua and Deng, Yang},
  booktitle = {Proceedings of the AAAI Conference on Artificial Intelligence},
  volume    = {40},
  number    = {37},
  pages     = {31636--31644},
  year      = {2026},
  doi       = {10.1609/aaai.v40i37.40430}
}
```
