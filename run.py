#!/usr/bin/env python3
"""
AI聊天助手启动脚本
"""

import os
import sys
from app import create_app, init_database


def main():
    """主函数"""
    print("=" * 50)
    print("🤖 AI聊天助手启动中...")
    print("=" * 50)

    # 检查环境变量
    required_env_vars = ["DEEPSEEK_API_KEY", "DATABASE_URL"]
    missing_vars = []

    for var in required_env_vars:
        if not os.environ.get(var):
            missing_vars.append(var)

    if missing_vars:
        print("❌ 缺少必要的环境变量:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n请检查 .env 文件配置或设置环境变量")
        print("参考 env_example.txt 文件进行配置")
        sys.exit(1)

    try:
        # 创建应用
        app = create_app()

        # 初始化数据库
        print("📊 初始化数据库...")
        init_database()

        # 启动应用
        print("🚀 启动Web服务器...")
        print("📍 访问地址: http://localhost:5000")
        print("📝 会话记录: http://localhost:5000/conversations")
        print("=" * 50)

        app.run(host="0.0.0.0", port=5000, debug=True)

    except Exception as e:
        print(f"❌ 启动失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
