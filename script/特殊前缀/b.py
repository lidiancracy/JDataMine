import javalang
import os
import chardet

# 递归遍历文件夹下所有的Java源代码文件
def traverse_dir(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.java'):
                yield os.path.join(root, file)

# 解析Java源代码文件并统计方法名
def count_methods(file_path):
    with open(file_path, 'rb') as f:
        encoding = chardet.detect(f.read())['encoding']
    with open(file_path, 'r', encoding=encoding) as f:
        try:
            tree = javalang.parse.parse(f.read())
            for _, node in tree:
                if isinstance(node, javalang.tree.MethodDeclaration):
                    yield node.name
        except Exception:
            # Java语法错误不统计
            pass

# 统计目录下所有Java源代码文件的方法名
def count_methods_in_dir(path):
    methods = set()
    for file_path in traverse_dir(path):
        for method_name in count_methods(file_path):
            methods.add(method_name)
    return methods

# 统计目录下所有Java源代码文件的方法名数量并输出方法名
def count_and_print_methods_in_dir(path):
    methods = set()
    get_methods = set()
    set_methods = set()
    is_methods = set()
    for file_path in traverse_dir(path):
        for method_name in count_methods(file_path):
            methods.add(method_name)
            if method_name.lower().startswith('get'):
                get_methods.add(method_name)
            elif method_name.lower().startswith('set'):
                set_methods.add(method_name)
            elif method_name.lower().startswith('is'):
                is_methods.add(method_name)
    print(f"Total number of method names: {len(methods)}")
    print(f"Number of method names starting with 'get': {len(get_methods)}")
    print(f"Number of method names starting with 'set': {len(set_methods)}")
    print(f"Number of method names starting with 'is': {len(is_methods)}")

if __name__ == '__main__':
    import sys
    path = sys.argv[1]
    count_and_print_methods_in_dir(path)
