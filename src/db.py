# db.py
# 数据存储模块 - 使用 SQLite 管理买/卖需求

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "demands.db")

def get_connection():
    """获取数据库连接"""
    abs_path = os.path.abspath(DB_PATH)
    print(f"数据库路径: {abs_path}")
    conn = sqlite3.connect(abs_path, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """初始化数据表"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS demands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            book_name TEXT NOT NULL,
            contact TEXT NOT NULL,
            matched INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def add_demand(demand_type, book_name, contact):
    """添加一条买/卖需求"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO demands (type, book_name, contact) VALUES (?, ?, ?)",
        (demand_type, book_name.strip(), contact.strip())
    )
    demand_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return demand_id

def get_unmatched_demands():
    """获取所有未匹配的需求"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM demands WHERE matched = 0 ORDER BY created_at")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def mark_as_matched(demand_id):
    """将需求标记为已匹配"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE demands SET matched = 1 WHERE id = ?", (demand_id,))
    conn.commit()
    conn.close()

# 测试代码
if __name__ == "__main__":
    init_db()
    print("数据库初始化完成")
    # 添加一条测试数据
    id1 = add_demand("buy", "高等数学", "test_buyer@tju.edu.cn")
    id2 = add_demand("sell", "高数", "test_seller@tju.edu.cn")
    print(f"已添加测试需求: buy_id={id1}, sell_id={id2}")
    # 查看所有未匹配需求
    all_demands = get_unmatched_demands()
    print(f"当前未匹配需求: {all_demands}")