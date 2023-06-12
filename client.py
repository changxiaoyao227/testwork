import socket
import subprocess 
import json
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, True)
#client.ioctl(socket.SIO_KEEPALIVE_VALS, (1, 60 * 1000, 30 * 1000))
con = 1
while con != 0 :
    con = client.connect_ex(('localhost',6969))
print('[already connected]')
while True:
    s = client.recv(1024).decode("utf-8")
    if s == "task":
        with open("re_task.py","w") as out_file:
            while True:
                data = client.recv(1024).decode("utf-8")
                print(f"{data }")
                if "EOF" in data:
                    data = data.replace("EOF","")
                    out_file.write(data)  # Write data to a file
                    print("[recived task file over]")
                    client.send("ACK".encode("utf-8"))
                    break
                out_file.write(data)  # Write data to a file
    if s == "data":
        with open("re_data.txt","w") as out_file:
            while True:
                data = client.recv(1024).decode("utf-8")
                if "EOF" in data:
                    data = data.replace("EOF","")
                    if len(data) == 0:
                        print("[recived data file over]")
                        break
                    #result = json.loads(result)
                    for line in data:
                        out_file.write(line)  # Write data to a file
                    break
                else:
                        for line in data:
                            out_file.write(line)  # Write data to a file
            print(f"{data}")
        res = subprocess.run(['python','re_task.py'],stdout=subprocess.PIPE)
        res = int(res.stdout)
        print(type(res))
        res = str(res)
        print(res)
        print(type(res))
        client.send(res.encode("utf-8"))
