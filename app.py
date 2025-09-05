from flask import Flask, render_template, request, redirect, url_for
from flask_cors import CORS
from models import db
from routes import api_bp
from config import Config
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def create_app():
    """创建Flask应用"""
    app = Flask(__name__)

    # 加载配置
    app.config.from_object(Config)

    # 启用CORS
    CORS(app)

    # 初始化数据库
    db.init_app(app)

    # 注册蓝图
    app.register_blueprint(api_bp)

    # 主页路由 - 聊天页面
    @app.route("/")
    def index():
        conversation_id = request.args.get("conversation")
        return render_template("chat.html", conversation_id=conversation_id)

    # 会话记录页面
    @app.route("/conversations")
    def conversations():
        return render_template("conversations.html")

    # 健康检查
    @app.route("/health")
    def health():
        return {"status": "healthy", "message": "AI聊天助手运行正常"}

    # 错误处理
    @app.errorhandler(404)
    def not_found(error):
        return render_template("chat.html"), 404

    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"服务器内部错误: {error}")
        return {"error": "服务器内部错误"}, 500

    return app


def init_database():
    """初始化数据库"""
    try:
        with app.app_context():
            db.create_all()
            logger.info("数据库初始化成功")
    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")
        raise


if __name__ == "__main__":
    app = create_app()

    # 初始化数据库
    init_database()

    # 启动应用
    logger.info("启动AI聊天助手...")
    app.run(host="0.0.0.0", port=5000, debug=True)
