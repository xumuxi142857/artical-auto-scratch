# 03 | ACL 2026（CCF-A）| GroupToM-Bench：群体心智理论与非线性的社会涌现

> **英文标题**：GroupToM-Bench: Benchmarking Group Theory of Mind and Nonlinear Social Emergence in MLLMs
> **中文译名**：GroupToM-Bench：面向多模态大模型的群体心智理论与非线性社会涌现基准

| 项目 | 内容 |
|---|---|
| 会议 | **ACL 2026**（第 64 届计算语言学协会年会，Long Paper） |
| CCF 等级 | **CCF-A**（自然语言处理） |
| 出版信息 | Proceedings of the 64th ACL（Volume 1: Long Papers），**pp. 40007–40031**，July 2–7, 2026；DOI: 10.18653/v1/2026.acl-long.1859 |
| 作者 | Weidong Tang, Jierui Li, Yueling Hou, Zihan Mei, Can Zhang, Xinyan Wan, Zhiyuan Liang, Pengfei Zhou, Yang You, Wangbo Zhao |
| 单位 | 西安电子科技大学、新加坡国立大学、电子科技大学、中国科学技术大学 |
| 官方页面 | https://aclanthology.org/2026.acl-long.1859/ |
| arXiv | https://arxiv.org/abs/2606.04184 |
| 数据 | https://huggingface.co/datasets/Twwwd/GroupToM-Bench |
| 主题标签 | 群体 ToM · BDI · 社会涌现 · 从众/群体思维 · 多模态评测 · MLLM |

## 一句话概括

把 ToM 评测从"单个人的信念追踪"推进到"**一群人的心理状态如何非线性聚合成集体结果**"：构建首个多模态群体 ToM 基准（240 个专家设计场景、8 个社会领域、7 级认知审计链），并揭示当前 MLLM 普遍存在 **"群体认知鸿沟（Group Cognitive Gap）"**——能读懂个体心思，却把群体当成个体意图的线性叠加，从而错过群体思维、赢家诅咒这类结构性陷阱。

## 为什么今天推荐它（与你的三个关键词的对应）

- **ToM 前沿评测**：从一阶/高阶信念（Hi-ToM、BigToM 那一类）跨到**群体层 ToM**，是 2026 年 ToM 研究明显的下一个增长点；ACL 2026 主会长文，方法学规范（含人类上限、LLM-as-judge 元评估、多模态必要性消融）。
- **LLM 心智推理的"诊断器"**：它给出的失败模式（线性叠加偏差、乐观理性共识、结构约束瓶颈）可以直接用来解释你观察到的模型行为。
- **做 GRPO/RL 实验的好靶场**：L5（结构约束）需要开放式生成、且与多项选择评测不相关，适合做"RL 能否教会模型推理结构约束"的对照实验。

## 核心贡献

1. **首个群体级 ToM 多模态基准**：240 个专家种子场景 + 生成式扩展 + 多模态合成，覆盖 8 个社会-心理领域（含权力、从众、面子、联盟等）。
2. **三层因果链建模**：微观 BDI 适应（信念/愿望/意图）→ 中观群体张力与结构约束 → 宏观集体结果预测与机制归因。
3. **七级认知审计框架（L1–L7）**：从个体心理状态识别，逐级推进到群体涌现动力学，可定位"在哪一级崩掉"。
4. **诊断性发现**：提出并量化 Group Cognitive Gap，指出视觉信息被当作背景噪声、模型系统性偏向"理性共识"。

## 主要结果（Table 1/2 口径）

| 层级 | 人类（Base） | GPT-4o | Qwen3-VL-8B |
|---|---|---|---|
| L1 | 91.7 | 79.8 | 73.3 |
| L2 | 90.5 | 75.3 | 68.8 |
| L3 | 88.4 | 72.7 | 69.6 |
| L4 | 89.4 | 50.3 | **37.3** |
| L5 | 90.1 | 47.2 | 47.8 |
| L6 | 89.2 | 48.6 | **34.3** |
| L7 | 88.1 | 53.4 | 53.6 |

- **个体层尚可、群体层崩塌**：人类全程稳定在 ~88–92%；模型从 L3 到 L4 断崖式下跌（Qwen3-VL-8B 69.6 → 37.3），L6 跨模型平均仅 **36.4%**（随机基线 6.7%）。
- **结构约束瓶颈（L5）**：该级要求开放式生成"层级权威与沟通拓扑如何把微观张力放大为集体假共识"。GPT-4o 在此被 Gemini 3-pro 反超（47.2% vs 59.7%），说明它考的既不是通用能力，也不是选择题套路。
- **多模态形同虚设**：去掉图像后 GPT-4o 平均只掉 **1.9 分**，人类掉 4.0 分，Qwen3-VL-8B 只掉 0.5 分——模型几乎没在用视觉结构线索，暴露"视觉盲"。
- **作者自述局限**：部分样本可仅凭文本解出；安全对齐可能抑制模型模拟"非理性/破坏性"集体结果；场景偏西方文化规范。

## 阅读建议

- 抓框架：§2.1 三层因果链 → §2.2 七级审计 → §2.3 基准构建与人类验证。
- 抓结论：§3.2 主结果（Group Cognitive Gap、结构约束瓶颈、L6 失败模式分类）→ §3.3 多模态必要性 → §5 结论与展望。
- 若要做 RL：把 L4–L6 当作 reward 难以定义的高难目标，正好检验 GRPO 在"开放式社会推理"上的边界。

## 文件说明

- `原文_ACL2026正式版.pdf`：**正式出版版**（ACL Anthology，pp.40007–40031，25 页，含官方排版与页码，引用时以此为准）
- `原文_arXiv2606.04184.pdf`：arXiv v2 预印版（便于检索/复制，内容与正式版基本一致）
- `翻译_正文中文.md`：正文全文中文翻译（标题 → 结论/局限/致谢，不含参考文献与附录）
- `翻译_正文中文.docx`：同一译文的 Word 版
- `README.md`：本导读

## BibTeX

```bibtex
@inproceedings{tang2026grouptom,
  title     = {GroupToM-Bench: Benchmarking Group Theory of Mind and Nonlinear Social Emergence in MLLMs},
  author    = {Tang, Weidong and Li, Jierui and Hou, Yueling and Mei, Zihan and Zhang, Can and Wan, Xinyan and Liang, Zhiyuan and Zhou, Pengfei and You, Yang and Zhao, Wangbo},
  booktitle = {Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics (ACL 2026)},
  year      = {2026},
  doi       = {10.18653/v1/2026.acl-long.1859}
}
```
