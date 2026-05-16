from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langgraph.runtime import Runtime
from langchain.agents import create_agent, AgentState


@tool(description="查询天气")
def get_weather(city: str) -> str:
    return "晴天"


"""
1. agent执行前
2. agent执行后
3. model执行前
4. model执行后
5. 工具执行中
6. 模型执行中
"""


def log_before_agent(state: AgentState, runtime: Runtime) -> None:
    print(f"[before agent]agent启动, 并附带{len(state['messages'])}消息")


def log_after_agent(state: AgentState, runtime: Runtime) -> None:
    print(f"[after agent]agent结束, 并附带{len(state['messages'])}消息")


def log_before_model(state: AgentState, runtime: Runtime) -> None:
    print(f"[before_model]模型即将调用, 并附带{len(state['messages'])}消息")


def log_after_model(state: AgentState, runtime: Runtime) -> None:
    print(f"[after_model]模型调用结束, 并附带{len(state['messages'])}消息")


def model_call_hook(request, handler):
    print("模型调用啦")
    return handler(request)


def monitor_tool(request, handler):
    print(f"工具执行: {request.tool_call['name']}")
    print(f"工具执行传入参数: {request.tool_call['args']}")
    return handler(request)

agent = create_agent(
    model=ChatOllama(model="qwen3:8b"),
    tools=[get_weather],
)

res = agent.invoke({"messages": [{"role": "user", "content": "今天天气如何呀，如何穿衣"}]})
print("*********\n", res)
