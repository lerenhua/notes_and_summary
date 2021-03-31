# 写在前面

* 在机器上进行深度学习实验或其他应用时,相关框架的安装过程总是少不了的.其中,以PyTorch为例记录Python环境下的安装思路过程
* 安装过程大致分为两类
    1. 联网安装
    2. 离线安装

# 联网安装

## 推荐官网上的方法

![](./pytorch1.png)
从[PyTorch官网](https://pytorch.org/)中,我们可以很简单的查询到命令行下载的方式.不过存在一个问题,下载速度可能会比较慢,这时推荐换源的方法或者科学上网, 再或者离线安装.

# 离线安装

对于网络的情况,我们可以不用联网安装的方法,而是使用离线安装的方法.

## pip安装

pip离线安装要求的是.whl文件, 因此需要自己下载Pytorch对应的.whl文件, 链接如下:https://download.pytorch.org/whl/torch_stable.html ,需要自己选择合适的文件.

## conda安装

参考: https://blog.csdn.net/Suan2014/article/details/80410144
进入清华的镜像软件站:https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/ 中根据操作系统选择下载所需的.tar.bz2文件.
* 在已激活的虚拟环境中执行: 
```
conda install --offline XXX.tar.bz2
```
XXX.tar.bz2为对应下载的文件

* 指定在哪个环境安装:
```
conda install --offline -n env_name XXX.tar.bz2
```
env_name为指定的环境名
