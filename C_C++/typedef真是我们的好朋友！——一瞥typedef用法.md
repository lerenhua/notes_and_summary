# 认识`typedef`
* `typedef` 是C语言中比较重要的关键字，其作用是为了给类型起别名
* `typedef` 的使用一般与C语言中的声明有着密切联系，如果你不能读懂形如` char * const *(*next)();` 这样的声明语句，那你可以去看看这篇[文章](/home/lerenhua/csdn_papers/C_C++/你可知C中声明的规则是这样的？！.md)
# 为什么我们要使用`typedef`
### 1.简化声明语句
我想C语言设计者提出这个`typedef`关键字肯定是考虑到了简化声明语句的功用，毕竟现在有的声明语句已经是复杂到让人第一眼看去就不想看了，像这样的声明语句 `void (*signal(int sig, void (*func)(int)))(int);`直接去阅读确实很不方便的，但是如果这样呢：
```C
typedef void (*func_ptr)(int);
func_ptr signal(int sig, func_ptr func);
```
根据C语言的声明解读规则，我们知道声明语句 `void (*signal(int sig, void (*func)(int)))(int);` 表示signal是返回函数指针的函数,该函数接受int及函数指针为参数,返回的函数指针指向无返回值的函数,该函数接受int参数.我们可以看出该声明中包含函数指针这样的概念，因此我们可以使用`typedef`定义一个函数指针的类型名
```C
typedef void (*func_ptr)(int); // func_ptr表示类型说明符，可以用于声明一个函数指针变量，指向的函数接受int参数，无返回值
```
通过此方式极大的简化了声明语句，便于阅读和理解。
### 2.