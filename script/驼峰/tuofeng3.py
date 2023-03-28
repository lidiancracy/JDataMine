import os
import chardet
from tqdm import tqdm
import javalang
import re
import matplotlib.pyplot as plt
import sys

sys.setrecursionlimit(1000000)

# 获取传入的参数
folder_path = sys.argv[1]
filename = sys.argv[2]

# 初始化异常文件数量
error_count = 0

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

                tree = javalang.parse.parse(java_code)
            except Exception:
                error_count += 1
                print(f"文件 {file_path} 的解析有误，跳过该文件")
                continue

            # 遍历语法树，提取方法名
            for path, node in tree:
                if isinstance(node, javalang.tree.MethodDeclaration):
                    method_name = node.name
                    method_names.append(method_name)

# 统计方法数量和驼峰式命名方法数量
method_count = len(method_names)
camel_case_method_count = 0

camel_case_pattern = r"^[a-z]+([A-Z][a-z]*)*$"
for method_name in tqdm(method_names, desc="正在分析方法"):
    if re.match(camel_case_pattern, method_name):
        camel_case_method_count += 1

# 计算驼峰式命名方法的占比
camel_case_method_ratio = camel_case_method_count / method_count

# 计算异常比例
error_ratio = error_count / (error_count + method_count)

# 画图并保存
if not os.path.exists(f'pic/{filename}'):
    os.mkdir(f'pic/{filename}')

# 驼峰式命名方法的占比饼图
labels = ["CamelCase Methods", "Other Methods"]
sizes = [camel_case_method_ratio, 1 - camel_case_method_ratio]
colors = ["lightblue", "lightgrey"]
fig, ax = plt.subplots()

count = sum(sizes)
wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', pctdistance=0.8, labeldistance=1.2, startangle=90)

# 添加具体数值
for i, autotext in enumerate(autotexts):
    autotext.set_text(f"{sizes[i]*100:.1f}%\n{sizes[i]*method_count:.0f}")

plt.savefig(f'pic/{filename}/CamelCaseMethods.png')

# 异常文件占比饼图
labels = ["Error Files", "Other Files"]
sizes = [error_ratio, 1 - error_ratio]
colors = ["lightcoral", "lightgrey"]
fig, ax = plt.subplots()
count = sum(sizes)
wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', pctdistance=0.8, labeldistance=1.2, startangle=90)

# 添加具体数值
for i, autotext in enumerate(autotexts):
    autotext.set_text(f"{sizes[i]*100:.1f}%\n{sizes[i]*(method_count+error_count):.0f}")

plt.savefig(f'pic/{filename}/ErrorFiles.png')

