from vector_stores import VectorStoreService
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import ChatOllama
import config_data as config
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from chat_history_store import get_history


class RagService(object):
    def __init__(self):
        self.vector_service = VectorStoreService(
            embedding=OllamaEmbeddings(model=config.embedding_model_name)
        )

        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", "以我提供的已知参考资料为主。"
                 "简洁和专业的回答用户问题。参考资料:{context}。"),
                ("system", "并且我提供用户的对话历史记录，如下:"),
                MessagesPlaceholder("history"),
                ("user", "请回答用户提问: {input}")
            ]
        )

        self.chat_model = ChatOllama(model=config.chat_model_name)
        self.chain = self.__get_chain()

    @staticmethod
    def print_prompt(prompt):
        print("=" * 20)
        print(prompt.to_string())
        print("=" * 20)
        return prompt

    def __get_chain(self):
        """获取最终的执行链"""
        retriever = self.vector_service.get_retriever()

        def format_document(docs: list):
            if not docs:
                return "无相关参考资料"

            formatted_str = ""
            for doc in docs:
                formatted_str += f"文档片段: {doc.page_content}\n文档元数据: {doc.metadata}\n\n"

            return formatted_str

        def format_for_retriever(value: dict) -> str:
            return value["input"]

        chain = (
            {
                "input": RunnableLambda(lambda x: x["input"]),
                "context": RunnableLambda(format_for_retriever) | retriever | format_document,
                "history": RunnableLambda(lambda x: x["history"])
            } | self.prompt_template | self.print_prompt | self.chat_model | StrOutputParser()
        )

        conversation_chain = RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key="input",
            history_messages_key="history",
        )

        return conversation_chain


if __name__ == '__main__':
    rag = RagService()
    response = rag.chain.invoke({"input": "酒店的设施 "}, config={"configurable": {"session_id": "test_session_001"}})
    print(response)
 