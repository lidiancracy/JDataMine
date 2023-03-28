import os
import chardet
from tqdm import tqdm
import javalang
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('agg')
import re

import sys
sys.setrecursionlimit(1000000) # 设置为你需要的递归深度

# 设置字体
plt.rcParams['font.family'] = 'Microsoft YaHei'

# 获取命令行参数
folder_path = sys.argv[1]
filename = sys.argv[2]

# 递归查找文件夹下的所有Java文件，并提取方法名
method_names = []
for root, dirs, files in os.walk(folder_path):
    for file in tqdm(files, desc="正在扫描文件夹"):
        if file.endswith(".java"):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "rb") as f:
                    content = f.read()
                    encoding = chardet.detect(content)["encoding"]
                with open(file_path, "r", encoding=encoding) as f:
                    java_code = f.read()

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
                    words = [word for word in re.split('([A-Z][a-z]*)', method_name) if word]
                    # 计算单词个数，并将单词个数加入到列表中
                    method_name_length = len(words)
                    method_names.append(method_name_length)

# 绘制柱状图
plt.hist(method_names, bins=range(1, 12), align='left', rwidth=0.8)
plt.xlabel('方法名中单词数量')
plt.ylabel('方法数量')
plt.xticks(range(1, 11))
for i in range(1, 11):
    count = method_names.count(i)
    plt.text(i-0.2 , count+0.3 , str(count), fontsize=10, color='black')

# 保存柱状图
if not os.path.exists("pic"):
    os.mkdir("pic")
pic_path = os.path.join("pic", filename + ".png")
plt.savefig(pic_path)
print(f"柱状图已保存至 {pic_path}")
