# scheduler.py
# 定时调度模块 - 定时执行匹配任务

import schedule
import time
from matcher import run_matching
from notifier import notify_match


def scheduled_match_job():
    """定时匹配任务：执行匹配，并处理新匹配结果"""
    print(f"\n[定时任务] {time.strftime('%Y-%m-%d %H:%M:%S')} 开始执行匹配")
    matches = run_matching()
    if matches:
        print(f"[定时任务] 发现 {len(matches)} 个新匹配，发送通知...")
        for match in matches:
            notify_match(match)
    else:
        print("[定时任务] 未发现新匹配")
    print("[定时任务] 本次执行结束\n")


def start_scheduler(interval_minutes=5):
    """
    启动定时调度器
    interval_minutes: 执行间隔（分钟），默认5分钟
    """
    # 设置定时任务
    schedule.every(interval_minutes).minutes.do(scheduled_match_job)

    # 立即执行一次（启动时先跑一次）
    print(f"[调度器] 启动，每 {interval_minutes} 分钟执行一次匹配")
    scheduled_match_job()

    # 持续循环
    try:
        while True:
            schedule.run_pending()
            time.sleep(30)  # 每30秒检查一次是否有任务需要执行
    except KeyboardInterrupt:
        print("\n[调度器] 收到停止信号，正在退出...")
        print("[调度器] 已停止")


if __name__ == "__main__":
    # 直接运行此文件可启动调度器（默认5分钟间隔）
    start_scheduler()