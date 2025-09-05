from flask import Blueprint, request, jsonify
from models import db, Conversation, Message
from llm_service import DeepSeekService
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# 创建蓝图
api_bp = Blueprint("api", __name__, url_prefix="/api")

# 初始化DeepSeek服务
llm_service = DeepSeekService()


@api_bp.route("/conversations", methods=["GET"])
def get_conversations():
    """获取所有会话列表"""
    try:
        conversations = Conversation.query.order_by(
            Conversation.updated_at.desc()
        ).all()
        return jsonify(
            {"success": True, "data": [conv.to_dict() for conv in conversations]}
        )
    except Exception as e:
        logger.error(f"获取会话列表失败: {str(e)}")
        return (
            jsonify({"success": False, "message": f"获取会话列表失败: {str(e)}"}),
            500,
        )


@api_bp.route("/conversations", methods=["POST"])
def create_conversation():
    """创建新会话"""
    try:
        conversation = Conversation(title="新对话")
        db.session.add(conversation)
        db.session.commit()

        return jsonify({"success": True, "data": conversation.to_dict()})
    except Exception as e:
        logger.error(f"创建会话失败: {str(e)}")
        return jsonify({"success": False, "message": f"创建会话失败: {str(e)}"}), 500


@api_bp.route("/conversations/<int:conversation_id>", methods=["GET"])
def get_conversation(conversation_id):
    """获取指定会话的详细信息"""
    try:
        conversation = Conversation.query.get_or_404(conversation_id)
        messages = (
            Message.query.filter_by(conversation_id=conversation_id)
            .order_by(Message.created_at.asc())
            .all()
        )

        return jsonify(
            {
                "success": True,
                "data": {
                    "conversation": conversation.to_dict(),
                    "messages": [msg.to_dict() for msg in messages],
                },
            }
        )
    except Exception as e:
        logger.error(f"获取会话详情失败: {str(e)}")
        return (
            jsonify({"success": False, "message": f"获取会话详情失败: {str(e)}"}),
            500,
        )


@api_bp.route("/conversations/<int:conversation_id>", methods=["DELETE"])
def delete_conversation(conversation_id):
    """删除会话"""
    try:
        conversation = Conversation.query.get_or_404(conversation_id)
        db.session.delete(conversation)
        db.session.commit()

        return jsonify({"success": True, "message": "会话删除成功"})
    except Exception as e:
        logger.error(f"删除会话失败: {str(e)}")
        return jsonify({"success": False, "message": f"删除会话失败: {str(e)}"}), 500


@api_bp.route("/conversations/<int:conversation_id>/messages", methods=["POST"])
def send_message(conversation_id):
    """发送消息并获取AI回复"""
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()

        logger.info(f"API收到用户消息: {user_message}")
        logger.info(f"请求数据: {data}")

        if not user_message:
            return jsonify({"success": False, "message": "消息内容不能为空"}), 400

        # 获取会话
        conversation = Conversation.query.get_or_404(conversation_id)

        # 保存用户消息
        user_msg = Message(
            conversation_id=conversation_id, role="user", content=user_message
        )
        db.session.add(user_msg)

        # 如果是第一条消息，生成标题
        if len(conversation.messages) == 0:
            title = llm_service.generate_title(user_message)
            conversation.title = title

        # 更新会话时间
        conversation.updated_at = datetime.utcnow()

        # 获取对话历史
        history_messages = (
            Message.query.filter_by(conversation_id=conversation_id)
            .order_by(Message.created_at.asc())
            .all()
        )
        conversation_history = [msg.to_dict() for msg in history_messages]

        # 生成AI回复
        ai_response = llm_service.generate_response(user_message, conversation_history)

        # 保存AI回复
        ai_msg = Message(
            conversation_id=conversation_id, role="assistant", content=ai_response
        )
        db.session.add(ai_msg)

        db.session.commit()

        return jsonify(
            {
                "success": True,
                "data": {
                    "user_message": user_msg.to_dict(),
                    "ai_message": ai_msg.to_dict(),
                    "conversation": conversation.to_dict(),
                },
            }
        )

    except Exception as e:
        logger.error(f"发送消息失败: {str(e)}")
        db.session.rollback()
        return jsonify({"success": False, "message": f"发送消息失败: {str(e)}"}), 500


@api_bp.route("/conversations/<int:conversation_id>/messages", methods=["GET"])
def get_messages(conversation_id):
    """获取指定会话的所有消息"""
    try:
        conversation = Conversation.query.get_or_404(conversation_id)
        messages = (
            Message.query.filter_by(conversation_id=conversation_id)
            .order_by(Message.created_at.asc())
            .all()
        )

        return jsonify({"success": True, "data": [msg.to_dict() for msg in messages]})
    except Exception as e:
        logger.error(f"获取消息列表失败: {str(e)}")
        return (
            jsonify({"success": False, "message": f"获取消息列表失败: {str(e)}"}),
            500,
        )
