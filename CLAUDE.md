# 记账小工具 — CLAUDE.md

## 项目概述
基于 Streamlit + SQLite3 的 Python Web 记账工具，支持账单的增删查和分类统计。

## 技术栈
- Python 3.8.10
- Streamlit 1.28.x（最后一个支持 3.8 的版本）
- SQLite3（标准库）
- pandas（Streamlit 传递依赖，统计页面直接使用）

## 项目结构

```
finace_cli/
├── app.py                    # 主入口 + 首页：st.set_page_config + 侧边栏 + 总览卡片 + 最近账单
├── database.py               # 数据库层：连接、建表、增删查
├── pages/
│   ├── __init__.py           # 空文件，标识为 Python 包
│   ├── 01_添加账单.py         # 页面1：添加账单（表单）
│   ├── 02_账单列表.py         # 页面2：账单列表（表格 + 筛选 + 删除）
│   └── 03_分类统计.py         # 页面3：分类统计（卡片 + 柱状图 + 统计表）
├── requirements.txt          # streamlit~=1.28.0
├── finance.db                # SQLite 数据库（运行时自动生成，不提交 git）
└── CLAUDE.md                 # 本文件
```

### 模块职责

| 文件 | 职责 | 备注 |
|------|------|------|
| `database.py` | SQLite 操作，不依赖 Streamlit | `init_db()`, `add_transaction()`, `get_transactions()`, `delete_transaction()`, `get_stats()`, `get_months()` |
| `pages/01_添加账单.py` | 添加账单表单 UI | Streamlit 原生页面，模块级代码直接执行 |
| `pages/02_账单列表.py` | 账单列表、筛选、删除 UI | 同上 |
| `pages/03_分类统计.py` | 统计卡片、柱状图、统计表 UI | 同上，直接 import pandas |
| `app.py` | 配置 + 首页（总览卡片、最近5条账单） | `init_db()` 在此调用，数据库在启动时初始化 |

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
Streamlit 原生多页面导航：`pages/` 目录下的文件自动注册为页面，文件名前缀 `01_`/`02_`/`03_` 控制顺序。侧边栏显示页面标题和导航。

### 首页（app.py）
- 三列 `st.metric`：总账单数 / 总支出 / 涉及分类数
- `st.dataframe()`：最近 5 条账单

### 页面1：添加账单（01_添加账单.py）
- `st.form("add_form", clear_on_submit=True)` 包裹输入控件
- 提交校验：金额 <= 0 时报错
- 调用 `database.add_transaction()` 写入 SQLite，成功后显示账单 ID
- 导入：`from database import CATEGORIES, add_transaction`

### 页面2：账单列表（02_账单列表.py）
- 两列筛选：月份下拉（`get_months()`）+ 分类下拉（`CATEGORIES`）
- `st.dataframe()` 展示表格，`column_config` 配置中文列名和金额格式
- 汇总行：`st.caption()` 显示总条数 + 总支出
- 无数据时显示 `st.info()` 提示
- 删除：`st.number_input` 输入 ID + `st.button("确认删除")` → `database.delete_transaction()`，成功后 `st.rerun()`
- 导入：`from database import CATEGORIES, delete_transaction, get_months, get_transactions`

### 页面3：分类统计（03_分类统计.py）
- 三列 `st.metric`：总账单数 / 总支出 / 平均每笔
- `st.bar_chart()`：分类 vs 金额柱状图（用 pandas DataFrame 构建）
- `st.dataframe()`：统计表（分类 / 总金额 / 笔数 / 占比%），`column_config` 配置金额格式
- 无数据时显示 `st.info()` 提示
- 导入：`import pandas as pd` + `from database import get_stats`

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
- 各页面通过 `database.py` 的函数访问数据，不直接写 SQL
- 页面文件使用 Streamlit 原生多页面模式（模块级执行，无需函数封装）
- 数据库在 `app.py` 启动时通过 `init_db()` 自动初始化，无需手动建表

## 实现状态

- [x] database.py
- [x] pages/__init__.py
- [x] pages/01_添加账单.py
- [x] pages/02_账单列表.py
- [x] pages/03_分类统计.py
- [x] app.py
- [x] requirements.txt
