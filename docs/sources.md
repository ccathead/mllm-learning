# 官方资料与版本记录

核验日期：2026-10-14。链接核验不代表环境、训练命令或显存需求已验证。

| 用途 | 来源 | 版本状态 |
|---|---|---|
| LLaVA 原生源码与训练 | https://github.com/haotian-liu/LLaVA | 实际使用 commit 待核验 |
| LLaVA HF 推理 | https://huggingface.co/docs/transformers/model_doc/llava | 使用版本与官方示例需匹配 |
| LLaVA 1.5 HF 权重 | https://huggingface.co/llava-hf/llava-1.5-7b-hf | 模型 revision 待核验 |
| MiniGPT-4 源码 | https://github.com/Vision-CAIR/MiniGPT-4 | 实际使用 commit 待核验；区分 MiniGPT-4 与 MiniGPT-v2 |
| Qwen2.5-VL 3B 权重与用法 | https://huggingface.co/Qwen/Qwen2.5-VL-3B-Instruct | 模型 revision、依赖和训练入口待核验 |

注意：访问 `https://github.com/QwenLM/Qwen2.5-VL` 时当前重定向到 Qwen3-VL。学习 Qwen2.5-VL 时从对应模型卡出发，明确源码 tag/commit 和训练框架版本，不直接将最新分支当作旧模型实现。

路线背景：[MLLM 学习博文](https://gongshangzheng.github.io/mllm-comprehensive-survey.html)；本计划依据参考对话整理，未独立核验该博文的全部表述。模型效果、资源需求与迁移收益以自己的实验为准。
