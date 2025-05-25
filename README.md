# LLM Chat Application

## 项目名称

LLM_Chat_Application

## 项目简介

Gradio-based LLM Chat Application.

基于 Gradio 构建的大语言模型对话应用。

> ***Relevant course***
> * Human Computer Interface 2025 (2025年同济大学用户交互技术)

功能点实现
- 基础对话功能：可以成功的调用LLM模型的API来回答用户的问题，存在基本的输入输出的页面。
- 多轮对话功能：在同一个对话下，记录同该用户之前的对话内容，一同输入给大模型，从而实现多轮对话功能。
- 历史记录功能：可以记录用户之前同LLM的对话历史记录，并且可以选择之前的历史记录继续聊天。
- 模型切换功能：用户可以再同一对话下自由切换响应模型，以对比不同的模型回答内容。

## 项目组成

* `/assets`
存放相关图片资源

* `app.py`
主程序

* `requirements.txt`
依赖集

* `report.docx`
报告

## 环境搭建

* 创建虚拟环境
```
python -m venv venv
```

* 激活虚拟环境
```
venv\Scripts\activate
```

* 安装依赖
```
pip install -r requirements.txt
```

## 项目运行

```
python app.py
```

## 文档更新日期

2025年5月25日
