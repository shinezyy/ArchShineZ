---
title: The myth of decoding large models
subtitle: 

# Summary for listings and search engines
summary: 在探讨大语言模型（LLM）的性能时，一个流传已久的说法是：“解码过程中的 Attention 操作是访存密集型（Memory Bound）的。” 这个观点深入人心，以至于许多优化讨论都以此为前提。然而，随着模型架构的演进和解码策略的创新，这一迷思正在被打破。

# Link this post with a project
projects: []

# Date published
date: "2025-09-21T00:00:00Z"

# Date updated
lastmod: "2025-09-21T00:00:00Z"

# Is this an unpublished draft?
draft: false

# Show this page in the Featured widget?
featured: true

# Featured image
# Place an image named `featured.jpg/png` in this page's folder and customize its options here.
image:
  caption: 'Image credit: [**Attention Variations — MQA vs GQA vs MHA vs MLA**](https://verticalserve.medium.com/group-query-attention-58283b337c65)'
  focal_point: ""
  placement: 2
  preview_only: false

authors:
- admin

tags:
- LLM

categories:
- 工作
---
<!-- 
# The myth of decoding large models

old myth: decoding large models is memory bound.

current reality: decoding large models is often not memory bound.

## attention 的计算密度取决于什么？

取决于 `q_seq_len` 和 `group_size`，`group_size` 就是 `GQA` 的 `group_size`。
MLA 在 decode 阶段如果采用[矩阵吸收](https://zhuanlan.zhihu.com/p/700214123)，则 attention 的核心计算类似于 [MQA](https://arxiv.org/abs/1911.02150)，
每个 head 对应同一个 compresed kv cache，其 `group_size` 就是 `head_num`。

## decoding MLA

MLA 按照如下配置的计算密度：
```
mla("MLA qlen=1", seq_len=1, head_num=128, head_dim=576, nope_dim=512, chunk_size=512, elem_size=2, o_size=2)
mla("MLA qlen=2", seq_len=2, head_num=128, head_dim=576, nope_dim=512, chunk_size=512, elem_size=2, o_size=2)
```

输出结果：
```
MLA qlen=1 compute_density: 164.22641509433961
MLA qlen=2 compute_density: 280.7741935483871
```
MLA(Deepseek V3) 一般采用集群方式，用 H100 进行推理。

H100 计算密度
```
H100, compute density: 295.2238805970149
```

因此，如果 qlen=2，对应 deepseek V3 开启 MTP=1，则 MLA 的理论 roofline 是计算访存平衡。

## decoding GQA

GQA 按照 QWEN3-32B 配置的计算密度：
```
GQA qlen=1 compute_density: 7.699, group size * q_seq_len: 8
GQA qlen=4 compute_density: 30.118, group size * q_seq_len: 32
GQA qlen=8 compute_density: 58.514, group size * q_seq_len: 64
GQA qlen=16 compute_density: 110.703, group size * q_seq_len: 128
GQA qlen=32 compute_density: 199.805, group size * q_seq_len: 256
GQA qlen=48 compute_density: 273.067, group size * q_seq_len: 384
GQA qlen=64 compute_density: 334.367, group size * q_seq_len: 512
```

各类硬件的计算密度：
```
H20, compute density: 37.000
RTX 5090, compute density: 116.760
AI MAX 395, compute density: 200.000 (INT8)
H100, compute density: 295.224
```

在 `qlen=4-8` 时，H20 上达到计算访存平衡；在 `qlen=48` 左右时，在 H100 上达到计算访存平衡。

| GQA Configuration | H20 | RTX 5090 | AI MAX 395 | H100 |
|---|---|---|---|---|
| GQA qlen=1 | Memory Bound | Memory Bound | Memory Bound | Memory Bound |
| GQA qlen=4 | Memory Bound | Memory Bound | Memory Bound | Memory Bound |
| GQA qlen=8 | Compute Bound | Memory Bound | Memory Bound | Memory Bound |
| GQA qlen=16 | Compute Bound | Memory Bound | Memory Bound | Memory Bound |
| GQA qlen=32 | Compute Bound | Compute Bound | Memory Bound | Memory Bound |
| GQA qlen=48 | Compute Bound | Compute Bound | Compute Bound | Memory Bound |
| GQA qlen=64 | Compute Bound | Compute Bound | Compute Bound | Compute Bound |


考虑到推理成本，QWEN3-32B 大概率不会在 H100、H20 这类数据中心计算卡上推理。
使用 AI MAX 395 在端侧部署，或者使用 RTX 5090 在云上部署（我不太确定？），是更合理的方案。
如果使用 AI MAX 395 进行端侧部署，一般会考虑使用 SOTA 的 [EAGLE3 推测解码]()，其典型 `qlen` 是32-64，此时 GQA 的计算访存比较为平衡。
如果使用 RTX 5090 在云上部署，则典型的 qlen=1-4，此时 GQA 的计算访存比很低，是典型的 memory bound。

## 总结 -->

# 破除解码大模型的迷思：Attention 操作并非总是访存密集型

在探讨大语言模型（LLM）的性能时，一个流传已久的说法是：“解码（Decoding）过程中的 Attention 操作是访存密集型（Memory Bound）的。” 这个观点深入人心，以至于许多优化讨论都以此为前提。然而，随着模型架构的演进和解码策略的创新，这一迷思正在被打破。

**迷思:** 解码大模型是一个访存密集型任务，其瓶颈在于内存带宽。

**现实:** 在许多先进的模型和解码策略下，Attention 操作的瓶颈正在从访存转向计算，或者达到计算与访存的平衡。

## Attention 的计算密度取决于什么？

要理解 Attention 操作的瓶颈所在，我们首先需要理解**计算密度 (Compute Density)**，即计算量（FLOPs）与访存量（Bytes）的比值。一个操作的计算密度如果高于硬件的计算密度（即硬件算力与带宽的比值），那么它就是计算密集型（Compute Bound）；反之，则是访存密集型（Memory Bound）。

对于 Attention 操作而言，其计算密度主要取决于两个核心参数：

1.  **`q_seq_len`**: Query 序列的长度。在自回归解码中，这通常代表一次前向传播中模型需要处理的 Query token 数量。传统的逐 token 解码 `q_seq_len=1`，而推测解码（Speculative Decoding）等技术会使其大于 1。
2.  **`group_size`**: 在 [Grouped-Query Attention (GQA)](https://arxiv.org/pdf/2305.13245) 中，这代表共享同一份 Key 和 Value 的 Query Head 的数量。

一个例子是 Deepseek V2/V3 中使用的 [**Multi-Head Latent Attention(MLA)**](https://arxiv.org/abs/2405.04434)。在解码阶段，如果采用[矩阵吸收](https://zhuanlan.zhihu.com/p/700214123)等先进技术，MLA 的核心计算在形式上等于只有个一个组的 GQA，即[Multi-Query Attention (MQA)](https://arxiv.org/abs/1911.02150)。在这种模式下，所有 Query Head 共享同一份压缩后的 KV Cache，其 `group_size` 实际上就等于总的 `head_num`。

下面，我们将通过具体的数据来分析 MLA 和 GQA 在不同场景下的计算密度表现。

## 解码 MLA：当 `qlen=2` 时已达平衡

我们首先考察 MLA 架构在解码阶段的计算密度。以下是基于 Deepseek V3 模型相关参数的模拟计算结果：

```
mla("MLA qlen=1", seq_len=1, head_num=128, head_dim=576, nope_dim=512, chunk_size=512, elem_size=2, o_size=2)
mla("MLA qlen=2", seq_len=2, head_num=128, head_dim=576, nope_dim=512, chunk_size=512, elem_size=2, o_size=2)
```

输出结果显示：

```
MLA qlen=1 compute_density: 164.23
MLA qlen=2 compute_density: 280.77
```

Deepseek V3 这类先进的 MLA 模型通常部署在如 NVIDIA H100 这样的高性能计算集群上。我们来看一下 H100 的理论计算密度（FP16/BF16 Tensor Core 算力 / HBM3 显存带宽）：

```
H100, compute density: 295.22
```

**数据解读：**

-   当 `qlen=1` 时（对应传统的逐 token 解码），MLA 的计算密度为 164.23，远低于 H100 的 295.22。在这种情况下，Attention 操作确实是 **访存密集型** 的，性能瓶颈在于显存带宽。
-   然而，当 `qlen` 仅仅增加到 2 时，计算密度飙升至 280.77，已经非常接近 H100 的硬件计算密度。

这意味着，对于 Deepseek V3 这类模型，如果采用能够一次性处理两个 Query token 的解码策略（例如并行解码或小规模的推测解码），其 Attention 操作在 H100 上就已经达到了 **计算与访存的平衡点 (Roofline Balance Point)**。如果 `qlen` 更大，它将彻底转变为一个计算密集型任务。

## 解码 GQA：解码策略与硬件共同决定瓶颈

接下来，我们分析应用更广泛的 GQA 架构。以 Qwen3-32B（其 Group Size = 8）的相关配置为例，我们观察不同 `qlen` 下的计算密度变化：

```
GQA qlen=1 compute_density: 7.70, group size * q_seq_len: 8
GQA qlen=4 compute_density: 30.12, group size * q_seq_len: 32
GQA qlen=8 compute_density: 58.51, group size * q_seq_len: 64
GQA qlen=16 compute_density: 110.70, group size * q_seq_len: 128
GQA qlen=32 compute_density: 199.81, group size * q_seq_len: 256
GQA qlen=48 compute_density: 273.07, group size * q_seq_len: 384
GQA qlen=64 compute_density: 334.37, group size * q_seq_len: 512
```

为了进行对比，我们列出几款典型硬件的计算密度：

```
H20, compute density: 37.00
RTX 5090, compute density: 116.76
AI MAX 395, compute density: 200.00 (INT8)
H100, compute density: 295.22
```

将 GQA 的计算密度与不同硬件的特性相结合，我们可以得到一张清晰的瓶颈分析表：

| GQA 配置 (qlen) | H20 (数据中心) | RTX 5090 (云/个人) | AI MAX 395 (个人) | H100 (数据中心) |
| :--- | :---: | :---: | :---: | :---: |
| GQA qlen=1 | Memory Bound | Memory Bound | Memory Bound | Memory Bound |
| GQA qlen=4 | Memory Bound | Memory Bound | Memory Bound | Memory Bound |
| GQA qlen=8 | **Compute Bound** | Memory Bound | Memory Bound | Memory Bound |
| GQA qlen=16 | **Compute Bound** | Memory Bound | Memory Bound | Memory Bound |
| GQA qlen=32 | **Compute Bound** | **Compute Bound** | Memory Bound | Memory Bound |
| GQA qlen=48 | **Compute Bound** | **Compute Bound** | **Compute Bound** | Memory Bound |
| GQA qlen=64 | **Compute Bound** | **Compute Bound** | **Compute Bound** | **Compute Bound** |

**数据解读与场景分析：**

1.  **高端数据中心卡 (H100/H20)**: 服务提供商一般会采用传统解码（`qlen=1`），或者小规模的推测解码（`qlen=2-4`），GQA 操作的计算密度极低（7.70 - 30.12）。
`qlen=4` 时勉强接近 H20 的计算访存比（37.00），难以企及 H100 的计算访存比（295.22）。
不过，考虑到高昂的部署成本和较低的 token 价格，像 Qwen3-32B 这类模型通常不会在高端数据中心卡上部署。

1.  **个人部署 (AI MAX 395)**: 在个人部署（如 PC、工作站）部署大模型时，为了获得可接受的交互速度，采用先进的解码策略至关重要。例如，SOTA 的 [EAGLE](https://github.com/SafeAILab/EAGLE) 等推测解码框架，其典型的 `qlen`（即一次猜测的 token 数量）可以达到 32-64。在这种场景下，GQA 的计算密度（199.81 - 334.37）与 AI MAX 395 的硬件计算密度（200.00）非常匹配，使得 Attention 操作处于 **计算访存平衡或计算密集状态**。

2.  **云端 (RTX 5090)**: 服务提供商一般会采用传统解码（`qlen=1`），或者小规模的推测解码（`qlen=2-4`），那么 GQA 操作的计算密度极低（7.70 - 30.12），远低于 RTX 5090 的理论计算密度（116.76）。此时，Attention 操作是典型的 **访存密集型**，符合传统认知。

## 总结

“Attention is memory bound” 这一论断，是在特定历史时期和技术背景下（主要是早期模型结构和 `qlen=1` 的自回归解码）形成的经验总结。然而，技术的发展已经让这个论断变得片面和过时。

本文的数据表明：

1.  **Attention 的瓶颈是动态的**：它并非固有属性，而是模型架构（MLA/GQA）、解码策略（`q_seq_len` 的大小）和硬件特性三者相互作用的结果。
2.  **先进解码策略是关键变量**：随着推测解码等技术的普及，`q_seq_len` 不再局限于 1。哪怕 `qlen` 仅增加到 2 或 4，也足以在许多现代硬件上显著改变 Attention 的瓶颈归属。

因此，在进行大模型性能分析和优化时，我们必须深入到具体的算法、模型配置和硬件参数中，通过计算密度的量化分析，才能做出准确的判断。