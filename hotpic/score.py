import os
import chardet
import javalang
import re
import nltk
import pandas as np
from nltk.corpus import wordnet as wn
import pandas as pd

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

                    # 计算分数
                    score = 0
                    if re.match(r'^[a-z]+([A-Z][a-z]+)*$', method_name):
                        score += 10
                    else:
                        score += 5
                    if has_verb:
                        score += 10
                    else:
                        score += 3
                    if has_docstring:
                        score += 10
                    else:
                        score += 8
                    if len(words) in [2, 3]:
                        score += 10
                    elif len(words) in [1, 4, 5]:
                        score += 6
                    else:
                        score += 2
                    # 存储分数和方法信息
                    method_info[method_name] = {'score': score/4, 'has_docstring': has_docstring}

                    # 输出方法信息
                    print(f"文件 {file_path} 中的方法 {method_name} 的分数为 {score/4}")
                    print(f"该方法是否有文档注释： {has_docstring}")
                

# 将方法信息存储到DataFrame中并按照分数排序
df = pd.DataFrame.from_dict(method_info, orient='index')
# df.sort_values(by=['score'], ascending=False, inplace=True)


                   

