import os
import chardet
import javalang
import re
import nltk
import pandas as pd
from nltk.corpus import wordnet as wn

import sys
sys.setrecursionlimit(1000000) # 设置为你需要的递归深度


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
                        is_camel_case = True
                    else:
                        score += 5
                        is_camel_case = False
                    if has_verb:
                        score += 10
                        has_action_word = True
                    else:
                        score += 3
                        has_action_word = False
                    if has_docstring:
                        score += 10
                        has_docstring_str = "Yes"
                    else:
                        score += 8
                        has_docstring_str = "No"
                    if len(words) in [2, 3]:
                        score += 10
                    elif len(words) in [1, 4, 5]:
                        score += 7
                    elif len(words) in [6, 7, 8]:
                        score += 4
                    
                    # 判断方法名是否为驼峰式
                    if re.match(r'^[a-z]+([A-Z][a-z]+)*$', method_name):
                        is_camel_case = True
                    else:
                        is_camel_case = False
                    # 计算token数量
                    num_tokens = len(words)
                    # 输出方法信息
                    print(f"文件 {file_path} 中的方法 {method_name} 的分数为 {score/4}")
                    print(f"该方法是否有文档注释： {has_docstring}")
                    print(f"该方法是否包含动词： {has_verb}")
                    print(f"该方法是否为驼峰式： {is_camel_case}")
                    print(f"该方法的token数量为： {num_tokens}")


                                    # 存储分数和方法信息
                    method_info[method_name] = {'score': score/4, 
                                            'has_docstring': has_docstring,
                                            'has_verb': has_verb,
                                            'is_camel_case': is_camel_case,
                                            'num_tokens': num_tokens}




import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import string
import os

# create a dataframe with the method information
df = pd.DataFrame.from_dict(method_info, orient='index')

# add a column for the initial of the method name
df['initial'] = df.index.str[0]

# create a pivot table with the scores as values, initial as columns, and num_tokens as index
table = pd.pivot_table(df, values='score', index='num_tokens', columns='initial', aggfunc='mean')

# filter the table to only include rows with token numbers between 1 and 8
table = table.loc[1:8, :]

# create a list of the alphabet
alphabet = list(string.ascii_lowercase)

# reorder the columns of the table based on the alphabet
table = table.reindex(columns=alphabet)

# create the heatmap
sns.set()
fig, ax = plt.subplots(figsize=(16, 10))


# get the minimum and maximum score values from the table
score_min = table.min().min()
score_max = table.max().max()

# create the heatmap with the updated vmin and vmax parameters
sns.heatmap(table, cmap='coolwarm', annot=True, fmt='.2f', cbar_kws={'label': 'Score'}, ax=ax, linewidths=0, yticklabels=['1', '2', '3', '4', '5', '6', '7', '8'], vmin=score_min, vmax=score_max)


sns.set(rc={'axes.facecolor':'white', 'figure.facecolor':'white'})

ax.invert_yaxis()
ax.set_xlabel('First letter of method name')
ax.set_ylabel('Token Number')

# add colorbar
cbar = ax.collections[0].colorbar
cbar.ax.set_ylabel('Score', rotation=270, labelpad=15)

# create 'pic' folder if it doesn't exist
if not os.path.exists('./pic'):
    os.makedirs('./pic')

# save the figure in 'pic' folder
plt.savefig('./pic/heatmap.png')


# import seaborn as sns
# import matplotlib.pyplot as plt
# import pandas as pd
# import string
# import os

# # create a dataframe with the method information
# df = pd.DataFrame.from_dict(method_info, orient='index')

# # add a column for the initial of the method name
# df['initial'] = df.index.str[0]

# # create a pivot table with the scores as values, initial as columns, and num_tokens as index
# table = pd.pivot_table(df, values='score', index='num_tokens', columns='initial', aggfunc='mean')

# # create a list of the alphabet
# alphabet = list(string.ascii_lowercase)

# # reorder the columns of the table based on the alphabet
# table = table.reindex(columns=alphabet)

# # create the heatmap
# sns.set()
# fig, ax = plt.subplots(figsize=(16, 10))
# sns.heatmap(table, cmap='coolwarm', annot=True, fmt='.2f', cbar_kws={'label': 'Score'}, ax=ax, linewidths=0, yticklabels=['1', '2', '3', '4', '5', '6', '7', '8'])
# sns.set(rc={'axes.facecolor':'white', 'figure.facecolor':'white'})

# ax.invert_yaxis()
# ax.set_xlabel('First letter of method name')
# ax.set_ylabel('Token Number')

# # add colorbar
# cbar = ax.collections[0].colorbar
# cbar.ax.set_ylabel('Score', rotation=270, labelpad=15)

# # create 'pic' folder if it doesn't exist
# if not os.path.exists('./pic'):
#     os.makedirs('./pic')

# # save the figure in 'pic' folder
# plt.savefig('./pic/heatmap.png')
