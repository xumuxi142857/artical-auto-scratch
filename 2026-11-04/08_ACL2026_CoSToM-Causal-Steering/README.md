# 08 | ACL 2026（CCF-A）| CoSToM：以因果导向引导实现大语言模型的内在心智理论对齐

> **英文标题**：CoSToM: Causal-oriented Steering for Intrinsic Theory-of-Mind Alignment in Large Language Models
> **中文译名**：CoSToM：面向大语言模型内在心智理论对齐的因果导向引导

| 项目 | 内容 |
|---|---|
| 会议 | **ACL 2026**（The 64th Annual Meeting of the Association for Computational Linguistics，2026-07-02~07，San Diego, California, USA；主会 07-05~07） |
| 论文类别 | **主会 Long Papers**（Volume 1: Long Papers） |
| CCF 等级 | **CCF-A**（人工智能 / 自然语言处理） |
| 荣誉 | **ACL 2026 Best Theme Paper**（ACL Anthology 条目页标注；主题为“用机制可解释性分析并干预 ToM 行为”） |
| 出版信息 | *Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, pp. **9302–9317**；Anthology ID: **2026.acl-long.421**；DOI: **10.18653/v1/2026.acl-long.421** |
| 作者 | Mengfan Li, Xuanhua Shi, Yang Deng |
| 单位 | ¹华中科技大学（国家大数据技术与系统国家工程研究中心、服务计算技术与系统实验室、集群与网格计算实验室）；²Singapore Management University（新加坡管理大学）；{limf, xhshi}@hust.edu.cn, ydeng@smu.edu.sg |
| 官方页面 | https://aclanthology.org/2026.acl-long.421/ |
| 官方 PDF | https://aclanthology.org/2026.acl-long.421.pdf |
| arXiv | https://arxiv.org/abs/2604.10031 |
| 代码 | https://github.com/CGCL-codes/CoSToM |
| 主题标签 | 心智理论 ToM · 因果追踪 causal tracing · 激活引导 activation steering · 机制可解释性 · LoRA/PEFT · 谈判对话生成 |

## 一句话概括

先用**因果追踪**证明 LLM 的 ToM 语义集中编码在**浅层**（约第 0–3 层，且“意图”比“信念/欲望”更难解码），再把这个发现变成干预手段：冻结 ToM 探针解码器当作**可微验证器**，让梯度经“激活接口”只回流到这些关键层的 LoRA 上，从而把 ToM 从“答得出”变成“用得上”——谈判任务上 ToM 分数从 0.081 提到 0.499（约 6 倍），且远优于全层 LoRA 的 0.245。

## 与三个关键词的对应

- **LLM 心智推理 ✓（本文主战场）**：不是再刷一个 ToM 榜单，而是追问“模型内部到底有没有稳定的 ToM 表征、能不能被外部行为用上”。用因果追踪 + 逐层探针把“内部知识 vs 外部行为”的错位量化出来，正好回答“LLM 是真懂还是靠提示脚手架演”。
- **ToM ✓（BDI 三元分解）**：把 ToM 拆成**信念（Belief）/ 欲望（Desire）/ 意图（Intent）**三类心理状态，在 NEGOTIATIONTOM 与 PERSUASIVE 两个策略互动场景上分别做逐层解码与逐层抑制，得到“浅层承载、深层可被破坏”的层间画像；且三类状态的峰值层并不相同（如说服者的欲望在 L4 达 52.84，意图在 L6 达 43.44）。
- **GRPO ✗（本文不含 RL）**：全文没有强化学习、没有 GRPO/PPO，训练目标就是“冻结探针的交叉熵 + 只训浅层 LoRA”（QLoRA 量化、r=16、α=32、lr 1e-4、≤10 epoch，见附录 A）。若你的研究线是 GRPO 式 ToM 微调，本文的价值是提供一个**非 RL 的强对照基线**：它说明仅靠“定位关键层 + 局部激活引导”就能拿到 0.5–0.75 的 ToM 质量分；反过来也提示，RL 带来的增益需要先扣掉“局部干预”这份便宜。原文通篇未与任何 RL 方法对比（这是导读的观察，非作者主张），也正好是能接着做的空白。

## 核心贡献

