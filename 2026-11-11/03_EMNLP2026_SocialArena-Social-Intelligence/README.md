# SocialArena: Evaluating Social Intelligence in Large Language Models

> **EMNLP 2026（Oral）｜CCF-B｜ACL Anthology 2026.emnlp-main.1060，pp. 24329–24355**
> 一句话：首个「角色扮演 → 心智状态推理 → 行为推理」三层框架的社会智能基准，5,702 个场景、全人工竞技场 Elo 评测（$132.4K 标注投入），并证明当前 LLM-as-a-Judge 远不能替代人类评审。

| 项目 | 内容 |
|---|---|
| 会议 | EMNLP 2026（Conference on Empirical Methods in Natural Language Processing），**Oral** |
| CCF 等级 | **CCF-B** |
| 出版信息 | Proceedings of EMNLP 2026，pp. 24329–24355，2026 年 10 月 24–29 日；DOI: 10.18653/v1/2026.emnlp-main.1060 |
| Anthology ID | 2026.emnlp-main.1060 |
| arXiv | https://arxiv.org/abs/2610.39247（v1，2026-10-29） |
| 篇幅 | 正文 10 页（6 节 + 局限）+ 参考文献 + 附录 A–E |

## 作者与单位

Zongqi Wang¹、Rui Wang²、Yuchuan Wu²、Hua Yang²、Bingxue Qiu²、Tianle Gu¹、Bing Zhao²、Yujiu Yang¹、Jieping Ye²、Yongbin Li²

¹ 清华大学（Tsinghua University）｜² 阿里巴巴集团（Alibaba Group）

## 一句话概括

首个三层框架的 LLM 社会智能基准：5,702 个场景、全人工竞技场 Elo 评测。

## 为什么值得读（与三个关键词的对应）

- **Theory of Mind（骨架）**：七类心智状态（情绪、欲望、意图、感知、知识、信念、非字面沟通）既是**场景标注维度**，也是**评语分项维度**（T1–T7），可直接复用为 ToM 评测的标签体系；并且把 ToM 拆成「角色一致性 → 心智状态推理 → 行为推理」三层，指出模型「懂但做不到」。
- **LLM 心智推理（评测对象）**：以 15 个模型两两对战、人类多数投票的 Elo 排名给出社会智能的相对刻度；人类评语显示行为推理与 ToM 推理「压倒性偏负」，作者称之为**能力幻觉**（表层像样、深层推理塌陷）。
- **GRPO / RL（不训练，但直接可用）**：全文没有 RL 实验，但 §2.3 明确「仅评结果的行为标注」刻意对齐 **RLVR 的结果奖励范式**，因此其成对偏好可直接用作 GRPO/RLVR 的偏好奖励或评测环境；`SocialArena-RewardBench`（152 样本）则用于校准 judge / reward model 是否可信——结论是**当前 LLM judge 不宜直接当奖励源**（人类标签准确率 0.8355 vs 最佳 LLM 0.4474）。

## 核心贡献

1. **三层能力框架**：把社会智能拆成 角色扮演（role consistency）→ 心智状态推理（ToM）→ 行为推理（情境恰当行动），并给出可操作定义：「推断自他心智状态、生成情境恰当行为、同时保持角色一致」。
2. **带显式角色思考的评测范式**：模型必须先输出结构化 `character thinking`（按情绪 / 欲望 / 意图 / 感知 / 知识 / 信念 / 非字面沟通七类组织），再输出行为；使三个维度可在同一次生成中分别打分。
3. **U-TRIMF 场景合成框架**：六个正交维度（用户存在性 U、拓扑关系 T、关系模型 R、利益结构 I、动机类型 M、正式性 F）自顶向下组合出 **600 个基础场景模板**，再以关键词引导扩写为 5,702 个场景，保证场景空间的结构化覆盖。
4. **人工竞技场协议（非 LLM 打分）**：投入 **$132.4K** 招募并培训标注员；每题 ≥3 人独立标注、多数投票、三人全不一致即丢弃；强制自然语言评语 + 九维分项标注（T1–T7、T、B）；累计 **17,676 条人类投票**，Elo 排名。
5. **诊断性产出**：从人类评语归纳出 **100 条评价细则**；构建 **SocialArena-RewardBench**（152 样本），证明 LLM-as-a-Judge 在此任务上远逊于人类。

