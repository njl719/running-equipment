import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# 全局配置（解决中文乱码和页面布局）
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False
st.set_page_config(
    page_title="跑步装备智能管理平台",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 内置你的演示数据（直接用你截图里的装备数据）
@st.cache_data
def load_demo_data():
    # 用户数据
    user_data = pd.DataFrame({
        "username": ["test"],
        "password": ["123456"],
        "height": [175.0],
        "weight": [70.0],
        "budget": [500.0],
        "scene": ["公路"]
    })
    
    # 你的装备数据（和你桌面版完全一致）
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

    # 新增运动记录数据
    sports_data = pd.DataFrame({
        "sport_id": [1, 2, 3],
        "username": ["test", "test", "test"],
        "equip_id": [1, 1, 2],
        "date": ["2026-06-05", "2026-06-08", "2026-06-10"],
        "distance": [5.2, 6.5, 8.2],
        "pace": ["5:30", "5:12", "4:58"],
        "heart_rate": [142, 146, 151],
        "duration": [28, 34, 41]
    })
    
    return user_data, equip_data, sports_data

# 初始化登录状态
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.current_user = None

# ------------------- 登录页面 -------------------
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #2c3e50;'>🏃 跑步装备智能管理与推荐平台</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #7f8c8d; margin-bottom: 50px;'>Python程序设计课程设计成果</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.subheader("用户登录")
        username = st.text_input("用户名", value="test", placeholder="请输入用户名")
        password = st.text_input("密码", type="password", value="123456", placeholder="请输入密码")
        
        if st.button("登录", type="primary", use_container_width=True):
            user_data, _, _ = load_demo_data()
            if (username in user_data["username"].values 
                and password == user_data[user_data["username"] == username]["password"].values[0]):
                st.session_state.logged_in = True
                st.session_state.current_user = username
                st.rerun()
            else:
                st.error("❌ 用户名或密码错误！")

# ------------------- 主界面 -------------------
else:
    # 侧边栏
    st.sidebar.title(f"👤 欢迎, {st.session_state.current_user}")
    st.sidebar.divider()
    if st.sidebar.button("退出登录", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()
    
    # 标签页导航（现在4个标签页都完整了）
    tab1, tab2, tab3, tab4 = st.tabs(["📦 装备生命周期管理", "🎯 个性化智能推荐", "📊 数据可视化分析", "🏃 运动记录管理"])
    
    _, equip_data, sports_data = load_demo_data()
    user_equips = equip_data[equip_data["username"] == st.session_state.current_user]
    user_sports = sports_data[sports_data["username"] == st.session_state.current_user]

    # ------------------- 标签页1：装备管理 -------------------
    with tab1:
        st.header("装备全生命周期管理")
        st.dataframe(user_equips, use_container_width=True, height=200)
        
        st.divider()
        col1, col2 = st.columns([1, 2])
        
        with col1:
            selected_equip = st.selectbox("选择装备查看详情", user_equips["name"])
            equip = user_equips[user_equips["name"] == selected_equip].iloc[0]
            
            st.subheader("装备基本信息")
            st.metric("装备名称", equip["name"])
            st.write(f"**品牌：** {equip['brand']}")
            st.write(f"**类型：** {equip['type']}")
            st.write(f"**购买价格：** ¥{equip['price']}")
            st.write(f"**购买日期：** {equip['buy_date']}")
            st.write(f"**适用场景：** {equip['fit_scene']}")
        
        with col2:
            st.subheader("使用状态")
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("累计里程", f"{equip['mileage']} km")
            with col_b:
                st.metric("磨损程度", equip["wear"])
            
            if equip['type'] == "跑鞋":
                remaining = max(0, 800 - equip['mileage'])
                st.metric("剩余使用寿命", f"{remaining:.1f} km")
                if remaining < 200:
                    st.warning("⚠️ 装备磨损严重，建议尽快更换！")
                elif remaining < 400:
                    st.info("ℹ️ 注意检查装备磨损情况")
            
            if st.button("生成磨损曲线", type="primary", use_container_width=True) and equip['type'] == "跑鞋":
                with st.spinner("正在生成图表..."):
                    fig, ax = plt.subplots(figsize=(10, 6))
                    mileage_points = np.linspace(0, 800, 100)
                    cushion_decay = 100 * np.exp(-0.0015 * mileage_points)
                    
                    ax.plot(mileage_points, cushion_decay, "b-", linewidth=2, label="理论缓震性能")
                    ax.axhline(y=60, color="orange", linestyle="--", label="预警阈值(60%)")
                    ax.axhline(y=30, color="red", linestyle="--", label="更换阈值(30%)")
                    
                    current_cushion = 100 * np.exp(-0.0015 * equip['mileage'])
                    ax.scatter([equip['mileage']], [current_cushion], color="red", s=150, zorder=5,
                              label=f"当前状态: {current_cushion:.1f}%")
                    
                    ax.set_title(f"{equip['brand']} {equip['name']} - 缓震性能衰减曲线", fontsize=14)
                    ax.set_xlabel("累计使用里程(km)", fontsize=12)
                    ax.set_ylabel("缓震性能剩余(%)", fontsize=12)
                    ax.set_ylim(0, 105)
                    ax.legend()
                    ax.grid(True, alpha=0.3)
                    
                    st.pyplot(fig)

    # ------------------- 标签页2：智能推荐 -------------------
    with tab2:
        st.header("个性化装备推荐")
        user_data, _, _ = load_demo_data()
        user_info = user_data[user_data["username"] == st.session_state.current_user].iloc[0]
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("单件装备预算", f"¥{user_info['budget']}")
        with col2:
            st.metric("日常跑步场景", user_info["scene"])
        
        st.divider()
        if st.button("一键智能推荐", type="primary", use_container_width=True):
            with st.spinner("正在为您推荐合适的装备..."):
                # 装备库
                equip_database = [
                    {"name": "赤兔7 Pro", "brand": "李宁", "type": "跑鞋", "price": 399, "fit_scene": "公路"},
                    {"name": "跑步腰包", "brand": "耐克", "type": "配件", "price": 129, "fit_scene": "通用"},
                    {"name": "速干上衣", "brand": "安德玛", "type": "服装", "price": 199, "fit_scene": "通用"},
                    {"name": "运动护膝", "brand": "李宁", "type": "配件", "price": 89, "fit_scene": "通用"}
                ]
                
                # 筛选推荐
                recommendations = []
                for equip in equip_database:
                    if equip["price"] <= user_info['budget'] and (equip["fit_scene"] == user_info['scene'] or equip["fit_scene"] == "通用"):
                        recommendations.append({
                            "装备名称": equip["name"],
                            "品牌": equip["brand"],
                            "品类": equip["type"],
                            "价格": f"¥{equip['price']}",
                            "推荐理由": f"售价¥{equip['price']}，低于您¥{user_info['budget']}的预算；适配{user_info['scene']}跑步场景"
                        })
                
                st.success(f"✅ 为您找到 {len(recommendations)} 款合适的装备")
                st.dataframe(pd.DataFrame(recommendations), use_container_width=True, height=300)

    # ------------------- 标签页3：数据可视化 -------------------
    with tab3:
        st.header("装备数据可视化分析")
        chart_type = st.selectbox("选择图表类型", ["装备分类占比", "装备里程统计", "磨损程度分布"])
        
        with st.spinner("正在生成图表..."):
            fig, ax = plt.subplots(figsize=(10, 6))
            
            if chart_type == "装备分类占比":
                type_counts = user_equips["type"].value_counts()
                ax.pie(type_counts.values, labels=type_counts.index, autopct="%1.1f%%", startangle=90, colors=["#3498db", "#2ecc71", "#f39c12"])
                ax.set_title("装备分类占比统计", fontsize=14)
            
            elif chart_type == "装备里程统计":
                bars = ax.bar(user_equips["name"], user_equips["mileage"], color="#3498db")
                ax.set_title("各装备累计使用里程", fontsize=14)
                ax.set_ylabel("累计里程(km)", fontsize=12)
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height, f"{height:.1f}km", ha="center", va="bottom", fontsize=11)
            
            elif chart_type == "磨损程度分布":
                wear_counts = user_equips["wear"].value_counts()
                color_map = {"轻微": "#2ecc71", "正常": "#f39c12", "严重": "#e74c3c"}
                bars = ax.bar(wear_counts.index, wear_counts.values, color=[color_map[w] for w in wear_counts.index])
                ax.set_title("装备磨损程度分布", fontsize=14)
                ax.set_ylabel("装备数量", fontsize=12)
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height, f"{int(height)}件", ha="center", va="bottom", fontsize=11)
            
            st.pyplot(fig)

    # ------------------- 标签页4：运动记录管理（新增完整内容） -------------------
    with tab4:
        st.header("运动记录管理")
        
        # 运动记录表格
        st.subheader("我的运动记录")
        # 关联装备名称
        display_sports = user_sports.merge(
            equip_data[["equip_id", "brand", "name"]], 
            on="equip_id", 
            how="left"
        )
        display_sports["使用装备"] = display_sports["brand"] + " " + display_sports["name"]
        display_sports = display_sports[["sport_id", "date", "使用装备", "distance", "pace", "heart_rate", "duration"]]
        display_sports.columns = ["记录ID", "日期", "使用装备", "距离(km)", "平均配速", "平均心率", "时长(分钟)"]
        
        st.dataframe(display_sports, use_container_width=True, height=250)
        
        st.divider()
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("运动统计")
            total_distance = user_sports["distance"].sum()
            total_duration = user_sports["duration"].sum()
            avg_heart_rate = user_sports["heart_rate"].mean()
            
            col_a, col_b, col_c = st.columns(3)
            col_a.metric("总跑量", f"{total_distance:.1f} km")
            col_b.metric("总时长", f"{total_duration} 分钟")
            col_c.metric("平均心率", f"{avg_heart_rate:.0f} 次/分")
        
        with col2:
            st.subheader("运动趋势")
            if st.button("生成运动统计图表", type="primary", use_container_width=True):
                with st.spinner("正在生成图表..."):
                    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
                    
                    # 每日跑量趋势
                    user_sports["date"] = pd.to_datetime(user_sports["date"])
                    daily_distance = user_sports.groupby("date")["distance"].sum()
                    
                    ax1.plot(daily_distance.index, daily_distance.values, "o-", color="#2ecc71", linewidth=2)
                    ax1.set_title("每日跑步距离趋势", fontsize=14)
                    ax1.set_ylabel("距离(km)", fontsize=12)
                    ax1.grid(True, alpha=0.3)
                    
                    # 心率与配速对比
                    ax3 = ax2.twinx()
                    
                    ax2.plot(user_sports["date"], user_sports["heart_rate"], "r-", label="平均心率", linewidth=2)
                    ax3.plot(user_sports["date"], user_sports["duration"]/user_sports["distance"], "b-", label="平均配速", linewidth=2)
                    
                    ax2.set_title("心率与配速变化趋势", fontsize=14)
                    ax2.set_ylabel("心率(次/分)", fontsize=12, color="red")
                    ax3.set_ylabel("配速(min/km)", fontsize=12, color="blue")
                    ax2.tick_params(axis="y", labelcolor="red")
                    ax3.tick_params(axis="y", labelcolor="blue")
                    
                    lines1, labels1 = ax2.get_legend_handles_labels()
                    lines2, labels2 = ax3.get_legend_handles_labels()
                    ax2.legend(lines1 + lines2, labels1 + labels2, loc="upper left")
                    
                    plt.tight_layout()
                    st.pyplot(fig)
