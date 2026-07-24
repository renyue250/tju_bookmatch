# notifier.py
# 通知推送模块 - 匹配成功后发送通知给买卖双方

import smtplib
import requests
from email.mime.text import MIMEText
from email.header import Header
from config import WECOM_WEBHOOK_URL, SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD
from llm_client import generate_match_message


def send_wecom(content):
    """
    通过企业微信机器人发送消息
    content: 消息文本
    返回: bool 是否成功
    """
    if not WECOM_WEBHOOK_URL:
        print("[通知] 未配置企业微信 Webhook，跳过")
        return False

    try:
        data = {"msgtype": "text", "text": {"content": content}}
        response = requests.post(WECOM_WEBHOOK_URL, json=data, timeout=10)
        if response.status_code == 200:
            print("[通知] 企业微信消息发送成功")
            return True
        else:
            print(f"[通知] 企业微信发送失败，状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"[通知] 企业微信发送异常: {e}")
        return False


def send_email(to_addr, subject, content):
    """
    通过邮件发送通知
    to_addr: 收件人邮箱
    subject: 邮件主题
    content: 邮件正文
    返回: bool 是否成功
    """
    if not SMTP_USER or not SMTP_PASSWORD:
        print("[通知] 未配置邮件服务器，跳过")
        return False

    try:
        msg = MIMEText(content, "plain", "utf-8")
        msg["Subject"] = Header(subject, "utf-8")
        msg["From"] = SMTP_USER
        msg["To"] = to_addr

        # 使用 TLS 加密连接（大多数服务器要求）
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, [to_addr], msg.as_string())
        server.quit()
        print(f"[通知] 邮件发送成功至 {to_addr}")
        return True
    except Exception as e:
        print(f"[通知] 邮件发送失败: {e}")
        return False


def notify_match(match_record):
    """
    发送匹配成功通知（组合了文案生成和发送）
    match_record = {
        'buy_contact': '...',
        'sell_contact': '...',
        'book_name': '...'
    }
    返回: bool 是否至少一种方式发送成功
    """
    book = match_record["book_name"]
    buyer = match_record["buy_contact"]
    seller = match_record["sell_contact"]

    # 1. 生成通知文案（使用大模型，如果失败则使用备用模板）
    message = generate_match_message(book, book, seller)
    if not message:
        message = f"""📚 二手书匹配成功！

您求购的《{book}》有人出售！
卖家联系方式：{seller}

请尽快联系，祝交易愉快 😊
—— 天大二手书智能匹配助手"""

    # 2. 发送给买家（根据联系方式类型选择通道）
    # 简单起见，我们假设联系方式是邮箱或手机号，先统一用邮件
    # 若联系人是邮箱，则发送邮件；若是手机号，则可能通过短信（暂不支持），这里演示用邮件
    # 你也可以根据实际需要添加更多判断

    success = False

    # 尝试邮件（如果联系方式看起来像邮箱）
    if "@" in buyer:
        if send_email(buyer, f"📚 二手书匹配成功：《{book}》", message):
            success = True
    else:
        # 对于手机号或微信号，我们暂时用企业微信发送（如果配置了）
        if WECOM_WEBHOOK_URL:
            # 将消息发送到企业微信（这里发给群，但更好的做法是私聊，需要企业微信应用）
            # 这里简化：在群内@所有人或发送公共消息
            full_msg = f"📚 匹配成功！\n买家：{buyer}\n卖家：{seller}\n书籍：《{book}》\n请双方自行联系。"
            if send_wecom(full_msg):
                success = True
        else:
            # 无通知渠道时，至少打印到控制台（用于演示）
            print(f"\n[通知模拟] 买家 {buyer} 应收到：\n{message}\n")
            success = True

    # 也可以通知卖家（可选）
    seller_msg = f"📚 您的《{book}》有买家求购！\n买家联系方式：{buyer}\n请尽快联系。"
    if "@" in seller:
        send_email(seller, f"📚 您的书籍《{book}》已被求购", seller_msg)
    else:
        print(f"[通知模拟] 卖家 {seller} 应收到：{seller_msg}\n")

    return success


# 简单的自测代码（不使用数据库，直接调用）
if __name__ == "__main__":
    # 测试通知模块
    test_match = {
        "buy_contact": "test_buyer@tju.edu.cn",
        "sell_contact": "test_seller@tju.edu.cn",
        "book_name": "高等数学"
    }
    notify_match(test_match)