# main.py
# 天津大学AI智能体大赛 - 二手书智能匹配助手

import sys
import db
from scheduler import start_scheduler


def show_help():
    print("=" * 40)
    print("  天大二手书智能匹配助手 v0.3")
    print("=" * 40)
    print("可用命令:")
    print("  python main.py start    - 启动定时调度（持续运行）")
    print("  python main.py test     - 测试校内词元服务")
    print("  python main.py help     - 显示帮助")
    print("=" * 40)


def test_llm():
    """测试校内词元服务"""
    print("\n正在测试校内词元服务...\n")
    try:
        from llm_client import call_tju_llm
        result = call_tju_llm("请用一句话介绍天津大学")
        print(f"测试结果: {result}")
    except Exception as e:
        print(f"测试失败: {e}")


def main():
    # 初始化数据库（确保表存在）
    db.init_db()

    if len(sys.argv) < 2:
        show_help()
        return

    cmd = sys.argv[1].lower()

    if cmd == "start":
        interval = 5
        if len(sys.argv) >= 3:
            try:
                interval = int(sys.argv[2])
            except ValueError:
                print("间隔时间必须为整数（分钟），使用默认值5分钟")
        start_scheduler(interval)

    elif cmd == "add":
        # 用法: python main.py add <buy/sell> <书名> <联系方式>
        if len(sys.argv) < 5:
            print("用法: python main.py add <buy/sell> <书名> <联系方式>")
            print("示例: python main.py add buy '高等数学' '微信: zhangsan'")
            return
        demand_type = sys.argv[2]
        book_name = sys.argv[3]
        contact = sys.argv[4]
        if demand_type not in ["buy", "sell"]:
            print("类型必须是 buy 或 sell")
            return
        demand_id = db.add_demand(demand_type, book_name, contact)
        print(f"✅ 需求已添加！ID: {demand_id}")

        # 添加后立即尝试运行一次匹配（让用户不用等5分钟）
        print("正在尝试快速匹配...")
        from matcher import run_matching
        matches = run_matching()
        if matches:
            print(f"🎉 匹配成功！发现 {len(matches)} 个新匹配，已发送通知。")
        else:
            print("⏳ 未找到匹配，已存入数据库，等待下次定时扫描。")

    elif cmd == "test":
        test_llm()

    elif cmd == "help":
        show_help()

    else:
        print(f"未知命令: {cmd}")
        show_help()


if __name__ == "__main__":
    main()