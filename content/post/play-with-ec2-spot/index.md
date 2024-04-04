---
title: 生成香山全系统负载和checkpoint的视频教程
subtitle: 为全系统模拟而付出的代价

# Summary for listings and search engines
summary: 最近，我们意识到让用户搞定香山处理器的仿真环境和负载程序是一件非常具有挑战的事情。为了让不同背景的用户更顺利地制作 SPEC CPU 2006 的负载和 Checkpoint，我们制作了一个视频教程。

# Link this post with a project
projects: []

# Date published
date: "2024-03-21T00:00:00Z"

# Date updated
lastmod: "2024-03-21T00:00:00Z"

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
- aws

categories:
- 工作
---

装包：
```shell
git clone https://github.com/shinezyy/vps-setup.git
cd vps-setup
./1.install-package-vanilla.sh
cd /tmp
wget https://bootstrap.pypa.io/get-pip.py
sudo -H python3 get-pip.py
```

如果EBS没有文件系统，格式化为ext4：

首次使用：
```shell
# sudo mkfs -t ext4 /dev/nvme1n1
```

创建用户zyy
```shell
# done in template
sudo useradd -m zyy
sudo usermod -aG sudo zyy
```

```shell
# do it manually
sudo passwd zyy
sudo chsh zyy -s /bin/zsh
```

挂载：
```shell
# do it manually
sudo mkdir -p /mnt/ebs/
sudo mount /dev/nvme1n1 /mnt/ebs/
sudo mkdir -p /mnt/ebs/zyy/
```

挂载后，配置zyy
``` shell
# do it manually
sudo usermod -d /mnt/ebs/zyy zyy
sudo chown zyy:zyy /mnt/ebs/zyy
```

挂载后，如果是首次使用EBS，需要：
```shell
# done in EBS
sudo cp -r ~/.ssh/ /mnt/ebs/zyy
sudo chown -R zyy:zyy /mnt/ebs/zyy

sudo chmod 700 /mnt/ebs/zyy/.ssh
# sudo chmod 700 /mnt/ebs/zyy
```