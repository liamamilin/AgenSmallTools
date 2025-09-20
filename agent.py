from openai import OpenAI
from tools.prompt_loader import load_system_prompt_from_name

def agent(name: str, user_prompt: str, model: str = "gemma3:12b") -> str:
    client = OpenAI(base_url="http://localhost:11434/v1", api_key="anything")
    system_prompt = load_system_prompt_from_name(name)

    response = client.chat.completions.create(
        model="llama3.2",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message.content

# if __name__ == "__main__":
#     result = agent("math-teacher", "请解释什么是二次函数？")
#     print(result)
