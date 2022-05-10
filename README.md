# TTSX

Convert Text Files(txt,md,...) to Voice Files(mp3, wav) under given directory

## 使用模块

[pyttsx3](https://pypi.org/project/pyttsx3/) 是Python中的文本到语音转换的一个常用软件包。
与其他同类包不一样，它可以离线使用，兼容Python 2 和 Python 3，使用非常方便。
可以调节语速、音量，选择男声、女声。

将文本文件转换成语音文件，除了多国语言是难点外，还有很多不同方言。这些都属于机器学习自然语言的一部分。

## 安装库

    pip install pyttsx3

## 运行方式

终端命令行中运行下面代码

    python ./src/ttsx.py ../tmp [filetype [<output_directory>]]

注：'filetype': 文本文件的后缀名，可以是 txt, md 等，缺省是 md；会自动过滤掉 markdown 中的 # 符号，自动过滤空行。

作用：自动将指定目录下的文本文件生成同名的音频文件。

## 结果

生成 mp3 文件，或者 wave 格式音频文件。

## 代码开放

[测试样例程序](https://github.com/liuxiang0/TTSX.git)参见我的[github主页](https://github.com/liuxiang0/)
