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

    # Opik配置
    OPIK_API_KEY = os.environ.get("OPIK_API_KEY")
    OPIK_PROJECT_NAME = os.environ.get("OPIK_PROJECT_NAME") or "flask-chat-app"
    OPIK_WORKSPACE = os.environ.get("OPIK_WORKSPACE")

    # 如果设置了Opik API密钥但没有设置工作空间，尝试从API密钥推断
    if OPIK_API_KEY and not OPIK_WORKSPACE:
        # 提示用户需要设置工作空间
        print("⚠️  请设置OPIK_WORKSPACE环境变量")
        print(
            "   从 https://comet.com/opik/your-workspace-name/get-started 获取正确的工作空间名称"
        )
