import os
import json
from py2neo import Graph, Node


class ComputerGraph:
    def __init__(self):
        self.data_path = os.path.join('data/clangfromcsv2.json')
        self.g = Graph("http://localhost:7474", username="neo4j", password="@")
        self.g.delete_all()

    def read_nodes(self):
        concepts = []
        subjects = []
        chapters = []
        priorities = []
        subclasses = []

        rel_subject = []
        rel_chapter = []
        rel_priority = []
        rel_subclass = []

        concept_infos = []  # 用于收集 data_dict 字典：使用 append() 添加至列表末尾

        count = 0
        for data in open(self.data_path, encoding='utf-8'):
            # concept_dict = {}  # 这个字典不需要，通过loads之后的json数据中的字段都是我们感兴趣的，不要再额外定义
            count += 1
            print(count)
            data_dict = json.loads(data)  # 这里的 data_dict 相当于医疗里的 disease_dict{}，里面的内容都是我们需要的
            concept = data_dict['name']  # 这里 name 字段的列表使用 concept 单独列出，为的是方便和其他实体建立联系
            concepts.append(data_dict['name'])
            subjects.append(data_dict['subject'])
            chapters.append(data_dict['chapter'])
            priorities.append(data_dict['priority'])
            subclasses += data_dict['subclass']

            rel_chapter.append([concept, data_dict['chapter']])
            rel_priority.append([concept, data_dict['priority']])
            rel_subject.append([concept, data_dict['subject']])
            for subclass in data_dict['subclass']:
                rel_subclass.append([concept, subclass])

            concept_infos.append(data_dict)
            
        return concepts, set(subjects), set(chapters), set(priorities), set(subclasses), \
                concept_infos, rel_subject, rel_chapter, rel_priority, rel_subclass

    '''建立节点'''
    def create_node(self, label, nodes):
        count = 0  # 统计相关节点个数，可能的方面有 drug，food，check，department，
        for node_name in nodes:
            node = Node(label, name=node_name)
            self.g.create(node)
            count += 1
            print(count, len(nodes))  # len(nodes)从一开始就已经固定不会随着程序运行而改变，比如 drug 的 nodes 长度 len() 从一开始就是 88
        return

    '''创建以概念为中心的知识图谱结点'''
    def create_concepts_nodes(self, Concept_infos):
        count = 0
        for data_dict in Concept_infos:
            node = Node("All_about_concept", name=data_dict['name'], subject=data_dict['subject'],\
            dedc=data_dict['desc'] , chapter=data_dict['chapter'], pripority=data_dict['priority'],\
            subclass=data_dict['subclass'])  # 这是一个标签为 "概念" 节点，尽管有这么多参数，但是都是这个实体结点的属性
            self.g.create(node)
            count += 1
            print(count)
        return

    def create_graphnodes(self):
        Concepts,Subjects,Chapters,Priorities,Subclasses,Concept_infos,Rels_subject,Rels_chapter,Rels_pripority,Rels_subclass = self.read_nodes()
        self.create_concepts_nodes(Concept_infos)
        self.create_node('Concept', Concepts)  #         self.create_node('概念', Concepts) 要注意标签的命名，在建立结点间关系的时候会按此匹配
        print(len(Concepts))
        self.create_node('Subject', Subjects)
        print(len(Subjects))
        self.create_node('Chapter', Chapters)
        print(len(Chapters))
        self.create_node('Priority', Priorities)
        print(len(Priorities))
        self.create_node('Subclass', Subclasses)
        print(len(Subclasses))
        return

    '''创建实体关系边'''
    def create_graphrels(self):
        Concepts,Subjects,Chapters,Priorities,Subclasses,Concept_infos,Rels_subject,Rels_chapter,Rels_priority,Rels_subclass = self.read_nodes()
        self.create_relationship('Concept', 'Subject', Rels_subject, 'belong_to', '从属科目')
        self.create_relationship('Concept', 'Chapter', Rels_chapter, 'part_of', '从属章节')
        self.create_relationship('Concept', 'Priority', Rels_priority, 'importance', '重要程度')
        self.create_relationship('Concept', 'Subclass', Rels_subclass, 'sub_concept', '子概念')


    '''创建实体关联边'''
    def create_relationship(self, start_node, end_node, edges, rel_type, rel_name):
        count = 0
        # 去重处理
        set_edges = []  # 
        for edge in edges:
            set_edges.append('###'.join(edge))
        all = len(set(set_edges))
        for edge in set(set_edges):
            edge = edge.split('###')
            p = edge[0]
            q = edge[1]
            # match 是按照节点的 label 去查找的，所以在在建立节点的时候就应该注意到这一点 76 行 
            query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (start_node, end_node, p, q, rel_type, rel_name)
            try:
                self.g.run(query)
                count += 1
                print(rel_type, count, all)
            except Exception as e:
                print(e)
        return

    '''导出数据，以供查询'''
    def export_data(self):
        Concepts,Subjects,Chapters,Priorities,Subclasses,Concept_infos,Rels_subject,Rels_chapter,Rels_priority,Rels_subclass = self.read_nodes()
        f_concept = open('concept.txt', 'w+', encoding='utf-8')
        f_subject = open('subjects.txt','w+', encoding='utf-8')
        f_chapter = open('chapter.txt','w+', encoding='utf-8')
        f_priority = open('priority.txt','w+', encoding='utf-8')
        f_subclass = open('subclass.txt','w+', encoding='utf-8')

        f_concept.write('\n'.join(list(Concepts)))
        f_subject.write('\n'.join(list(Subjects)))
        f_chapter.write('\n'.join(list(Chapters)))
        f_priority.write('\n'.join(list(Priorities)))
        f_subclass.write('\n'.join(list(Subclasses)))
 
        f_subclass.close()
        f_chapter.close()
        f_priority.close()
        f_subclass.close()

        return


if __name__ == '__main__':
    handler = ComputerGraph()
    # handler.export_data()
    handler.create_graphnodes()
    handler.create_graphrels()
