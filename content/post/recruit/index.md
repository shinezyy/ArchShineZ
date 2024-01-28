---
title: 香山处理器的模拟器组招聘
subtitle: 

# Summary for listings and search engines
summary: 北京开源芯片研究院持续招聘ISA模拟器和微架构模拟器工程师，欢迎有兴趣的同学投递简历。

# Link this post with a project
projects: []

# Date published
date: "2024-01-28T00:01:00Z"

# Date updated
lastmod: "2024-01-28T00:01:00Z"

# Is this an unpublished draft?
draft: false

# Show this page in the Featured widget?
featured: true

# Featured image
# Place an image named `featured.jpg/png` in this page's folder and customize its options here.
image:
  caption: 'Image credit: [**GEM5**](https://gem5.org/)'
  focal_point: ""
  placement: 2
  preview_only: false

authors:
- admin

tags:
- Architecture
- GEM5
- RISC-V
- 开源芯片研究院

categories:
- 工作
---

# 我们组做什么

本组的工作服务于香山处理器的架构迭代和系统级测试。其中**CPU微架构模拟器**和**性能分析基础设施**服务于香山处理器的架构迭代，**CPU golden model**服务于系统级测试。

## CPU微架构模拟器

CPU微架构模拟器是处理器设计的前锋，它帮助处理器架构师快速验证设计想法，寻找有效功能点（feature）。
香山处理器的架构模拟器（XS-GEM5，具体见[XS-GEM5简介博客]({{< ref "/post/xs-gem5" >}} "XS-GEM5简介博客")和视频
[XS-GEM5](https://www.bilibili.com/video/BV1VF411k7uL/)），
在香山V3架构（昆明湖架构）的设计过程中起到了关键作用，
XS-GEM5微架构模拟器输出了Stream预取器调优、Stride预取器调优等重要功能点。
同时还服务于硅前编译器优化，用于编译器调优。

## 性能分析基础设施

在香山处理器团队，我们使用SimPoint和RVGCpt等工具来加速XS-GEM5和RTL的仿真
（视频介绍：[香山的Checkpoint和采样基础设施](https://www.bilibili.com/video/BV1eb4y167cE/)）。
我们使用Topdown分析方法来分析处理器性能瓶颈。
本组负责在XS-GEM5和ISA模拟器上实现上述功能。

## ISA模拟器：CPU golden model

CPU golden model是处理器的功能验证工具，香山处理器所使用的golden model是[NEMU](https://github.com/OpenXiangShan/NEMU/)。
它可以结合Difftest来验证RTL的正确性（
论文：[MINJIE](https://ieeexplore.ieee.org/document/9923860/)，
代码仓库：[Difftest RTL](https://github.com/OpenXiangShan/difftest)）。
此外，NEMU还服务于[性能分析基础设施](#性能分析基础设施)，用于部分profiling工作和检查点生成。

# 岗位介绍

## CPU微架构模拟器工程师

开源芯片研究院招聘 CPU架构设计工程师 （性能建模）
工作职责
1. 设计高性能通用RISC-V 处理器
2. 负责高性能处理器的架构设计和性能建模，对缓存预取、分支预测、取指、访存等部件进行优化
3. 负责与高性能处理器的RTL团队进行沟通，落地feature、对齐性能gap
4. 负责针对特定应用的高性能处理器的性能分析与调优

应届生（实习、校招）要求：
1. 深入学习过高级计算机体系结构课程，并进行相关的项目设计。理论方面，需要理解分支预测、乱序执行、高速缓存。应届生如无相关经验，以下学习路径可供参考：
    * 必选：完成一生一芯A线的CPU（流水线、带cache，或同等水平实验课）和 NEMU实验，面试30%问这个
    * 架构岗必选：把 [UWisc ECE752](https://ece752.ece.wisc.edu/) 的Lecture7-11学透，面试40%问这个
    * 可选：深入理解一种2010年以后提出的预取分支预测算法，并用GEM5/Champsim实现和进行性能分析
1. 熟练使用C++，debug能力强。
2. 掌握Python、Bash等脚本语言。
3. 能熟练使用搜索引擎、技术文档，从stackoverflow、mailing list、社区issue里面寻找解决问题的方法

实力出众但是不方便线下实习的外地学生可以远程实习

## RISC-V ISA模拟器工程师

开源芯片研究院招聘 ISA模拟器开发工程师
工作职责
1. 设计并维护ISA模拟器，实现不同RISC-V指令集扩展，对齐实现到指令集手册
2. 负责处理RTL团队反馈的ISA模拟器使用问题并解决
3. 根据调试需求设计更多ISA模拟器的调试工具
4. 根据团队需求修改ISA模拟器的功能，例如增加更多的数据接口，增加profiling功能等

应届生（实习、校招）要求：
1. 学习过操作系统原理、计算机体系结构课程，并进行过相关的项目设计和课程实验。
    * 必选：NJU-PA（NEMU）实验 PA1-4
    * 必选：实验课：MIT6.828/MIT6.S081；理论课：MIT6.828/MIT6.S081或NJU蒋炎岩的OS课
    * 可选：熟悉NEMU/QEMU等模拟器，并能够独立调试、阅读、分析代码、增加新功能
    * 可选：完成一生一芯第五期A线的学习或第六期B线的学习，完成5级流水线CPU设计（或同等水平实验课）
2. 熟练使用C，debug能力强。
3. 熟练使用Linux命令行工具，并掌握像Python、Bash、Makefile这样的脚本语言。
4. 熟练使用git、ssh、tmux等基本工具
5. 能熟练使用搜索引擎、技术文档，从stackoverflow、mailing list、社区issue里面寻找解决问题的方法

## 对能力要求的解释

在此，我们对上述两个岗位的能力要求进行解释，即学习这些东西对以后的工作有什么样的帮助。

上述两个岗位都需要较强的Coding能力和问题解决能力，所以基本的编程和工具就不再展开解释。

微架构模拟器岗：
- 写过简单的ISA模拟器（对应一生一芯中的NEMU PA）。经过本项目，同学对模拟器和CPU之间的关系有初步认知。
- 写过扎实的本科生级别的CPU的RTL（对应一生一芯中的CPU设计）。经过本项目，同学认识到电路大概是怎么回事，
不至于在微架构模拟器中写出过于离谱的结构，避免和RTL设计同学对接的障碍。
- 深入学习高级计算机体系结构课程（例如，UWisc ECE752）。经过对ECE752的学习，同学能知道现代处理器在做什么，
和自己的toy CPU有什么差别，能读懂GEM5中乱序执行、预取、分支预测等部件的代码。这也是以后工作的核心。

ISA模拟器岗：
- 写过简单的ISA模拟器（对应一生一芯中的NEMU PA）。经过本项目，同学对模拟器和CPU之间的关系有初步认知。
- 深入学习操作系统。因为ISA模拟器岗位中的性能分析基础设施和debug经常在和OS、特权指令打交道，
MIT6.828/MIT6.S081这样的课程可以帮忙补充这部分的能力。

上述要求很难吗？
在南京大学，ISA模拟器是本科二年级上半学期的课，而操作系统是二年级下半学期的课，
与ysyx A线对应的组成原理实验课则开在三年级上半学期，与ECE752对应的计算机体系结构课则开在三年级下半学期。
所以，就必选内容而言，ISA模拟器岗对应了**2门本科生课程**，而微架构模拟器岗对应了**4门本科生课程**。
同学们不要被JD里的要求唬住，从现在开始一步一步地学习，就能达到要求。

## 联系方式
邮箱：archshinez x outlook x com