1. **首个系统性的 ToM 层间因果画像**：对 Llama-3-8B-Instruct 与 Qwen2.5-7B-Instruct 做逐层因果追踪（noising + denoising 恢复），给出 BDI 三类状态在 0–27 层的可解码性曲线，结论是 ToM 信息集中在浅层、中深层几乎不可解码——"深层失效"而非"全层弥散"。
2. **CoSToM 框架（解释 → 干预两段式）**：第一阶段用冻结的线性探针当"ToM 验证器"（可微、不用人工标注）；第二阶段把探针梯度通过激活接口回传到被注入层的 LoRA 参数，实现"只改该改的层"的轻量对齐，且推理时不需要探针、不需要提示脚手架（plug-and-play）。
3. **表征韧性证据**：在"逐层抑制 → 逐层恢复"实验里，CoSToM 显著缓解了深层抑制造成的 ToM 崩塌——Agent 1 的欲望在第 24 层从 2.39% 恢复到 51.48%，说服者的欲望在第 2 层从 51.03% 恢复到 99.23%，说明被对齐的是"可复用的内部表征"而非表层措辞。
4. **下游对话的实质提升**：NEGOTIATIONTOM（N=100）上对 Zero-shot、MindDial（提示与微调两版）、Full-Layer LoRA、LatentQA 做对照；18 个「指标 × 骨干 × 评判者」格子里 16 格第一（ToM 维度 6/6 全胜），仅两处极小差距落后（见下）；Qwen2.5 骨干上 ToM 达 0.751（Llama-3.3-70B 评判）、0.565（人工评判）。
5. **诚实的边界**：Limitations 只写了 **两条**——①泛化性仅验证于谈判、说服两类策略互动，更广的社会场景待探索；②方法必须能访问并操纵内部激活与梯度流，故只适用于开源权重模型。另外，评测依赖 LLM-as-judge（Llama-3.3-70B 与 GPT-5.1，辅以人工，评分细则见附录 F）；Ethical Considerations 提示了“说服能力被增强”的双用途风险。

## 主要结果（原文口径）

- **浅层峰值（表 1，NEGOTIATIONTOM 逐层探针）**：Llama-3 的欲望在第 2 层最高（Agent 1 40.79、Agent 2 37.41），Qwen2.5 的信念在第 2 层 28.13；"意图"的可解码性明显最低（表 1 内约为 4–21%），远低于信念/欲望，说明"想要什么"比"知道什么"更难从激活里直接读出。
- **说服场景峰值（表 2）**：Llama-3 说服者的欲望在第 2 层 51.03、第 4 层 52.84；对比之下 Qwen2.5 的"欲望（说服者）"Base 行高达 98.45（原文未解释，见译注 8）。
- **RQ3 招牌数字（§4.3）**：Agent 1 欲望在第 24 层 2.39% → 51.48%；说服者欲望在第 2 层 51.03% → 99.23%。
- **主结果（表 4a，谈判 N=100，Llama-3-8B 骨干，Llama-3.3-70B 评判）**：Zero-shot ToM 0.081 / Coh. 0.315 / NSE 0.294；MindDial(prompt) 0.306/0.575/0.440；MindDial(FT) 0.405/0.578/0.452；Full-Layer LoRA 0.245/0.511/0.467；LatentQA 0.221/0.359/0.271；**CoSToM 0.499/0.629/0.598**。GPT-5.1 评判 0.467/0.524/0.571，人工评判 0.485/0.580/0.595。**注意两处例外**（都在 Llama 骨干 + GPT-5.1 评判）：Coh. 0.524 低于 MindDial(FT) 与 Full-Layer LoRA 的 0.542；NSE 0.571 低于 Full-Layer LoRA 的 0.576（差 0.005）。这与原文“全层优化在保持通用语言连贯性上略优”的说法一致，不必当成矛盾。
- **跨骨干（表 4b，Qwen2.5-7B）**：CoSToM **0.751/0.842/0.835**（Llama 评判）、0.511/0.528/0.651（GPT-5.1）、0.565/0.710/0.680（人工）；同块 Full-Layer LoRA 仅 0.153/0.469/0.413，差距比 Llama 骨干更大。
- **泛化到说服（表 5，附录 D，N=200，指标为 ToM/Coh./PSE）**：Llama 骨干 CoSToM 0.797/0.811/0.757（Llama 评判）、0.703/0.807/0.744（GPT-5.1）、0.715/0.805/0.740（人工）；Qwen 骨干 0.802/0.811/0.713、0.746/0.888/0.812、0.760/0.840/0.795——换任务、换骨干后依然领先，原文表注也自称“almost all metrics”；唯一例外仍是 Llama 骨干 + GPT-5.1 的 Coh.（0.807 对 Full-Layer LoRA 的 0.864），与表 4 的同一模式吻合。
- **数据规模（表 3）**：NEGOTIATIONTOM 训练 1,335 / 验证 334 / 测试 711；PERSUASIVETOM 训练 10,355 / 验证 2,219 / 测试 2,222（只用到其中分层抽取的 N=100 与 N=200 子集）。

