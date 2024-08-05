---
title: 非 AI 背景的人如何入门大模型
subtitle: 坐观垂钓者，徒有羡鱼情

# Summary for listings and search engines
summary: 昨天

# Link this post with a project
projects: []

# Date published
date: "2024-07-30T00:00:00Z"

# Date updated
lastmod: "2024-07-30T00:00:00Z"

# Is this an unpublished draft?
draft: true

# Show this page in the Featured widget?
featured: true

# Featured image
# Place an image named `featured.jpg/png` in this page's folder and customize its options here.
image:
  caption: 'Image credit: [**OpenXiangShan**](https://github.com/OpenXiangShan/)'
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

# 非 AI 背景的人如何入门大模型

现在我工作的地方，同事、同学主要是计算机系统结构和微电子背景。很多人其实也对 AI 有兴趣，
但多是坐观垂钓者，徒有羡鱼情。
为此，我写了这篇文章来介绍要理解现在大语言模型（LLM）用到的算法，以及算法的负载特征所需要的最小知识子集。
本文假设读者是计算机或者相关背景，学习过线性代数和概率论。

其实也是系统结构背景，
但是从本科到研究生，我身边的机器学习氛围一直很浓，使得我这几年多少了解一些 AI 进展。
因此我斗胆来写这样一篇文章。

本文只会介绍理解 Attention 所依赖的前置知识，和基于 Attention 所构建的 LLM 宇宙。
出于“最小知识子集”的目的，本文省略了很多机器学习的重要进展，
例如卷积神经网络（CNN）和强化学习（RL）都在上一个年代留下了浓墨重彩的一笔，但是本文不会介绍。
不过，我仍然鼓励读者了解相关知识和历史：机器如何在视觉任务、围棋上战胜人类。

本文所推荐的阅读材料主要是论文，对于最基础的内容会推荐教科书的章节。
因为这个领域实在发展太快，哪怕是最新出版的教科书也没能包含这个领域最重要的进展。

## 机器学习基础

首先是机器学习的基础知识，需要学习《西瓜书》第二章模型评估、第四章决策树和第五章神经网络。
因为我以前上周志华的课，所以用《西瓜书》举例。
可以根据个人偏好替换为李航的《统计机器学习》或者 Jordan 的《Pattern Recognition and Machine Learning》中的对应部分。
学习模型评估，是为了让初学者理解训练和预测、过拟合、泛化等基本概念。
学习决策树，是为了方便理解 gradient boosting tree。
学习神经网络，应该就不用讲原因了吧？

如果要加深这部分的认知，建议推一推链式求导（我曾经会，现在也忘了，哈哈）。
用 C++ 实现一下简单的神经网络和 gradient boosting tree（我曾经写过，现在也忘了，哈哈）。

然后，我建议学习 gradient boosting tree 和何恺明的 residual connection。
很多年前，周志华老师和包云岗老师有过一次关于算法和算力的讨论，
周志华老师谈论算法的进化时，说到人类近几年才掌握训练深层网络的技巧，这里的“技巧”指的应该就是 residual connection 和 ReLU 等技术。
就我自己写 gradient boosting 的代码的感受来看，gradient boosting 和 residual connection 两者的思想是非常相似的。
因此我建议把二者放在一起学习。


## Attention is All You Need

Attention is All You Need 或许是这个领域最重要的论文，不过它用到的思想并非凭空诞生。
为了训练深度网络，它用到了 Residual Connection，这不必多说。
因为是序列预测，它的序列预测结构和 Recurrent Neural Network（RNN）也非常相似。

此外，私以为它最核心的两个思想是 feature interaction 和 explicit memory。
Explicit memory 是指神经网络架构显式地存储一些数据到一个 “soft addressable” 的存储器中，
比较典型的工作是 Neural Turing Machine。
Neural Turing Machine 让神经网络拥有读写存储器的能力，可以用来学习一些计算机算法。
而 Attention 结构里的 `V` 也可以理解为一种只读的存储器，
对它的 “寻址” 是通过 `Q` 和 `K` 的相乘之后的 Softmax 来实现。

Feature interaction 是指神经网络架构显式地让输入特征之间相互作用，
从而让后层的神经元能接受到输入 feature 之间相互作用的信息。
做过分支预测器算法的同学应该很了解单层神经网络无法解决异或问题，
有的工作就通过显式的将分支历史之间进行异或来得到新的 feature，
从而使单层神经网络分支预测器拥有解决异或问题的能力。
Feautre interaction 就是这个思想的泛化版本，
它的典型架构是 Deep & Cross Network，被用于推荐系统。
Attention 结构里的 `Q` 和 `K` 的相乘就是一种 feature interaction。


## 推理加速

## 遗漏的部分

关于 Transfromer，本文遗漏了一些前置知识，后续补上：
- Word2Vec
- Softmax

从 2010 至今机器学习算法的重要进展，本文没有覆盖：
- 卷积神经网络
- 强化学习
- 生成对抗网络