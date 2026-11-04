# 01 | ICML 2026（CCF-A）| 从捷径到推理：用强化学习做稳健的心智理论后训练

> **英文标题**：From Shortcuts to Reasoning: Robust Post-Training of Theory of Mind with Reinforcement Learning
> **中文译名**：从捷径到推理：以强化学习实现稳健的心智理论后训练

| 项目 | 内容 |
|---|---|
| 会议 | **ICML 2026**（第 43 届国际机器学习大会，Seoul，2026-07-06~11） |
| CCF 等级 | **CCF-A**（人工智能） |
| 出版信息 | Proceedings of Machine Learning Research, Vol. 306, pp. 164397–164419 |
| 作者 | Jike Zhong, Yuxiang Lai, Ming Li, Yuheng Li, Wuao Liu, Behzad Dariush, Konstantinos Psounis, Shao-Yuan Lo |
| 单位 | 南加州大学、埃默里大学、马里兰大学、佐治亚理工、马萨诸塞大学阿默斯特分校、Honda Research Institute USA、台湾大学 |
| 官方页面 | https://proceedings.mlr.press/v306/zhong26i.html |
| arXiv | https://arxiv.org/abs/2606.09092 |
| 代码 | https://github.com/jkz-338/Robust-ToM-RL |
| 主题标签 | 心智理论 ToM · 强化微调 RFT/RLVR · 高阶信念推理 · 多模态 ToM · 捷径审计 |

## 一句话概括

作者先证明"很多 ToM 基准可以靠虚假相关刷到 99% 准确率"，再构建一套**捷径审计流程**筛出无捷径数据集，然后在这套干净数据上证明：**带显式思维链的可验证奖励强化微调（Thinking-RFT）稳定优于 SFT 和无思维链 RFT**，且泛化更好、更抗反事实扰动。

## 为什么今天推荐它（与你的三个关键词的对应）

- **LLM 心智推理**：直接把 ToM 当作"后训练能力"来研究，而不是再刷一个 benchmark，属于"怎么把 ToM 训出来"这一支。
- **ToM**：核心对象就是 belief / desire / intention 等心理状态的推断与使用。
- **GRPO / RL 后训练**：用的是规则化可验证奖励的强化微调（rule-based RFT，即 RLVR 路线），和 GRPO 属于同一技术家族；本文结论对"ToM 到底该不该用 RL 训"这个争议给出了关键解释。
- **方法论价值高**：它解释了文献中"有人说 SFT 更好、有人说 RL 更好"的矛盾——**差异主要来自基准是否可走捷径**。这一点对你设计 ToM 实验很有用。

## 核心贡献

1. **捷径审计框架**：提出可操作的流程，量化 ToM 数据集被"伪因果相关"利用的程度；发现可归约为纯状态追踪的问题（如 belief）远比需要真正推理的问题（如 intention）更容易被捷径攻破。
2. **清洗后的评测套件**：在叙事、对话、多模态三类 ToM 语境下，整理出 4 个"无捷径"数据集，作为公平比较 RFT 与 SFT 的基础。
3. **Thinking-RFT**：把"显式推理链 + 可验证奖励 + RL"组合起来做 ToM 后训练。
4. **机制分析**：通过推理轨迹与注意力分析指出，RFT 之所以有效，是模型学会了把推理**锚定到因果线索（关键词、状态变化）**上，而不是表面模式。

## 主要结果（原文摘要口径）

- Thinking-RFT 相对 SFT：整体 **+6%**；复杂高阶推理 **+10%**；多模态情形 **+7%**。
- Thinking-RFT 相对 No-Thinking-RFT：平均 **+7%**，说明 ToM 的提升来自"推理"与"RL"的**联合作用**，而非单纯 RL。
- 在未见领域、更高阶查询上泛化更好；对反事实信息更稳健。
- 与 Lu et al. (2025) 的相反结论做了对照：在捷径严重的基准（Hi-ToM、ExploreToM）上 SFT 反而更好，这正说明**数据筛选决定结论**。

## 阅读建议

- 想快速抓重点：读 §1 引言、§2.1–2.3（捷径审计与发现）、§4.2 主结果、§7 结论。
- 想做实验复现：重点看 §3（RL 目标与奖励设计）、§4.1（实验设置）与附录中的训练细节。
- 若你关心 GRPO：本文未直接点名 GRPO，但奖励构造与训练范式与 GRPO/RLVR 高度同源，可对照本目录第 2 篇（MindZero，明确使用 GRPO）。

## 文件说明

- `原文_ICML2026正式版_PMLR306.pdf`：**正式出版版**（PMLR Vol.306, pp.164397–164419，23 页，含官方排版与页码，引用时以此为准）
- `原文_arXiv2606.09092.pdf`：arXiv 预印版（便于检索/复制，内容与正式版一致）
- `翻译_正文中文.md`：正文全文中文翻译（标题 → 结论，不含参考文献与附录）
- `翻译_正文中文.docx`：同一译文的 Word 版，便于批注与打印
- `README.md`：本导读

## BibTeX

```bibtex
@inproceedings{zhong2026shortcuts,
  title     = {From Shortcuts to Reasoning: Robust Post-Training of Theory of Mind with Reinforcement Learning},
  author    = {Zhong, Jike and Lai, Yuxiang and Li, Ming and Li, Yuheng and Liu, Wuao and Dariush, Behzad and Psounis, Konstantinos and Lo, Shao-Yuan},
  booktitle = {Proceedings of the 43rd International Conference on Machine Learning},
  series    = {Proceedings of Machine Learning Research},
  volume    = {306},
  pages     = {164397--164419},
  year      = {2026},
  publisher = {PMLR}
}
```
