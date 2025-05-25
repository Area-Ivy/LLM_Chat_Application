import gradio as gr
import requests
import uuid
from datetime import datetime

API_KEYS = {
    "deepseek": "your_deepseek_key",
    "kimi": "your_kimi_key",
    "tongyi": "your_tongyi_key"
}

MODEL_ENDPOINTS = {
    "deepseek": {
        "url": "https://api.deepseek.com/v1/chat/completions",
        "headers": {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEYS['deepseek']}"
        }
    },
    "kimi": {
        "url": "https://api.moonshot.cn/v1/chat/completions",
        "headers": {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEYS['kimi']}"
        }
    },
    "tongyi": {
        "url": "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation",
        "headers": {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEYS['tongyi']}"
        }
    }
}

def call_llm_api(model, messages):
    endpoint = MODEL_ENDPOINTS[model]
    
    if model == "deepseek":
        data = {
            "model": "deepseek-chat",
            "messages": messages,
            "temperature": 0.7
        }
    elif model == "kimi":
        data = {
            "model": "moonshot-v1-8k",
            "messages": messages,
            "temperature": 0.3
        }
    elif model == "tongyi":
        data = {
            "model": "qwen-turbo",
            "input": {
                "messages": messages
            },
            "parameters": {
                "temperature": 0.5
            }
        }
    
    try:
        response = requests.post(
            url=endpoint["url"],
            headers=endpoint["headers"],
            json=data
        )
        response.raise_for_status()
        
        if model == "tongyi":
            return response.json()["output"]["text"]
        else:
            return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"API调用失败: {str(e)}"

def create_new_session():
    return {
        "id": str(uuid.uuid4()),
        "title": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "messages": []
    }

def format_messages(messages):
    return [(None, msg["content"]) if msg["role"] == "user" else (msg["content"], None) for msg in messages]

def respond(message, chat_history, model, current_session, history_sessions):
    if not message.strip():
        return "", chat_history, current_session, history_sessions
    
    current_session["messages"].append({"role": "user", "content": message})
    api_response = call_llm_api(model, current_session["messages"])
    current_session["messages"].append({"role": "assistant", "content": api_response})
    
    updated_history = []
    session_exists = False
    for session in history_sessions:
        if session["id"] == current_session["id"]:
            updated_history.append(current_session)
            session_exists = True
        else:
            updated_history.append(session)
    
    if not session_exists:
        updated_history = [current_session] + history_sessions
    
    return "", format_messages(current_session["messages"]), current_session, updated_history

def load_session(selected_session, history_sessions):
    if selected_session:
        for session in history_sessions:
            if session["title"] == selected_session:
                return session, format_messages(session["messages"])
    return current_session, chat_history

def create_new_chat(history_sessions):
    new_session = create_new_session()
    return new_session, [new_session] + history_sessions, []

with gr.Blocks(
    title="LLM Chat",
    css="""
    .chatbox { min-height: 600px; }
    .msg-input { flex-grow: 1; }
    .history-list .wrap { max-width: 100% !important; }
    .user-bubble { 
        margin-left: auto !important;
        background: #007bff !important;
        color: white !important;
    }
    .bot-bubble { 
        margin-right: auto !important;
        background: #e9ecef !important;
        color: black !important;
    }
    .action-btns { 
        width: 100%;
        justify-content: flex-end;
    }
    .secondary-btn { 
        background: #6c757d !important;
        color: white !important;
    }
    """
) as demo:
    gr.Markdown("## 🚀 LLM 多模型对话系统", elem_classes=["title"])
    
    current_session = gr.State(create_new_session())
    history_sessions = gr.State([])
    
    with gr.Row(equal_height=False):
        # 左侧边栏
        with gr.Column(scale=2, min_width=250):
            with gr.Group():
                gr.Markdown("### 📚 历史会话")
                history_list = gr.Radio(
                    label="",
                    choices=[],
                    type="value",
                    interactive=True,
                    elem_classes=["history-list"]
                )
            new_chat_btn = gr.Button(
                "🆕 新建聊天", 
                variant="secondary",
                elem_classes=["secondary-btn"]
            )

        # 主聊天区
        with gr.Column(scale=8):
            chatbot = gr.Chatbot(
                height=600,
                bubble_full_width=False,
                avatar_images=("./assert/bot.png", "./assert/user.png"),
                elem_classes=["chatbox"],
                show_label=False
            )
            
            # 输入区域
            with gr.Column():
                with gr.Row():
                    msg = gr.Textbox(
                        label="",
                        placeholder="输入消息...",
                        max_lines=3,
                        elem_classes=["msg-input"],
                        scale=4
                    )
                    model_selector = gr.Dropdown(
                        label="选择模型",
                        choices=[
                            ("DeepSeek", "deepseek"),
                            ("Kimi", "kimi"),
                            ("Tongyi", "tongyi")
                        ],
                        value="deepseek",
                        scale=1
                    )

                # 操作按钮行
                with gr.Row(elem_classes=["action-btns"]):
                    submit_btn = gr.Button("📤 发送", variant="primary")
                    clear_btn = gr.Button("🗑️ 清空输入", variant="secondary")

    msg.submit(
        respond,
        [msg, chatbot, model_selector, current_session, history_sessions],
        [msg, chatbot, current_session, history_sessions]
    )
    
    submit_btn.click(
        respond,
        [msg, chatbot, model_selector, current_session, history_sessions],
        [msg, chatbot, current_session, history_sessions]
    )
    
    new_chat_btn.click(
        create_new_chat,
        [history_sessions],
        [current_session, history_sessions, chatbot]
    )
    
    history_list.change(
        load_session,
        [history_list, history_sessions],
        [current_session, chatbot]
    )
    
    history_sessions.change(
        lambda sessions: gr.Radio(choices=[s["title"] for s in sessions]),
        [history_sessions],
        [history_list]
    )
    
    clear_btn.click(lambda: "", outputs=[msg])

demo.launch()
