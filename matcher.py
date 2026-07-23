# matcher.py
# 匹配引擎 - 从数据库读取需求，调用大模型进行语义匹配

import db
from llm_client import is_same_book


def run_matching():
    """
    执行一轮匹配扫描（从数据库读取未匹配需求）
    返回匹配结果列表，并更新数据库状态
    """
    # 1. 从数据库获取所有未匹配的需求
    all_demands = db.get_unmatched_demands()
    
    if len(all_demands) < 2:
        print("[匹配] 未匹配需求不足，跳过")
        return []
    
    # 2. 分离买和卖
    buy_list = [d for d in all_demands if d["type"] == "buy"]
    sell_list = [d for d in all_demands if d["type"] == "sell"]
    
    if not buy_list or not sell_list:
        print("[匹配] 只有单边需求，等待匹配")
        return []
    
    print(f"[匹配] 当前有 {len(buy_list)} 条买方需求，{len(sell_list)} 条卖方需求")
    
    # 3. 执行匹配逻辑
    new_matches = []
    
    for buy in buy_list:
        for sell in sell_list:
            # 调用大模型判断书名是否匹配
            if is_same_book(buy["book_name"], sell["book_name"]):
                print(f"[匹配] ✅ 匹配成功！买家: {buy['book_name']} ↔ 卖家: {sell['book_name']}")
                
                # 记录匹配结果
                match_record = {
                    "buy_id": buy["id"],
                    "sell_id": sell["id"],
                    "book_name": buy["book_name"],
                    "buy_contact": buy["contact"],
                    "sell_contact": sell["contact"]
                }
                new_matches.append(match_record)
                
                # 更新数据库状态（标记为已匹配）
                db.mark_as_matched(buy["id"])
                db.mark_as_matched(sell["id"])
                
                # 一个买需求匹配一个卖需求后，跳出内层循环
                break
    
    print(f"[匹配] 本轮共发现 {len(new_matches)} 个新匹配")
    return new_matches


# 测试代码（使用数据库中的真实数据）
if __name__ == "__main__":
    print("=" * 40)
    print("测试匹配引擎（从数据库读取数据）")
    print("=" * 40)
    
    # 先确保数据库已初始化
    db.init_db()
    
    # 如果数据库为空，先插入测试数据
    existing = db.get_unmatched_demands()
    if not existing:
        print("数据库为空，插入测试数据...")
        db.add_demand("buy", "高等数学", "test_buyer@tju.edu.cn")
        db.add_demand("sell", "高数", "test_seller@tju.edu.cn")
        db.add_demand("buy", "数据结构", "buyer2@tju.edu.cn")
        db.add_demand("sell", "线性代数", "seller2@tju.edu.cn")
        print("已插入测试数据")
    
    # 执行匹配
    results = run_matching()
    
    # 输出结果
    print("\n匹配结果：")
    for m in results:
        print(f"  📚 《{m['book_name']}》")
        print(f"     买家: {m['buy_contact']}")
        print(f"     卖家: {m['sell_contact']}")
        print()