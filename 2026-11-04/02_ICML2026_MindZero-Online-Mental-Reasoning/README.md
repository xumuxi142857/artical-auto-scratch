# 02 | ICML 2026（CCF-A）| MindZero：零标注的在线心智推理

> **英文标题**：MindZero: Learning Online Mental Reasoning With Zero Annotations
> **中文译名**：MindZero：零标注学习在线心智推理

| 项目 | 内容 |
|---|---|
| 会议 | **ICML 2026**（第 43 届国际机器学习大会，Seoul，2026-07-06~11） |
| CCF 等级 | **CCF-A**（人工智能） |
| 出版信息 | Proceedings of Machine Learning Research, Vol. 306（PMLR） |
| 作者 | Shunchi Zhang\*, Jin Lu\*, Chuanyang Jin\*, Yichao Zhou\*, Zhining Zhang, Tianmin Shu（\*同等贡献） |
| 单位 | 约翰霍普金斯大学（JHU）、北京大学 |
| 官方页面 | https://proceedings.mlr.press/v306/zhang26dx.html |
| arXiv | https://arxiv.org/abs/2606.00240 |
| 项目页 | https://scai.cs.jhu.edu/MindZero |
| 主题标签 | 心智理论 ToM · **GRPO** · 自监督强化学习 · 在线信念推断 · 主动辅助 · 多模态大模型 |

## 一句话概括

不做心理状态标注、也不靠"猜完再验证"的慢速模型式推理：MindZero 用**自监督强化学习（GRPO）**，以"生成的信念假设能多好地解释智能体观察到的行为"为奖励，把模型式 ToM 的推理结构**内化进 MLLM 的单次前向**，从而同时获得准确率、不确定度追踪能力和实时效率。

## 为什么今天推荐它（与你的三个关键词的对应）

- **GRPO 实战范例**：全文明确使用 GRPO（§4.1 与附录训练细节：标准 GRPO + VeRL + 4×H100），是"GRPO 用来训 ToM / 心理状态推理"的少数已录用会议论文之一，工程细节完整，非常值得对照复现。
- **ToM 的"在线"版本**：不是一次性故事问答，而是随观测流不断更新多个假设的后验概率——更接近真实交互中的心智推理。
- **LLM 心智推理的方法论**：回答了"要不要显式维护假设分布"这一关键设计问题——答案是"训练时用、推理时不用"。

## 核心贡献

1. **自监督 RL 框架**：奖励来自"假设对观测行为的解释力"（由 planner 估计动作似然），**完全不需要心理状态真值标注**，解决了真实场景无标注的痛点。
2. **在线多假设维护**：模型逐步输出多个目标/信念假设及其概率，随新动作更新，能处理歧义与不确定度（对应 Figure 1 的"拿第二个盘子 → 假设概率翻转"示例）。
3. **推理时摊销**：训练完成后把模型式（model-based）推理**蒸馏进单次前向**，避免 ThoughtTracing / AutoToM 那类测试时的高昂计算。
4. **系统性评测**：GridWorld 与 Household 两个域 × 问答与主动辅助两类任务，并含人类实验与消融。

## 主要结果（原文口径）

- **问答**：GridWorld QA 上 Qwen3-VL-4B/8B 均为最佳，较基座提升约 **2.1–2.5 个点**；Household QA 上 MindZero + Llama-3.2-3B 在开源与测试时扩展方法中最高，接近最强闭源系统而推理成本极低。
- **主动辅助（任务完成加速）**：GridWorld 中 Qwen3-VL-4B / 8B 分别取得 **23.0% / 24.5%** 的加速；Household 中 Qwen3-4B 达 **19.1%**。相比之下 GPT-5.2、Gemini-3-Flash 的假设不断跳变，导致动作不稳定、几乎无加速——说明"稳定的不确定度追踪"本身就是能力。
- **效率**：相同或更优准确率下，推理成本显著低于 model-based 基线。
- **消融**：验证了 GRPO、多假设表示、planner 似然奖励各自的必要性。

## 阅读建议

- 抓方法：§3 问题形式化（在线心智推理 + 主动辅助）→ §4.1–4.2（SSRL 与奖励设计）→ 附录训练细节（GRPO/VeRL 超参）。
- 抓结论：§6.1 总体结果、§6.2 在线目标推断动态、§6.3 消融、§6.4 人类实验。
- 局限（作者自述）：不建模多智能体间的递归推理；输入序列变长时 token 开销上升。

## 文件说明

- `原文_ICML2026正式版_PMLR306.pdf`：**正式出版版**（PMLR Vol.306，21 页，含官方排版与页码，引用时以此为准）
- `原文_arXiv2606.00240.pdf`：arXiv 预印版（便于检索/复制，内容与正式版一致）
- `翻译_正文中文.md`：正文全文中文翻译（标题 → 结论，不含参考文献与附录）
- `翻译_正文中文.docx`：同一译文的 Word 版
- `README.md`：本导读

## BibTeX

```bibtex
@inproceedings{zhang2026mindzero,
  title     = {MindZero: Learning Online Mental Reasoning With Zero Annotations},
  author    = {Zhang, Shunchi and Lu, Jin and Jin, Chuanyang and Zhou, Yichao and Zhang, Zhining and Shu, Tianmin},
  booktitle = {Proceedings of the 43rd International Conference on Machine Learning},
  series    = {Proceedings of Machine Learning Research},
  volume    = {306},
  year      = {2026},
  publisher = {PMLR}
}
```
