# notifier.py
# 通知推送模块 - 匹配成功后发送通知给买卖双方

import smtplib
import requests
from email.mime.text import MIMEText
from email.header import Header
from config import WECOM_WEBHOOK_URL, SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD
from llm_client import call_tju_llm  # 改为导入 call_tju_llm


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
    book = match_record["book_name"]
    buyer = match_record["buy_contact"]
    seller = match_record["sell_contact"]

    # 买家版：只显示卖家联系方式
    buyer_msg = f"📚 您求购的《{book}》有人出售！\n卖家联系方式：{seller}\n\n请尽快联系，祝交易愉快 😊"

    # 卖家版：只显示买家联系方式
    seller_msg = f"📚 您的《{book}》有买家求购！\n买家联系方式：{buyer}\n\n请尽快联系，祝交易愉快 😊"

    print(f"[通知模拟] 买家 {buyer} 应收到：\n{buyer_msg}")
    print(f"[通知模拟] 卖家 {seller} 应收到：\n{seller_msg}")

    return buyer_msg, seller_msg


# 简单的自测代码
if __name__ == "__main__":
    test_match = {
        "buy_contact": "test_buyer@tju.edu.cn",
        "sell_contact": "test_seller@tju.edu.cn",
        "book_name": "高等数学"
    }
    buyer_msg, seller_msg = notify_match(test_match)
    print("\n=== 返回结果 ===")
    print(f"买家版:\n{buyer_msg}")
    print(f"卖家版:\n{seller_msg}")