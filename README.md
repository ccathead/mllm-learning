# MLLM 实践学习

通过 **跑通开源项目 → 跟踪源码 → 做一个受控改动 → 评测 → 记录结论** 学习多模态大模型。

目标：理解图像如何进入语言模型、训练 loss 如何计算，并完成一个可评测、可微调的图像理解应用。已有 Python / PyTorch / Transformer 基础；本地 Windows 管理代码与笔记，云端 Linux GPU 运行推理和训练。

## 当前入口

- [项目进度](index.md)：已完成内容、决策和下一步。
- [第1章 notebook](src/chapter1_llava_baseline.ipynb)：环境配置、单图与逐张推理、人工评分、张量观察和遮挡实验。
- [第1章报告](experiments/chapter1-baseline.md)：30 题基线、十个代表性错误案例及第2章任务。
- [第2章 notebook](src/chapter2_llava_dataflow.ipynb)：图像 token、视觉特征、真实图文融合、生成步骤与遮挡对照，含 MiniGPT-4 连接模块练习。
- [学习与版本管理工作流](docs/workflow.md)：本地 / 云端同步、文件归档和提交范围。

目前已完成 **30 张 COCO 图片的开放式中文视觉问答**，总分 38/60，平均 1.2667/2，归一化得分 63.33%；15 题满分，满分比例为 50%。这是人工评分的小样本基线，归一化得分不等于准确率。本轮是推理与评测，未训练模型。

下一步进入 **第2章：跟踪视觉特征如何进入 LLM**。打开第2章 notebook，继续使用成功运行的 `llava-week1` 环境和固定模型 revision。代码已完成本地结构、语法与小型 CPU 逻辑检查，完整模型实验仍需在云端执行。

## 六章学习路线

按章节目标与验收推进，完成一章后再进入下一章，学习时间根据实际情况安排。当前练习任务为 COCO 图片问答；原先暂定的商品属性提取可在后续领域应用阶段重新评估。

| 章节 | 开源项目与实践 | 验收产物 |
|---|---|---|
| 第1章（已完成） | LLaVA：单图 → 30 张图逐张推理与人工评分 | notebook、基线报告、10 个代表性错误案例 |
| 第2章 | LLaVA：跟踪预处理、视觉编码器、投影层、LLM；MiniGPT-4：对比连接方式 | 带实际张量形状的数据流图、关键函数与 commit |
| 第3章 | Qwen2.5-VL：复用开发对照集比较模型、提示词与裁剪；另留新图片评估 | 模型与策略对比报告、应用原型 |
| 第4章 | 拆解数据处理、聊天模板、labels 与冻结策略；20–50 条样本过拟合检查 | 样本检查、梯度检查、训练流程记录 |
| 第5章 | 整理约 500–2,000 条领域指令数据并做 LoRA；按实体/图片来源划分数据 | 未见数据上的微调对比、通用能力检查 |
| 第6章 | 封装交互界面或 API，加入 JSON 校验、失败重试和批量处理 | 可演示应用、复现说明 |

视频与 Agent 放在六章主线完成之后。数据数量是教学起点，实际效果待实验验证。

## 如何记录学习成果

1. 从 [源码拆解模板](templates/source-analysis.md) 建立 `notes/` 笔记；阅读论文时使用 [论文模板](templates/paper-note.md)。
2. 每次实验使用 [实验模板](templates/experiment.md)，将报告与小型汇总保存到 `experiments/`。
3. 将关键结论、卡点和下一步同步到 [项目进度](index.md)。
4. 数据、原始预测和权重另行备份；Git 只管理代码、文档、配置和精简复现材料。

## 仓库布局

- `docs/`：学习与版本管理工作流。
- `notes/`：源码拆解与概念笔记。
- `src/`：自己编写的推理、评测、应用代码。
- `configs/`：推理与训练配置。
- `experiments/`：实验报告和小型汇总指标。
- `examples/`：有权分享的少量示例素材。
- `templates/`：源码、论文和实验记录模板。
- `data/`、`checkpoints/`、`outputs/`、`external/`：本地或云端使用，忽略提交。

## 已验证环境与资料

第1章使用 RTX 4090 D、Python 3.10.22、PyTorch 2.6.0+cu124、Transformers 4.57.1。安装入口为 [src/requirements.txt](src/requirements.txt)，成功运行后的完整依赖快照为 [experiments/chapter1/requirements-freeze.txt](experiments/chapter1/requirements-freeze.txt)。该记录只代表本次环境；其他项目使用独立环境。已有环境与内核名 `llava-week1` 保留为运行标识，无需为章节改名重建环境。

| 用途 | 官方资料 | 本项目版本状态 |
|---|---|---|
| LLaVA HF 推理与源码 | [4.57.1 文档](https://huggingface.co/docs/transformers/v4.57.1/en/model_doc/llava)、[对应源码](https://github.com/huggingface/transformers/blob/v4.57.1/src/transformers/models/llava/modeling_llava.py) | 第1章实际使用 Transformers 4.57.1 |
| LLaVA 1.5 HF 权重 | [模型卡](https://huggingface.co/llava-hf/llava-1.5-7b-hf) | 第1章 revision：`b234b804b114d9e37bb655e11cbbb5f5e971b7a9` |
| 原生 LLaVA 架构与训练 | [官方仓库](https://github.com/haotian-liu/LLaVA) | 第2章对照阅读；实际使用 commit 待记录 |
| MiniGPT-4 连接模块 | [官方仓库](https://github.com/Vision-CAIR/MiniGPT-4) | 尚未运行；需区分 MiniGPT-4 与 MiniGPT-v2 |
| Qwen2.5-VL 应用与微调 | [3B 模型卡](https://huggingface.co/Qwen/Qwen2.5-VL-3B-Instruct) | 第3章起使用；revision、环境和训练框架待验证 |

HF 实现与原生 LLaVA 分别记录，模型 revision 与源码 commit 分开保存。学习特定版本模型时，从对应模型卡及匹配的源码版本出发，不把仓库最新分支直接视为旧模型实现。

路线背景：[MLLM 学习博文](https://gongshangzheng.github.io/mllm-comprehensive-survey.html)。所有实验结论以本项目代码、配置、数据校验或日志为依据；未验证信息标注“待核验”。
