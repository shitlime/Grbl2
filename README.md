# Grbl2
**覌白**，取自然码双拼的码作为项目名，2代表第二代（第一代是2021年以前的事了）

是一个基于[Ariadne](https://github.com/GraiaProject/Ariadne)框架的QQ机器人

[覌白的图片_由AI画图产生](头像v2.png)  

**⚠主要是自用的，应该不会花时间管理本仓库**

# 使用须知

## Ariadne的安装

### 安装
安装Ariadne  
*基础*
```
pip install graia-ariadne
```

安装Saya  
*支持Bot分模块*
```
pip install graia-saya
```

安装Graia Scheduler  
*支持Bot定时发送消息*
```
pip install graia-scheduler
```

### 其他
详见：[官方文档](https://graia.readthedocs.io/ariadne/)✅  
或：[社区文档](https://graiax.cn/)⚠️注意浓度  

## 其他Python依赖
```bash
pip install pillow
pip install pypinyin
pip install pyyaml
```
*未经过测试，可能漏了一些（屑~*

# 运行需要
+ [Mirai](https://github.com/mamoe/mirai)

# 配置文件
`bot_config.yaml` 是配置文件的 **模板**  
实际使用时请按模板写一个名为 `grbl_config.yaml` 的配置文件  

## 说明
分为以下四个主要部分
```yaml
# 基本信息
info:

# Ariadne连接配置（可查阅Ariadne文档的详细说明）
ariadne_config:

# Saya载入的模块（这些模块会被运行，格式基本按Python的标准写）
modules:

# 各模块的配置（见对应模块源码，有部分注释）
modules_config:
```

# 模块
`modules`是模块文件夹

里面是覌白的各种功能模块

## 说明
+ `search_char` 模块需要 `观星三拼` 和其附带的 `四角号码`查字文件（未提供，可以考虑不运行此模块）

+ `break_tofu` 模块运行需要[天珩字体库](http://cheonhyeong.com/Simplified/download.html)

*暂时懒得写了（屑~*