## 阅读建议

- **先看图 1 与图 2**：图 1 用一个谈判实例把问题摆出来——（左）模型正确推断出用户对柴火的欲望，（中）但按一般任务指令作答时却提出"送水"，（右）只有在提示里点明心理状态才给出恰当回应；图 2 是 CoSToM 的两阶段总览（因果追踪定位关键层 → 关键层内做激活引导）。理解这两张图，后面所有实验都是在解释这个"能推断却不用"的缺口。
- **重点读 §3.1 式 (1) 与 §3.2 式 (2)**：式 (1) 是 noising/denoising 的恢复度定义（这也是"因果"二字的落点）；式 (2) 是"冻结探针 + 梯度桥 + 只更新浅层 LoRA"的目标函数，全文的技术核心就在这两行。
- **对照表 1/表 2 与图 4/图 5 看"抑制—恢复"**：表给的是逐层准确率，图给的是抑制曲线；注意图 4/图 5 的横轴只标了部分层（3/6/10/15/24 与 2/4/6/10/15/20/27），是绘图抽样，不要误读为"只在这些层做了实验"（见译注 7）。
- **表 4 要横着读**：同一行内三种评判者（Llama-3.3-70B / GPT-5.1 / Human）的分数并排，能直接看出 LLM-as-judge 的松紧；同一设置下 GPT-5.1 比 Llama-3.3-70B 低 0.03–0.31（Qwen 骨干的 ToM 甚至从 0.751 掉到 0.511），所以绝对分数别太当真，跨评判者的**排序**才是稳的。
- **附录值得回看**：附录 A 是完整超参（QLoRA NF4、r=16、α=32、lr 1e-4、≤10 epoch、early stop patience 3、seed 42），复现必需；附录 D 的表 5 是说服任务的完整结果；附录 F 是 LLM 评判的评分细则。
- **注意两处原文瑕疵**：§4.2 说"三项关键观察"却只列两点；4.1 节 LatentQA 的署名（Pan et al., 2024）与表 4 的（Jafari et al., 2025）不一致。译文未改数字，只在文末"译注"里记录。

## 文件说明

- `原文_ACL2026正式版.pdf`：ACL Anthology 正式版（16 页，pp. 9302–9317，含 ACL 排版与页眉）
- `原文_arXiv2604.10031.pdf`：arXiv 预印版（便于检索/复制；与正式版有出入时以正式版为准）
- `_原文提取.txt`：pypdf 抽取的全文纯文本（带 `===== PAGE n =====` 分页标记，供核对数字与原文措辞）
- `翻译_正文中文.md`：正文全文中文翻译（标题 → 摘要 → 引言 → 相关工作 → 方法 → 实验 → 结论 → 局限 → 伦理 → 致谢，含表 1–4 与图 1–6 要点；不含参考文献与附录 A–F）
- `翻译_正文中文.docx`：同一译文的 Word 版
- `README.md`：本导读

## BibTeX

```bibtex
@inproceedings{li-etal-2026-costom,
  title     = {CoSToM: Causal-oriented Steering for Intrinsic Theory-of-Mind Alignment in Large Language Models},
  author    = {Li, Mengfan and Shi, Xuanhua and Deng, Yang},
  booktitle = {Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)},
  pages     = {9302--9317},
  year      = {2026},
  address   = {San Diego, California, United States},
  publisher = {Association for Computational Linguistics},
  doi       = {10.18653/v1/2026.acl-long.421}
}
```
