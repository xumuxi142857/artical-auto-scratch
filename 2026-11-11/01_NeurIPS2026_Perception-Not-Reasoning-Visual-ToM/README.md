# Perception, Not Reasoning, Limits Visual Theory of Mind

> **NeurIPS 2026（Evaluations & Datasets Track）｜CCF-A｜arXiv:2611.10694**
> 一句话：视觉心智理论（ToM）的瓶颈不在「推不出」，而在「看不见」——把真值场景状态喂给模型，视觉→文本的 20 多个百分点差距基本闭合。

| 项目 | 内容 |
|---|---|
| 会议 | NeurIPS 2026（第 40 届神经信息处理系统大会），Evaluations and Datasets Track |
| CCF 等级 | **CCF-A** |
| 出版信息 | NeurIPS 2026 论文集（2026 年 12 月出版，本文件夹为 arXiv 预印本 v1，2026-11-07 提交） |
| arXiv | https://arxiv.org/abs/2611.10694 |
| 项目页 | https://kurbanintelligencelab.github.io/perception-not-reasoning/ |
| 篇幅 | 正文 10 页（7 图 7 表）+ 参考文献 + 附录 A–H |

## 作者与单位

Mohamed Rayan Barhdadi¹、Syed Talal Wasim²˒³、Juergen Gall²˒³、Erchin Serpedin¹、Hasan Kurban⁴

¹ Texas A&M University｜² University of Bonn｜³ Lamarr Institute for Machine Learning and AI｜⁴ Hamad Bin Khalifa University

## 一句话概括

视觉心智理论的瓶颈是**场景状态感知**而非信念推理，补上真值场景描述即可闭合视觉与文本之间的差距。

## 为什么值得读（与三个关键词的对应）

- **Theory of Mind（核心主题）**：以 Sally-Anne 虚假信念任务为经典检验，按「物体个体化 → 目标归赋 → 信念建模」的发展级联组织三阶段探针，覆盖知识通达、意外内容、双房间转移、视角分歧、二阶信念等 10 个模板；理论框架借用 Apperly & Butterfill 的双系统与 Leslie 的元表征要求。
- **LLM 心智推理（直接相关，对象是 VLM）**：把「文本侧心智推理」当作**上限基线**（抽象图板阶段 3 纯文本 94.5%），据此论证语言侧推理基本完好、缺陷在视觉前端。它不是提出新的推理方法，而是给「LLM/VLM 到底缺推理还是缺感知」这一争论提供**可证伪的测量工具**。
- **GRPO / 强化学习（不涉及）**：全文为纯推理期评测，七个模型经 OpenRouter 以温度 0、单轮、零样本访问，**没有任何训练、微调或 RL 环节**；文中的「scaffold（支架）」指输入侧文本提示增强，与 RL 无关。

## 核心贡献

1. **五条件解离协议**：把同一个虚假信念问题的感知保真度从「纯视觉」经三个支架档（自动解析器支架 $B_a$、感知级支架 $B_p$、真值支架 $B_f$）连续变到「纯文本」，在推理任务恒定的条件下分离感知贡献与概念贡献。
2. **感知贡献率（Perceptual Contribution Ratio, PCR）**：$\mathrm{PCR}_x=[\mathrm{Acc}(B_x)-\mathrm{Acc}(A)]/[\mathrm{Acc}(C)-\mathrm{Acc}(A)]$，用单一剂量-反应比值刻画「给定保真度的支架闭合了视觉→文本差距的多大份额」；并证明它是同时满足端点校准、正仿射不变性、仿射依赖三条公理的唯一形式（§D.4）。
3. **跨两类刺激范式验证**：抽象 2D 图板（Heider–Simmel 传统，1,000 个程序化探针）与自然主义 3D 场景（MuMA-ToM 900 题、MindPower 492 场景 × 6 层）。
4. **病因学结论**：真值支架在各范式均大幅闭合差距（抽象与 MuMA-ToM 上甚至超过纯文本上限），而自动解析器（含前沿 VLM 充当解析器）失效；纯视觉下 **60% 的错误是「现实偏差」**——模型报告物体真实位置，而非缺席主体所信的位置。
5. **排除替代解释**：用内容阶梯、等长损坏对照、可见性陈述剥离三组实验，逐层排除「文本体量」「格式启动」「直接给出推理谓词」等解释。

## 关键实验数字

