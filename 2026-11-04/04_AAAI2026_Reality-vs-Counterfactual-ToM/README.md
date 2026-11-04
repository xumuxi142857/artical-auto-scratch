# 04 | AAAI 2026（CCF-A）| 现实 vs 反事实：多世界对比强化学习提升 MLLM 的自我中心视频心智理论

> **英文标题**：Reality vs Counterfactual: Multi-World Contrastive Reinforcement Learning for Enhancing MLLM's Theory of Mind in Egocentric Videos
> **中文译名**：现实 vs 反事实：多世界对比强化学习提升多模态大模型在自我中心视频中的心智理论能力

| 项目 | 内容 |
|---|---|
| 会议 | **AAAI-26**（第 40 届 AAAI 人工智能会议，2026-01-20~27，Singapore） |
| CCF 等级 | **CCF-A**（人工智能） |
| 出版信息 | *Proceedings of the AAAI Conference on Artificial Intelligence*, Vol. 40, No. 3, pp. **1828–1836**；DOI: **10.1609/aaai.v40i3.37162**；2026-03-14 出版 |
| 分会场 | AAAI Technical Track on Cognitive Modeling & Cognitive Systems |
| 作者 | Guiyang Hou$^{1*}$, Yihui Fu$^{2*}$, Chen Wu$^{1}$, Xiang Huang$^{3}$, Zhe Zheng$^{1}$, Wenqi Zhang$^{1}$, Yongliang Shen$^{1}$, Weiming Lu$^{1\dagger}$（\*同等贡献，$\dagger$通讯作者） |
| 单位 | $^{1}$ 浙江大学；$^{2}$ 西北大学；$^{3}$ 通义实验室（Tongyi Lab） |
| 官方页面 | https://ojs.aaai.org/index.php/AAAI/article/view/37162 |
| 官方 PDF | https://ojs.aaai.org/index.php/AAAI/article/view/37162/41124 |
| arXiv | 未找到 arXiv 版本（截至 2026-11-04 用 arXiv API 按标题检索无结果），仅有 AAAI 正式版 |
| 代码 | 原文未给出代码链接；截至抓取时未发现公开仓库 |
| 数据 | 训练/域内评测用 EgoToM（Li et al., 2025c）；域外评测用 EgoTaskQA（Jia et al., 2022），均为公开数据集 |
| 主题标签 | 心智理论 ToM · **GRPO** · 对比强化学习 · 多模态大模型 MLLM · 自我中心视频 · 具身智能体 |

## 一句话概括

针对“仅用结果奖励的 GRPO 会靠孤立动作走捷径”的问题，作者在 GRPO 中加入**多世界对比奖励**：同一个 ToM 问题分别喂入真实动作序列与打乱的反事实序列，只有当真实序列的答对比例显著高于反事实序列时才给正奖励，从而逼模型学习动作序列中的时间/因果演化模式；在 EgoToM 域内把 7B 骨干从 54.67% 提升到 84.67%（+30.00%），并比原始 GRPO 高 2.00%。

## 为什么今天推荐它（与三个关键词的对应）

- **GRPO 的直接改进**：不是简单套用 GRPO，而是指出“结果奖励 + 格式奖励”在 ToM 上会奖励捷径，并给出一个可复用的对比奖励设计（式 4），对做 RL 后训练的人最有方法迁移价值。
- **ToM 的多模态/具身版本**：把 ToM 从文本故事推进到**第一人称自我中心视频**，目标、信念、下一动作三类心理状态都有评测，补上了现有 ToM 工作“文本域强、具身域弱”的缺口。
- **LLM 心智推理的机制分析**：除数字外，作者对比了 Base / Vanilla GRPO / MWCRL 的推理轨迹，报告“aha moment”（“Let's verify”“Oh, I know”）以及“真正依赖序列演化”与“依赖孤立动作捷径”的定性差异。

## 核心贡献

