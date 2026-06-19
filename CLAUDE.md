# 记账小工具 — CLAUDE.md

## 项目概述
基于 Streamlit + SQLite3 的 Python Web 记账工具，支持账单的增删查和分类统计。

## 技术栈
- Python 3.8.10
- Streamlit 1.28.x（最后一个支持 3.8 的版本）
- SQLite3（标准库）
- pandas（Streamlit 传递依赖，无需单独安装）

## 项目结构

```
finace_cli/
├── app.py              # 主入口：st.set_page_config + 侧边栏导航 + 页面路由
├── database.py         # 数据库层：连接、建表、增删查
├── pages/
│   ├── __init__.py     # 空文件，标识为 Python 包
│   ├── add.py          # 页面1：添加账单（表单）
│   ├── list.py         # 页面2：账单列表（表格 + 筛选 + 删除）
│   └── stats.py        # 页面3：分类统计（卡片 + 柱状图 + 统计表）
├── requirements.txt    # streamlit~=1.28.0
├── finance.db          # SQLite 数据库（运行时自动生成，不提交 git）
└── CLAUDE.md           # 本文件
```

### 模块职责

| 文件 | 职责 | 暴露的函数 |
|------|------|-----------|
| `database.py` | SQLite 操作，不依赖 Streamlit | `init_db()`, `add_transaction()`, `get_transactions()`, `delete_transaction()`, `get_stats()`, `get_months()` |
| `pages/add.py` | 添加账单表单 UI | `render_add_page()` |
| `pages/list.py` | 账单列表、筛选、删除 UI | `render_list_page()` |
| `pages/stats.py` | 统计卡片、柱状图、统计表 UI | `render_stats_page()` |
| `app.py` | 组装入口，调用各页面函数 | — |

## 数据库设计

```sql
CREATE TABLE IF NOT EXISTS transactions (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    amount   REAL    NOT NULL,
    category TEXT    NOT NULL,
    date     TEXT    NOT NULL,   -- YYYY-MM-DD 格式，便于 strftime 按月筛选
    notes    TEXT    DEFAULT ''
);
```

## 预设分类

```python
CATEGORIES = ["餐饮", "交通", "购物", "娱乐", "居住", "其他"]
```

## 页面设计

### 导航
`st.sidebar.radio("导航", ["添加账单", "账单列表", "分类统计"])` 三页切换。

### 页面1：添加账单
- `st.form` 包裹输入控件（金额 / 分类下拉 / 日期选择 / 备注）
- 提交校验：金额 > 0，分类有效
- 调用 `database.add_transaction()` 写入 SQLite

### 页面2：账单列表
- 两列筛选：月份下拉（从数据库查去重月份）+ 分类下拉
- `st.dataframe()` 展示表格，中文列名
- 汇总行：总条数 + 总支出
- 删除：`st.number_input` 输入 ID + `st.button` 确认 → `database.delete_transaction()`

### 页面3：分类统计
- 三列 `st.metric`：总账单数 / 总支出 / 平均每笔
- `st.bar_chart()`：分类 vs 金额柱状图
- `st.dataframe()`：统计表（分类 / 总金额 / 笔数 / 占比%）

## 如何运行

```bash
# 首次：创建虚拟环境 + 安装依赖
python -m venv venv
venv\Scripts\pip install -r requirements.txt

# 每次启动
venv\Scripts\streamlit run app.py
```

## 编码约定
- 所有用户可见文字使用中文
- 变量名、函数名、注释使用英文
- database.py 不引入 streamlit，保持纯逻辑层
- 页面函数统一命名为 `render_xxx_page()`
- 各页面通过 `database.py` 的函数访问数据，不直接写 SQL

## 实现状态

- [ ] database.py
- [ ] pages/__init__.py
- [ ] pages/add.py
- [ ] pages/list.py
- [ ] pages/stats.py
- [ ] app.py
- [ ] requirements.txt
