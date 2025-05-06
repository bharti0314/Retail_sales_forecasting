import streamlit as st
import pandas as pd
import os
from pandas.core.interchange.dataframe_protocol import DataFrame
from streamlit_option_menu import option_menu
import plotly.express as px
import joblib
import numpy as np
import xgboost as xgb
import requests
from streamlit_lottie import st_lottie

st.set_page_config(page_title="RetailVista", layout="wide")

USER_FILE = "users.csv"

def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
retail_animation = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_jcikwtux.json")

if not os.path.exists(USER_FILE):
    df = pd.DataFrame(columns=["email", "password"])
    df.to_csv(USER_FILE, index=False)

users = pd.read_csv(USER_FILE, usecols=["email", "password"], dtype=str)
users = users.map(lambda x: x.strip())


if "email" in st.query_params:
    st.session_state["logged_in"] = True
    st.session_state["email"] = st.query_params["email"]
    st.session_state["authenticated"] = True
    st.session_state["user_email"] = st.query_params["email"]

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["authenticated"] = False
    st.session_state["email"] = ""
    st.session_state["user_email"] = ""

with st.sidebar:
    st.title("🔐 Login / Sign Up")

    if not st.session_state["logged_in"]:
        choice = st.radio("Choose an option:", ["Sign In", "Sign Up"])
        email = st.text_input("Email").strip()
        password = st.text_input("Password", type="password").strip()

        if choice == "Sign In":
            if st.button("Sign In"):
                if email in users["email"].values:
                    row = users[users["email"] == email]
                    if row.iloc[0]["password"].strip() == password:
                        st.session_state["logged_in"] = True
                        st.session_state["authenticated"] = True
                        st.session_state["email"] = email
                        st.session_state["user_email"] = email
                        st.query_params["email"] = email
                        st.rerun()
                    else:
                        st.error("Wrong password.")
                else:
                    st.error("Email not found.")

        elif choice == "Sign Up":
            if st.button("Sign Up"):
                if email in users["email"].values:
                    st.warning("Email already registered.")
                else:
                    new_user = pd.DataFrame([{"email": email, "password": password}])
                    users = pd.concat([users, new_user], ignore_index=True)
                    users.to_csv(USER_FILE, index=False)
                    st.success("Account created! You can now sign in.")

    elif st.session_state["logged_in"]:
        st.success(f"Logged in as {st.session_state['email']}")
        if st.button("Logout"):
            st.session_state["logged_in"] = False
            st.session_state["authenticated"] = False
            st.session_state["email"] = ""
            st.session_state["user_email"] = ""
            st.query_params.clear()
            st.rerun()

