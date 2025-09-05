// 聊天页面JavaScript
class ChatApp {
    constructor() {
        this.currentConversationId = null;
        this.isLoading = false;
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadConversations();
        this.setupMessageInput();
    }

    bindEvents() {
        // 新对话按钮
        document.getElementById('new-chat-btn').addEventListener('click', () => {
            this.createNewConversation();
        });

        // 发送按钮
        document.getElementById('send-btn').addEventListener('click', () => {
            this.sendMessage();
        });

        // 清空对话按钮
        document.getElementById('clear-chat-btn').addEventListener('click', () => {
            this.clearCurrentChat();
        });

        // 回车发送消息
        document.getElementById('message-input').addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
    }

    setupMessageInput() {
        const input = document.getElementById('message-input');
        const charCount = document.querySelector('.char-count');

        input.addEventListener('input', () => {
            const length = input.value.length;
            charCount.textContent = `${length}/2000`;

            // 自动调整高度
            input.style.height = 'auto';
            input.style.height = Math.min(input.scrollHeight, 120) + 'px';

            // 启用/禁用发送按钮
            const sendBtn = document.getElementById('send-btn');
            sendBtn.disabled = length === 0 || this.isLoading;
        });
    }

    async loadConversations() {
        try {
            const response = await fetch('/api/conversations');
            const data = await response.json();

            if (data.success) {
                this.renderConversations(data.data);
            } else {
                console.error('加载会话列表失败:', data.message);
            }
        } catch (error) {
            console.error('加载会话列表失败:', error);
        }
    }

    renderConversations(conversations) {
        const container = document.getElementById('conversations-list');
        container.innerHTML = '';

        conversations.forEach(conv => {
            const item = document.createElement('div');
            item.className = 'conversation-item';
            item.dataset.conversationId = conv.id;

            if (conv.id === this.currentConversationId) {
                item.classList.add('active');
            }

            item.innerHTML = `
                <div class="conversation-title">${conv.title}</div>
                <div class="conversation-time">${this.formatTime(conv.updated_at)}</div>
            `;

            item.addEventListener('click', () => {
                this.loadConversation(conv.id);
            });

            container.appendChild(item);
        });
    }

    async createNewConversation() {
        try {
            this.showLoading(true);

            const response = await fetch('/api/conversations', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            const data = await response.json();

            if (data.success) {
                this.currentConversationId = data.data.id;
                this.clearMessages();
                this.updateChatTitle(data.data.title);
                this.loadConversations();
            } else {
                alert('创建新对话失败: ' + data.message);
            }
        } catch (error) {
            console.error('创建新对话失败:', error);
            alert('创建新对话失败: ' + error.message);
        } finally {
            this.showLoading(false);
        }
    }

    async loadConversation(conversationId) {
        try {
            this.showLoading(true);

            const response = await fetch(`/api/conversations/${conversationId}`);
            const data = await response.json();

            if (data.success) {
                this.currentConversationId = conversationId;
                this.updateChatTitle(data.data.conversation.title);
                this.renderMessages(data.data.messages);
                this.updateActiveConversation(conversationId);
            } else {
                alert('加载对话失败: ' + data.message);
            }
        } catch (error) {
            console.error('加载对话失败:', error);
            alert('加载对话失败: ' + error.message);
        } finally {
            this.showLoading(false);
        }
    }

    async sendMessage() {
        const input = document.getElementById('message-input');
        const message = input.value.trim();

        if (!message || this.isLoading) return;

        // 如果没有当前对话，先创建一个
        if (!this.currentConversationId) {
            await this.createNewConversation();
            if (!this.currentConversationId) return;
        }

        try {
            this.isLoading = true;
            this.showLoading(true);

            // 添加用户消息到界面
            this.addMessage('user', message);
            input.value = '';
            input.style.height = 'auto';
            document.getElementById('send-btn').disabled = true;
            document.querySelector('.char-count').textContent = '0/2000';

            console.log('发送消息:', message);
            console.log('会话ID:', this.currentConversationId);

            const response = await fetch(`/api/conversations/${this.currentConversationId}/messages`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: message })
            });

            const data = await response.json();

