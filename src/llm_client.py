# llm_client.py
# 天津大学校内词元服务调用封装
# 功能：提供统一的API调用接口，供项目其他模块使用

import requests
import json
import time
from config import LLM_API_URL, LLM_API_KEY, LLM_MODEL


def call_tju_llm(prompt: str, temperature: float = 0.1, max_retries: int = 3) -> str:
    """
    调用天津大学校内词元服务（大模型API）
    
    参数:
        prompt: 输入给模型的提示词
        temperature: 温度参数（0-1），越低回答越确定、越保守
        max_retries: 调用失败时的最大重试次数
    
    返回:
        模型返回的文本内容，如果失败则返回空字符串
    """
    headers = {
        "Authorization": f"Bearer {LLM_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": LLM_MODEL,
        "messages": [
            {
                "role": "system", 
                "content": "你是一个天津大学校园助手，回答要简洁、准确、友好。"
            },
            {
                "role": "user", 
                "content": prompt
            }
        ],
        "temperature": temperature
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.post(
                LLM_API_URL, 
                headers=headers, 
                json=payload, 
                timeout=30  # 30秒超时
            )
            response.raise_for_status()  # 如果状态码不是200，会抛出异常
            
            result = response.json()
            # 从返回结果中提取模型回复的内容
            content = result["choices"][0]["message"]["content"].strip()
            return content
            
        except requests.exceptions.Timeout:
            print(f"[LLM调用] 超时，第 {attempt+1}/{max_retries} 次重试...")
            time.sleep(2)  # 等待2秒后重试
            
        except requests.exceptions.RequestException as e:
            print(f"[LLM调用] 网络错误: {e}，第 {attempt+1}/{max_retries} 次重试...")
            time.sleep(2)
            
        except (KeyError, json.JSONDecodeError) as e:
            print(f"[LLM调用] 返回格式解析失败: {e}")
            print(f"[LLM调用] 原始返回: {response.text[:200] if 'response' in locals() else '无响应'}")
            break  # 格式错误不重试，直接退出
    
    print("[LLM调用] 所有重试失败，返回空字符串")
    return ""


def is_same_book(book1: str, book2: str) -> bool:
    """
    使用大模型判断两本书名是否指同一本书（考虑简称、版本差异）
    
    参数:
        book1: 书名1
        book2: 书名2
    
    返回:
        是同一本书返回 True，否则返回 False
    """
    prompt = f"""
请判断以下两本书名是否指的是同一本书。

书名A：{book1}
书名B：{book2}

判断规则：
1. "高等数学"和"高数"算同一本
2. "数据结构（C语言版）"和"数据结构 C语言版"算同一本  
3. "第7版"和"第七版"算同一本
4. 如果有副标题，副标题可以忽略，只看主书名

只回答"是"或"否"，不要输出其他任何内容。
"""
    
    result = call_tju_llm(prompt, temperature=0.1)
    return "是" in result


def generate_match_message(buy_book: str, sell_book: str, contact: str) -> str:
    """
    使用大模型生成有温度的匹配通知文案（优化版）
    """
    # 极简 prompt，只要求生成一句话，降低模型处理负担
    prompt = f"买家求购《{buy_book}》，卖家出售《{sell_book}》，联系方式：{contact}。请用一句友好、温暖的话通知买家，字数不超过30字。"
    
    message = call_tju_llm(prompt, temperature=0.3)  # 降低 temperature
    
    if not message:
        # 备用模板
        message = f"📚 二手书匹配成功！\n\n您求购的《{buy_book}》有人出售！\n卖家联系方式：{contact}\n\n请尽快联系，祝交易愉快 😊\n—— 天大二手书智能匹配助手"
    
    return message


# ========== 本文件自测代码（方便验证API是否通） ==========
if __name__ == "__main__":
    print("=" * 40)
    print("测试校内词元服务连接...")
    print("=" * 40)
    
    # 测试1：简单对话
    print("\n【测试1】简单对话")
    result = call_tju_llm("请用一句话介绍天津大学")
    print(f"返回结果: {result}")
    
    # 测试2：书名匹配
    print("\n【测试2】书名语义匹配")
    result = is_same_book("高等数学", "高数")
    print(f"'高等数学' 和 '高数' 是同一本书吗？ {result}")
    
    result = is_same_book("数据结构", "线性代数")
    print(f"'数据结构' 和 '线性代数' 是同一本书吗？ {result}")
    
    # 测试3：匹配消息生成
    print("\n【测试3】匹配消息生成")
    message = generate_match_message("高等数学第七版", "高数第7版", "微信: tju123")
    print(f"生成的消息:\n{message}")
    
    print("\n" + "=" * 40)
    print("测试完成！")