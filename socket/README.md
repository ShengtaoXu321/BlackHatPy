# Python 网络编程

## 简介

Python的网络编程，都离不开`socket`模块

## TCP

### TCP客户端

TCP客户端常可用来：测试服务、发送垃圾数据、进行Fuzz

```python
# 导入socket包
import socket

# 配置目标服务器主机和端口号
target_host="www.google.com"
target_port="80"

# 创建一个socket对象
cli = socket.socket(socket.AF_INET, sockrt.SOCK_STREAM)  # AF.INET代表IPV4，SOCK_STREAM代表TCP，流

# 连接服务器
cli.connect(target_host,target_port)

# 发送函数
cli.send(b"GET / HTTP/1.1\r\nHOST: google.com\r\n\r\n")

# 接收函数
resp = cli.recv(4096)   # 4096为设置的接收的最大

print(resp.decode)     # 不解码将会以其他进制方式展示

# 关闭客户端
cli.close()
```

### TCP服务端

TCP服务端常可用来：远程代码执行工具、代理工具

```python
import socket
import threading   # 多线层模块

IP='0.0.0.0'   # 全开
PORT='9998'

def main():
  # 创建一个socket对象
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  # 绑定IP和端口
  s.bind(IP, PORT)
  # 开始监听
  s.listen(5)
  print(f'[*]Listening on {IP}:{PORT}')
  
  # 循环等待连接并处理
  while True:
    # 当成功建立连接
    cli, addr = s.accept()  # cli保存及诶收到客户端的socket对象，addr接收远程连接的详细信息
    print(f'[*]Accepted connection from {addr[0]}:{addr[1]}')
    # 创建一个新的线程，指向handle_client函数，并传入cli参数
    cli_handler = threading.Thread(target=handle_cli, args=(cli,))  # handle_cli为自己写的函数
    # 启动线程处理刚才收到的请求
    cli.handler.start()
    
def handle_cli(cli_socket):
  """
  处理函数，调用recv()
  """ 
  with cli_socket as sock:
    request = sock.recv(1024)
    print(f'[*]Received: {request.decode("utf-8")}')
    sock.send(b'ACK')
    
# main，仅在本节次执行
if __name__ = '__main__':
  main()
    
```

