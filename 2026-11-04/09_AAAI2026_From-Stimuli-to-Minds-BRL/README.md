# From Stimuli to Minds: Enhancing Psychological Reasoning in LLMs via Bilateral Reinforcement Learning

> **会议**：AAAI 2026（AAAI-26），CCF-A
> **出版**：Proceedings of the AAAI Conference on Artificial Intelligence, Vol. 40, No. 1, pp. 274–282（2026）
> **作者**：Yichao Feng*、Haoran Luo*、Lang Feng、Shuai Zhao、Anh Tuan Luu（* 同等贡献；南洋理工大学计算与数据科学学院）
> **代码**：https://github.com/Githubuseryf/Stimuli2Minds ｜ **扩展版**：arXiv:2508.02458
> **本地文件**：`原文_AAAI2026正式版.pdf`（9 页）、`原文_arXiv2508.02458.pdf`（17 页）、`翻译_正文中文.md/.docx`

## 一句话概括

用“专家心理标注数据 + 双边奖励的轨迹感知 GRPO（T-GRPO）”训练小模型，让 Qwen2.5 系列（0.5B/1.5B/3B）在 ToMbench、SimpleToM、SocialIQa 等 OOD 心理基准上追上甚至超过用 70B 模型合成数据训练的效果。

## 与三个关键词的对应

| 关键词 | 对应程度 | 说明 |
| --- | --- | --- |
| LLM 心智推理 / 心理推理 | 强 | 任务就是心理状态推断（特定情绪、目标情绪、变化方向、自我认同、需求满足、国家主题六个维度） |
| 心智理论 ToM | 中 | 以 ToMbench 等 ToM 基准做主评测，但方法本身是“心理推理”而非严格意义上的信念推断 |
| GRPO | 强 | 核心算法是 T-GRPO（Trajectory-aware Group Relative Policy Optimization），双边奖励（bilateral reward, BR） |

## 核心贡献

1. **StimuliQA 数据集**：以心理学理论 + 真实访谈为基础，3,000+ 条刺激、58 个心理变量的人工标注数据，再转成 QA；训练/测试各 10,800 / 5,400 条实例。
2. **Psy-Interpreter 框架**：受双系统理论启发，把轨迹缓存（trajectory cache）与双边推理（bilateral reasoning, BR）结合，在多种心理任务上做“类专家”推理。
3. **双边奖励**：把词元准确率、格式合规、推理深度、重复控制整合成一个统一奖励，并做长度归一化；比 Basic R1、单侧奖励更均衡。
4. **持续学习**：用高置信预测自标注，迭代提升，缩小“专家监督”与“自主推理”的差距。
5. **可判断是否需要推理**（RQ5）：模型能识别哪些题需要显式推理、哪些可直接回答。

## 主要结果（数字取自正式版）

- **表 1（SFT，StimuliQA vs 合成数据 LlamaQA / MistralQA）**：Qwen2.5-3B 在 StimuliQA 上 ToMbench F1 22.06 / Acc 42.38%，SimpleToM F1 37.62 / Acc 56.44%，SocialIQa F1 43.40 / Acc 53.74%，均高于两个合成数据基线（如 SimpleToM：LlamaQA 18.48/26.16%，MistralQA 35.02/33.33%）。
- **表 2（奖励设计）**：BR 把 Qwen2.5-1.5B 总体 F1 从 34.46 提到 39.98；需求满足 +5.66、国家主题 +5.71。跨规模增益稳定（Qwen-3B +5.34、Qwen-0.5B +5.74）。
- **核心结论**：小模型 + 专家标注 + 结构化 RL，可以在多个基准上媲美大得多的系统。

## 阅读建议

- 先看 §3 方法（StimuliQA 构建、T-GRPO 目标、双边奖励、轨迹缓存、持续学习），公式集中在 T-GRPO 目标那一节。
- 再看 §4.2/§4.3（RQ1 数据质量、RQ2 奖励设计），这两节是全文最有信息量的实验。
- 与同日的 `04_AAAI2026_Reality-vs-Counterfactual-ToM` 对照读：那篇用反事实对比奖励改 GRPO 做多模态 ToM，这篇用双边奖励改 GRPO 做心理推理，奖励设计思路可以互相借鉴。

## 文件说明

| 文件 | 内容 |
| --- | --- |
| `原文_AAAI2026正式版.pdf` | AAAI-26 正式版（9 页），引用以它为准 |
| `原文_arXiv2508.02458.pdf` | arXiv 扩展版（17 页，含附录） |
| `翻译_正文中文.md` | 正文全文中文翻译（不含 References/附录） |
| `翻译_正文中文.docx` | 同上 Word 版 |

## BibTeX

```bibtex
@inproceedings{feng2026stimuli,
  title     = {From Stimuli to Minds: Enhancing Psychological Reasoning in {LLMs} via Bilateral Reinforcement Learning},
  author    = {Feng, Yichao and Luo, Haoran and Feng, Lang and Zhao, Shuai and Luu, Anh Tuan},
  booktitle = {Proceedings of the AAAI Conference on Artificial Intelligence},
  volume    = {40},
  number    = {1},
  pages     = {274--282},
  year      = {2026}
}
```
