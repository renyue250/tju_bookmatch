# config.py
# 天津大学校内词元服务配置
# 后续登录 https://ai.tju.edu.cn 获取API Key后填入

LLM_API_URL = "https://ai.tju.edu.cn/api/agent2026/gitlab-49-agent2026-gl-bot/chat/completions"
LLM_API_KEY = "tk-JJZUrL90R8oY4Uj6YcWa4QmPfTC7K-7BUgu5JfuFybhaDROS"
LLM_MODEL = "tju-llm"

# ========== 企业微信机器人配置 ==========
# 在企业微信群中添加机器人后获取 Webhook URL
WECOM_WEBHOOK_URL = ""  # 例如: "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxx"

# ========== 邮件服务器配置（使用学校邮箱或其它） ==========
SMTP_SERVER = "smtp.tju.edu.cn"   # 天津大学邮箱 SMTP 服务器
SMTP_PORT = 587                  # TLS 端口
SMTP_USER = "renyue06@tju.edu.cn"   # 你的学校邮箱
SMTP_PASSWORD = "#ATJT4jCcTJx#J4J"       # 邮箱授权码（不是登录密码）