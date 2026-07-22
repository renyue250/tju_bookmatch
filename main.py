# main.py
# 天津大学AI智能体大赛 - 二手书智能匹配助手
# 项目名称：agent2026-book-match

import sys

def show_help():
    print("=" * 40)
    print("  天大二手书智能匹配助手 v0.2")
    print("=" * 40)
    print("可用命令:")
    print("  python main.py test    - 测试校内词元服务")
    print("  python main.py help    - 显示帮助")
    print("=" * 40)


def test_llm():
    """测试校内词元服务是否正常工作"""
    print("\n正在测试校内词元服务...\n")
    
    # 导入并执行测试
    import llm_client
    # 直接运行 llm_client.py 中的测试代码
    # 但为了避免重复导入问题，用 exec 方式
    exec(open("llm_client.py", encoding="utf-8").read())


def main():
    if len(sys.argv) < 2:
        show_help()
        return
    
    cmd = sys.argv[1].lower()
    
    if cmd == "test":
        test_llm()
    elif cmd == "help":
        show_help()
    else:
        print(f"未知命令: {cmd}")
        show_help()


if __name__ == "__main__":
    main()