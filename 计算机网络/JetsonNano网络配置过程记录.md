# 看在前面

本文记录JestonNano网络配置过程,方便以后自己复盘,提供思路.本文假设读者了解JestonNano并且配置完Nvidia官方提供的镜像等过程.

# 问题场景

Nvidia JestonNano是一个类似于树莓派的开发板,但是板子缺少WiFi网卡,因此对于上网需求有两个解决问题的方向:
```
    1. 使用USB无线网卡
    2. 使用以太网
```
但是我有如下限制: 
```
    1. 没有USB无线网卡,同时可能存在ubuntu系统下无线网卡难装的问题
    2. 无网络宽带可用,即JestonNano没法直接使用以太网线进行联网
    3. 可以使用笔记本共享网络 
```
我有如下需求:
```
    1. 通过ssh连接,在笔记本电脑上进行JestonNano的开发,而不对板子连接其他外设
    2. JestonNano可以访问Internet
```

# 解决过程
解决的总体思路: 使用以太网线将JestonNano与笔记本相连,然后在笔记本上开启网络共享设置.
具体过程如下:
```
1. 配置JestonNano的以太网卡
2. 打开笔记本网络共享设置
```

## 配置网卡

在我的情景中,JestonNano没有接外设,只有一根网线,我只能借助ssh连接使用命令行进行网卡的配置.此处有必要说明我配置网卡的原因: 在初次启动JestonNano时,我使用了显示器等外设,并且在图形化界面下配置了网卡的静态IP,这样使得通过一根网线我的笔记本和JestonNano可以建立ssh连接,但是在之后有联网的需求时,并无使用外设的条件.

* 使用ssh连接,修改/etc/network/interfaces文件

```shell
vim /etc/network/interfaces
```
说明: JetsonNano官方提供的镜像是Ubuntu18.04系统,有些博客提到Ubuntu18.04提供了netplan程序进行网络配置,但是在JestonNano下命令行下修改/etc/netwok/interfaces文件进行配置仍然是有效的.

* 添加配置信息如下

```
# 配置静态IP使用以下内容
auto eth0                    # eth0为以太网卡名称,可以使用ifconfig查询
iface eth0 inet static
    address 192.168.137.100    # IP地址
    netmask 255.255.255.0    # 子网掩码
    gateway 192.168.1.1

# 配置动态IP使用以下内容
auto eth0    
iface eth0 inet dhcp 
```
说明:使用笔记本共享网络情况下,JestonNano本应该将网卡配置为动态IP,但是考虑到我没有外设,如果使用动态IP的话,IP改变我没法使用ssh登录JestonNano了.因此我使用了静态IP设置,不过需要注意此IP的网段不能和笔记本电脑连接Internet的网段相同.

* 重启使得配置生效
```
# 有些博客提及使用 systemctl restart ifup@eth0重启网卡,但是实际在JestonNano无效
reboot
```

## 打开网络共享设置

* 此处请参考文章:https://blog.csdn.net/acsder2010413/article/details/40395621

说明:

1. 我的笔记本是win10系统;
2. 要搞清楚共享的连接和需要此共享的连接,因为网卡接口是网络通信IP的实体,因此可以连接到Internet的接口就是我们共享的连接,而和JestonNano连接到接口就是需要此共享的连接.
3. 共享有线连接的网络时,可能会将LAN接口配置成一个固定IP如192.168.137.1,所以在共享之前,JestonNano上的网卡配置成与其同网段的IP即可,如IP:192.168.137.100, netmask:255.255.255.0
