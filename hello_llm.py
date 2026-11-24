"""W1 验收脚本：连续调用 3 次大模型 API。

用法
----
    1. copy .env.example .env     # 然后填入自己的 API Key
    2. uv run python hello_llm.py

通过标准
--------
    3 个问题全部拿到中文回答，且最后打印 "3 次全部成功"。
"""

import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

# 从 .env 文件读取配置，而不是把 key 写在代码里。
# 这是最重要的一个习惯：密钥永远不进代码、不进 Git。
load_dotenv()

API_KEY = os.getenv("LLM_API_KEY")
BASE_URL = os.getenv("LLM_BASE_URL")
MODEL = os.getenv("LLM_MODEL")

# 三个用来验收的问题，都是你专业里最基础的概念。
QUESTIONS = [
    "用一句话解释什么是风景园林。",
    "景观设计中的“空间序列”指的是什么？",
    "列举 3 个影响植物配置的因素。",
]


def check_config() -> None:
    """检查 .env 是否填好，缺什么就直接说缺什么，别让新手对着 traceback 发呆。"""
    missing = []

    if not API_KEY or API_KEY.startswith(("sk-your", "your-")):
        missing.append("LLM_API_KEY（还是模板里的占位符）")
    if not BASE_URL:
        missing.append("LLM_BASE_URL")
    if not MODEL:
        missing.append("LLM_MODEL")

    if missing:
        print("[配置缺失] 请在 .env 里填写：")
        for item in missing:
            print(f"  - {item}")
        print("\n提示：如果还没有 .env，先执行  copy .env.example .env")
        sys.exit(1)


def ask(question: str) -> str:
    """问一次模型，返回回答文本。"""
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "你是一个严谨的专业助手，回答简洁、准确，不超过 3 句话。",
            },
            {"role": "user", "content": question},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content or ""


def main() -> None:
    check_config()

    print(f"模型：{MODEL}")
    print(f"接口：{BASE_URL}")
    print("=" * 50)

    for index, question in enumerate(QUESTIONS, start=1):
        print(f"\n[{index}/3] 问：{question}")
        try:
            answer = ask(question)
        except Exception as exc:  # noqa: BLE001 - 新手需要看到全部原因
            print(f"❌ 第 {index} 次调用失败：{exc}")
            print("\n常见原因，按概率排序：")
            print("  1. key 复制不全，或方案 A/B 的 key 与 base_url 混用了")
            print("  2. 账户余额不足（DeepSeek 需要充值）")
            print("  3. 模型名写错：deepseek-chat / glm-4-flash")
            print("  4. 网络不通")
            sys.exit(1)
        print(f"答：{answer}")

    print("\n" + "=" * 50)
    print("✅ 3 次全部成功 —— W1 验收项 C 通过")


if __name__ == "__main__":
    main()
