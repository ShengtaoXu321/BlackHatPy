"""
# -*- coding: utf-8 -*-
# Author: Tack_Ding
# Datetime: 2023/7/22 1:00 AM
# Filename: tools.py
# Description: Only for learning, please abide by the law
"""
import shlex      # 用于解析命令行字符串
import subprocess  # 进程创建接口，用于创建和控制子进程的模块


# exec()函数：接收一条命令并执行，将结果作为字符串返回
def execute(cmd):
    """
    接收cmd输入的命令并执行，返回结果作为字符串返回
    :param cmd:
    :return:
    """
    cmd = cmd.strip()   # 去除首尾空格
    print(cmd+'*')
    if not cmd:         # 无输入则返回
        return
    # cmd_split = shlex.split(cmd)
    # print(cmd_split)
    output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)    # check_output()会在本机运行一条命令
    # shlex.split(cmd) 将传入的 cmd 字符串按照空格分割为一个命令和参数的列表。
    # stderr = subprocess.STDOUT：这个参数指定将标准错误输出（stderr）与标准输出（stdout）合并
    # subprocess.check_output()是subprocess模块中的一个方法，用于执行命令并捕获其输出。

    return output.decode()
