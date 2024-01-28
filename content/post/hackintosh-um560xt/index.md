---
title: 铭凡UM560xt (AMD 5600H) 黑苹果流水账
subtitle: 
# Summary for listings and search engines
summary: 铭凡UM560xt (AMD 5600H) 黑苹果流水账
# Link this post with a project
projects: []
draft: false
# image: "img/portfolio/a4-paper.jpg"
# Show this page in the Featured widget?
featured: false
description: ""
date: "2023-12-17T00:00:00Z"
lastmod: "2023-12-17T00:00:00Z"
categories:
- 生活

tags:
- Hackintosh

authors:
- admin

---

# UM560xt 黑苹果

花了一天多时间搞黑苹果，最开始走了一些弯路。后来follow [Dortania](https://dortania.github.io/OpenCore-Install-Guide/installer-guide/mac-install.html#setting-up-opencore-s-efi-environment)
的教程，终于走出来了。

我所使用的EFI基于[小兵的um560xt](https://github.com/daliansky/minisforum-UM560XT-Hackintosh)，我的仓库：[minisforum-UM560XT-Hackintosh](https://github.com/shinezyy/minisforum-UM560XT-Hackintosh)

## 弯路

最开始用gibMacOS 下载了Catalina，尝试用网络安装，但是不确定是不是因为硬盘上已经有一个 Ubuntu，Catalina 下载完了之后安装重启一次之后就找不到MacOS的启动项了。


## 根据Dortania的教程制作LiveCD

根据这个教程，我终于知道，基于Win和Linux现在只能制作网络安装器，只有基于MacOS才能制作离线安装器。
MacOS可以安装PKG，在系统里得到一个应用，该应用可以把安装器刻录到U盘的第二个分区。

在此之前，需要把整个U盘格式化为 Mac OS 扩展文件系统（带日志），实际上它还会自动弄出来一个EFI分区（分区1），
分区2是MacOS的文件系统，用来装镜像的。
用PKG安装后得到的安装器，可以往分区2写入镜像，我第一次写入不知道为什么失败了，第二次是成功的。

写入成功后，用[EFIMount](https://github.com/corpnewt/MountEFI)挂载分区1，然后把OpenChip的基本文件放进去，按照教程，删来只剩下4个最重要的。

然后把别人准备好的驱动程序拷贝到/EFI/OC文件夹，我用的是[小兵的um560xt](https://github.com/daliansky/minisforum-UM560XT-Hackintosh)。
有重复的文件，我选择的是**合并**。

## 目标硬盘的准备

有些人说安装了先其它系统（Linux 或者 Win）的硬盘不能再安装MacOS，这是不正确的。
至少，我的Big Sur 安装完之后，能正常启动。

## WiFi

我没有用博通的卡，而是用了Intel AX200

用itlwm.kext可以在Catalina的安装过程中看到Intel的卡，但是不能连接WiFi。

在完成安装后，在itlwm的基础上，用HeliPort 可以让AX200连接到WiFi。

## 蓝牙

建议升级到12+之后再折腾蓝牙，因为 [Monterey 以后所需的kext和以前的不一样](https://openintelwireless.github.io/IntelBluetoothFirmware/FAQ.html#what-additional-steps-should-i-do-to-make-bluetooth-work-on-macos-monterey-and-newer)。

具体地，我用到了3个kext：

(1) IntelBTPatcher.kext and (2) IntelBluetoothFirmware.kext from [IntelBluetoothFirmware v2.3.0](https://github.com/OpenIntelWireless/IntelBluetoothFirmware/releases/tag/v2.3.0)
(3) BlueToolFixup.kext from [BrcmPatchRAM](https://github.com/acidanthera/BrcmPatchRAM)