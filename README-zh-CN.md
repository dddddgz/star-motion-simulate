# Pygame 天体运动模拟

## 简介

这是一个天体运动模拟程序。

**⚠ 注意！该项目在 Windows 上运行时需要 100% 的缩放比例。如果缩放比例不正确可能会导致体验不佳。**

准备：

```
# macOS
python3 -m pip install pyini pygame

# Windows
python -m pip install pyini pygame
```

## 版本信息

目前仍未发布正式版。下载方式：

第一种(***推荐***)：在终端执行 `git clone` 命令：

> `git clone https://github.com/dddddgz/star-motion-simulate`

这样就会有 `.git` 文件夹，可以使用 [Git](https://git-scm.com) 进行操作。

第二种：使用 [GitHub Desktop](https://desktop.github.com)

第二种：可以点击 Code 按钮，然后点击“Download Zip”下载此项目的 `zip` 版本。  

第三种：如果以上方法都不可行，请[提出 Issue](https://github.com/dddddgz/star-motion-simulate/issues/new/choose)

## 项目配置

### 语言设置

如果默认的语言（英语）不是你希望显示的语言（~~肯定不是~~），则你可以打开 `config/config.ini`，找到 <span style="color: #9b2393; font-family: 'Consolas', 'Courier New';"><b>[language]</b></span> 下的 <span style="color: #9b2393; font-family: 'Consolas', 'Courier New';">default</span> 选项，将它更改为你希望显示语言（如 zh-cn）。

### 加载模拟

在 `config/config.ini` 里找到 <span style="color: #9b2393; font-family: 'Consolas', 'Courier New';"><b>[simulation]</b></span> 部分，将 <span style="color: #9b2393; font-family: 'Consolas', 'Courier New';">file</span> 选项更改为你想加载的模拟（在 `simulation` 目录下有很多模拟，随便选择一个，复制它的文件名，并且*去掉扩展名*粘贴到 <span style="font-family: 'Consolas', 'Courier New';">=</span> 后面。

## 操作说明

> 这个部分介绍在程序运行起来后，该如何操作它。

- 放大 / 缩小：鼠标滚轮 / + 和 - 键
- 移动视角：鼠标拖动 / ↑↓←→
- 暂停：空格键
- 导出为图片：Ctrl+S 组合键