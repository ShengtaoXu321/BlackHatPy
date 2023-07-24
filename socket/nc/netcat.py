"""
# -*- coding: utf-8 -*-
# Author: Tack_Ding
# Datetime: 2023/7/19 12:23 AM
# Filename: netcat.py
# Description: Only for learning, please abide by the law
"""

# 导入需要的模块
import argparse  # 创建一个命令行工具的参数解析器
import sys
import textwrap     # 用于格式化文本
from N2Class import NetCat   # 封装了Netcat的类




if __name__ == '__main__':
    """
    创建main代码块，用来解析命令行参数并调用其他函数
    """
    parser = argparse.ArgumentParser(       # ArgumentParser 是 argparse 模块中的类，用于创建一个参数解析器对象。
        description= 'BHP Net Tool',        # descrption参数，对命令工具行的一个简短描述
        formatter_class=argparse.RawDescriptionHelpFormatter,   # formatter_clas参数，
                                           # 这个参数指定使用 argparse.RawDescriptionHelpFormatter 类来格式化帮助文档，不额外缩进换行，原格式输出
        epilog=textwrap.dedent('''Example:                    
            netcat.py -t 192.168.1.108 -p 555 -l -c   # command shell
            netcat.py -t 192.168.1.108 -p 555 -l -u=mytest.txt   # upload to file
            netcat.py -t 192.168.1.108 -p 555 -l -e=\"cat /etc/passwd\"  # execute command
            echo 'ABC' | ./netcat/py -t 192.168.1.1 -p 999 # echo text to server port 999
            netcat.py -t 192.168.1.1 -p 5555 # connect to server   
        '''
        )  # epilog参数，对工具行的额外描述，给出一些用法示例。
           # 使用 textwrap.dedent() 函数来移除额外的缩进，使得帮助文档中的示例字符串对齐。
    )

    # parser.add_argument(name or flags, ..., **kwargs)
    # parser.add_argument() 方法是 argparse 模块中用于向参数解析器（ArgumentParser 对象）添加命令行参数的方法。
    # 调用 add_argument() 方法来向解析器添加不同的命令行参数，以配置工具的行为
    parser.add_argument('-c', '--command', action='store_true', help='command shell')
    parser.add_argument('-e', '--execute', help='execute specified command')
    parser.add_argument('-l', '--listen', action='store_true', help='listen')
    parser.add_argument('-p', '--port', type=int, default=999, help='specified port')
    parser.add_argument('-t', '--target', default='192.168.20.123', help='specified ip')
    parser.add_argument('-u', '--upload',  help='upload file')

    # 调用 parser.parse_args() 来解析上面paser.add_argument()命令行参数
    args=parser.parse_args()    # 解析命令行参数
    if args.listen:             # 获取用户指定的参数值，如果是-l或者说--listen监听状态
        buffer = ''             # buf则是空字符串
    else:
        buffer = sys.stdin.read()   # 否则，就从标准输入 读取数据

    nc = NetCat(args, buffer.encode('utf-8'))    # 实例化一个NetCat 类的nc对象
    nc.run()      # 启动程序