---
# Display name
title: Zhou, Yaoyang

# Is this the primary user of the site?
superuser: true

# Role/position/tagline
role: Architect of LLM DSA; Maintainer of u-arch simulator for Xiangshan; PhD of Computer Architecture

# Organizations/Affiliations to show in About widget
organizations:
- name: Beijing Institute of Open Source Chip
  url: https://www.bosc.ac.cn/

# Short bio (displayed in user profile at end of posts)
bio: I specialize in LLM DSA and CPU micro-architecture.

# Interests to show in About widget
interests:
- LLM inference
- CPU micro-architecture
- Investment
- Badminton

# Education to show in About widget
Education:
  courses:
  - course: PhD in Computer Architecture
    institution: Institute of Computing Technology, CAS
    year: 2017 - 2023
  - course: BSc in Computer Science
    institution: Nanjing University
    year: 2013 - 2017

# Social/Academic Networking
# For available icons, see: https://wowchemy.com/docs/getting-started/page-builder/#icons
#   For an email link, use "fas" icon pack, "envelope" icon, and a link in the
#   form "mailto:your-email@example.com" or "/#contact" for contact widget.
social:
- icon: github
  icon_pack: fab
  link: https://github.com/shinezyy/
- icon: envelope
  icon_pack: fas
  link: "/#contact"
# - icon: twitter
#   icon_pack: fab
#   link: https://twitter.com/GeorgeCushen
# - icon: graduation-cap  # Alternatively, use `google-scholar` icon from `ai` icon pack
#   icon_pack: fas
#   link: https://scholar.google.co.uk/citations?user=sIwtMXoAAAAJ
# - icon: linkedin
#   icon_pack: fab
#   link: https://www.linkedin.com/

# Link to a PDF of your resume/CV.
# To use: copy your resume to `static/uploads/resume.pdf`, enable `ai` icons in `params.toml`, 
# and uncomment the lines below.
# - icon: cv
#   icon_pack: ai
#   link: uploads/resume.pdf

# Enter email to display Gravatar (if Gravatar enabled in Config)
email: ""

# Highlight the author in author lists? (true/false)
highlight_name: true
---

I am interested in LLM inference and CPU micro-architecture.

For LLM inference, I am interested in
- CPU-style LLM inference architecture, such as [XSAI (Xianshan + AI)](https://github.com/OpenXiangShan/XSAI)
- Modeling LLM kernels, chips, and clusters, such as [Softmax first-order model](https://github.com/shinezyy/softmax_sim) and [Deepseek V3 model](https://shinezyy.github.io/ArchShineZ/post/modeling-deepseek/)
- Speculative decoding

During Oct. 2024 - Oct. 2025,
I worked on XSAI ([XSAI slides here](https://raw.githubusercontent.com/OpenXiangShan/XiangShan-doc/main/slides/20250716&0718-RVSC-XSAI%EF%BC%9A%E4%BB%A5CPU%E7%9A%84%E7%BC%96%E7%A8%8B%E8%8C%83%E5%BC%8F%E6%94%AF%E6%8C%81%E7%8E%B0%E4%BB%A3LLM%E6%A0%B8%E5%87%BD%E6%95%B0.pdf),
[XSAI repo here](https://github.com/OpenXiangShan/XSAI)).
We hope to provide hardware support for modern LLM kernels in a CPU paradigm on Xianshan, and hide memory latency automatically with
out-of-order execution and prefetching.
See XSAI's roadmap [here](https://github.com/OpenXiangShan/XSAI/issues/4).

For CPU performance, I am experienced in
- Prefetchers
- Workload characterization
- Performance counter architecture
- Performance evaluation framework

During 2022 - 2024, I led the performance analysis and modeling team of Xiangshan processor in Beijing Institute of Open Source Chip (BOSC).
Our team played a significant role in the design of 3rd generation architecture of the Xiangshan processor,
achieving a SPECint2k6 score of 15/GHz on both C++ simulator and RTL.
I will continue maintaining the micro-architecture simulator for Xiangshan and contribute to the open-source community
when leading the LLM inference project in BOSC.

My hobbies include playing badmiton, investment.
I obtained my Ph.D. degree from the Institute of Computing Technology, Chinese Academy of Sciences, and B.Sc. degree from Nanjing University.

<!-- {{< icon name="download" pack="fas" >}} Download my {{< staticref "uploads/CV-En-latex.pdf" "newtab" >}}resumé{{< /staticref >}} or {{< staticref "uploads/CV-Chn.pdf" "newtab" >}}简历{{< /staticref >}}. -->

