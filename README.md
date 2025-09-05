# AI聊天助手

基于Flask和DeepSeek API的智能聊天应用，支持会话管理和历史记录查看。

## 功能特性

- 🤖 基于DeepSeek大模型的智能对话
- 💬 实时聊天界面，支持多轮对话
- 📝 会话管理，自动生成对话标题
- 📚 会话历史记录查看和管理
- 🎨 现代化响应式UI设计
- 🔍 会话搜索和排序功能

## 技术栈

- **后端**: Flask + SQLAlchemy + LangChain
- **数据库**: PostgreSQL
- **前端**: HTML5 + CSS3 + JavaScript
- **AI模型**: DeepSeek API
- **样式**: 自定义CSS + Font Awesome图标
- **监控**: Opik (LLM调用跟踪和监控)

## 安装和运行

### 1. 克隆项目

```bash
git clone <repository-url>
cd opik-demo
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

复制 `env_example.txt` 为 `.env` 并填入相应配置：

```bash
cp env_example.txt .env
```

编辑 `.env` 文件，配置数据库连接、DeepSeek API密钥和Opik API密钥：

**获取Opik API密钥**: 访问 https://comet.com/opik/your-workspace-name/get-started

```env
# 数据库配置
DATABASE_URL=postgresql://username:password@localhost:5432/chat_db

# DeepSeek API配置
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com

# Flask配置
FLASK_ENV=development
SECRET_KEY=your_secret_key_here

# Opik配置
OPIK_API_KEY=your_opik_api_key_here
OPIK_PROJECT_NAME=flask-chat-app
OPIK_WORKSPACE=your_workspace_name
```

### 4. 创建数据库

确保PostgreSQL服务正在运行，创建数据库：

```sql
CREATE DATABASE chat_db;
```

### 5. 运行应用

```bash
python app.py
```

应用将在 `http://localhost:5000` 启动。

## 项目结构

```
opik-demo/
├── app.py                 # 主应用文件
├── config.py             # 配置文件
├── models.py             # 数据库模型
├── routes.py             # API路由
├── llm_service.py        # 大模型服务
├── requirements.txt      # 依赖列表
├── env_example.txt       # 环境变量示例
├── README.md            # 项目说明
├── static/              # 静态文件
│   ├── css/
│   │   ├── chat.css     # 聊天页面样式
│   │   └── conversations.css  # 会话记录页面样式
│   └── js/
│       ├── chat.js      # 聊天页面脚本
│       └── conversations.js  # 会话记录页面脚本
└── templates/           # HTML模板
    ├── chat.html        # 聊天页面
    └── conversations.html  # 会话记录页面
```

## API接口

### 会话管理

- `GET /api/conversations` - 获取所有会话列表
- `POST /api/conversations` - 创建新会话
- `GET /api/conversations/<id>` - 获取指定会话详情
- `DELETE /api/conversations/<id>` - 删除指定会话

### 消息管理

- `POST /api/conversations/<id>/messages` - 发送消息
- `GET /api/conversations/<id>/messages` - 获取会话消息列表

## 使用说明

1. **开始新对话**: 点击"新对话"按钮创建新的聊天会话
2. **发送消息**: 在输入框中输入消息，按回车或点击发送按钮
3. **查看历史**: 点击侧边栏中的会话标题查看历史对话
4. **管理会话**: 访问会话记录页面进行搜索、排序和删除操作

## 配置说明

### DeepSeek API配置

1. 访问 [DeepSeek官网](https://platform.deepseek.com/) 注册账号
2. 获取API密钥
3. 在环境变量中配置 `DEEPSEEK_API_KEY`

### 数据库配置

确保PostgreSQL服务正常运行，并创建相应的数据库和用户。

## 开发说明

### 代码规范

- 遵循PEP8规范
- 使用black格式化（max_line_length=120）
- 变量命名采用snake_case
- 禁止使用 `from module import *`

### 扩展功能

- 支持更多AI模型
- 添加用户认证系统
- 实现文件上传功能
- 添加对话导出功能

## 许可证

MIT License
