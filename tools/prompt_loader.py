import os
import yaml
from pathlib import Path
import yaml
BASE_DIR = Path(__file__).resolve().parents[1]
PROMPTS_DIR = BASE_DIR / "prompts"
PROMPT_DIR = os.path.join(os.path.dirname(__file__), "..", "prompts")

# 缓存字典：name -> file_path
_yaml_cache = {}

def build_yaml_cache():
    """初始化缓存，把 prompts 文件夹里的所有 yaml 加载到缓存"""
    global _yaml_cache
    _yaml_cache = {}  # 重置
    for filename in os.listdir(PROMPT_DIR):
        if filename.endswith((".yaml", ".yml")):
            file_path = os.path.join(PROMPT_DIR, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                if not data:  # 跳过空文件
                    print(f"⚠️ 跳过空文件: {filename}")
                    continue
                name = data.get("name")
                if name:
                    _yaml_cache[name] = file_path
                else:
                    print(f"⚠️ {filename} 缺少 name 字段，已跳过")


def find_yaml_by_name(target_name: str) -> str:
    """根据 name 在缓存里查找对应文件路径"""
    if not _yaml_cache:  # 如果缓存为空，先构建
        build_yaml_cache()
    if target_name in _yaml_cache:
        return _yaml_cache[target_name]
    raise FileNotFoundError(f"未找到 name={target_name} 的 YAML 文件")

def load_system_prompt_from_name(target_name: str) -> str:
    """根据 name 获取拼接后的 system prompt"""
    file_path = find_yaml_by_name(target_name)
    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    system = data["system"]
    return (
        f"任务目标:\n{system['objective']}\n\n"
        f"上下文:\n{system['context']}\n\n"
        f"角色:\n{system['role']}\n\n"
        f"样例:\n{system['examples']}\n\n"
        f"输出格式:\n{system['output_format']}"
    )
def load_system_prompt_from_file(filename: str) -> str:
    p = Path(filename)
    if not p.is_absolute():
        p = PROMPTS_DIR / filename
    # 容错：允许 - 与 _ 互换 以及补 .yaml
    cand = [
        p,
        p.with_suffix(".yaml"),
        PROMPTS_DIR / filename.replace("-", "_"),
        PROMPTS_DIR / filename.replace("_", "-"),
        (PROMPTS_DIR / filename.replace("-", "_")).with_suffix(".yaml"),
        (PROMPTS_DIR / filename.replace("_", "-")).with_suffix(".yaml"),
    ]
    target = next((c for c in cand if c.exists()), None)
    if target is None:
        raise FileNotFoundError(f"未找到文件 {p}")

    with open(target, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    system = data.get("system", "")
    if isinstance(system, dict):
        parts = [system.get("objective"), system.get("context"), system.get("role")]
        system = "\n".join([str(x) for x in parts if x])
    return str(system).strip()


def find_yaml_by_name(target_name: str) -> Path:
    norm = target_name.replace("-", "_")
    for p in PROMPTS_DIR.glob("*.yaml"):
        with open(p, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        name = str(data.get("name", "")).strip()
        if name.replace("-", "_") == norm:
            return p
    raise FileNotFoundError(f"未找到 name={target_name} 的 YAML 文件")

if __name__ == "__main__":
    print("当前 PROMPT_DIR:", PROMPT_DIR)
    print("目录内容:", os.listdir(PROMPT_DIR))
    system_prompt = load_system_prompt_from_name("math-teacher")
    print("加载到的 system prompt:\n", system_prompt)
