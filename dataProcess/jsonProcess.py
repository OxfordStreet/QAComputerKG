import os
import json


'''对层次化的json数据进行处理，使其对象成为以行为单位的结构化数据'''

def jsonToObjectLines():
    with open("data\JSONfromHTML1.json", encoding="utf-8") as fin:
        lines = '\n'.join(fin).split('},')
        print("划分完毕")

    with open("data\JSONfromHTML3.json","w+",encoding="utf-8") as fout:
        fout.write('}\n{'.join(lines))
        print("导入完毕")

    fin.close()
    fout.close()
    return


'''在线工具https://www.aconvert.com/cn/document/csv-to-json/
将csv数据转化为json数据后，这里我们再将json数据其中的对象变成以行为单位的结构化数据'''

def jsonFromCsv():
    with open("data\clangfromcsv.json", encoding="utf-8") as fin:
        lines = ''.join(fin).split("\n,")

    with open("data\clangfromcsv1.json", "w+", encoding="utf-8") as fout:
        fout.write(''.join(lines))
        print("逗号去除，空行消除完毕\n")
    
    fin.close()
    fout.close()
    return


'''将json数据中subclass字段的数组value值进行分析，如果长度冗余则删除'''

def simplifyList():
    entity_json_path=os.path.join("data\clangfromcsv1.json")
    with open("data\clangfromcsv2.json","w+",encoding='utf-8') as f:
        for data_json in open(entity_json_path, encoding='utf-8'):
            data_dic = json.loads(data_json)
            List = data_dic['subclass']
            for i,subclass in enumerate(List):
                if subclass == '':
                    del List[i:len(List)]
                    break
            # 将修剪后的 List 添加到字典 data_dic 的 subclass 字段，最后由 json.dumps() 函数 字典结果转换为 json 类型
            # data_dic['subclass'] = List
            data_json = json.dumps(data_dic,ensure_ascii = False)
            print(data_json)
            f.write(data_json+'\n')
    return




if __name__ == '__main__':
    # jsonToObjectLines()  # json层次化数据用行来组织，处理 JSONfromHTML.json
    # jsonFromCsv()  # 将由 csv 在线转化而来的 json 数据处理为一行一对象的形式，去除空格和逗号
    simplifyList()  # 解决数组长度冗余的情况
