from question_classifier import *
from question_parser import *
from answer_search import *

'''将以上三个模块的所有内容导入到当前命名空间'''

class ChatBotGraph:
    def __init__(self):                         # __init__方法可以有多个参数，但是第一个参数必须是self，代表创建的类实例本身
        self.classifier = QuestionClassifier()  # 创建 问题分类 对象 classifier
        self.parser = QuestionParser()          # 创建 问题解析 对象 parser
        self.searcher = AnswerSearcher()        # 创建 问题查询 对象 searcher

    def chat_main(self, sent):                  # 在类中定义的函数不同于普通函数，其第一参数永远是类的本身实例变量 self，并且调用时不用传递该参数；sent 代表问题内容的传递参数
        answer = '没能理解您的问题，我数据量有限。。。能不能问的标准点'         # 对于无法处理的问题输出这句话
        res_classify = self.classifier.classify(sent)   # 返回问题分类结果
        if not res_classify:                            # 如果问题分类结果为空，输出 answer 
            return answer
        res_sql = self.parser.parser_main(res_classify) # 将 问题分类返回值 res_classfy 作为参数，通过类的属性对象 parser 调用 parser_main 函数返回语法分析结果
        final_answers = self.searcher.search_main(res_sql)  # 将 语法分析返回值 res_sql 作为参数，通过类的属性对象 searcher 调用 searcher_main 函数返回问题查询结果
        if not final_answers:                               # 如果最终结果为空，输出 answer
            return answer
        else:
            return '\n'.join(final_answers)                 # 结果不为空，换行输出最终答案


if __name__ == '__main__':
    handler = ChatBotGraph()                        # 创建聊天机器人对象 handler
    while 1:
        question = input('咨询:')                   # 输入要查询的问题
        answer = handler.chat_main(question)        # 以 输入问题 queation 为参数，通过调用对象 handler 的 chat_main() 函数进行问题查询
        print('客服机器人:', answer)                 # 输出查询结果
