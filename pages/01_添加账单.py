"""添加账单页面"""

from datetime import date

import streamlit as st

from database import CATEGORIES, add_transaction

st.header("💰 添加账单")

with st.form("add_form", clear_on_submit=True):
    amount = st.number_input("金额（元）", min_value=0.01, step=0.01, format="%.2f")
    category = st.selectbox("分类", CATEGORIES)
    trans_date = st.date_input("日期", value=date.today())
    notes = st.text_input("备注", placeholder="选填")

    submitted = st.form_submit_button("提交")

    if submitted:
        if amount <= 0:
            st.error("金额必须大于 0")
        else:
            trans_id = add_transaction(
                amount=amount,
                category=category,
                date=trans_date.strftime("%Y-%m-%d"),
                notes=notes.strip(),
            )
            st.success(f"添加成功！账单 ID：{trans_id}")
