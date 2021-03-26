import os
import csv

def getFromNameNum():
    pending_one_path = os.path.join('datacsv\Clang.csv')  # 待处理数据 1
    pending_two_path = os.path.join('datacsv\ClangRels.csv')  # 待处理数据 2
    obj_data_path = os.path.join('datacsv\ClangForJSON.csv')

    with open(pending_one_path, encoding="utf-8") as f1:
        reader1 = csv.reader(f1)
        nameList=([row[0] for row in reader1])

    with open(pending_two_path, encoding="utf-8") as f2:
        reader2 = csv.reader(f2)
        subclassList=[row[2] for row in reader2]

    with open(pending_two_path, encoding="utf-8") as f2:
        reader2 = csv.reader(f2)
        fromNameList=[row[0] for row in reader2]  # 不知道为什么，文件一定要打开两次才可以读取到第二个列值

    with open(pending_one_path, encoding="utf-8") as f1:
        reader1 = csv.reader(f1)
        objRow=[row for row in reader1]
        # print(objRow[3])

    for num1,name in enumerate(nameList):
        for num2,subclass in enumerate(subclassList):
            if name == subclass:
                objRow[num1].append(fromNameList[num2])
        print(objRow[num1])
        output = open(obj_data_path, 'a', newline='',encoding='utf-8')
        writer = csv.writer(output)
        writer.writerow(objRow[num1])
        # print("保存文件成功，处理结束")

    f1.close()
    f2.close()





if __name__=='__main__':
    getFromNameNum()
    # num = getFromNameNum()
    # subclassInto(num)