# Grbl2

**覌白** 是一个基于[Ariadne](https://github.com/GraiaProject/Ariadne)框架的Python QQ Bot，依靠 `Ariadne` + `mirai-api-http` + `Mirai` 形成完整Bot运行环境。

> 项目名取自然码双拼的码，2代表第二代（第一代是2021年以前的事了）


[覌白的图片_由AI画图产生](头像v2.png)  


~~⚠️摸鱼声明：应该不会花时间管理本仓库~~


# 快速开始

## Docker

利用Dockerfile快速启动

0. 获得源代码
```shell
git clone --recurse-submodules https://github.com/shitlime/Grbl2.git

cd Grbl2
```

1. 安装Docker（有多种安装方式，不提供参考）

2. 获取Python3镜像
```
docker pull python
```

3. 构建Grbl2镜像
```
docker build -t grbl2 .
```

4. 运行容器
```
docker run -it --rm --name grbl2-running grbl2
```
在后台运行
```
docker run -itd --rm --name grbl2-running grbl2
```


## 直接运行

> ⚠️注意：开发使用的Python版本为3.10.7，若使用小于该版本号的，可能出现一些bug


0. 获得源代码
```shell
git clone --recurse-submodules https://github.com/shitlime/Grbl2.git

cd Grbl2
```

1. 依赖安装
```shell
pip install -r requirements.txt
```


2. 运行Bot

* Windows：
```shell
bot.py
```

* Linux：
```shell
python3 ./bot.py
```


# 使用须知

## Ariadne框架

+ `graia-ariadne` *Ariadne基础*
+ `graia-saya` *支持Bot分模块开发*
+ `graia-scheduler` *支持Bot定时发送消息*


**更多：**  
详见：[官方文档](https://graia.readthedocs.io/ariadne/)✅  
或：[社区文档](https://graiax.cn/)⚠️注意浓度  


## Bot完整运行需要

+ [Mirai](https://github.com/mamoe/mirai)
+ 以及Mirai相关的组件/插件


# 配置文件
`bot_config.yaml` 是配置文件的 **模板**  
实际使用时请按模板写一个名为 `grbl_config.yaml` 的配置文件  

## 说明
分为以下四个主要部分
```yaml
# 基本信息
info:

# Ariadne连接Mirai的配置（可查阅Ariadne文档的详细说明）
ariadne_config:

# Saya载入的模块（这些模块会被运行，格式基本按Python 里 import导包的标准写）
modules:

# 各模块的配置（见对应模块源码，有部分注释）
modules_config:
```


# 项目结构

## 模块
`modules` 是模块文件夹

里面是覌白的各种功能模块

### 重要说明
+ `modules/SearchThing/search_char`
    - 模块运行需要对应的查字文件（未提供，可以考虑不运行此模块）

+ `modules/BreakTofu`
    - 模块运行需要对应的字体文件（未提供，可以考虑不运行此模块）

+ `modules/AIDrawing`
    - 该模块已经失效


## 资源
`resources` 是资源文件夹（未提供）

所有模块运行需要的资源都可以放在这里，之后在配置文件中指定相对路径即可


# 其他

+ 感谢飞梧的 [cjk_split](https://github.com/asgsdbrseg/cjk_split)