## 关键实验数字

| 项目 | 数值 | 出处 |
|---|---|---|
| 标注总投入 | **$132.4K**（招募 + 培训人类标注员） | 摘要 |
| 数据规模 | **5,702** 个社会场景 / **17,676** 条人类投票；**600** 个 U-TRIMF 基础模板 | §2.1、表 1 |
| 评测规模 | **15** 个模型两两对战，每对 **50–80** 场；每场 ≥3 名标注员、多数投票 | §3.1 |
| Elo 榜首 vs 末位 | gpt-5.1-2025-11-13 **1553.0**；qwen3-max **1400.0**；doubao-seed-1-8 **1398.5**；末位 olmo-3.1-32b-think **828.5**（极差 **724.5**） | 图 2 |
| 人类 vs LLM 评判（标签准确率） | Human **0.8355**；最佳 LLM claude-sonnet-4.6 **0.4474**（低 0.388）；gpt-5.4 0.4408、kimi-k2.5 0.4473、qwen3-max 0.4276 | 表 3 |
| 人类 vs LLM 评判（评语一致性） | Human **0.7632**；最佳 LLM qwen3-max **0.2500**（低 0.513） | 表 3 |
| 瓶颈定位 | Top-10 人类评语聚类中心中 **6 个**属「行为推理」，ToM / 角色扮演各 2 个 → 瓶颈在「做」不在「懂」 | 图 3 |
| 场景特异性 | 场景内 Kendall τ 对角 0.60–0.94（陌生人最高 0.94）；跨场景最低 **0.41**（冲突 × 恋爱/邻里） | 图 5 |
| 能力差距形态 | 角色扮演正/负评语较均衡，行为与 ToM 推理「压倒性偏负」（原文为比例图，未给标量分数） | 图 4 |

> 注：原文没有给出三层能力的百分制分数，只用图 4 的正/负评语比例呈现；也未报告与 MMLU 等基准的定量相关系数——引用时不要补具体 ρ 值。

## 主要局限（作者自述）

1. **偏好偏差**：标注者仅为英语与中文母语者，个体背景 / 沟通风格会引入偏差；计划以 Chatbot Arena 式的公开平台 **SocialArena-Platform** 众包更多视角。
2. **仅单轮**：多轮标注成本过高，先做单轮；待单轮数据充足后再开放多轮。
3. **隐性局限（读者可补）**：模型池仅 15 个且含 2025–2026 闭源快照，Elo 会随版本漂移；每对 50–80 场，Elo 置信区间不窄；场景由 Qwen3-235B 合成，存在生成模型自身的分布偏置。

## 阅读建议

- 想快速判断值不值得读：摘要 + 图 2 + 表 3（约 5 分钟）。
- 想做数据 / 评测复现：§2.2（U-TRIMF 六维）、§2.3（输出格式）、§2.4（协议与九维标注）、附录 C（关键词与过滤）、附录 D（标注指南）。
- 想做 reward model / RL：§4 + 表 3 + 附录 E.1（100 条细则体系）；注意表 3 的结论——LLM judge 现在还不能当奖励源。

## 文件说明

| 文件 | 说明 |
|---|---|
| `原文_EMNLP2026正式版.pdf` | 会议正式版（ACL Anthology，pp. 24329–24355，27 页含附录）。引用以正式版为准。 |
| `翻译_正文中文.docx` | 正文全文中译（摘要 → 结论与局限），不含参考文献与附录。 |
| `README.md` | 本文件。 |

## BibTeX

```bibtex
@inproceedings{wang2026socialarena,
  title     = {SocialArena: Evaluating Social Intelligence in Large Language Models},
  author    = {Wang, Zongqi and Wang, Rui and Wu, Yuchuan and Yang, Hua and Qiu, Bingxue
               and Gu, Tianle and Zhao, Bing and Yang, Yujiu and Ye, Jieping and Li, Yongbin},
  booktitle = {Proceedings of the 2026 Conference on Empirical Methods in Natural Language Processing},
  pages     = {24329--24355},
  year      = {2026},
  doi       = {10.18653/v1/2026.emnlp-main.1060},
  url       = {https://aclanthology.org/2026.emnlp-main.1060/}
}
```
