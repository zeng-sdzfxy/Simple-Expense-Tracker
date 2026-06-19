"""账单列表页面——筛选、查看、删除"""

import streamlit as st

from database import CATEGORIES, delete_transaction, get_months, get_transactions

st.header("📋 账单列表")

# ---- filters ----
months = get_months()
col1, col2 = st.columns(2)
month = col1.selectbox("月份", ["全部"] + months, key="filter_month")
category = col2.selectbox("分类", ["全部"] + CATEGORIES, key="filter_category")

# ---- load data ----
rows = get_transactions(
    month=None if month == "全部" else month,
    category=None if category == "全部" else category,
)

if not rows:
    st.info("暂无账单数据，请先在「添加账单」页面添加。")
else:
    # summary
    total_amount = sum(r["amount"] for r in rows)
    st.caption(f"共 **{len(rows)}** 条记录，总支出 **¥{total_amount:,.2f}**")

    # table
    st.dataframe(
        rows,
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

# ---- delete ----
st.divider()
st.subheader("🗑 删除账单")

del_id = st.number_input("输入要删除的账单 ID", min_value=1, step=1)
if st.button("确认删除"):
    affected = delete_transaction(del_id)
    if affected > 0:
        st.success(f"已删除 ID 为 {del_id} 的账单")
        st.rerun()
    else:
        st.warning(f"未找到 ID 为 {del_id} 的账单")
