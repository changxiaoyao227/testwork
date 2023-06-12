import random
with open("data1.txt","w") as out_file:
    for i in range(600):
        out_file.write(str(random.randint(1,9999))+'\n')