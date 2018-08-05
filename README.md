# 提取安卓恶意软件的gram特征



## 参考资料

　　本代码是参考乌云上的一篇文章实现的，链接如下：http://wooyun.jozxing.cc/static/drops/mobile-13428.html
，如果有理解的不妥的地方，请大家帮忙指出



## 原理

　　原理就不详细讲了，我参考资料中给的链接已经说得很清楚了，我就说一说原文中说得不是很清楚，我自己进行了一些揣摩理解的地方。

　　我以method作为单位进行提取，每个method看成互不相关的“句子”。以3-gram为例，如果method中的指令数目小于3的话则忽略该method。

　　原文按照一定的标准将指令分为MRGITPV七类，我按照Android4.1.2源码下的dalvik-bytecode.html对其进行了整理，所有的字节码到其分类的映射规则都位于/infrastructure/map.py文件中。

　　看原文的意思似乎最后的特征是通过汇总每种n-gram在app中出现的次数得到的，但是我思考了一下，如果app规模的大小相差很大的，这么做似乎不是很妥，因为规模大的app的指令出现数量自然应该倾向于比较多，比如我手头里的样本，恶意样本的规模大多都比较小，而良性样本的规模大多都很大，所以这里最终提取的特征是按照每种n-gram是否出现，如果出现过就为1，不出现就为0。我认为这样会更加合理的原因是，恶意软件往往都不是从头开始写的，大多数应该都是通过重用以前的代码而实现的，通过判断一种恶意n-gram是否出现应该能有一定的恶意软件鉴别效果。

## 如何运行

　　本软件是基于python3.6开发的，反汇编使用的工具是apktool，我已经将其放在了本仓库的根目录下，唯一的依赖是pandas，如果还没有安装的话，请使用pip install pandas安装。

　　首先在clone下来的目录下新建/smalis/malware和/smalis/kind两个文件夹（这两个是存放反汇编结果的目录）。


　　然后打开batch_disasseble.py，将27行的virus_root变量的值改成自己电脑上存放恶意软件apk样本根目录，32行的kind_root变量的值改成自己电脑上存放正常apk样本的目录，然后按照以下顺序执行命令即可（或者直接执行run.bat，里面写的就是这些命令）：
```
python batch_disasseble.py
python bytecode_extract.py
python n_gram.py 6
python n_gram.py 5
python n_gram.py 4
python n_gram.py 3
python n_gram.py 2
```


​    　其中batch_disasseble.py是用于反汇编apk的；

​       python bytecode_extract.py执行结束后会在当前目录生成一个data.csv，这个是在n-gram处理之前的特征，data.csv由SoftwareName,Feature,isMalware三个字段组成，分别代表软件名称，特征和是否恶意软件（是为1，不是为0），其中Feature字段是该app的所有操作码（被分为了MRGITPV七类表示），其中用"|"分隔不同的method。

　　`python n_gram.py`后面接的参数的含义就是n-gram中的n，命令运行结束之后会在当前目录生成一个n-gram.csv文件，比如`python n_gram.py 2`，命令执行结束后就会在当前目录生成一个2-gram.csv文件。

　　这些脚本我已经用自己手头上的样本运行过一遍了，本仓库根目录下的data.csv（因为超过了github限制的最大文件限制，所以没有上传），6_gram.csv（同样的原因没有上传），5_gram.csv，4_gram.csv，3_gram.csv，2_gram.csv就是我在那些样本上提取的特征。

## 仓库中的数据说明

　　5_gram.csv，4_gram.csv，3_gram.csv，2_gram.csv前600个样本是恶意样本，后面583个样本是良性样本

## 软件模块

　　概述：batch_disasseble.py，bytecode_extract.py，n_gram.py是三个可以直接执行的脚本，/infrastructure下的模块全部是给这些脚本提供一些封装好的基础设施，比如smali解析等等。

　　batch_disasseble.py:将恶意apk从指定目录反汇编到/smalis/malware/目录下，将良性apk从指定目录反汇编到/smalis/kind/目录下的脚本

　　bytecode_extract.py:将字节码从smali文件中提取出来并映射成其分类，最终存储到当前目录下的data.csv的脚本

　　n_gram.py:将data.csv提取n_gram特征转换成n_gram.csv的脚本

　　infrastructure.map:我在这里配置了所有字节码到MRGITPV分类的映射关系　

　　infrastructure.smali:Smali类的每个实例代表一个smali文件，用于封装解析smali文件的逻辑

　　infrastructure.ware:Ware类的实例代表一个安卓app，该类的实例会包含多个Smali实例，这些Smali实例都是从该app反汇编得到的smali文件得到的




