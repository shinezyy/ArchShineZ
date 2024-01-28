---
title: "Omegaflow: a high-performance dependency-based architecture"

# Authors
# If you created a profile for a user (e.g. the default `admin` user), write the username (folder name) here 
# and it will be replaced with their full name and linked to their profile.
authors:
- admin
- Zihao Yu
- Chuanqi Zhang
- Yinan Xu
- Huizhe Wang
- Sa Wang
- Ninghui Sun
- Yungang Bao

# Author notes (optional)
# author_notes:
# - "Equal contribution"
# - "Equal contribution"

date: "2021-06-21T00:00:00Z"
doi: ""

# Schedule page publish date (NOT publication's date).
publishDate: "2021-06-14T00:00:00Z"

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ["1"]

# Publication name and optional abbreviated publication name.
publication: In *Conference on Supercomputing*
publication_short: In *ICS 2021*

abstract: This paper investigates how to better track and deliver dependency in dependency-based cores to exploit instruction-level parallelism (ILP) as much as possible. To this end, we first propose an analytical performance model for the state-of-art dependency-based core, Forwardflow, and figure out two vital factors affecting its upper bound of performance. Then we propose Omegaflow,a dependency-based architecture adopting three new techniques, which respond to the discovered factors. Experimental results show that Omegaflow improves IPC by 24.6% compared to the state-of-the-art design, approaching the performance of the OoO architecture with an ideal scheduler (94.4%) without increasing the clock cycle and consumes only 8.82% more energy than Forwardflow.

# Summary. An optional shortened abstract.
# summary: Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis posuere tellus ac convallis placerat. Proin tincidunt magna sed ex sollicitudin condimentum.

tags: []

# Display this page in the Featured widget?
featured: false

# Custom links (uncomment lines below)
# links:
# - name: Custom Link
#   url: http://example.org

url_pdf: ''
url_code: ''
url_dataset: ''
url_poster: ''
url_project: ''
url_slides: ''
url_source: ''
url_video: ''

# Featured image
# To use, add an image named `featured.jpg/png` to your page's folder. 
# image:
#   caption: 'Image credit: [**Unsplash**](https://unsplash.com/photos/pLCdAaMFLTE)'
#   focal_point: ""
#   preview_only: false

# Associated Projects (optional).
#   Associate this publication with one or more of your projects.
#   Simply enter your project's folder or file name without extension.
#   E.g. `internal-project` references `content/project/internal-project/index.md`.
#   Otherwise, set `projects: []`.
# projects:
# - example

# Slides (optional).
#   Associate this publication with Markdown slides.
#   Simply enter your slide deck's filename without extension.
#   E.g. `slides: "example"` references `content/slides/example/index.md`.
#   Otherwise, set `slides: ""`.
slides: ""
---


Omegaflow是我博士期间的一个研究工作，它是一种基于前向数据流的思想的指令调度和执行架构。
前向数据流架构与传统Tomasulo算法不同，由producer指令记录consumer的位置，并在计算完成后主动向consumer指令传递数据。
基于此，每次指令计算完成之后，只需要传递有限次包含唤醒信息的Token就可以唤醒所有依赖于该指令的consumer指令。
而在传统Tomasulo算法中，无论是隐式重命名需要向整个issue queue广播寄存器tag和value，
而显示重命名则需要向整个issue queue广播寄存器tag。
由于指令的依赖存在局部性，前向数据流架构可以将调度和执行引擎划分为多个组，组间的通信显著少于组内的通信，
从而实现可扩展的指令窗口。
Omegaflow为前向数据流架构提出了一种性能上限分析工具，并改进了Token的处理和传输速度。
（虽然但是，如论文中报告的一样，前向数据流架构仍然无法outperform 传统Tomasulo算法。）
Omegaflow的代码在：[Omegaflow project](https://github.com/shinezyy/ff-reshape)。