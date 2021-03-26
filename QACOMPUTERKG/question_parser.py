'''问题解析模块'''

class QuestionParser:  # 语法解析程序

    '''构建实体节点'''
    def build_entitydict(self, args):
        entity_dict = {}                    # 字典中类型是字段+列表： {'disease': ['肺气肿','百日咳']}
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)

        return entity_dict

    '''解析主函数'''
    def parser_main(self, res_classify):
        args = res_classify['args']
        entity_dict = self.build_entitydict(args)           # 创建实体字典
        question_types = res_classify['question_types']     # 
        sqls = []
        for question_type in question_types:
            sql_ = {}
            sql_['question_type'] = question_type
            sql = []
            








if __name__ == '__main__':
    handler = QuestionParser()