"""分类统计页面——卡片、柱状图、统计表"""

import pandas as pd
import streamlit as st

from database import get_stats

st.header("📊 分类统计")

stats = get_stats()

if not stats:
    st.info("暂无数据，请先在「添加账单」页面添加。")
else:
    # ---- summary cards ----
    total_count = sum(r["count"] for r in stats)
    total_amount = sum(r["total"] for r in stats)
    avg_amount = total_amount / total_count if total_count else 0

    c1, c2, c3 = st.columns(3)
    c1.metric("总账单数", total_count)
    c2.metric("总支出", f"¥{total_amount:,.2f}")
    c3.metric("平均每笔", f"¥{avg_amount:,.2f}")

    # ---- bar chart ----
    chart_df = pd.DataFrame(stats).set_index("category")
    st.subheader("各分类支出柱状图")
    st.bar_chart(chart_df["total"])

    # ---- stats table ----
    st.subheader("分类统计表")

    table_data = []
    for r in stats:
        pct = (r["total"] / total_amount * 100) if total_amount else 0
        table_data.append({
            "分类": r["category"],
            "总金额": r["total"],
            "笔数": r["count"],
            "占比": f"{pct:.1f}%",
        })

    st.dataframe(
        table_data,
        column_config={
            "总金额": st.column_config.NumberColumn("总金额", format="¥%.2f"),
        },
        use_container_width=True,
        hide_index=True,
    )