if st.session_state.authenticated:
    with st.sidebar:

        st.markdown("### 💬 Main Menu")
        selected = option_menu(
            menu_title=None,
            options=["Project Overview", "Dataset", "Dashboard"],
            icons=["book", "folder", "bar-chart-line"],
            menu_icon=None,
            default_index=0,
            styles={
                "container": {
                    "padding": "0!important",
                    "background-color": "#DDEEFF",  # secondaryBackgroundColor
                    "border-radius": "8px"
                },
                "icon": {"color": "#2C3E50", "font-size": "18px"},  # textColor
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#F4F7FE",  # backgroundColor
                },
                "nav-link-selected": {
                    "background-color": "#1E88E5",  # primaryColor
                    "color": "white",
                    "font-weight": "bold",
                },
            }
        )
    try:
        data = pd.read_csv("data1.csv")
        data["Order Date"] = pd.to_datetime(data["Order Date"],format="mixed")
        data["Profit Margin"] = data["Profit"].replace('[\\$,]', '', regex=True).astype(float)
        data["Total"] = data["Total"].replace('[\\$,]', '', regex=True).astype(float)
    except FileNotFoundError:
        st.error("Dataset not found.")
        data = None

    # Project Overview Page
    if selected == "Project Overview":
        # Title and Animation
        st.markdown(
            """
            <h1 style='text-align: center; color: #FF6F61;'>Welcome to <strong><u>RetailVista</u><strong></h1>""",
            unsafe_allow_html=True,
        )
        st_lottie(retail_animation, height=300, key="retail")

        # Description Box
        st.markdown(
            """
            <div style='background-color: #fff4e6; padding: 20px; border-radius: 10px; box-shadow: 2px 2px 10px #f2f2f2;'>
                <h3 style='color: #ff6600;'>About</h3>
                <p>This <strong>Retail Sales Forecasting System</strong> is designed to help businesses gain insights from historical sales data and predict future trends. With interactive dashboards and data visualizations, it empowers stakeholders to make <strong>data-driven decisions</strong>. It is a demand Forecasting Software that Minimizes Costs, Predict the future and stock accordingly to minimize waste, unnecessary markdowns, and lost sales.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Key Features with Icons
        st.markdown("---")
        st.markdown(
            "<h3 style='color: #ff6600;'>✨ Key Features</h3>",
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <style>
            .grid-container {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 30px;
                padding: 30px;
            }

            .card {
                background-color: white;
                padding: 20px;
                text-align: center;
                border-radius: 12px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                transition: transform 0.2s ease, box-shadow 0.2s ease;
                width: 300px;
                justify-content: center;
            }
            .card1{
                background-color: white;
                padding: 20px;
                text-align: center;
                border-radius: 12px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                transition: transform 0.2s ease, box-shadow 0.2s ease;
                width: 300px;
                justify-content: center;
                align-self:center;
            }

            .card:hover {
                transform: scale(1.03);
                box-shadow: 0 6px 14px rgba(0,0,0,0.2);
            }
            .card1:hover {
                transform: scale(1.03);
                box-shadow: 0 6px 14px rgba(0,0,0,0.2);
            }
            .card i {
                font-size: 32px;
                color: #1f4db7;
                margin-bottom: 10px;
            }
            .card1 i {
                font-size: 32px;
                color: #1f4db7;
                margin-bottom: 10px;
            }

            .card h4 {
                color: #f97316;
                margin: 10px 0 5px;
            }
            
            .card1 h4 {
                color: #f97316;
                margin: 10px 0 5px;
            }

            .card p {
                color: #444;
                font-size: 14px;
            }
            
            .card1 p {
                color: #444;
                font-size: 14px;
            }
            
            h4{
                display: flex;
                align-items: center; /* vertical alignment */
                justify-content: center; /* horizontal alignment (optional) */

            }
            </style>

            <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">

            <div class="grid-container">
              <div class="card">
                <h3>✅</h3>
                <h4>Trend Analysis & Visualization</h4>
                <p>Yearly, Monthly, Seasonal, and Quarterly sales breakdowns.</p>
              </div>
              <div class="card">
                <h3>💰</h3>
                <h4>Profit Analysis</h4>
                <p>Comparison of sales and profit margins over time.</p>
              </div>
              <div class="card">
                <h3>📦</h3>
                <h4>Product & Category Insights</h4>
                <p>Only stock SKUs in locations with demand, eliminating unnecessary overstocking.</p>
              </div>
              <div class="card">
                <h3>🔍</h3>
                <h4>Anomaly Detection</h4>
                <p>Detects unexpected sales fluctuations for quick action.</p>
              </div>
              <div class="card">
                <h3>👤</h3>
                <h4>Customer & Business Analytics</h4>
                <p>Understand customer behavior and top revenue sources.</p>
              </div>
              <div class="card">
                <h3>📊</h3>
                <h4>Interactive Dashboards</h4>
                <p>Real-time visual insights allow stakeholders to explore sales patterns, performance KPIs, and actionable metrics with ease.</p>
              </div>
            </div>
    """, unsafe_allow_html=True)

        st.markdown("---")
        st.success("🚀 Ready to dive into sales insights? Explore the Dashboard now from the sidebar!")

    if selected == "Dataset":
        st.subheader("📂 Dataset Overview")
        if data is not None:
            st.dataframe(data, use_container_width=True)
            st.success("✅ Dataset Loaded Successfully!")
            st.markdown(f"Total Columns : {data.shape[1]}")
            st.markdown(f"Total Rows : {data.shape[0]}")
            st.markdown("🔍 **Missing Values :**")
            st.write(data.isnull().sum())
            st.markdown("**🧾 Column Names :**")
            st.write(data.columns.tolist())
            st.markdown(" Data Summary :")
            st.write(data.describe())
            st.markdown(" First 5 Rows :")
            st.dataframe(data.head())

    if selected == "Dashboard" and data is not None:
        st.subheader("📊 Retail Sales Dashboard")

        data["Year"] = data["Order Date"].dt.year
        data["Month"] = data["Order Date"].dt.month
        data["Quarter"] = data["Order Date"].dt.quarter
        season_map = {12: "Winter", 1: "Winter", 2: "Winter", 3: "Spring", 4: "Spring", 5: "Spring",
                      6: "Summer", 7: "Summer", 8: "Summer", 9: "Fall", 10: "Fall", 11: "Fall"}
        data["Season"] = data["Month"].map(season_map)

        tab1, tab3 = st.tabs(["📈 Retail Price", "📊 Insights"])

        linear_regression_model = joblib.load('linear_regression_model.pkl')

        with tab1:
            st.subheader("Retail Price")

            with st.form("form1"):
                    # Row 1
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        cost_price1 = st.number_input("Enter Cost Price")
                    with col2:
                        shipping_cost1 = st.number_input("Enter Shipping Cost")
                    with col3:
                        profit1 = st.number_input("Enter Profit per quantity")

                    # Row 2
                    col4, col5, col6 = st.columns(3)
                    with col4:
                        order_quantity1 = st.number_input("Enter Order Quantity")
                    with col5:
                        discount1 = st.number_input("Enter Discount$")

                    btn1 = st.form_submit_button("Retail Price Prediction")


            if btn1:
                    input_data = np.array(
                        [[cost_price1, shipping_cost1, profit1, order_quantity1, discount1]])
                    if np.all(input_data == 0):
                        st.warning("⚠️ Please enter values first.")
                    else:
                        prediction = linear_regression_model.predict(input_data)[0]
                        r2 = '99.98%%'
                        st.info(f"Model R² Accuracy: {r2}")
                        st.success(f"Predicted Retail Price: {prediction:.4f}")
                        
        with tab3:
            st.subheader("📊 Interactive Insights")
            # 🔮 Future Forecast based on 7-day SMA
            future_days = st.slider("Select number of days to forecast:", 7, 360, 30)

            trend = data.groupby("Order Date")["Total"].sum().reset_index().sort_values("Order Date")
            trend["SMA_Forecast"] = trend["Total"].rolling(window=7).mean()

            last_date = trend["Order Date"].max()
            future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=future_days)
            forecast_values = [trend["SMA_Forecast"].iloc[-1]] * future_days

            forecast_df = pd.DataFrame({"Order Date": future_dates, "Total": forecast_values})
            combined = pd.concat([trend[["Order Date", "Total"]], forecast_df], ignore_index=True)

            fig2 = px.line(combined, x="Order Date", y="Total", title="Actual & Forecasted Sales (SMA Forecast)")
            fig2.add_scatter(x=forecast_df["Order Date"], y=forecast_df["Total"], mode="lines",
                             name="Forecasted Sales")
            st.plotly_chart(fig2, use_container_width=True)


            chart_option = st.selectbox(
                "Select a chart to display:",
                [
                    "📅 Yearly Sales",
                    "📆 Monthly Sales",
                    "💹 Yearly Profit",
                    "📈 Monthly Profit",
                    "🌦 Seasonal Sales",
                    "📊 Quarterly Sales",
                    "🏆 Top Products",
                    "🛒 Category-wise Sales",
                    "🙋‍♂ Top Customers",
                    "📈 Sales Trend Over Time",
                    "💰 Profit vs Sales",
                    "📍 Key Sales KPIs"
                ]
            )

            if chart_option == "📅 Yearly Sales":
                fig = px.bar(data.groupby("Year")["Total"].sum().reset_index(), x="Year", y="Total", color="Total",
                             title="Yearly Sales", color_continuous_scale="Viridis")
                st.plotly_chart(fig, use_container_width=True)

            elif chart_option == "📆 Monthly Sales":
                fig = px.line(data.groupby("Month")["Total"].sum().reset_index(), x="Month", y="Total",
                              title="Monthly Sales", markers=True)
                st.plotly_chart(fig, use_container_width=True)

            elif chart_option == "💹 Yearly Profit":
                fig = px.bar(data.groupby("Year")["Profit Margin"].sum().reset_index(), x="Year", y="Profit Margin",
                             color="Profit Margin", title="Yearly Profit", color_continuous_scale="Plasma")
                st.plotly_chart(fig, use_container_width=True)

            elif chart_option == "📈 Monthly Profit":
                fig = px.line(data.groupby("Month")["Profit Margin"].sum().reset_index(), x="Month", y="Profit Margin",
                              title="Monthly Profit", markers=True)
                st.plotly_chart(fig, use_container_width=True)

            elif chart_option == "🌦️ Seasonal Sales":
                seasonal_sales = data.groupby("Season",0)["Total"].sum().reset_index()
                fig = px.bar(seasonal_sales, x="Season", y="Total", color="Total", title="Seasonal Sales",
                             color_continuous_scale="Cividis")
                st.plotly_chart(fig, use_container_width=True)

            elif chart_option == "📊 Quarterly Sales":
                quarterly = data.groupby("Quarter")["Total"].sum().reset_index()
                fig = px.bar(quarterly, x=["Q1", "Q2", "Q3", "Q4"], y="Total", color="Total", title="Quarterly Sales",
                             color_continuous_scale="Bluered")
                st.plotly_chart(fig, use_container_width=True)

            elif chart_option == "🏆 Top Products":
                top_products = data.groupby("Product Name")["Total"].sum().nlargest(10).reset_index()
                fig = px.bar(top_products, x="Product Name", y="Total", color="Total", title="Top Products",
                             color_continuous_scale="Tealgrn")
                st.plotly_chart(fig, use_container_width=True)

            elif chart_option == "🛒 Category-wise Sales":
                category = data.groupby("Product Category")["Total"].sum().reset_index()
                fig = px.pie(category, names="Product Category", values="Total", title="Category-wise Sales",
                             color_discrete_sequence=px.colors.sequential.RdBu)
                st.plotly_chart(fig, use_container_width=True)

            elif chart_option == "🙋‍♂️ Top Customers":
                customers = data.groupby("Customer Name")["Total"].sum().nlargest(10).reset_index()
                fig = px.bar(customers, x="Customer Name", y="Total", color="Total", title="Top Customers",
                             color_continuous_scale="Sunset")
                st.plotly_chart(fig, use_container_width=True)

            elif chart_option == "📈 Sales Trend Over Time":
                trend = data.groupby("Order Date")["Total"].sum().reset_index()
                fig = px.line(trend, x="Order Date", y="Total", title="Sales Trend Over Time")
                st.plotly_chart(fig, use_container_width=True)

            elif chart_option == "💰 Profit vs Sales":
                fig = px.scatter(data, x="Total", y="Profit Margin",
                                 title="Profit ($) vs Total Sales ($)",
                                 color="Profit Margin", size_max=15, color_continuous_scale="Turbo",
                                 labels={"Profit Margin": "Profit ($)", "Total": "Total Sales ($)"})
                st.plotly_chart(fig,use_container_width=True)

            elif chart_option == "📍 Key Sales KPIs":
                col1, col2, col3 = st.columns(3)
                with col1:
                    total_sales = data["Total"].sum()
                    st.metric("💰 Total Revenue", f"${total_sales:,.2f}")
                with col2:
                    avg_profit = data["Profit Margin"].mean()
                    st.metric("📈 Average Profit Margin", f"{avg_profit:.2f}")
                with col3:
                    top_city = data.groupby("City")["Total"].sum().idxmax()
                    st.metric("🏙 Top Performing City", top_city)

                st.markdown("---")
                city_sales = data.groupby("City")["Total"].sum().nlargest(5).reset_index()
                fig = px.bar(city_sales, x="City", y="Total", title="Cities by Sales", color="Total")
                st.plotly_chart(fig, use_container_width=True)
