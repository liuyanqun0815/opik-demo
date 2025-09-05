// 会话记录页面JavaScript
class ConversationsApp {
    constructor() {
        this.conversations = [];
        this.filteredConversations = [];
        this.sortBy = 'updated_desc';
        this.searchTerm = '';
        this.deleteConversationId = null;
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadConversations();
    }

    bindEvents() {
        // 刷新按钮
        document.getElementById('refresh-btn').addEventListener('click', () => {
            this.loadConversations();
        });

        // 搜索输入
        document.getElementById('search-input').addEventListener('input', (e) => {
            this.searchTerm = e.target.value.toLowerCase();
            this.filterAndRenderConversations();
        });

        // 排序选择
        document.getElementById('sort-select').addEventListener('change', (e) => {
            this.sortBy = e.target.value;
            this.filterAndRenderConversations();
        });

        // 模态框关闭
        document.getElementById('modal-close').addEventListener('click', () => {
            this.hideDeleteModal();
        });

        document.getElementById('cancel-delete').addEventListener('click', () => {
            this.hideDeleteModal();
        });

        // 确认删除
        document.getElementById('confirm-delete').addEventListener('click', () => {
            this.confirmDelete();
        });

        // 点击模态框背景关闭
        document.getElementById('delete-modal').addEventListener('click', (e) => {
            if (e.target.id === 'delete-modal') {
                this.hideDeleteModal();
            }
        });
    }

    async loadConversations() {
        try {
            this.showLoading(true);

            const response = await fetch('/api/conversations');
            const data = await response.json();

            if (data.success) {
                this.conversations = data.data;
                this.filterAndRenderConversations();
            } else {
                console.error('加载会话列表失败:', data.message);
                this.showError('加载会话列表失败: ' + data.message);
            }
        } catch (error) {
            console.error('加载会话列表失败:', error);
            this.showError('加载会话列表失败: ' + error.message);
        } finally {
            this.showLoading(false);
        }
    }

    filterAndRenderConversations() {
        // 过滤会话
        this.filteredConversations = this.conversations.filter(conv => {
            return conv.title.toLowerCase().includes(this.searchTerm);
        });

        // 排序会话
        this.filteredConversations.sort((a, b) => {
            switch (this.sortBy) {
                case 'created_desc':
                    return new Date(b.created_at) - new Date(a.created_at);
                case 'title_asc':
                    return a.title.localeCompare(b.title);
                case 'updated_desc':
                default:
                    return new Date(b.updated_at) - new Date(a.updated_at);
            }
        });

        this.renderConversations();
    }

    renderConversations() {
        const container = document.getElementById('conversations-list');
        const emptyState = document.getElementById('empty-state');

        if (this.filteredConversations.length === 0) {
            container.innerHTML = '';
            emptyState.classList.remove('hidden');
            return;
        }

        emptyState.classList.add('hidden');
        container.innerHTML = '';

        this.filteredConversations.forEach(conv => {
            const card = this.createConversationCard(conv);
            container.appendChild(card);
        });
    }

    createConversationCard(conversation) {
        const card = document.createElement('div');
        card.className = 'conversation-card';
        card.dataset.conversationId = conversation.id;

        card.innerHTML = `
            <div class="conversation-header">
                <div>
                    <div class="conversation-title">${this.escapeHtml(conversation.title)}</div>
                </div>
                <div class="conversation-time">${this.formatTime(conversation.updated_at)}</div>
            </div>
            
            <div class="conversation-stats">
                <div class="stat-item">
                    <i class="fas fa-comments"></i>
                    <span>${conversation.message_count} 条消息</span>
                </div>
                <div class="stat-item">
                    <i class="fas fa-calendar"></i>
                    <span>${this.formatDate(conversation.created_at)}</span>
                </div>
            </div>
            
            <div class="conversation-actions">
                <button class="action-btn view-btn" onclick="conversationsApp.viewConversation(${conversation.id})">
                    <i class="fas fa-eye"></i>
                    查看
                </button>
                <button class="action-btn delete-btn" onclick="conversationsApp.showDeleteModal(${conversation.id})">
                    <i class="fas fa-trash"></i>
                    删除
                </button>
            </div>
        `;

        return card;
    }

    viewConversation(conversationId) {
        // 跳转到聊天页面并加载指定会话
        window.location.href = `/?conversation=${conversationId}`;
    }

    showDeleteModal(conversationId) {
        this.deleteConversationId = conversationId;
        document.getElementById('delete-modal').classList.remove('hidden');
    }

    hideDeleteModal() {
        this.deleteConversationId = null;
        document.getElementById('delete-modal').classList.add('hidden');
    }

    async confirmDelete() {
        if (!this.deleteConversationId) return;

        try {
            const response = await fetch(`/api/conversations/${this.deleteConversationId}`, {
                method: 'DELETE'
            });

            const data = await response.json();

            if (data.success) {
                // 从本地数组中移除已删除的会话
                this.conversations = this.conversations.filter(conv => conv.id !== this.deleteConversationId);
                this.filterAndRenderConversations();
                this.hideDeleteModal();
            } else {
                this.showError('删除会话失败: ' + data.message);
            }
        } catch (error) {
            console.error('删除会话失败:', error);
            this.showError('删除会话失败: ' + error.message);
        }
    }

    showLoading(show) {
        const loadingState = document.getElementById('loading-state');
        if (show) {
            loadingState.classList.remove('hidden');
        } else {
            loadingState.classList.add('hidden');
        }
    }

    showError(message) {
        // 简单的错误提示，实际项目中可以使用更好的提示组件
        alert(message);
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
        } else if (diff < 604800000) { // 1周内
            return Math.floor(diff / 86400000) + '天前';
        } else {
            return date.toLocaleDateString('zh-CN');
        }
    }

    formatDate(timeString) {
        const date = new Date(timeString);
        return date.toLocaleDateString('zh-CN', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// 初始化应用
let conversationsApp;
document.addEventListener('DOMContentLoaded', () => {
    conversationsApp = new ConversationsApp();
});