1. **提出“心理世界模型”论点**：具身智能体除了物理世界模型，还需要对用户心理状态（目标、信念、下一动作）建模；这是把 ToM 纳入具身智能体架构的明确主张。
2. **MWCRL 方法**：在 GRPO 的格式/结果/长度奖励之外，引入多世界对比奖励 $r_{\text{mwc}}$——真实动作序列与反事实（打乱）序列分组比较，只有 $p > \mu\tilde{p}$ 才给 $\alpha$ 奖励，显式鼓励利用时间与因果演化模式。
3. **首个自我中心视频 ToM 的 RL 后训练研究**：以 Qwen2.5-VL-7B-Instruct 为骨干，在 EgoToM 上做域内评测，并自建四类 OOD 问题（动作因果依赖、下一动作、信念、多跳）检验泛化。
4. **SFT vs RL 的系统对比**：域内直接 SFT 与混合多域 SFT 仅 56.00%/56.67%，远低于 RL 方法，支持“SFT 记忆、RL 泛化”的判断。
5. **超参数与失败模式分析**：给出 $\alpha$、$\mu$ 的取值建议（$\alpha$ 不宜过大，$\mu$ 适度放松更好），并指出“目标推断易、信念与动作推断难”的稳定模式。

## 主要结果（原文口径）

- **域内（EgoToM）**：MWCRL（α=0.3, µ=0.8）平均 **84.67%**；骨干 Qwen2.5-VL-7B 为 54.67%（**+30.00%**），原始 GRPO 为 82.67%（**+2.00%**）。分项：信念 82.00%、目标 94.00%、下一动作 78.00%。人类 83.33%，Gemini-2.5-pro 73.33%。
- **域外（EgoTaskQA，4 类 × 30 视频）**：MWCRL 平均 **57.50%**；骨干 51.67%（**+5.83%**），原始 GRPO 52.50%（**+5.00%**）。分项：动作依赖 46.67%（对 GRPO +10.00%）、信念 66.67%（对骨干 +13.34%）、动作—物体状态 63.33%、多跳 53.33%。
- **SFT 对照**：Direct SFT 56.00%，Mixed Multi-domain SFT 56.67%，仅比骨干高 +1.33%/+2.00%。
- **超参数**：α=0.3、µ=0.6 时平均最高 85.33%；α 从 0.3 增至 0.6 会下降 2.67%～4.67%；µ 从 1.0 放宽到 0.8/0.6 提升 0.67%～1.33%。
- **训练成本**：Qwen2.5-VL-7B + VeRL + DeepSpeed ZeRO-3，4×A800（80GB），3 epoch，每次约 8～10 小时；全局批大小 4，最大提示 16,384 token，最大生成 768 token。

## 阅读建议

- **先看方法**：§“Multi-World Contrastive Reinforcement Learning via GRPO” 的奖励建模（式 1–5）与图 2；重点理解 $r_{\text{mwc}}$ 为什么能抑制“孤立动作捷径”。
- **再看结果**：表 1（域内）、表 2（OOD）；注意最优平均分 85.33% 出现在 α=0.3、µ=0.6，而正文主配置是 84.67%。
- **最后看分析**：§“Goal Inference Is Easy; Belief and Action Inferences Are Hard” 与 Case Study，对设计新实验最有启发。
- **局限（作者未单列 Limitations，读者需自行注意）**：仅 7B 单骨干、单一 EgoToM 训练集；OOD 仅 120 段视频；对比奖励依赖“打乱序列”这一反事实构造，打乱方式本身可能引入偏置；未报告多次随机种子的方差。

## 文件说明

- `原文_AAAI2026正式版.pdf`：AAAI-26 正式出版版（9 页，pp. 1828–1836，含 DOI 与官方排版，引用以此为准）
- `翻译_正文中文.md`：正文全文中文翻译（标题 → 结论/致谢，含图 1–3 说明与表 1–2；不含参考文献）
- `翻译_正文中文.docx`：同一译文的 Word 版
- `README.md`：本导读

## BibTeX

```bibtex
@inproceedings{hou2026reality,
  title     = {Reality vs Counterfactual: Multi-World Contrastive Reinforcement Learning for Enhancing MLLM's Theory of Mind in Egocentric Videos},
  author    = {Hou, Guiyang and Fu, Yihui and Wu, Chen and Huang, Xiang and Zheng, Zhe and Zhang, Wenqi and Shen, Yongliang and Lu, Weiming},
  booktitle = {Proceedings of the AAAI Conference on Artificial Intelligence},
  volume    = {40},
  number    = {3},
  pages     = {1828--1836},
  year      = {2026},
  doi       = {10.1609/aaai.v40i3.37162}
}
```
