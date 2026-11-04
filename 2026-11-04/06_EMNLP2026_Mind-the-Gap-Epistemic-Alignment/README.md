# 06 | EMNLP 2026 Findings（CCF-B）| 弥合差距：以心智理论为基础的摩擦信号用于认知对齐

> **英文标题**：Mind the Gap: Theory-of-Mind-Grounded Friction for Epistemic Alignment
> **中文译名**：弥合差距：以心智理论为基础的摩擦信号用于认知对齐

| 项目 | 内容 |
|---|---|
| 会议 | **EMNLP 2026**（Conference on Empirical Methods in Natural Language Processing，2026-10-24~29，Budapest, Hungary） |
| 论文类别 | **Findings of EMNLP 2026**（Findings 子集，非主会；按 EMNLP 的 CCF-B 口径标注，引用时请注明 Findings） |
| CCF 等级 | **CCF-B**（自然语言处理；Findings 非主会，部分单位不计入 CCF-B 主会成果） |
| 出版信息 | *Findings of the Association for Computational Linguistics: EMNLP 2026*, pp. **12763–12778**；DOI: **10.18653/2026.findings-emnlp.605** |
| 作者 | Yifan Zhu, Kyeongmin Rim, James Pustejovsky |
| 单位 | Brandeis University（布兰迪斯大学），Waltham, MA, USA |
| 官方页面 | https://aclanthology.org/2026.findings-emnlp.605/ |
| 官方 PDF | https://aclanthology.org/2026.findings-emnlp.605.pdf |
| arXiv | https://arxiv.org/abs/2608.30719 |
| 代码/数据 | 原文未给出公开代码仓库；数据基于 HCRC MapTask 与 Li et al. (2026) 的视角主义标注 |
| 主题标签 | 心智理论 ToM · 认知对齐 epistemic alignment · 摩擦策略优化 FPO · 偏好优化 DPO · 二阶信念 · 对话干预 |

## 一句话概括

把 ToM 推断做成**可计算的摩擦信号**：对每个指称表达抽取“说话者意图指称 / 受话者理解 / 说话者对受话者的信念 / 受话者对说话者的信念”四元组，用其分歧计算 $F^-$（风险）与 $F^+$（干预收益），再注入 FPO 的三种变体（FAR/FPP/FTR）；在 MapTask 上，FAR/FTR 相比 DPO 把干预 F1 从 0.344 提到 0.416/0.417，ECE 从 0.432 降到 0.227/0.178，且三次训练运行的标准差从 0.106 降到 0.023/0.009。

## 为什么今天推荐它（与三个关键词的对应）

- **ToM 的“功能化”用法**：不是让模型回答“别人怎么想”，而是把二阶信念分歧作为**策略干预的控制信号**；这对应 Riemer 等（2025）的 functional ToM，和只做问答评测的 ToM 工作形成互补。
- **RL/偏好后训练的实战对照**：以 DPO 为基线，系统比较奖励塑形（FAR）、偏好配对（FPP）、信赖域（FTR）三种注入方式，并做“摩擦感知监督 vs 逐实例条件化 vs 二阶结构”的三级消融，方法论上很适合借鉴到 GRPO/RLHF 实验设计。
- **LLM 心智推理的可解释信号**：四标识符模式把“静默分歧（双方都自信但指称不同）”变成可检测量；消融二阶通道使误解召回从约 65% 掉到 26%，是“二阶 ToM 有实质作用”的量化证据。

## 核心贡献

