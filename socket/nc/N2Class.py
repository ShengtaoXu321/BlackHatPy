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
        发送，更像client端
        :return:
        """
        # 如果缓冲区有数据，就直接发送；否则进行try处理
        self.socket.connect((self.args.target, self.args.port))    # 进行连接
        print(f'{self.args.target} : {self.args.port}  connecting.....')
        if self.buffer:
            self.socket.send(self.buffer)

        try:
            while True:    # 大循环，对数据进行接收，以4096为单位，小于直接接收；大于则以4096分段接收
                recv_len = 1
                response = ''
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode()
                    if recv_len < 4096:      # 退出循环的条件
                        break

                if response:     # 外循环，否则可能就执行不到这个了
                    print(response)
                    buffer = input(f'{self.args.target}@ $ > ')  # 输出完response内容，暂停等待用户的输入才继续
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
        print('listening......')
        self.socket.bind((self.args.target, self.args.port))    # 设置监听IP和端口
        self.socket.listen(5)  # 最大连接数为5

        while True:
            client_socket, _ = self.socket.accept()      # 连接成功，返回客户端信息
            print(f'{self.args.target} : {self.args.port}  connect well.....')
            # print(client_socket)
            client_thread = threading.Thread(
                target=self.handle, args=(client_socket,)  # 保证cleint_socket参数是一个元组
                # 线程设置，这里clinet_socket加,是因为向目标函数传递一个参数，但是只有一个参数，加,是必须的
             # 在 Python 中，当你想将单个值传递给函数，但该值又不是元组或列表时，需要在该值后面加上一个逗号来表示这是一个单元素的元组。
            )
            client_thread.start()



    # handle()方法
    def handle(self, client_socket):
        """
        实现 上传文件、执行命令、创建交互式命令行
        :param client_socket:
        :return:
        """
        # -e 参数：执行命令
        if self.args.execute:
            output = execute(self.args.execute)
            # self.socket.send(output.encode()) 为哈不是这个原因，这个是服务端调用send方法，主监听套接字，会发送给所有连接到服务器的客户端
            client_socket.send(output.encode()) # 这个服务端创建的新线程中调用send方法，将数据发送给特定的客户端，只对当前线程中客户端有效

        # -u 参数：文件上传
        elif self.args.upload:
            file_buffer = b''   # 文件传输接收buf
            while True:
                data = client_socket.recv(4096)   # 循环接收socket传来的内容
                if data:
                    file_buffer += data    # 接收到数据拼接放到buf里
                else:
                    break

            # 写接收到的数据到指定参数文件中
            with open(self.args.upload, 'wb') as f:     # self.args.upload参数文件名 -u text.txt
                f.write(file_buffer)
            message = f'Save file {self.args.upload}'
            client_socket.send(message.encode())


        # -c 参数：创建shell
        elif self.args.command:
            cmd_buffer = b''  # 存储发送的命令
            while True:
                try:
                    client_socket.send(b'# > ')    # 向发送方发送提示符：black hat python，等到其发回命令
                    while '\n' not in cmd_buffer.decode():
                        cmd_buffer += client_socket.recv(64)   # 客户端收到的内容拼接到buf中
                    response = execute(cmd_buffer.decode())    # 调用execute()函数
                    if response:
                        # print(response)   # 加上这个会返回打印数据
                        client_socket.send(response.encode())   # 向发送方发送执行命令后的输出内容
                        pass
                    cmd_buffer = b''     # 将 cmd_buffer 重置为空，准备接收下一个命令。
                except Exception as e:
                    print(f'Server Killded {e}')
                    self.socket.close()
                    sys.exit()





