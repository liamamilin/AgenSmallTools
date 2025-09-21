import argparse
import pandas as pd
from agent import agent

def run_batch(input_file, output_file, agent_name="math-teacher"):
    # 读取输入文件
    df = pd.read_csv(input_file)

    results = []
    for _, row in df.iterrows():
        user_id = row["id"]
        prompt = row["user_prompt"]
        try:
            result = agent(agent_name, prompt)
        except Exception as e:
            result = f"调用失败: {e}"
        results.append({"id": user_id, "user_prompt": prompt, "result": result})

    # 保存输出文件
    out_df = pd.DataFrame(results)
    out_df.to_csv(output_file, index=False, encoding="utf-8-sig")
    print(f"✅ 批量任务完成，结果已保存到 {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="批量调用 Agent")
    parser.add_argument("input", help="输入文件路径 (CSV)，包含 id 和 user_prompt 两列")
    parser.add_argument("output", help="输出文件路径 (CSV)，会包含结果")
    parser.add_argument("--agent", default="math-teacher", help="Agent 名称，默认 math-teacher")

    args = parser.parse_args()
    run_batch(args.input, args.output, args.agent)
