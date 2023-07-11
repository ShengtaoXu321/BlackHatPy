# Python环境设置

## 1. 设置虚拟环境

## 1.1 安装`Python3-venv`软件包

创建一套虚拟环境，需要安装`python3-venv`软件包

```shell
sudo apt-get install python3-venv
```

## 1.2 创建虚拟环境

创建一个新的目录，然后将虚拟环境放进去

```shell
mkdir bhp
cd bhp
# 在此处进入终端模式
python3 -m venv venv3   # 向Python3传递了-m选项来调用venv包，并且传递了创建的环境名venv3
source venv3/bin/activate # 运行active脚本激活这个环境
# 当环境被激活，命令行提示前会多一个(venv3)的环境名字
deactivate # 退出虚拟环境
```

![image-20230711213852156](https://github.com/ShengtaoXu321/BlackHatPy/blob/main/bhp/pic/image-20230711213852156.png?raw=true)

## 1.3 在venv虚拟环境中pip安装软件包

在虚拟环境中，我们看到输入python也会是python3，那是因为在创建虚拟环境的时候是使用python3创建的。

接下来，我们使用`pip`命令在虚拟环境中安装Python包

```shell
# 搜索hashcrack软件包
pip search hashcrack

# 安装lxml库--网页爬虫使用到
pip install lxml
```

![image-20230711215020467](https://github.com/ShengtaoXu321/BlackHatPy/blob/main/bhp/pic/image-20230711215020467.png?raw=true)

别问上面为啥报错，`pip search`报错一搜一堆问题，这里不探讨了。要么直接`pip isntall`，要么直接转向`Conda`。记住，这不是镜像源的原因，我是全局代理。

![image-20230711215243300](https://github.com/ShengtaoXu321/BlackHatPy/blob/main/bhp/pic/image-20230711215243300.png?raw=true)



## 2. IDE

Python的IDE不用说，最受欢迎的肯定是`PyCharm`，这里以📚上的`VS Code`为例子

你可以在kali或者任何平台上安装，这里以Debian系列为例

```shell
sudo apt-get install code

# 官网下载最新的VS Code，然后apt-get来安装
sudo apt-get install -f ./code_1.39******.deb
```



