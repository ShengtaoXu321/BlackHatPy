"""
# -*- coding: utf-8 -*-
# Author: Tack_Ding
# Datetime: 2023/7/19 11:18 PM
# Filename: N2Class.py
# Description: Only for learning, please abide by the law
"""
import socket
import sys
import threading
from tools import execute

class NetCat:
    def __init__(self, args, buffer=None):
        """
        传入的命令行参数和缓冲区参数，初始化一个nc对象，创建一个socket对象
        :param args:
        :param buffer:
        """
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   # 用于设置套接字选项的方法socket.setsockopt()
        """解释socket.setsockopt()方法为啥要设置level=socket.SOL_SOCKET, opt=socket.SO_REUSEADDR, value=1
        在服务器端等待连接时，如果服务器套接字关闭后，仍然需要一段时间才能释放该地址，
        这可能会导致在此期间无法立即重新绑定相同的地址和端口，从而导致 "Address already in use" 错误。
        使用 SO_REUSEADDR 选项后，可以允许重新绑定本地地址，即使套接字处于 TIME_WAIT 状态。
        """

    def run(self):
        """
        执行函数入口
        :return:
        """
        if self.args.listen:    # 如果是接收方，则执行listen()
            self.listen()
        else:
            self.send()         # 如果是发送方，就执行send()



    # send()方法
    def send(self):
        """
        发送，更新client端
        :return:
        """
        # 如果缓冲区有数据，就直接发送；否则进行try处理
        self.socket.connect((self.args.target, self.args.port))    # 进行连接
        if self.buffer:
            self.socket.send(self.buffer)

        try:
            while True:    # 大循环，对数据进行接收，以4096为单位，小于直接接收；大于则以4096分段接收
                recv_len = 1
                response = ''
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len=len(data)
                    response += data.decode()
                    if recv_len < 4096:      # 退出循环的条件
                        break

                    if response:
                        print(response)
                        buffer = input('> ')  # 输出完response内容，暂停等待用户的输入才继续
                        buffer += '\n'
                        self.socket.send(buffer.encode())    # 发送出用户输入的新内容，进行下一轮新循环
        except KeyboardInterrupt:    # 按下ctr+c就退出循环
            print('User terminated.')
            self.socket.close()
            sys.exit()


    # listen()方法
    def listen(self):
        """
        监听，更像server端
        :return:
        """
        self.socket.bind((self.args.target, self.args.port))    # 设置监听IP和端口
        self.socket.listen(5)  # 最大连接数为5
        while True:
            client_socket, _ = self.socket.accept()      # 连接成功，返回客户端信息
            client_thread = threading.Thread(
                target=self.handle, args=(client_socket,)    # 线程设置
            )
            client_thread.start()



    # handle()方法
    def handle(self, client_socket):
        """
        实现 上传文件、执行命令、创建交互式命令行
        :param client_socket:
        :return:
        """
        pass