1. **时点 ToM 模式**：为 HCRC MapTask 的每个指称表达重建一阶（①意图指称、②受话者理解）与二阶（③说话者对受话者解释的信念、④受话者对说话者意图的信念）信念，并加入 `UPTAKE_QUALITY`、`SURFACE_SIGNALS`、`IS_EXISTENCE_QUERY` 三个辅助字段。
2. **可计算的摩擦模块**：$F^-(h)$ 由不确定性（UNC）、已显现矛盾/修复（CONTR）、传播风险（HAZ）、高阶信念冲突（VALCONF）加权组成；$F^+(h,a)$ 是澄清/核实/重定向/拒绝四个动作的认知收益查找表。五种典型构型（Aligned、Silent intent fixing、两种 Asymmetric、Mutual awareness）把分歧结构化。
3. **信号验证**：四标识符解析成功率 98.5%（训练）/100%（测试）；误解召回 67.6%（训练）/65.2%（测试）；$F^-$ 在 pending→misunderstood 上单调上升（0.185→0.375、0.193→0.390）；二阶通道消融使召回降到 23.4%/26.1%。
4. **FPO 训练器适配与评估**：把摩擦注入 FAR/FPP/FTR，与 DPO、DPO-FB 对比；主要指标为干预 F1 与有依据上下文校准（ECE、Brier），并做三次独立 QLoRA 运行的稳定性分析。
5. **诚实的边界分析**：作者明确指出摩擦是离线计算的、二阶标签由 GPT-5 推断而非金标准、$F^+$ 绑定于特定动作空间，并在 Limitations/Potential Risks 中讨论泛化与双用途风险。

## 主要结果（原文口径）

- **主结果（表 5，n=278：120 有依据 + 158 对齐）**：DPO F1 0.344、ECE$_{warr}$ 0.432、Brier$_{warr}$ 0.411；FAR 0.416/0.227/0.281；FTR 0.417/0.178/0.293；FPP 虽 F1 0.603，但对所有实例都干预，ECE$_{align}$=1.000、净胜 −91.4，属于坍缩。
- **稳定性（表 6，三次运行）**：DPO F1 0.298±0.106、ECE 0.523±0.090；FAR 0.411±0.023、0.225±0.038；FTR 0.430±0.009、0.192±0.011。六组同种子比较 McNemar $p \le 3\times10^{-3}$。
- **分阶段消融（表 7）**：DPO-FB 0.282 → DPO 0.344 → FAR 0.416 / FTR 0.417；Brier 0.532 → 0.411 → 0.281/0.293。
- **二阶 ToM 消融（表 8）**：FAR 0.368→0.416（+13.0%），FTR 0.400→0.417（+4.3%）；校准效应混合，作者将其解释为“干预行为改善”而非普遍校准优势。
- **测试时信念可及性（表 9）**：未训练骨干 + ToM 前导已达 F1 0.410；ICL 0.490–0.510（随机示例与摩擦脚手架相当）；移除前导后 FAR/FTR 降到 0.343/0.349，仍略高于 DPO 的 0.330。

## 阅读建议

- **先看 §4.1 与表 1**：四标识符模式与五种认知构型是全文的“数据结构”，不理解它就很难读懂后面的摩擦计算。
- **再看 §4.2 式 (1)–(2)**：$F^-$ 的四个分量与权重、$F^+$ 的动作空间；注意 $F^-$ 不是简单的“一致/不一致”分数。
- **重点看 §7.1–7.2 与表 5–8**：主结果、稳定性、三级消融；尤其注意 FPP 的“高 F1 但坍缩”这一反例，对设计 RL 奖励很有警示意义。
- **最后看 Limitations 与 Potential Risks**：作者对“离线摩擦”“二阶标签非金标准”“GPT-5 偏差”“双用途”的说明比较克制，适合作为复现时的边界条件。
- **注意**：本文是 **Findings** 而非 EMNLP 主会；若单位只认主会 CCF-B，请把本篇按“Findings（非主会）”处理。

## 文件说明

- `原文_EMNLP2026正式版.pdf`：ACL Anthology 正式版（16 页，pp. 12763–12778，含 DOI 与官方排版）
- `原文_arXiv2608.30719.pdf`：arXiv 预印版（便于检索/复制；正式版与预印版以正式版为准）
- `翻译_正文中文.md`：正文全文中文翻译（标题 → 结论、Limitations、致谢、Potential Risks，含表 1–9 与图 1 说明；不含参考文献与附录）
- `翻译_正文中文.docx`：同一译文的 Word 版
- `README.md`：本导读

## BibTeX

```bibtex
@inproceedings{zhu2026mind,
  title     = {Mind the Gap: Theory-of-Mind-Grounded Friction for Epistemic Alignment},
  author    = {Zhu, Yifan and Rim, Kyeongmin and Pustejovsky, James},
  booktitle = {Findings of the Association for Computational Linguistics: EMNLP 2026},
  pages     = {12763--12778},
  year      = {2026},
  doi       = {10.18653/2026.findings-emnlp.605}
}
```
