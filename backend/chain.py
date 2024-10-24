from langchain_core.prompts.prompt import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage
from util.utils import video_frame_to_base64



class Chain:
    def __init__(self, model_name="phi3", ollama_host="http://localhost:11434"):
        self.__prompt = PromptTemplate.from_template("""
        你是AI助手

        Human: {human_input}
        AI: 
        """)
        self.__model_name = model_name
        self.__ollama_host = ollama_host
        self.__chain = self.__create_chain()
        self.model = ChatOpenAI(model="gpt-4")

    def __create_chain(self):
        model = ChatOpenAI(model="gpt-4")
        return self.__prompt | model | StrOutputParser()

    def set_model(self, model_name: str):
        self.__model_name = model_name
        self.__chain = self.__create_chain()

    def set_ollama_host(self, ollama_host: str):
        self.__ollama_host = ollama_host
        self.__chain = self.__create_chain()

    def get_chain(self):
        return self.__chain

    def get_img_chain(self,content: str,img_path = None):

        if img_path is None :
            return self.__chain.stream({"human_input": content})
        img_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                    # 角色
                    你是一个精准的意图判断高手，能够在模拟视频通话中，根据用户问题迅速判断是否需要用户提供视频图片来回答问题。
                    ## 技能
                    ### 技能 1：判断需求
                    1. 仔细分析用户提出的问题，判断该问题是否与用户自身信息跟环境问题关且需要视频图片才能更好地回答。如果需要回复“1”；如果不需要，回复“2”。
                    2.如果问的是别人或者你的问题,一律回复2
                    ##返回示例
                    返回示例
                    1
                    返回示例
                    2
                    """,
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
        message = HumanMessage(
            content=[
                {"type": "text", "text": content},

            ]
        )
        print("chain start 1")
        try:
            img_chain = img_prompt | ChatOpenAI(model="gpt-4") | StrOutputParser()
            type  = img_chain.invoke({"messages": [message]})
        except Exception as e:
            print("chain start erre",e)
        print("type",type)
        print("chain start 2")
        if type == "1" and img_path:

            gener_prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        """
                         你是AI助手
                         根据上传的图片判断用户问题.
                         图片当做是用户自己的
                        """,
                    ),
                    MessagesPlaceholder(variable_name="messages"),
                ]
            )

            ger_chain = gener_prompt | ChatOpenAI(model="gpt-4o") | StrOutputParser()
            message = HumanMessage(
                content=[
                    {"type": "text", "text": content},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{video_frame_to_base64(img_path)}"},
                    },
                ]
            )
            return ger_chain.invoke({"messages": [message]})
        else:
            return self.__chain.stream({"human_input": content})


