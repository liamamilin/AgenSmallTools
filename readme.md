太好了 👍 采用 **固定 `outputs/` 目录** + **下载按钮** 的方案会简单很多，也避免浏览器路径权限问题。

下面我给你写一个 **项目 README.md**，清晰地告诉使用者如何安装、运行和使用。

---

# 📘 Agent 客户端项目

本项目是一个基于 **FastAPI + Jinja2** 的 Web 客户端，用于管理和运行自定义的 **Prompt Agent**。

支持功能：

* 单条对话：选择 Prompt，输入用户问题，实时得到大模型回复
* 批处理：上传 CSV 文件（两列：`id`, `user_prompt`），批量运行并生成结果文件
* Prompt 管理：新增、编辑、保存 Prompt（YAML 格式）

所有批处理的结果文件将保存在 **`outputs/` 文件夹**，并可通过网页直接下载。

---

## 📂 项目结构

```
Agent_v1/
│── main.py              # FastAPI 启动入口
│── agent.py             # Agent 调用逻辑（大模型接口）
│── tools/
│    └── prompt_loader.py # 加载 YAML Prompt 的工具
│── prompts/             # 存放所有 YAML Prompt 文件
│── templates/           # Jinja2 模板 (HTML 页面)
│── static/              # 静态文件 (CSS, JS)
│── outputs/             # 批处理结果保存目录
```

---

## 🚀 安装步骤

### 1. 克隆项目

```bash
git clone https://github.com/yourname/AgentClient.git
cd AgentClient/Agent_v1
```

### 2. 创建虚拟环境并安装依赖

```bash
conda create -n agent python=3.11 -y
conda activate agent
pip install -r requirements.txt
```

如果没有 `requirements.txt`，可手动安装：

```bash
pip install fastapi uvicorn jinja2 pydantic pandas openai
```

### 3. 启动服务

```bash
uvicorn main:app --reload
```

浏览器访问 👉 [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🖥️ 使用说明

### 1. 单条对话

* 在网页选择一个 `Prompt (YAML)`
* 输入 `User Prompt`
* 点击 **运行** → 页面显示结果

### 2. 批处理

* 准备一个 CSV 文件，格式如下：

  ```csv
  id,user_prompt
  1,请解释什么是二次函数
  2,帮我总结柏拉图哲学的核心
  ```
* 在网页选择 Prompt
* 上传 CSV 文件
* 输入输出文件名，例如：`result.csv`
* 点击 **运行批处理**
* 稍等几秒，结果文件会保存到 `outputs/` 文件夹，并提供「下载按钮」

### 3. Prompt 管理

* 进入 `Prompt 管理` 页面
* 新建 / 编辑 YAML Prompt 文件，例如：

  ```yaml
  name: philosophy_prompt
  description: 你是一个专业的哲学老师
  system:
    objective: "你需要讲解哲学体系"
    context: "分析组成部分，解释原理机制，给出应用与价值"
    role: "哲学老师"
  ```
* 保存后可立即在对话和批处理页面使用

---

## 📂 批处理结果

* 所有批处理结果默认保存在 `outputs/` 文件夹
* 可以通过网页点击「下载结果」直接获取

---

## 🔧 待办优化

* [ ] 增加进度条显示批处理状态
* [ ] 支持多模型切换（如 OpenAI / 本地模型）
* [ ] Prompt 分类和搜索功能

---

👉 建议：我可以帮你生成一个 `requirements.txt`，这样你下次直接 `pip install -r requirements.txt` 就能一键安装。

要不要我帮你写一个 **requirements.txt**？
