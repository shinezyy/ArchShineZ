---
title: "QoSMT: supporting precise performance control for simultaneous multithreading architecture"

# Authors
# If you created a profile for a user (e.g. the default `admin` user), write the username (folder name) here 
# and it will be replaced with their full name and linked to their profile.
authors:
- Xin Jin
- admin
- Bowen Huang
- Zihao Yu
- Xusheng Zhan
- Huizhe Wang
- Sa Wang
- Ningmei Yu
- Ninghui Sun
- Yungang Bao

# Author notes (optional)
author_notes:
- "Equal contribution"
- "Equal contribution"

date: "2021-06-20T00:00:00Z"
doi: ""

# Schedule page publish date (NOT publication's date).
publishDate: "2019-06-14T00:00:00Z"

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ["1"]

# Publication name and optional abbreviated publication name.
publication: In *Conference on Supercomputing*
publication_short: In *ICS 2019*

abstract: Simultaneous multithreading (SMT) technology improves CPU throughput, but also causes unpredictable performance fluctuations for co-located workloads. Although recent major SMT processors have adopted some techniques to promote hardware support for quality-of-service (QoS), achieving both precise performance control and high throughput on SMT architectures is still a challenging open problem. In this paper, we perform some comprehensive experiments on real SMT systems and cycle-accurate simulators. From these experiments, we observe that almost all in-core resources may suffer from severe contention as workloads vary. We consider this observation as the fundamental reason leading to the challenging problem above. Thus, we introduce QoSMT, a novel hardware scheme that leverages a closed-loop controlling mechanism to enforce precise performance control for specific targets, e.g. achieving 85%, 90% or 95% of the performance of a workload running alone respectively. We implement a prototype on GEM5 simulator. Experimental results show that the control error is only 1.4%, 0.5% and 3.6%.


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

{{% callout note %}}
Click the *Cite* button above to demo the feature to enable visitors to import publication metadata into their reference management software.
{{% /callout %}}

{{% callout note %}}
Create your slides in Markdown - click the *Slides* button to check out the example.
{{% /callout %}}

Supplementary notes can be added here, including [code, math, and images](https://wowchemy.com/docs/writing-markdown-latex/).
