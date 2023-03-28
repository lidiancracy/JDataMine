import os
import chardet
import javalang
import re
import nltk
import pandas as np
from nltk.corpus import wordnet as wn

def is_verb(word):
    # 将单词转换为小写形式
    word = word.lower()
    # 获取单词的同义词集
    synsets = wn.synsets(word)
    # 遍历同义词集
    for synset in synsets:
        # 如果同义词集的词性为动词
        if synset.pos() == 'v':
            return True
        # 如果同义词集的词性不为动词，但是包含输入单词的原形动词
        elif word in synset.lemma_names() and any(hasattr(lemma, 'pos') and lemma.pos() == 'v' for lemma in synset.lemmas()):
            return True
    return False

# 获取文件夹路径
folder_path = input("请输入文件夹路径：")

# 存储方法信息的字典
method_info = {}

# 递归查找文件夹下的所有Java文件，并提取方法名
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.endswith(".java"):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "rb") as f:
                    content = f.read()
                    encoding = chardet.detect(content)["encoding"]
                with open(file_path, "r", encoding=encoding) as f:
                    java_code = f.read()
                
                # 判断文件是否有文档注释
                if re.search(r'/\*\*(?:[^*]|\*(?!/))*\*/', java_code):
                    has_docstring = True
                else:
                    has_docstring = False


                # 使用javalang解析Java代码
                tree = javalang.parse.parse(java_code)
            except Exception:
                print(f"文件 {file_path} 解析有误，跳过该文件")
                continue

            # 遍历语法树，提取方法名
            for path, node in tree:
                if isinstance(node, javalang.tree.MethodDeclaration):
                    method_name = node.name
                    # 将方法名按照驼峰命名法拆分成单词
                    words = [word for word in nltk.tokenize.regexp_tokenize(method_name, pattern='[A-Z]?[a-z]+')]
                    has_verb = False
                    for word in words:
                        if is_verb(word):
                            has_verb = True
                            break
                    # 组装方法信息
                    method_data = {
                        "name": method_name,
                        "is_camel_case": True if re.match(r'^[a-z]+([A-Z][a-z]+)*$', method_name) else False,
                        "has_verb": has_verb,
                        "token_count": len(words),
                        "has_docstring": has_docstring,
                    }
                    # 将方法信息添加到字典中
                    first_char = method_name[0].upper()
                    if first_char not in method_info:
                        method_info[first_char] = []
                    method_info[first_char].append(method_data)



# 根据方法名首字母进行分组
grouped_method_info = {}
for key, value in method_info.items():
    grouped_value = {}
    for method_data in value:
        if method_data["name"][0] not in grouped_value:
            grouped_value[method_data["name"][0]] = []
        grouped_value[method_data["name"][0]].append(method_data)
    grouped_method_info[key] = grouped_value

# 输出分组后的信息
for key, value in grouped_method_info.items():
    print(f"首字母为 {key} 的方法信息如下：")
    for k, v in value.items():
        print(f"\t方法名首字母为 {k} 的方法数量为 {len(v)}，详细信息如下：")
        for method_data in v:
            print(f"\t\t方法名：{method_data['name']}")
            print(f"\t\t方法名是否符合驼峰命名法：{method_data['is_camel_case']}")
            print(f"\t\t方法名中是否包含动词：{method_data['has_verb']}")
            print(f"\t\t方法名中单词数量：{method_data['token_count']}")
            print(f"\t\t方法名中是否有注释：{method_data['has_docstring']}")
            print()



