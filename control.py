import socket
import threading
import time
import json
lock = threading.Lock()
lock_rev = threading.Lock()
num = 0
num_rev = 0
task_filename = ""
data_filename = ""
lines = 0
re = []
def send_file(socket,addr,start,end):
    global num_rev,re
    print(f"[Got connection from {addr}]")
    socket.send("task".encode("utf-8"))
    with open(task_filename, "r") as in_file:
        data = in_file.read(1024)
        while data:
            socket.send(data.encode("utf-8"))
            #print(f"Sent {data!r}")
            data = in_file.read(1024)
        socket.send("EOF".encode("utf-8"))
    s = socket.recv(1024).decode("utf-8")
    print('[Done sending task file!]')
    if s == 'ACK':
        lock_rev.acquire()
        num_rev = num_rev + 1
        lock_rev.release()
        print('[client received task file!]')
    while num_rev != 3 :
        #print("[this is not already for data]")
        continue
    #现在所有的客户端都受到了任务。
    #time.sleep(2)#等所有的客户端线程都开启，并且传输完文件，这样做不太好，用客户端返回是否接受完，再计数，比较num和传输完的线程是否一样吧。
    #print('[start sending data file: its No.'+str(no)+' file, server will send part of all data]')
    socket.send("data".encode("utf-8"))
    with open(data_filename,"r") as in_file:
        print(start,end)
        result = in_file.readlines()[start:end]
        for i in result:
            socket.send(i.encode("utf-8"))
        #print(f"Sent {result!r}")
    socket.send("EOF".encode("utf-8"))
    print('[Done sending data file!]')
    t = socket.recv(1024).decode("utf-8") 
    re.append(t)
    print(re)
    return
'''
    temp = max(re)
    if(len(re) == 3): 
        print("max = "+str(temp))
'''



if __name__ == '__main__':
    server = socket.socket()
    server.bind(('localhost',6969))
    server.listen(20)  #假定最多20个计算节点
    print('[waiting for connect]')
    #task_filename =  input('input taskfilename (with all word):') #在控制端选择计算任务和计算数据集。
    #data_filename =  input('input datafilename(with all word):') #在控制端选择计算任务和计算数据集。
    task_filename = "task1.py"
    data_filename = "data1.txt"
    with open(data_filename, "r") as file:
        lines = len(file.readlines())
    while True:
        client_socket, client_address = server.accept()
        lock.acquire()
        start, end = lines//3*num,lines//3*(num+1)
        thread = threading.Thread(target=send_file,args=(client_socket,client_address,start,end))
        thread.start()
        num = num+1
        lock.release()
        if len(re)==3:
            temp = max(re)
            thread.join()
    print("result"+re)