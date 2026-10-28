# 学习与版本管理工作流

## 每次学习的循环

1. 定一个问题，例如“视觉特征如何进入 LLM”。
2. 先跑官方最小示例，再跟踪实际调用链。
3. 打印张量/labels/梯度，以运行证据验证理解。
4. 每次只改一个因素，用固定数据比较前后结果。
5. 写实验报告，将关键结论和下一步更新到 `index.md`。

## 本地与云端

本地编辑 → commit / push → 云端 pull → 运行实验 → 保存报告与小型汇总 → commit / push → 本地 pull。

仓库根目录运行下面的命令。云端 notebook 修改后先保存；有未提交修改时，先检查差异并提交或妥善保存，再执行 pull。

```bash
# 每次开始先同步；存在未提交修改时先处理，避免覆盖工作。
git pull --ff-only

# 明确选择要提交的文件；以下为 W1 报告的例子。
git status --short
git add README.md index.md docs/workflow.md experiments/week1-baseline.md experiments/week1
git diff --cached --stat
git diff --cached
git commit -m "Record experiment and learning notes"
git push
```

实例销毁前，将权重、完整日志与数据备份到持久化存储；实验报告记录存储位置和校验信息。不要将云端输出是否保存交给 Git 忽略规则决定。

## 文件整理与 Git 范围

| 内容 | 保存位置 | 提交到 Git |
|---|---|---|
| 推理、选图、评测代码与正式 notebook | `src/` | 是；notebook 提交前按下述流程清空输出 |
| 可复用参数与安装入口 | `configs/`、`src/requirements.txt` | 是 |
| 学习笔记、实验报告、模板 | `notes/`、`experiments/*.md`、`templates/` | 是 |
| 小型指标、依赖快照、文件校验清单 | 如 `experiments/week1/` | 是 |
| 原始图片、题目与标注 | `data/` | 否；保留独立备份 |
| 原始预测、评分表、运行日志和实验图片 | `outputs/` | 否；保留独立备份 |
| 模型权重与外部源码 | `checkpoints/`、`external/` | 否 |
| Jupyter 检查点、临时诊断、环境与缓存 | `.ipynb_checkpoints/`、`cloud_debug_*/`、`.venv/`、`.cache/` 等 | 否 |

在清空 notebook 输出前，先确认原始结果已保存到 `outputs/` 并完成备份；需要保留含输出 notebook 时，也另存到 `outputs/`。随后在 JupyterLab 的 Edit 菜单选择清空所有输出，保存正式 notebook，再提交。已经写入报告的原始 notebook 哈希用于标识当时的文件，清空后变化是正常的，不应改写历史校验清单。

`.gitignore` 只影响未跟踪文件。已被 Git 跟踪的自动检查点或临时文件，需要先用 `git rm --cached -- 具体文件路径` 停止跟踪；该命令保留本地文件。清理记录随下一次正常提交生效。不要对整个仓库批量取消跟踪。

报告可以链接忽略目录中的本地证据，但 GitHub 上无法直接查看这些文件；报告自身应包含足够的设置、指标、案例摘要及校验值。需要公开示例时，在确认可分享后另放到 `examples/`。

## 外部项目

- 官方项目克隆到 `external/`（忽略提交）或仓库外；每次记录 URL 和实际 commit。
- 修改模型源码时再 fork，在 fork 保存改动；学习仓库记录 fork URL、commit 和结论。
- 不把官方代码直接复制进主仓库；需要引用片段时注明来源与许可。
- 模型权重 revision 与项目代码 commit 分开记录，不能用模型名称代替版本。
- 各项目使用独立环境，运行成功后保存依赖版本到相应实验目录。

## 训练学习的五项检查

- 打印 `input_ids`、`labels`，核对图片位置、用户输入、padding 是否按框架预期计算 loss。
- 列出可训练参数并检查梯度，验证冻结策略。
- 先用 20–50 条样本做过拟合检查，失败时排查数据、模板、标签和优化设置。
- 按商品/图片来源划分数据，避免相似图片跨集合；测试集不用于提示词或超参数选择。
- 对比基础模型、优化提示词、LoRA，区分格式改善与内容准确率改善，保留通用问答检查能力退化。
