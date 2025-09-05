import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """应用配置类"""

    # 基础配置
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-change-in-production"

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL")
        or "postgresql://username:password@localhost:5432/chat_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # DeepSeek API配置
    DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")
    DEEPSEEK_BASE_URL = (
        os.environ.get("DEEPSEEK_BASE_URL") or "https://api.deepseek.com"
    )

    # 聊天配置
    MAX_MESSAGE_LENGTH = 2000
    MAX_CONVERSATION_MESSAGES = 100
