
# 启动方法

## 创建虚拟环境
python -m venv venv
## 激活虚拟环境（Windows）
venv\Scripts\activate
## 激活虚拟环境（Mac/Linux）
source venv/bin/activate
## 安装依赖
pip install -r requirements.txt
## 运行
python app.py


# 功能点实现
- 基础对话功能：可以成功的调用LLM模型的API来回答用户的问题，存在基本的输入输出的页面。
- 多轮对话功能：在同一个对话下，记录同该用户之前的对话内容，一同输入给大模型，从而实现多轮对话功能。
- 历史记录功能：可以记录用户之前同LLM的对话历史记录，并且可以选择之前的历史记录继续聊天。
- 模型切换功能：用户可以再同一对话下自由切换响应模型，以对比不同的模型回答内容。
