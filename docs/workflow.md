# 学习与版本管理工作流

## 每次学习的循环

1. 定一个问题，例如“视觉特征如何进入 LLM”。
2. 先跑官方最小示例，再跟踪实际调用链。
3. 打印张量/labels/梯度，以运行证据验证理解。
4. 每次只改一个因素，用固定数据比较前后结果。
5. 写实验报告，将关键结论和下一步更新到 `index.md`。

## 本地与云端

本地编辑 → commit / push → 云端 pull → 运行实验 → 保存报告与小型汇总 → commit / push → 本地 pull。

```bash
# 每次开始先同步；存在未提交修改时先处理，避免覆盖工作。
git pull --ff-only

# 明确选择要提交的学习成果。
git add README.md index.md docs notes src configs experiments templates
git diff --cached
git commit -m "Record experiment and learning notes"
git push
```

实例销毁前，将权重、完整日志与数据备份到持久化存储；实验报告记录存储位置和校验信息。不要将云端输出是否保存交给 Git 忽略规则决定。

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
