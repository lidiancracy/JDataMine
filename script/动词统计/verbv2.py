import os
import sys
import javalang
import chardet
import nltk
from nltk.corpus import wordnet as wn
import matplotlib.pyplot as plt
import matplotlib
# 设置为你需要的递归深度
sys.setrecursionlimit(1000000)

matplotlib.use('agg')

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

# 获取命令行参数
if len(sys.argv) != 3:
    print("Usage: python your_script.py folder_path filename")
    sys.exit(1)
folder_path = sys.argv[1]
filename = sys.argv[2]

# 初始化动词方法名计数器和非动词方法名计数器
verb_method_count = 0
non_verb_method_count = 0

# 遍历文件夹下所有.java文件
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
                tree = javalang.parse.parse(java_code)
            except Exception:
                print(f"文件 {file_path} 的语法有误，跳过该文件")
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
                    if has_verb:
                        verb_method_count += 1
                    else:
                        non_verb_method_count += 1
                    print(f"方法名: {method_name}, 是否包含动词: {has_verb}")

# 创建文件夹
if not os.path.exists("pic"):
    os.mkdir("pic")

# 绘制饼图
labels = ['verb method', 'no verb method']
sizes = [verb_method_count, non_verb_method_count]
fig, ax = plt.subplots()
patches, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)

# 添加具体数量标注到图例中
for i in range(len(sizes)):
    labels[i] += f" ({sizes[i]})"
ax.legend(patches, labels, loc="best")

# 保存饼图到文件
if not os.path.exists("pic"):
    os.mkdir("pic")
plt.savefig(f"pic/{filename}.png")


# # 定义标签和比例列表
# labels = ['verb method', 'no verb method']
# sizes = [verb_method_count, non_verb_method_count]

# # 绘制饼图
# fig1, ax1 = plt.subplots()
# patches, texts, autotexts = ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)

# # 设置饼图样式
# for text in texts:
#     text.set_fontsize(14)
# for autotext in autotexts:
#     autotext.set_fontsize(14)

# plt.axis('equal')

# # 设置图片保存路径和文件名
# pic_folder = 'pic'
# pic_path = os.path.join(pic_folder, f"{filename}.png")

# # 保存图片
# plt.savefig(pic_path)

# # 展示图片
# plt.show()


