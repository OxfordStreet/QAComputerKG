import os
import ahocorasick
'''问题分类模块'''

class QuestionClassifier:  # 问题分类
    def __init__(self):
        self.concept_path = os.path.join('dict/concept.txt')
        self.subject_path = os.path.join('dict/disease.txt')  # 知识点词典路径
        self.chapter_path = os.path.join('dict/chapter.txt')
        self.priority_path = os.path.join('dict/priority.txt')
        self.subclass_path = os.path.join('dict/subclass.txt')

        self.concept_wds= [i.strip() for i in open(self.concept_path,encoding="utf-8") if i.strip()]  # 剥离字符串中的space字符或者换行符，if用于判断当前行剥离空白内容之后不为空则for循环继续读取文件内容
        self.subject_wds= [i.strip() for i in open(self.subject_path,encoding="utf-8") if i.strip()] 
        self.chapter_wds= [i.strip() for i in open(self.chapter_path,encoding="utf-8") if i.strip()] 
        self.priority_wds= [i.strip() for i in open(self.priority_path,encoding="utf-8") if i.strip()] 
        self.subclass_wds= [i.strip() for i in open(self.subclass_path,encoding="utf-8") if i.strip()] 
        self.region_words = set(self.concept_wds + self.subject_wds + self.chapter_wds + self.priority_wds + self.subclass_wds)  # region_words用于存储所有实体特征词的集合，用户输入的语句在region_words中进行匹配

        self.region_tree = self.build_actree(list(self.region_words))        # 构造领域 actree 加速匹配
        self.wdtype_dict = self.build_wdtype_dict()                          # 构建由特征词和对应类型列表组成的字典

        # 问句疑问词
        self.importance_qwds = ['程度','重要']
        # 。。。。。。

        print('model init finished ......')

        return



    '''分类主函数'''
    def classify(self, question):
        data = {}
        entity_dict = self.check_entity(question)  # entity_dict 来自 medical_dict， check_entity 来自 check_medical
        if not entity_dict:
            return {}
        data['args'] = entity_dict
        # 收集问句中涉及的实体类型
        types = []
        for type_ in entity_dict.values():
            types += type_
        question_type = 'others'   # 如果一下的if语句没有成功匹配问题，那么问题分类就保持为 others

        question_types = []

        # 知识点重要程度
        if self.check_words(self.importance_qwds, question) and 'concept' in types:
            question_type = 'concept_importance'
            question_types.append(question_type)


        data['question_types'] = question_types

        return data




    '''构造特征词词对应的类型，存储到字典 wd_dict 中'''
    def build_wdtype_dict(self):
        wd_dict = dict()
        for wd in self.region_words:
            wd_dict[wd] = []
            if wd in self.concept_wds:
                wd_dict[wd].append('concept')
            if wd in self.subject_wds:
                wd_dict[wd].append('subject')
            if wd in self.chapter_wds():
                wd_dict[wd].append('chapter')
            if wd in self.priority_wds():
                wd_dict[wd].append('priority')
            if wd in self.subclass_wds():
                wd_dict[wd].append('subclass')
        return wd_dict
    
    
    '''构造actree，加速过滤'''
    '''没搞懂这里在干嘛，返回的actree只有 kind: 2 store: 30 , 但是后面的代码确实用到了'''
    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):  # enumrate() 将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，同时列出数据和数据下标
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    '''问句过滤'''
    def check_entity(self, question):              
        region_wds = []
        for i in self.region_tree.iter(question):   
            wd = i[1][1]
            region_wds.append(wd)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        final_wds = [i for i in region_wds if i not in stop_wds]
        final_dict = {i:self.wdtype_dict.get(i) for i in final_wds}

        return final_dict
        
    '''检查疑问词是否在问句中'''
    def check_words(self, wds, sent):   # 检查疑问词是否在问句中
        for wd in wds:
            if wd in sent:              # 如果问题疑问词在问句中，返回 True
                return True
        return False

    

if __name__ == '__main__':
    handler = QuestionClassifier()
    while 1:
        question = input('input an question:')
        data = handler.classify(question)
        print(data)