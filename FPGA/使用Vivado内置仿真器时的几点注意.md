# 在Windows上使用Vivado内置仿真器的几点注意

1. 注意C盘空间的大小
    <br> 
    在使用Vivado内置的仿真器时，仿真过程的数据会暂时的保存在C盘的用户文件夹下的隐藏文件夹AppData， 临时数据的具体路径一般为 `C:\Users\Administrator\AppData\Local\Temp`, 其中`Administrator`表示自己使用的用户名文件夹。由于仿真过程中的临时数据保存在C盘中，所以对于长时间的仿真，要关注C盘空间的剩余情况，否则程序会因为C盘剩余空间不足而被杀死。

2. 仿真结果的可信程度
