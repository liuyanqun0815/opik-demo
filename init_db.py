#!/usr/bin/env python3
"""
数据库初始化脚本
"""

import os
import sys
from app import create_app
from models import db


def init_database():
    """初始化数据库表"""
    app = create_app()

    with app.app_context():
        try:
            print("📊 正在创建数据库表...")
            db.create_all()
            print("✅ 数据库表创建成功!")

            # 显示创建的表
            from sqlalchemy import inspect

            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"📋 已创建的表: {', '.join(tables)}")

        except Exception as e:
            print(f"❌ 数据库初始化失败: {e}")
            sys.exit(1)


if __name__ == "__main__":
    init_database()
