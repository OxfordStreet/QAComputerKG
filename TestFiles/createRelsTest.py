import os
from py2neo import Graph, Node

class Test:
    def __init__(self):
        self.L1 = ['C语言','数组']
        self.g = Graph("http://localhost:7474", username="neo4j", password="@")
        self.g.delete_all()
    
    '''建立节点'''
    def create_node(self, label, nodes):
        for node_name in nodes:
            node = Node(label, name=node_name)
            self.g.create(node)
            print(len(nodes))  
        return


    def createRels(self, start_node, end_node, edges, rel_type, rel_name):
        count = 0
        p = edges[0]
        q = edges[1]
        query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (start_node, end_node, p, q, rel_type, rel_name)
        try:
            self.g.run(query)
            count += 1
            print(rel_type, count, all)
        except Exception as e:
            print(e)








if __name__ == '__main__':
    handler = Test()
    handler = createRels('Subject','内容',self.L1,'','')

   
    


