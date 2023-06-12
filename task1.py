res = []
if __name__ == "__main__":
    with open("re_data.txt","r")as in_file:
        f=in_file.readlines()
        for i in f:
            i.replace("\n"," ")
            res.append(int(i))
    print(max(res))