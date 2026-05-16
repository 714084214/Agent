"""
为整个工程提供绝对路径
"""

import os

"""
获取项目根目录
"""
def get_project_root():
    current_file = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file)
    project_root = os.path.dirname(current_dir)
    return project_root

def get_abs_path(relative_path:str) -> str:
    ptoject_root = get_project_root()
    return os.path.join(ptoject_root, relative_path)

if __name__ == "__main__":
    print(get_abs_path("path_tool.py"))