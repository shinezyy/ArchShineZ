---
title: Play rocket-chip with intellij IDEA
subtitle: 

# Summary for listings and search engines
summary: Play rocket-chip with intellij IDEA

# Link this post with a project
projects: []

# Date published
date: "2018-12-13T00:00:00Z"

# Date updated
lastmod: "2018-12-13T00:00:00Z"

# Is this an unpublished draft?
draft: false

# Show this page in the Featured widget?
featured: false

# Featured image
# Place an image named `featured.jpg/png` in this page's folder and customize its options here.
image:
  focal_point: ""
  placement: 2
  preview_only: false

authors:
- admin

tags:
- Architecture
- GEM5
- RISC-V
- RocketChip

categories:
- 工作
---

### 前置条件

确保已经用rocket自带的sbt-launch.jar编译过rocket chip，比如已经可以上FPGA或者已经编译出emulator了。

### 导入的图文过程

假如已经用idea打开过rocket chip，但是没有成功导入依赖导致全线飘红，可以考虑删除.idea目录重新导入。

首先启动intellij，"Import Project"

![启动界面](launch.png)

然后选择rocket chip的项目目录

![选择项目目录](choose-dir.png)

然后intellij发现这是一个sbt项目，提示可以通过sbt导入。所以我们选择从sbt导入，"Next"

![从sbt导入](import-from-sbt.png)

接下来是导入的设置界面，这是我的设置：

![导入设置](settings.png)

注意Launcher那里选择Custom，使之指向rocket chip自带的sbt：

![选择rocket-chip自带的sbt启动器](choose-jar.png)

最后在设置页面点Finish即可，过几分钟就可以解析完了。
