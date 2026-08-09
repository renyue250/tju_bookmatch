import streamlit as st
import db
from matcher import run_matching
from notifier import notify_match

# --- 页面设置 ---
st.set_page_config(page_title="天大二手书智能匹配", page_icon="📚", layout="centered")
st.title("📚 天大二手书智能匹配助手")
st.caption("让你的闲置书找到新主人")

# 初始化数据库
db.init_db()

# 初始化 session_state，用于存储匹配结果
if "match_result" not in st.session_state:
    st.session_state.match_result = None

# --- 显示匹配结果（如果有） ---
if st.session_state.match_result:
    st.success("🎉 匹配结果：")
    for match in st.session_state.match_result:
        st.write(f"- 书籍：《{match['book_name']}》，买家：{match['buy_contact']}，卖家：{match['sell_contact']}")
    # 清除结果，避免下次重复显示
    # st.session_state.match_result = None


# --- 主界面：添加新需求 ---
st.subheader("📝 发布你的需求")
with st.form("add_demand_form"):
    col1, col2 = st.columns(2)
    with col1:
        demand_type = st.selectbox("需求类型", ["buy", "sell"], format_func=lambda x: "求购" if x == "buy" else "出售")
    with col2:
        book_name = st.text_input("书名", placeholder="例如：高等数学")
    contact = st.text_input("联系方式", placeholder="微信号 / 手机号 / 邮箱")

    submitted = st.form_submit_button("📤 发布需求")

    if submitted:
        if not book_name or not contact:
            st.error("请完整填写书名和联系方式！")
        else:
            # 添加需求
            new_id = db.add_demand(demand_type, book_name, contact)
            st.success(f"✅ 需求已添加 (ID: {new_id})！正在尝试匹配...")

            # 只执行一次匹配，不重复执行
            matches = run_matching()
            if matches:
                st.balloons()
                st.session_state.match_result = matches
                for match in matches:
                    st.success(f"🎉 匹配成功！《{match['book_name']}》")
                    # 发送通知，并获取通知内容
                    buyer_msg, seller_msg = notify_match(match)
                    st.info(f"📧 给买家的通知：\n{buyer_msg}")
                    st.info(f"📧 给卖家的通知：\n{seller_msg}")
            else:
                st.info("⏳ 暂未找到匹配，已加入等待队列。")