| # | 数字 | 出处 |
|---|---|---|
| 1 | 抽象 2D 阶段 3：纯视觉 **73.9%** vs 纯文本 **94.5%**，视觉→文本差距 **20.6 个百分点**；真值支架 $B_f$ 达 **98.4%**，$\mathrm{PCR}_f=1.19$（95% CI [1.09, 1.30]） | 表 1a、表 2a、表 3 |
| 2 | 七个 VLM 在抽象阶段 3 的 $\mathrm{PCR}_f$：前沿 1.22 / 中规模 1.01 / 小规模 1.26，**全部 ≥1**（超过纯文本上限） | 表 2a |
| 3 | MuMA-ToM：聚合 $\mathrm{PCR}_f=1.44$（前沿 1.81 / 中规模 1.57 / 小规模 0.66），$B_f$ 均值 **58.1%** vs 纯视觉 44.7% | 表 2b、表 4 |
| 4 | MindPower：$B_f$ 恢复 13.9 个百分点差距中的 **59%**（中规模 $\mathrm{PCR}_f=0.86$ 最强）；受泄漏控制的 $B_p$ 在前沿仅恢复 39%、中规模 42% | 表 2c、表 1c |
| 5 | 自动解析器失效：抽象阶段 3 聚合 $\mathrm{PCR}_a=0.09$，**中规模档位 −1.10（解析器主动误导）**；MindPower 上 GPT-4o 作解析器 −0.06、Claude 作解析器 −0.08 | 表 2a、表 5 |
| 6 | 现实偏差占纯视觉错误的 **549/915 = 60.0%**；该占比在各能力档位间差异 <5 个百分点 | §4（图 4） |
| 7 | 内容阶梯增量：实体列表 +0.1 pp（p=.84）、静态位置 +2.8 pp（p=.0033）、**跨帧事件结构 +12.1 pp（最大单项）**、可见性/缺席 +9.6 pp，合计 +24.5 pp | 表 6 |
| 8 | 等长损坏对照：$D_{\text{mismatch}}$ +0.8 pp（p=.38，不显著）、$D_{\text{noise}}$ +5.6 pp、$D_{\text{shuffled}}$ +6.7 pp，三者合计不及 $B_p$ 增益 14.9 pp 的一半 | 表 6 |
| 9 | 提示侧稳健性：思维链平均 −1.7 pp，自支架 **−18.7 pp**；三种问题改写下纯视觉准确率波动 ≤4.0 pp | 表 7 |
| 10 | 评测规模：**7 个 VLM、约 159,000 次 API 调用**（抽象 ~111,000、自然主义 ~48,000），温度 0、单轮、≤200 输出 token | §3.4 |

## 主要局限（作者自述，§6）

1. **覆盖面**：只测两种刺激范式与七个**黑盒 API 模型**；野外视频与开放权重的「以对象为中心」模型未测。
2. **解释层级**：论断是**功能性**的（供给场景状态则缺陷闭合），而非**机制性**的；感知与推理在实现上交织（思维链对 Claude Sonnet 4 有效 78.8→90.6，但仍未超过其 $B_p$ 的 97.6）。
3. **边界依赖操作定义**：「跨帧事件链接」被归入感知；若改归推理，阶梯中 +12.1 pp 的增量归属会移动。
4. **对照偏弱**：损坏对照依赖具体模型，$D_{\text{mismatch}}$ 可能被有用模板线索抵消，因此只反驳了「文本体量」解释，**未判定收益是否必须是与图像绑定的内容**。
5. **上限不可完全解读**：抽象图板上 $B_f$ 与 C 的文本本身不同，作者明确不进一步解读 PCR>1。

## 阅读建议

先读 §3.1 的五条件定义与 §3.3 的 PCR 公式（全文测量骨架），再读 §4 前三条论断（真值支架有效 / 自动解析器失效 / 剂量-反应单调），最后看 §4 的现实偏差分类（60% 这个数字最有传播力）与 §6 局限。若只关心接口，直接看 §3.3 的「PCR 是唯一满足三条公理的指标」证明（§D.4）与 §5 的架构含义段。

## 文件说明

| 文件 | 说明 |
|---|---|
| `原文_arXiv2611.10694.pdf` | 论文原文（arXiv v1）。NeurIPS 2026 正式论文集 2026 年 12 月出版，届时可替换为正式版；引用如无页码，用 arXiv 号。 |
| `翻译_正文中文.docx` | 正文全文中译（摘要 → §7 结论 → 致谢，含 7 张表），不含参考文献与附录。 |
| `README.md` | 本文件。 |

## BibTeX

```bibtex
@inproceedings{barhdadi2026perception,
  title         = {Perception, Not Reasoning, Limits Visual Theory of Mind},
  author        = {Barhdadi, Mohamed Rayan and Wasim, Syed Talal and Gall, Juergen
                   and Serpedin, Erchin and Kurban, Hasan},
  booktitle     = {Advances in Neural Information Processing Systems (NeurIPS 2026),
                   Track on Evaluations and Datasets},
  year          = {2026},
  eprint        = {2611.10694},
  archivePrefix = {arXiv},
  primaryClass  = {cs.CV},
  url           = {https://arxiv.org/abs/2611.10694}
}
```
