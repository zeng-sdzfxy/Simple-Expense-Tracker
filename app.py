"""💰 记账小工具 — 首页"""

import streamlit as st

from database import get_stats, get_transactions, init_db

# ---- app config ----
st.set_page_config(page_title="💰 记账小工具", page_icon="💰", layout="wide")

# ---- init database ----
init_db()

# ---- sidebar ----
st.sidebar.title("💰 记账小工具")

# ---- home page ----
st.title("💰 记账小工具")
st.caption("一个简单的个人账本，帮你记录每一笔开销。")

# quick summary
transactions = get_transactions()
stats = get_stats()

if transactions:
    total_amount = sum(r["amount"] for r in transactions)
    total_count = len(transactions)

    c1, c2, c3 = st.columns(3)
    c1.metric("总账单数", total_count)
    c2.metric("总支出", f"¥{total_amount:,.2f}")
    c3.metric("涉及分类", f"{len(stats)} 个")

    st.divider()
    st.subheader("最近 5 条账单")
    recent = transactions[:5]
    st.dataframe(
        recent,
        column_config={
            "id": "ID",
            "amount": st.column_config.NumberColumn("金额", format="¥%.2f"),
            "category": "分类",
            "date": "日期",
            "notes": "备注",
        },
        column_order=["id", "amount", "category", "date", "notes"],
        use_container_width=True,
        hide_index=True,
    )
else:
    st.info("还没有账单记录，去「添加账单」页面开始记账吧！")
