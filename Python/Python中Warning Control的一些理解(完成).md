# 写在前面

最近在pytorch运行网络模型时,因为版本的问题,有大量的warning输出,这对于根据输出查看训练状态来说是很麻烦的,所以有了忽略warning输出的需求.

# Python中的warning Control

## 基本概念

### warning类型分类

Python中有多种warning类型,其中`Warning`为其他所有warning类型的基类.详情如下:

* `UserWarning`: 用户警告
* `DeprecationWarning`:弃用警告
* `SyntaxWarning`: 语法警告
* `RuntimeWarning`: 运行时警告
* `FutureWarning`: 未来可能发生的警告
* `PendingDeprecationWarning`: 未来可能被弃用的警告
* `ImportWarning`: 导入警告
* `UnicodeWarning`: 与Unicode编码相关的警告
* `BytesWarning`: 与字节或者字节数组相关的警告
* `ResourceWarning`: 与资源使用相关的警告

详情可查看[此处](https://docs.python.org/3/library/warnings.html#warning-categories)

### warning filter

警告过滤器可以理解为是一个表中的一个条目,格式为`(action, message, category, module, lineno)`,其中,`action`表示匹配到的警告采用什么样的频率输出, `message`表示警告输出信息,此处是一个正则匹配项,`category`表示匹配的warning类型, `module`表示警告发出所在的模块名,也是正则匹配项, `lineno`表示警告发出的行号,只有`(message, category, module, lineno)`都匹配到发出的警告时,相应的`action`才会进行.此处我们需要简单的理解一个警告发出的过程

* 首先调用`warnings.warn(message, category)`表示此处有个警告需发出
* 然后根据给定的警告类型`category`,在warning filter构成的列表中寻找匹配项,找到匹配的filter, 然后对该类型的警告执行`action`操作,如果没有匹配的filter则对该类型警告执行默认操作.

因此我们可以看出warning filter的作用是用于控制警告的输出动作.

### cation分类

`action`表示对于将发出的警告需执行的动作,包含着输出的频率

* `default`: 对于匹配的警告,打印在每个位置第一次出现时输出（模块+行号）,之后在同一位置出现时不输出.
* `error`: 将匹配的警告变为异常
* `ignore`: 忽略警告,不进行输出
* `always`: 总是打印输出匹配的警告
* `module`: 对于匹配到的警告,在一个模块中第一次出现时才输出（与行号无关）,之后不管在模块的哪个位置出现都不输出.
* `once`: 对于匹配到的警告只打印输出一次,而不管在哪个位置.


## warn代码原理剖析

警告发出的关键方法是`warnings.warn()`,在warnings.py文件中,因此可以深入去理解该部分代码,部分进行了省略.

```python
def warn(message, category=None, stacklevel=1, source=None):
    # 1.类型检查
    # 2.设置行号,设置模块名, 设置文件名
    registry = globals.setdefault("__warningregistry__", {})
    warn_explicit(message, category, filename, lineno, module, registry,
                  globals, source)

def warn_explicit(message, category, filename, lineno,
                  module=None, registry=None, module_globals=None,
                  source=None):
    # 3.获取警告信息,设置行号,构建一个key
    key = (text, category, lineno)
    if registry.get(key):  # registry是一个字典,保存了执行once,module,default操作的警告请求
        return
    # 4.遍历filter列表,寻找匹配项
    for item in filters:
        action, msg, cat, mod, ln = item
        if ((msg is None or msg.match(text)) and
            issubclass(category, cat) and
            (mod is None or mod.match(module)) and
            (ln == 0 or lineno == ln)):
            break
    else:
        action = defaultaction # 没有找到匹配的filter则使用default操作
    # 5.根据对应的action执行是否输出警告的操作
    if action == "ignore":
        return
    if action == "error":
        raise message
    if action == "once":
        registry[key] = 1
        oncekey = (text, category)
        if onceregistry.get(oncekey):
            return
        onceregistry[oncekey] = 1
    elif action == "always":
        pass
    elif action == "module":
        registry[key] = 1
        altkey = (text, category, 0)
        if registry.get(altkey):
            return
        registry[altkey] = 1
    elif action == "default":
        registry[key] = 1
    else:
        # 不能处理的错误
        raise RuntimeError(
              "Unrecognized action (%r) in warnings.filters:\n %s" %
              (action, item))
    # 6. 按格式输出警告信息
    msg = WarningMessage(message, category, filename, lineno, source)
    _showwarnmsg(msg)
```

注意: 在python2, 和python3中,略有不同,python2使用的是warnings.py所定义的方法,而在python3中虽然也提供了warnings.py,但是在warnings.py中导入了_warnings模块,所以实际上python3中使用的warn方法定义在_warning模块中,而模块_warnings是在python虚拟机初始化中创建的模块对象,也就是说用C语言内置在python虚拟机中....不过我们可以将warnings.py中的模块_warnings导入注释掉,从而使用warnings.py中定义的方法.

# 警告控制的一些实践

在理解python的警告控制相关的原理后,我们便能够根据自己的需要控制警告信息如何输出,因此从中,我们可以知道控制警告的关键便是如何设置warning filter.设置filter的方式有两种,一是在代码中,二是启动虚拟机时使用命令行参数

## warnings.filterwarnings方法

在源代码中,调用`warnings.filterwarnings()`函数设置filter条目,示例如下
```python
# 以下在python3
import warnings

def f():
    warnings.warn("warn occur!", UserWarning)

warnings.filterwarnings('module', category=UserWarning)
print(warnings.filters)
f()
print('hello')
for i in range(3):
	f()
print('world!')
```

```
# 输出结果
[('module', None, <class 'UserWarning'>, None, 0), ('default', None, <class 'DeprecationWarning'>, '__main__', 0), ('ignore', None, <class 'DeprecationWarning'>, None, 0), ('ignore', None, <class 'PendingDeprecationWarning'>, None, 0), ('ignore', None, <class 'ImportWarning'>, None, 0), ('ignore', None, <class 'ResourceWarning'>, None, 0)]
test.py:4: UserWarning: warn occur!
  warnings.warn("warn occur!", UserWarning)
hello
world!
```
注意: filter设置必须在发出警告请求之前

## 命令行参数 -W

在启动虚拟机时使用`-W`参数同样可以设置filter条目,参数格式如下
```
-W action:message:category:module:lineno
其中各部分含义与warning filter条目设置各项含义相同
```
注意: 如果某项缺省,如message,module,lineno缺省则参数形式为`-W ignore::UserWarning`,其中`UserWarning`后面部分的符号`:`可以省略,但是前面的不行.

# 注意

python提供的警告控制也有着局限性,只有对于使用了`warnings.warn()`函数发出的警告,可以通过设置warning filter条目控制警告输出,但是对于一些使用底层函数进行警告输出的信息无法控制,例如在pytorch中,一些涉及到tensor操作的函数以底层C/C++实现,并且将警告信息嵌入其中,对于这种情况输出警告信息,我们没法控制,所以如果不想看输出的警告信息,还是乖乖根据警告提示修改代码吧^_^
