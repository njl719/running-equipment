import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# ------------------- 全局配置 -------------------
st.set_page_config(
    page_title="跑步装备智能管理平台",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------- 数据初始化 -------------------
def init_session_data():
    """初始化会话数据，支持动态增删改"""
    if "users" not in st.session_state:
        st.session_state.users = pd.DataFrame({
            "username": ["test"],
            "password": ["123456"],
            "height": [175.0],
            "weight": [70.0],
            "budget": [500.0],
            "scene": ["公路"]
        })
    
    if "equips" not in st.session_state:
        st.session_state.equips = pd.DataFrame({
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
    
    if "sports" not in st.session_state:
        st.session_state.sports = pd.DataFrame({
            "sport_id": [1, 2, 3],
            "username": ["test", "test", "test"],
            "equip_id": [1, 1, 2],
            "date": ["2026-06-05", "2026-06-08", "2026-06-10"],
            "distance": [5.2, 6.5, 8.2],
            "pace": ["5:30", "5:12", "4:58"],
            "heart_rate": [142, 146, 151],
            "duration": [28, 34, 41]
        })

# 初始化数据
init_session_data()

# ------------------- 登录注册系统 -------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.session_state.show_register = False

# 登录/注册页面
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #2c3e50;'>🏃 跑步装备智能管理与推荐平台</h1>", unsafe_allow_html=True)
    st.markdown("<div style='margin-bottom: 70px;'></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if not st.session_state.show_register:
            st.subheader("用户登录")
            username = st.text_input("用户名", value="test", placeholder="请输入用户名", key="login_username")
            password = st.text_input("密码", type="password", value="123456", placeholder="请输入密码", key="login_password")
            
            col_login, col_register = st.columns(2)
            with col_login:
                if st.button("登录", type="primary", use_container_width=True, key="login_btn"):
                    users = st.session_state.users
                    if (username in users["username"].values 
                        and password == users[users["username"] == username]["password"].values[0]):
                        st.session_state.logged_in = True
                        st.session_state.current_user = username
                        st.rerun()
                    else:
                        st.error("❌ 用户名或密码错误！")
            
            with col_register:
                if st.button("注册新账号", use_container_width=True, key="goto_register_btn"):
                    st.session_state.show_register = True
                    st.rerun()
        
        else:
            st.subheader("用户注册")
            new_username = st.text_input("新用户名", placeholder="请输入用户名", key="reg_username")
            new_password = st.text_input("新密码", type="password", placeholder="请输入密码（6-12位）", key="reg_password")
            confirm_password = st.text_input("确认密码", type="password", placeholder="请再次输入密码", key="reg_confirm_pwd")
            
            col_back, col_submit = st.columns(2)
            with col_back:
                if st.button("返回登录", use_container_width=True, key="back_login_btn"):
                    st.session_state.show_register = False
                    st.rerun()
            
            with col_submit:
                if st.button("提交注册", type="primary", use_container_width=True, key="submit_register_btn"):
                    if not new_username or not new_password:
                        st.error("❌ 用户名和密码不能为空！")
                    elif new_password != confirm_password:
                        st.error("❌ 两次输入的密码不一致！")
                    elif len(new_password) < 6 or len(new_password) > 12:
                        st.error("❌ 密码长度必须在6-12位之间！")
                    elif new_username in st.session_state.users["username"].values:
                        st.error("❌ 用户名已存在！")
                    else:
                        # 添加新用户
                        new_user = pd.DataFrame({
                            "username": [new_username],
                            "password": [new_password],
                            "height": [None],
                            "weight": [None],
                            "budget": [500.0],
                            "scene": ["公路"]
                        })
                        st.session_state.users = pd.concat([st.session_state.users, new_user], ignore_index=True)
                        st.success("✅ 注册成功！请返回登录")
                        st.session_state.show_register = False

# ------------------- 主界面 -------------------
else:
    # 侧边栏
    st.sidebar.title(f"👤 欢迎, {st.session_state.current_user}")
    st.sidebar.divider()
    if st.sidebar.button("退出登录", use_container_width=True, key="logout_btn"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.rerun()
    
    # 标签页导航
    tab1, tab2, tab3, tab4 = st.tabs(["📦 装备生命周期管理", "🎯 个性化智能推荐", "📊 数据可视化分析", "🏃 运动记录管理"])
    
    current_user = st.session_state.current_user
    user_equips = st.session_state.equips[st.session_state.equips["username"] == current_user]
    user_sports = st.session_state.sports[st.session_state.sports["username"] == current_user]

    # ------------------- 标签页1：装备生命周期管理 -------------------
    with tab1:
        st.header("装备全生命周期管理")
        
        # 操作按钮区
        col_add, col_edit, col_delete = st.columns(3)
        with col_add:
            with st.expander("➕ 添加新装备"):
                with st.form("add_equip_form"):
                    name = st.text_input("装备名称*", key="add_equip_name")
                    equip_type = st.selectbox("装备类型", ["跑鞋", "运动手表", "腰包", "运动服", "其他"], key="add_equip_type")
                    brand = st.text_input("品牌", key="add_equip_brand")
                    price = st.number_input("购买价格(元)", min_value=0.0, step=0.1, key="add_equip_price")
                    buy_date = st.date_input("购买日期", value=datetime.now(), key="add_equip_date")
                    mileage = st.number_input("初始里程(km)", min_value=0.0, step=0.1, key="add_equip_mileage")
                    fit_scene = st.selectbox("适用场景", ["公路", "山地", "越野", "田径场", "通用"], key="add_equip_scene")
                    
                    if st.form_submit_button("提交添加", type="primary", key="add_equip_submit"):
                        if not name:
                            st.error("装备名称不能为空！")
                        else:
                            new_id = st.session_state.equips["equip_id"].max() + 1 if not st.session_state.equips.empty else 1
                            wear = "轻微" if mileage < 200 else "正常" if mileage < 600 else "严重"
                            
                            new_equip = pd.DataFrame({
                                "equip_id": [new_id],
                                "username": [current_user],
                                "name": [name],
                                "type": [equip_type],
                                "brand": [brand or "未知"],
                                "price": [price],
                                "buy_date": [str(buy_date)],
                                "mileage": [mileage],
                                "wear": [wear],
                                "fit_scene": [fit_scene]
                            })
                            st.session_state.equips = pd.concat([st.session_state.equips, new_equip], ignore_index=True)
                            st.success("✅ 装备添加成功！")
                            st.rerun()
        
        with col_edit:
            with st.expander("✏️ 修改装备"):
                if user_equips.empty:
                    st.info("暂无装备可修改")
                else:
                    edit_equip_id = st.selectbox("选择要修改的装备", user_equips["equip_id"], 
                                               format_func=lambda x: f"{x} - {user_equips[user_equips['equip_id']==x]['name'].iloc[0]}",
                                               key="edit_equip_select")
                    equip_to_edit = user_equips[user_equips["equip_id"] == edit_equip_id].iloc[0]
                    
                    with st.form("edit_equip_form"):
                        new_name = st.text_input("装备名称", value=equip_to_edit["name"], key="edit_equip_name")
                        new_type = st.selectbox("装备类型", ["跑鞋", "运动手表", "腰包", "运动服", "其他"], 
                                              index=["跑鞋", "运动手表", "腰包", "运动服", "其他"].index(equip_to_edit["type"]),
                                              key="edit_equip_type")
                        new_brand = st.text_input("品牌", value=equip_to_edit["brand"], key="edit_equip_brand")
                        new_price = st.number_input("购买价格(元)", value=equip_to_edit["price"], key="edit_equip_price")
                        new_buy_date = st.date_input("购买日期", value=datetime.strptime(equip_to_edit["buy_date"], "%Y-%m-%d"), key="edit_equip_date")
                        new_mileage = st.number_input("累计里程(km)", value=equip_to_edit["mileage"], key="edit_equip_mileage")
                        new_scene = st.selectbox("适用场景", ["公路", "山地", "越野", "田径场", "通用"],
                                               index=["公路", "山地", "越野", "田径场", "通用"].index(equip_to_edit["fit_scene"]),
                                               key="edit_equip_scene")
                        
                        if st.form_submit_button("提交修改", type="primary", key="edit_equip_submit"):
                            idx = st.session_state.equips[st.session_state.equips["equip_id"] == edit_equip_id].index[0]
                            new_wear = "轻微" if new_mileage < 200 else "正常" if new_mileage < 600 else "严重"
                            
                            st.session_state.equips.loc[idx, "name"] = new_name
                            st.session_state.equips.loc[idx, "type"] = new_type
                            st.session_state.equips.loc[idx, "brand"] = new_brand
                            st.session_state.equips.loc[idx, "price"] = new_price
                            st.session_state.equips.loc[idx, "buy_date"] = str(new_buy_date)
                            st.session_state.equips.loc[idx, "mileage"] = new_mileage
                            st.session_state.equips.loc[idx, "wear"] = new_wear
                            st.session_state.equips.loc[idx, "fit_scene"] = new_scene
                            
                            st.success("✅ 装备信息修改成功！")
                            st.rerun()
        
        with col_delete:
            with st.expander("🗑️ 删除装备"):
                if user_equips.empty:
                    st.info("暂无装备可删除")
                else:
                    delete_equip_id = st.selectbox("选择要删除的装备", user_equips["equip_id"],
                                                  format_func=lambda x: f"{x} - {user_equips[user_equips['equip_id']==x]['name'].iloc[0]}",
                                                  key="delete_equip_select")
                    if st.button("确认删除", type="primary", use_container_width=True, key="delete_equip_btn"):
                        st.session_state.equips = st.session_state.equips[st.session_state.equips["equip_id"] != delete_equip_id]
                        st.success("✅ 装备删除成功！")
                        st.rerun()
        
        st.divider()
        st.subheader("我的装备列表")
        st.dataframe(user_equips, use_container_width=True, height=200)
        
        st.divider()
        col1, col2 = st.columns([1, 2])
        
        with col1:
            if not user_equips.empty:
                selected_equip = st.selectbox("选择装备查看详情", user_equips["name"], key="detail_equip_select")
                equip = user_equips[user_equips["name"] == selected_equip].iloc[0]
                
                st.subheader("装备基本信息")
                st.metric("装备名称", equip["name"])
                st.write(f"**品牌：** {equip['brand']}")
                st.write(f"**类型：** {equip['type']}")
                st.write(f"**购买价格：** ¥{equip['price']}")
                st.write(f"**购买日期：** {equip['buy_date']}")
                st.write(f"**适用场景：** {equip['fit_scene']}")
        
        with col2:
            if not user_equips.empty:
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
                
                if st.button("生成磨损曲线", type="primary", use_container_width=True, key="wear_curve_btn") and equip['type'] == "跑鞋":
                    with st.spinner("正在生成图表..."):
                        # Streamlit原生折线图，100%中文支持
                        mileage_points = np.linspace(0, 800, 100)
                        cushion_decay = 100 * np.exp(-0.0015 * mileage_points)
                        
                        chart_data = pd.DataFrame({
                            "累计使用里程(km)": mileage_points,
                            "理论缓震性能(%)": cushion_decay
                        })
                        
                        st.subheader(f"{equip['brand']} {equip['name']} - 缓震性能衰减曲线")
                        st.line_chart(chart_data, x="累计使用里程(km)", y="理论缓震性能(%)", use_container_width=True)
                        
                        st.info(f"当前状态：缓震性能剩余 {100 * np.exp(-0.0015 * equip['mileage']):.1f}%")
                        st.info("预警阈值：60% | 更换阈值：30%")

    # ------------------- 标签页2：个性化智能推荐 -------------------
    with tab2:
        st.header("个性化装备推荐")
        user_info = st.session_state.users[st.session_state.users["username"] == current_user].iloc[0]
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("单件装备预算", f"¥{user_info['budget']}")
        with col2:
            st.metric("日常跑步场景", user_info["scene"])
        
        st.divider()
        if st.button("一键智能推荐", type="primary", use_container_width=True, key="recommend_btn"):
            with st.spinner("正在为您推荐合适的装备..."):
                equip_database = [
                    {"name": "赤兔7 Pro", "brand": "李宁", "type": "跑鞋", "price": 399, "fit_scene": "公路"},
                    {"name": "飞马40", "brand": "耐克", "type": "跑鞋", "price": 599, "fit_scene": "公路"},
                    {"name": "跑步腰包", "brand": "耐克", "type": "配件", "price": 129, "fit_scene": "通用"},
                    {"name": "速干上衣", "brand": "安德玛", "type": "服装", "price": 199, "fit_scene": "通用"},
                    {"name": "运动护膝", "brand": "李宁", "type": "配件", "price": 89, "fit_scene": "通用"}
                ]
                
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

    # ------------------- 标签页3：数据可视化分析（全部改用Streamlit原生图表） -------------------
    with tab3:
        st.header("装备数据可视化分析")
        chart_type = st.selectbox("选择图表类型", ["装备分类占比", "装备里程统计", "磨损程度分布"], key="chart_type_select")
        
        if not user_equips.empty:
            with st.spinner("正在生成图表..."):
                if chart_type == "装备分类占比":
                    type_counts = user_equips["type"].value_counts().reset_index()
                    type_counts.columns = ["装备类型", "数量"]
                    st.subheader("装备分类占比统计")
                    st.pie_chart(type_counts, values="数量", names="装备类型", use_container_width=True)
                
                elif chart_type == "装备里程统计":
                    mileage_data = user_equips[["name", "mileage"]].rename(columns={"name": "装备名称", "mileage": "累计里程(km)"})
                    st.subheader("各装备累计使用里程")
                    st.bar_chart(mileage_data, x="装备名称", y="累计里程(km)", use_container_width=True, color="#3498db")
                
                elif chart_type == "磨损程度分布":
                    wear_counts = user_equips["wear"].value_counts().reset_index()
                    wear_counts.columns = ["磨损程度", "数量"]
                    st.subheader("装备磨损程度分布")
                    st.bar_chart(wear_counts, x="磨损程度", y="数量", use_container_width=True, color=["#2ecc71", "#f39c12", "#e74c3c"])
        else:
            st.info("暂无装备数据，无法生成图表")

    # ------------------- 标签页4：运动记录管理 -------------------
    with tab4:
        st.header("运动记录管理")
        
        # 操作按钮区
        col_add_sport, col_delete_sport = st.columns(2)
        with col_add_sport:
            with st.expander("➕ 添加运动记录"):
                with st.form("add_sport_form"):
                    sport_date = st.date_input("运动日期", value=datetime.now(), key="add_sport_date")
                    if user_equips.empty:
                        st.info("请先添加装备才能记录运动")
                        submit_disabled = True
                    else:
                        use_equip = st.selectbox("使用装备", user_equips["equip_id"],
                                               format_func=lambda x: f"{x} - {user_equips[user_equips['equip_id']==x]['name'].iloc[0]}",
                                               key="add_sport_equip")
                        submit_disabled = False
                    
                    distance = st.number_input("跑步距离(km)", min_value=0.1, step=0.1, key="add_sport_distance")
                    pace = st.text_input("平均配速(min/km)", placeholder="例如: 5:30", key="add_sport_pace")
                    heart_rate = st.number_input("平均心率(次/分)", min_value=60, max_value=220, step=1, key="add_sport_hr")
                    duration = st.number_input("运动时长(分钟)", min_value=1, step=1, key="add_sport_duration")
                    
                    if st.form_submit_button("提交添加", type="primary", disabled=submit_disabled, key="add_sport_submit"):
                        if not pace:
                            st.error("平均配速不能为空！")
                        else:
                            new_id = st.session_state.sports["sport_id"].max() + 1 if not st.session_state.sports.empty else 1
                            
                            new_sport = pd.DataFrame({
                                "sport_id": [new_id],
                                "username": [current_user],
                                "equip_id": [use_equip],
                                "date": [str(sport_date)],
                                "distance": [distance],
                                "pace": [pace],
                                "heart_rate": [heart_rate],
                                "duration": [duration]
                            })
                            st.session_state.sports = pd.concat([st.session_state.sports, new_sport], ignore_index=True)
                            
                            # 同步更新装备里程
                            equip_idx = st.session_state.equips[st.session_state.equips["equip_id"] == use_equip].index[0]
                            st.session_state.equips.loc[equip_idx, "mileage"] += distance
                            total_mileage = st.session_state.equips.loc[equip_idx, "mileage"]
                            st.session_state.equips.loc[equip_idx, "wear"] = "轻微" if total_mileage < 200 else "正常" if total_mileage < 600 else "严重"
                            
                            st.success("✅ 运动记录添加成功！装备里程已同步更新")
                            st.rerun()
        
        with col_delete_sport:
            with st.expander("🗑️ 删除运动记录"):
                if user_sports.empty:
                    st.info("暂无运动记录可删除")
                else:
                    delete_sport_id = st.selectbox("选择要删除的记录", user_sports["sport_id"],
                                                  format_func=lambda x: f"{x} - {user_sports[user_sports['sport_id']==x]['date'].iloc[0]}",
                                                  key="delete_sport_select")
                    if st.button("确认删除", type="primary", use_container_width=True, key="delete_sport_btn"):
                        st.session_state.sports = st.session_state.sports[st.session_state.sports["sport_id"] != delete_sport_id]
                        st.success("✅ 运动记录删除成功！")
                        st.rerun()
        
        st.divider()
        st.subheader("我的运动记录")
        if not user_sports.empty:
            # 关联装备名称
            display_sports = user_sports.merge(
                user_equips[["equip_id", "brand", "name"]], 
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
                if st.button("生成运动统计图表", type="primary", use_container_width=True, key="sport_chart_btn"):
                    with st.spinner("正在生成图表..."):
                        # 每日跑量趋势
                        user_sports["date"] = pd.to_datetime(user_sports["date"])
                        daily_data = user_sports.groupby("date").agg({
                            "distance": "sum",
                            "heart_rate": "mean"
                        }).reset_index()
                        
                        # 转换配速为数值
                        pace_values = []
                        for p in user_sports["pace"]:
                            m, s = p.split(":")
                            pace_values.append(float(m) + float(s)/60)
                        daily_data["平均配速(min/km)"] = pace_values
                        daily_data = daily_data.rename(columns={"distance": "距离(km)", "heart_rate": "平均心率(次/分)"})
                        
                        st.subheader("每日跑步距离趋势")
                        st.line_chart(daily_data, x="date", y="距离(km)", use_container_width=True, color="#2ecc71")
                        
                        st.subheader("心率与配速变化趋势")
                        col_chart1, col_chart2 = st.columns(2)
                        with col_chart1:
                            st.line_chart(daily_data, x="date", y="平均心率(次/分)", use_container_width=True, color="#e74c3c")
                        with col_chart2:
                            st.line_chart(daily_data, x="date", y="平均配速(min/km)", use_container_width=True, color="#3498db")
        else:
            st.info("暂无运动记录，点击上方按钮添加第一条记录吧！")
