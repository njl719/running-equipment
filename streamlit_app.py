import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# 配置
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False
st.set_page_config(page_title="跑步装备智能管理平台", layout="wide")


# 内置演示数据
@st.cache_data
def load_default_data():
    user_data = pd.DataFrame({
        "username": ["test"],
        "password": ["123456"],
        "height": [175.0],
        "weight": [70.0],
        "budget": [500.0],
        "scene": ["公路"]
    })

    equip_data = pd.DataFrame({
        "equip_id": [1, 2, 3, 4],
        "username": ["test", "test", "test", "test"],
        "name": ["赤兔", "飞马40", "波士顿11", "oppo watch3"],
        "type": ["跑鞋", "跑鞋", "跑鞋", "运动手表"],
        "brand": ["李宁", "nike", "阿迪达斯", "oppo"],
        "price": [328.0, 599.0, 899.0, 2500.0],
        "buy_date": ["2026-01-04", "2026-06-11", "2025-06-20", "2025-06-06"],
        "mileage": [137.0, 60.0, 200.0, 0.0],
        "wear": ["轻微", "轻微", "正常", "轻微"],
        "fit_scene": ["公路", "公路", "公路", "通用"]
    })

    return user_data, equip_data


# 登录状态
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.current_user = None

# 登录页面
if not st.session_state.logged_in:
    st.title("🏃 跑步装备智能管理与推荐平台")
    st.subheader("请登录")

    username = st.text_input("用户名", value="test")
    password = st.text_input("密码", type="password", value="123456")

    if st.button("登录", type="primary"):
        user_data, _ = load_default_data()
        if username in user_data["username"].values and password == \
                user_data[user_data["username"] == username]["password"].values[0]:
            st.session_state.logged_in = True
            st.session_state.current_user = username
            st.rerun()
        else:
            st.error("用户名或密码错误")

# 主界面
else:
    st.sidebar.title(f"欢迎, {st.session_state.current_user}")
    if st.sidebar.button("退出登录"):
        st.session_state.logged_in = False
        st.rerun()

    tab1, tab2, tab3, tab4 = st.tabs(["装备管理", "智能推荐", "数据可视化", "运动记录"])

    _, equip_data = load_default_data()
    user_equips = equip_data[equip_data["username"] == st.session_state.current_user]

    with tab1:
        st.header("装备生命周期管理")
        st.dataframe(user_equips, use_container_width=True)

        selected_equip = st.selectbox("选择装备查看详情", user_equips["name"])
        equip = user_equips[user_equips["name"] == selected_equip].iloc[0]

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("装备基本信息")
            st.write(f"**品牌：** {equip['brand']}")
            st.write(f"**类型：** {equip['type']}")
            st.write(f"**购买价格：** ¥{equip['price']}")
            st.write(f"**购买日期：** {equip['buy_date']}")

        with col2:
            st.subheader("使用状态")
            st.write(f"**累计里程：** {equip['mileage']}km")
            st.write(f"**磨损程度：** {equip['wear']}")
            st.write(f"**适用场景：** {equip['fit_scene']}")

            if equip['type'] == "跑鞋":
                remaining = max(0, 800 - equip['mileage'])
                st.metric("剩余寿命", f"{remaining:.1f}km")
                if remaining < 200:
                    st.warning("⚠️ 建议尽快更换！")

        if st.button("生成磨损曲线", type="primary") and equip['type'] == "跑鞋":
            fig, ax = plt.subplots(figsize=(10, 6))
            mileage_points = np.linspace(0, 800, 100)
            cushion_decay = 100 * np.exp(-0.0015 * mileage_points)

            ax.plot(mileage_points, cushion_decay, "b-", linewidth=2, label="理论缓震性能")
            ax.axhline(y=60, color="orange", linestyle="--", label="预警阈值(60%)")
            ax.axhline(y=30, color="red", linestyle="--", label="更换阈值(30%)")

            current_cushion = 100 * np.exp(-0.0015 * equip['mileage'])
            ax.scatter([equip['mileage']], [current_cushion], color="red", s=100, zorder=5,
                       label=f"当前状态: {current_cushion:.1f}%")

            ax.set_title(f"{equip['brand']} {equip['name']} - 缓震性能衰减曲线")
            ax.set_xlabel("累计使用里程(km)")
            ax.set_ylabel("缓震性能剩余(%)")
            ax.legend()
            ax.grid(True, alpha=0.3)

            st.pyplot(fig)

    with tab2:
        st.header("个性化装备推荐")
        user_data, _ = load_default_data()
        user_info = user_data[user_data["username"] == st.session_state.current_user].iloc[0]

        st.write(f"**当前预算：** ¥{user_info['budget']}")
        st.write(f"**常用场景：** {user_info['scene']}")

        if st.button("一键智能推荐", type="primary"):
            equip_database = [
                {"name": "赤兔7 Pro", "brand": "李宁", "type": "跑鞋", "price": 399, "fit_scene": "公路"},
                {"name": "跑步腰包", "brand": "耐克", "type": "配件", "price": 129, "fit_scene": "通用"},
                {"name": "速干上衣", "brand": "安德玛", "type": "服装", "price": 199, "fit_scene": "通用"}
            ]

            recommendations = []
            for equip in equip_database:
                if equip["price"] <= user_info['budget'] and (
                        equip["fit_scene"] == user_info['scene'] or equip["fit_scene"] == "通用"):
                    recommendations.append({
                        "装备名称": equip["name"],
                        "品牌": equip["brand"],
                        "品类": equip["type"],
                        "价格": f"¥{equip['price']}",
                        "推荐理由": f"售价¥{equip['price']}，低于您¥{user_info['budget']}的预算；适配{user_info['scene']}跑步场景"
                    })

            st.dataframe(pd.DataFrame(recommendations), use_container_width=True)

    with tab3:
        st.header("数据可视化分析")
        chart_type = st.selectbox("选择图表类型", ["装备分类占比", "装备里程统计", "磨损程度分布"])

        fig, ax = plt.subplots(figsize=(10, 6))

        if chart_type == "装备分类占比":
            type_counts = user_equips["type"].value_counts()
            ax.pie(type_counts.values, labels=type_counts.index, autopct="%1.1f%%", startangle=90)
            ax.set_title("装备分类占比统计")

        elif chart_type == "装备里程统计":
            bars = ax.bar(user_equips["name"], user_equips["mileage"], color="#3498db")
            ax.set_title("各装备累计使用里程")
            ax.set_ylabel("累计里程(km)")
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2., height, f"{height:.1f}km", ha="center", va="bottom")

        elif chart_type == "磨损程度分布":
            wear_counts = user_equips["wear"].value_counts()
            bars = ax.bar(wear_counts.index, wear_counts.values,
                          color=["#2ecc71", "#f39c12", "#e74c3c"][:len(wear_counts)])
            ax.set_title("装备磨损程度分布")
            ax.set_ylabel("装备数量")
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2., height, f"{int(height)}件", ha="center", va="bottom")

        st.pyplot(fig)