            if (data.success) {
                // 更新对话标题
                this.updateChatTitle(data.data.conversation.title);

                // 添加AI回复到界面
                this.addMessage('assistant', data.data.ai_message.content);

                // 重新加载会话列表以更新标题
                this.loadConversations();
            } else {
                this.addMessage('assistant', '抱歉，发送消息失败: ' + data.message);
            }
        } catch (error) {
            console.error('发送消息失败:', error);
            this.addMessage('assistant', '抱歉，发送消息失败: ' + error.message);
        } finally {
            this.isLoading = false;
            this.showLoading(false);
            document.getElementById('send-btn').disabled = false;
        }
    }

    addMessage(role, content) {
        const container = document.getElementById('messages-container');

        // 如果是第一条消息，清除欢迎信息
        if (container.querySelector('.welcome-message')) {
            container.innerHTML = '';
        }

        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${role}`;

        const avatar = role === 'user' ?
            '<i class="fas fa-user"></i>' :
            '<i class="fas fa-robot"></i>';

        messageDiv.innerHTML = `
            <div class="message-avatar">${avatar}</div>
            <div class="message-content">
                ${this.formatMessageContent(content)}
                <div class="message-time">${this.formatTime(new Date().toISOString())}</div>
            </div>
        `;

        container.appendChild(messageDiv);
        container.scrollTop = container.scrollHeight;
    }

    renderMessages(messages) {
        const container = document.getElementById('messages-container');
        container.innerHTML = '';

        if (messages.length === 0) {
            container.innerHTML = `
                <div class="welcome-message">
                    <div class="welcome-icon">
                        <i class="fas fa-robot"></i>
                    </div>
                    <h3>开始新的对话</h3>
                    <p>输入您的消息开始与AI助手对话！</p>
                </div>
            `;
            return;
        }

        messages.forEach(msg => {
            this.addMessage(msg.role, msg.content);
        });
    }

    clearMessages() {
        const container = document.getElementById('messages-container');
        container.innerHTML = `
            <div class="welcome-message">
                <div class="welcome-icon">
                    <i class="fas fa-robot"></i>
                </div>
                <h3>开始新的对话</h3>
                <p>输入您的消息开始与AI助手对话！</p>
            </div>
        `;
    }

    updateChatTitle(title) {
        document.getElementById('chat-title').textContent = title;
    }

    updateActiveConversation(conversationId) {
        // 移除所有active类
        document.querySelectorAll('.conversation-item').forEach(item => {
            item.classList.remove('active');
        });

        // 添加active类到当前对话
        const activeItem = document.querySelector(`[data-conversation-id="${conversationId}"]`);
        if (activeItem) {
            activeItem.classList.add('active');
        }
    }

    async clearCurrentChat() {
        if (!this.currentConversationId) return;

        if (confirm('确定要清空当前对话吗？')) {
            try {
                const response = await fetch(`/api/conversations/${this.currentConversationId}`, {
                    method: 'DELETE'
                });

                const data = await response.json();

                if (data.success) {
                    this.currentConversationId = null;
                    this.clearMessages();
                    this.updateChatTitle('开始新的对话');
                    this.loadConversations();
                } else {
                    alert('清空对话失败: ' + data.message);
                }
            } catch (error) {
                console.error('清空对话失败:', error);
                alert('清空对话失败: ' + error.message);
            }
        }
    }

    formatMessageContent(content) {
        // 简单的换行处理
        return content.replace(/\n/g, '<br>');
    }

    formatTime(timeString) {
        const date = new Date(timeString);
        const now = new Date();
        const diff = now - date;

        if (diff < 60000) { // 1分钟内
            return '刚刚';
        } else if (diff < 3600000) { // 1小时内
            return Math.floor(diff / 60000) + '分钟前';
        } else if (diff < 86400000) { // 1天内
            return Math.floor(diff / 3600000) + '小时前';
        } else {
            return date.toLocaleDateString('zh-CN');
        }
    }

    showLoading(show) {
        const loading = document.getElementById('loading');
        if (show) {
            loading.classList.remove('hidden');
        } else {
            loading.classList.add('hidden');
        }
    }
}

// 初始化应用
document.addEventListener('DOMContentLoaded', () => {
    new ChatApp();
});
