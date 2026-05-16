"""
配置文件处理模块
用于加载项目中的各种YAML配置文件
"""

import os
import sys
import yaml

# 确保能找到同目录下的 path_tool（支持直接在 utils/ 目录下运行）
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from path_tool import get_abs_path


def load_rag_config(config_path: str = get_abs_path("config/rag.yml"), encoding: str = "utf-8"):
    """
    加载RAG（检索增强生成）相关配置

    Args:
        config_path: 配置文件路径，默认为 config/rag.yml
        encoding: 文件编码，默认 utf-8

    Returns:
        dict: RAG配置字典，包含分块、嵌入、检索等参数
    """
    with open(config_path, "r", encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def load_chroma_config(config_path: str = get_abs_path("config/chroma.yml"), encoding: str = "utf-8"):
    """
    加载Chroma向量数据库配置

    Args:
        config_path: 配置文件路径，默认为 config/chroma.yml
        encoding: 文件编码，默认 utf-8

    Returns:
        dict: Chroma配置字典，包含数据库路径、集合名称等参数
    """
    with open(config_path, "r", encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def load_prompts_config(config_path: str = get_abs_path("config/prompts.yml"), encoding: str = "utf-8"):
    """
    加载提示词模板配置

    Args:
        config_path: 配置文件路径，默认为 config/prompts.yml
        encoding: 文件编码，默认 utf-8

    Returns:
        dict: 提示词配置字典，包含系统提示词、用户提示词模板等
    """
    with open(config_path, "r", encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def load_agent_config(config_path: str = get_abs_path("config/agent.yml"), encoding: str = "utf-8"):
    """
    加载Agent智能体配置

    Args:
        config_path: 配置文件路径，默认为 config/agent.yml
        encoding: 文件编码，默认 utf-8

    Returns:
        dict: Agent配置字典，包含模型名称、工具列表、系统提示词等
    """
    with open(config_path, "r", encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


# 模块加载时自动读取各配置文件，供其他模块直接导入使用
rag_conf = load_rag_config()       # RAG检索增强配置
chroma_conf = load_chroma_config()  # Chroma向量数据库配置
prompts_conf = load_prompts_config() # 提示词模板配置
agent_conf = load_agent_config()     # Agent智能体配置

if __name__ == "__main__":
    print(rag_conf["chat_model_name"])