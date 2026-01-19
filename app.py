import streamlit as st
import pandas as pd
import plotly.express as px

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="Pantry December Dashboard",
    layout="wide"
)

st.title("🥫 Pantry December 2025 Dashboard")

# ==================================================
# LOAD KPI DATA (SINGLE SOURCE OF TRUTH)
# ==================================================
kpi_df = pd.read_excel(
    "data/Pantry_December_2025_Correct_KPI_Data.xlsx"
)

kpi = dict(zip(kpi_df["Metric"], kpi_df["Value"]))

total_customers = int(kpi["Total Customers"])
new_customers = int(kpi["New Customers"])
old_customers = int(kpi["Old Customers"])
total_profit = int(kpi["Gross Profit"])
avg_retention = float(kpi["Average Retention (%)"])

# ==================================================
# LOAD DAILY DATA FOR CHARTS
# ==================================================
daily_customer_df = pd.read_excel(
    "data/Dec_2025_Daily_Pivot_Count.xlsx"
)

retention_df = pd.read_excel(
    "data/Dec_2025_Daily_Retention.xlsx"
)

profit_df = pd.read_excel(
    "data/December_2025_Gross_Profit.xlsx"
)

# ==================================================
# DATE FIX
# ==================================================
daily_customer_df["Date"] = pd.to_datetime(
    daily_customer_df["Date"], errors="coerce", dayfirst=True
)

retention_df["Date"] = pd.to_datetime(
    retention_df["Date"], errors="coerce", dayfirst=True
)

profit_df["Date"] = pd.to_datetime(
    profit_df["Date"], errors="coerce", dayfirst=True
)

# ==================================================
# AUTO COLUMN DETECTION
# ==================================================
daily_count_col = [c for c in daily_customer_df.columns if "count" in c.lower()][0]
retention_col = [c for c in retention_df.columns if "retention" in c.lower()][0]
profit_col = [c for c in profit_df.columns if "profit" in c.lower()][0]

# ==================================================
# KPI CARDS
# ==================================================
k1, k2, k3, k4, k5 = st.columns(5)

k1.metric("👥 Total Customers", total_customers)
k2.metric("🆕 New Customers", new_customers)
k3.metric("♻️ Old Customers", old_customers)
k4.metric("💰 Gross Profit", f"₹ {total_profit:,.0f}")
k5.metric("🔁 Avg Retention", f"{avg_retention}%")

st.markdown("---")

# ==================================================
# NEW vs OLD CUSTOMER PIE CHART
# ==================================================
pie_df = kpi_df[
    kpi_df["Metric"].isin(["New Customers", "Old Customers"])
]

st.subheader("🥧 New vs Old Customers")

fig_pie = px.pie(
    pie_df,
    names="Metric",
    values="Value",
    hole=0.45
)

st.plotly_chart(fig_pie, use_container_width=True)

# ==================================================
# LINE CHARTS
# ==================================================
c1, c2 = st.columns(2)

with c1:
    st.subheader("📈 Daily Gross Profit")
    st.plotly_chart(
        px.line(
            profit_df,
            x="Date",
            y=profit_col,
            markers=True
        ),
        use_container_width=True
    )

with c2:
    st.subheader("🔁 Daily Retention Rate")
    st.plotly_chart(
        px.line(
            retention_df,
            x="Date",
            y=retention_col,
            markers=True
        ),
        use_container_width=True
    )

# ==================================================
# DAILY CUSTOMER COUNT
# ==================================================
st.subheader("👥 Daily Wise Customer Count")

st.plotly_chart(
    px.line(
        daily_customer_df,
        x="Date",
        y=daily_count_col,
        markers=True
    ),
    use_container_width=True
)

# ==================================================
# FOOTER
# ==================================================
st.markdown(
    "<center>📊 YCP Infratech Pantry Dashboard — December 2025</center>",
    unsafe_allow_html=True
)
