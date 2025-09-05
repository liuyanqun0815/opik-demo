#!/usr/bin/env python3
"""
API测试脚本
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"


def test_health():
    """测试健康检查接口"""
    print("🔍 测试健康检查接口...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ 健康检查通过")
            return True
        else:
            print(f"❌ 健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 健康检查异常: {e}")
        return False


def test_conversations():
    """测试会话管理接口"""
    print("\n🔍 测试会话管理接口...")

    # 创建新会话
    print("  创建新会话...")
    try:
        response = requests.post(f"{BASE_URL}/api/conversations")
        if response.status_code == 200:
            data = response.json()
            if data["success"]:
                conversation_id = data["data"]["id"]
                print(f"  ✅ 会话创建成功，ID: {conversation_id}")
                return conversation_id
            else:
                print(f"  ❌ 会话创建失败: {data['message']}")
                return None
        else:
            print(f"  ❌ 会话创建失败: {response.status_code}")
            return None
    except Exception as e:
        print(f"  ❌ 会话创建异常: {e}")
        return None


def test_send_message(conversation_id):
    """测试发送消息接口"""
    print("\n🔍 测试发送消息接口...")

    if not conversation_id:
        print("  ❌ 没有有效的会话ID")
        return False

    try:
        message_data = {"message": "你好，请介绍一下你自己"}

        response = requests.post(
            f"{BASE_URL}/api/conversations/{conversation_id}/messages",
            json=message_data,
            headers={"Content-Type": "application/json"},
        )

        if response.status_code == 200:
            data = response.json()
            if data["success"]:
                print("  ✅ 消息发送成功")
                print(f"  📝 用户消息: {data['data']['user_message']['content']}")
                print(f"  🤖 AI回复: {data['data']['ai_message']['content'][:100]}...")
                return True
            else:
                print(f"  ❌ 消息发送失败: {data['message']}")
                return False
        else:
            print(f"  ❌ 消息发送失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ 消息发送异常: {e}")
        return False


def test_get_conversations():
    """测试获取会话列表接口"""
    print("\n🔍 测试获取会话列表接口...")

    try:
        response = requests.get(f"{BASE_URL}/api/conversations")
        if response.status_code == 200:
            data = response.json()
            if data["success"]:
                conversations = data["data"]
                print(f"  ✅ 获取会话列表成功，共 {len(conversations)} 个会话")
                for conv in conversations[:3]:  # 只显示前3个
                    print(f"    - {conv['title']} (ID: {conv['id']})")
                return True
            else:
                print(f"  ❌ 获取会话列表失败: {data['message']}")
                return False
        else:
            print(f"  ❌ 获取会话列表失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ 获取会话列表异常: {e}")
        return False


def main():
    """主测试函数"""
    print("=" * 60)
    print("🧪 AI聊天助手API测试")
    print("=" * 60)

    # 检查服务是否运行
    if not test_health():
        print("\n❌ 服务未运行，请先启动应用: python app.py")
        return

    # 测试会话管理
    conversation_id = test_conversations()

    # 测试发送消息
    if conversation_id:
        test_send_message(conversation_id)

    # 测试获取会话列表
    test_get_conversations()

    print("\n" + "=" * 60)
    print("🎉 API测试完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
