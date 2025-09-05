
from langchain_openai import ChatOpenAI

from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain.memory import ConversationBufferWindowMemory
from config import Config
import logging

logger = logging.getLogger(__name__)


class DeepSeekService:
    """DeepSeek大模型服务类"""

    def __init__(self):
        """初始化DeepSeek服务"""
        self.api_key = Config.DEEPSEEK_API_KEY
        self.base_url = Config.DEEPSEEK_BASE_URL

        if not self.api_key:
            raise ValueError("DEEPSEEK_API_KEY 环境变量未设置")

        # 初始化ChatOpenAI模型
        self.llm = ChatOpenAI(
            model="deepseek-chat",
            openai_api_key=self.api_key,
            openai_api_base=self.base_url,
            temperature=0.7,
            max_tokens=2000,
            streaming=True,
        )

        # 初始化记忆
        self.memory = ConversationBufferWindowMemory(
            k=10, return_messages=True  # 保留最近10轮对话
        )

    def generate_response(self, user_message, conversation_history=None):
        """
        生成AI回复

        Args:
            user_message (str): 用户消息
            conversation_history (list): 对话历史，格式为 [{"role": "user/assistant", "content": "..."}]

        Returns:
            str: AI回复内容
        """
        try:
            # 构建消息列表
            messages = []

            # 添加系统消息
            system_prompt = """你是一个有用的AI助手，请用中文回答用户的问题。回答要准确、有帮助，并且简洁明了。"""
            messages.append(SystemMessage(content=system_prompt))

            # 添加对话历史
            if conversation_history:
                for msg in conversation_history[-10:]:  # 只保留最近10轮对话
                    if msg["role"] == "user":
                        messages.append(HumanMessage(content=msg["content"]))
                    elif msg["role"] == "assistant":
                        messages.append(AIMessage(content=msg["content"]))

            # 添加当前用户消息
            messages.append(HumanMessage(content=user_message))

            # 生成回复
            response = self.llm(messages)

            return response.content

        except Exception as e:
            logger.error(f"生成AI回复时出错: {str(e)}")
            return f"抱歉，生成回复时出现错误：{str(e)}"

    def generate_title(self, first_message):
        """
        根据第一条消息生成对话标题

        Args:
            first_message (str): 第一条用户消息

        Returns:
            str: 生成的标题
        """
        try:
            title_prompt = f"""请为以下对话生成一个简洁的标题（不超过20个字符）：
            
用户消息：{first_message}

标题："""

            messages = [
                SystemMessage(
                    content="你是一个标题生成助手，请根据用户消息生成简洁的对话标题。"
                ),
                HumanMessage(content=title_prompt),
            ]

            response = self.llm(messages)
            title = response.content.strip()

            # 限制标题长度
            if len(title) > 20:
                title = title[:20] + "..."

            return title

        except Exception as e:
            logger.error(f"生成标题时出错: {str(e)}")
            return "新对话"
