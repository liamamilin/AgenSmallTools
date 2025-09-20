from flask import Flask, request, jsonify, Response
from openai import OpenAI
from tools.prompt_loader import load_system_prompt_from_name
from agent import agent
import json
 

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

# 本地 Ollama API
OLLAMA_BASE_URL = "http://localhost:11434/v1"
client = OpenAI(base_url=OLLAMA_BASE_URL, api_key="anything")

@app.route("/chat", methods=["POST"])
def chat():
    """
    输入 JSON：
    {
      "agent_name": "math-teacher",
      "user_prompt": "请解释什么是二次函数？"
    }
    """
    data = request.get_json()
    agent_name = data.get("agent_name")
    user_prompt = data.get("user_prompt")

    if not agent_name or not user_prompt:
        return jsonify({"error": "缺少 agent_name 或 user_prompt"}), 400

    try:
        # 加载 system prompt
        # system_prompt = load_system_prompt_from_name(agent_name)

        # # 调用本地大模型
        # response = client.chat.completions.create(
        #     model="llama3.2",
        #     messages=[
        #         {"role": "system", "content": system_prompt},
        #         {"role": "user", "content": user_prompt}
        #     ]
        # )

        result = agent(agent_name, user_prompt)
        return Response(
            json.dumps({"response": result}, ensure_ascii=False),
            mimetype="application/json"
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
