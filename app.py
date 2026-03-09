import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Superstore BI Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Superstore Business Intelligence Dashboard")
st.caption("Interactive BI dashboard built with Streamlit, Pandas and Plotly")

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv("SuperStoreOrders - SuperStoreOrders.csv")
    return df

df = load_data()

# --------------------------------------------------
# CLEAN COLUMN NAMES
# --------------------------------------------------
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("-", "_")
)

# --------------------------------------------------
# CLEAN NUMERIC COLUMNS
# --------------------------------------------------
numeric_cols = ["sales", "profit", "discount"]

for col in numeric_cols:
    if col in df.columns:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace("$", "", regex=False)
            .str.replace(",", "", regex=False)
            .str.strip()
        )
        df[col] = pd.to_numeric(df[col], errors="coerce")

# --------------------------------------------------
# OPTIONAL DATE CLEANING
# --------------------------------------------------
if "order_date" in df.columns:
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------
st.sidebar.header("Filters")

def build_options(dataframe: pd.DataFrame, column: str) -> list[str]:
    if column not in dataframe.columns:
        return ["All"]
    return ["All"] + sorted(dataframe[column].dropna().astype(str).unique().tolist())

market_options = build_options(df, "market")
country_options = build_options(df, "country")
category_options = build_options(df, "category")
segment_options = build_options(df, "segment")
ship_mode_options = build_options(df, "ship_mode")

selected_market = st.sidebar.selectbox("Market", market_options)
selected_country = st.sidebar.selectbox("Country", country_options)
selected_category = st.sidebar.selectbox("Category", category_options)
selected_segment = st.sidebar.selectbox("Segment", segment_options)
selected_ship_mode = st.sidebar.selectbox("Ship Mode", ship_mode_options)

st.sidebar.markdown("---")
st.sidebar.subheader("Discount Chart Filter")

discount_chart_options = (
    sorted(df["category"].dropna().astype(str).unique().tolist())
    if "category" in df.columns
    else []
)

selected_discount_categories = st.sidebar.multiselect(
    "Select categories for Discount vs Profit",
    discount_chart_options,
    default=discount_chart_options
)

# --------------------------------------------------
# APPLY GLOBAL FILTERS
# --------------------------------------------------
filtered_df = df.copy()

if selected_market != "All" and "market" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["market"] == selected_market]

if selected_country != "All" and "country" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["country"] == selected_country]

if selected_category != "All" and "category" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["category"] == selected_category]

if selected_segment != "All" and "segment" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["segment"] == selected_segment]

if selected_ship_mode != "All" and "ship_mode" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["ship_mode"] == selected_ship_mode]

# --------------------------------------------------
# APPLY FILTERS FOR DISCOUNT CHART ONLY
# Same filters as above, but WITHOUT the global category filter
# --------------------------------------------------
discount_base_df = df.copy()

if selected_market != "All" and "market" in discount_base_df.columns:
    discount_base_df = discount_base_df[discount_base_df["market"] == selected_market]

if selected_country != "All" and "country" in discount_base_df.columns:
    discount_base_df = discount_base_df[discount_base_df["country"] == selected_country]

if selected_segment != "All" and "segment" in discount_base_df.columns:
    discount_base_df = discount_base_df[discount_base_df["segment"] == selected_segment]

if selected_ship_mode != "All" and "ship_mode" in discount_base_df.columns:
    discount_base_df = discount_base_df[discount_base_df["ship_mode"] == selected_ship_mode]

# --------------------------------------------------
# EMPTY CHECK
# --------------------------------------------------
if filtered_df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# --------------------------------------------------
# KPI
# --------------------------------------------------
total_sales = filtered_df["sales"].sum() if "sales" in filtered_df.columns else 0
total_profit = filtered_df["profit"].sum() if "profit" in filtered_df.columns else 0
avg_discount = filtered_df["discount"].mean() if "discount" in filtered_df.columns else 0
total_orders = filtered_df["order_id"].nunique() if "order_id" in filtered_df.columns else len(filtered_df)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", f"${total_sales:,.0f}")
col2.metric("Total Profit", f"${total_profit:,.0f}")
col3.metric("Avg Discount", f"{avg_discount:.2%}")
col4.metric("Total Orders", f"{total_orders:,}")

st.divider()

# --------------------------------------------------
# GEOGRAPHIC PERFORMANCE
# --------------------------------------------------
st.header("Geographic Performance")

col1, col2 = st.columns(2)

if "market" in filtered_df.columns and "sales" in filtered_df.columns:
    market_sales = (
        filtered_df.groupby("market", as_index=False)["sales"]
        .sum()
        .sort_values("sales", ascending=False)
    )

    fig_market = px.bar(
        market_sales,
        x="market",
        y="sales",
        text="sales",
        title="Sales by Market"
    )
    fig_market.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
    fig_market.update_layout(
        xaxis_title="Market",
        yaxis_title="Sales"
    )
    col1.plotly_chart(fig_market, use_container_width=True)
else:
    col1.info("Market data not available.")

if "country" in filtered_df.columns and "sales" in filtered_df.columns:
    country_sales = (
        filtered_df.groupby("country", as_index=False)["sales"]
        .sum()
        .sort_values("sales", ascending=False)
        .head(15)
    )

    fig_country = px.bar(
        country_sales,
        x="country",
        y="sales",
        text="sales",
        title="Top Countries by Sales"
    )
    fig_country.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
    fig_country.update_layout(
        xaxis_title="Country",
        yaxis_title="Sales",
        xaxis_tickangle=-35
    )
    col2.plotly_chart(fig_country, use_container_width=True)
else:
    col2.info("Country data not available.")

st.divider()

# --------------------------------------------------
# PRODUCT PERFORMANCE
# --------------------------------------------------
st.header("Product Performance")

col1, col2 = st.columns(2)

if "category" in filtered_df.columns and "sales" in filtered_df.columns:
    category_sales = (
        filtered_df.groupby("category", as_index=False)["sales"]
        .sum()
        .sort_values("sales", ascending=False)
    )

    fig_cat = px.bar(
        category_sales,
        x="category",
        y="sales",
        text="sales",
        title="Sales by Category"
    )
    fig_cat.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
    fig_cat.update_layout(
        xaxis_title="Category",
        yaxis_title="Sales"
    )
    col1.plotly_chart(fig_cat, use_container_width=True)
else:
    col1.info("Category data not available.")

if "sub_category" in filtered_df.columns and "profit" in filtered_df.columns:
    sub_profit = (
        filtered_df.groupby("sub_category", as_index=False)["profit"]
        .sum()
        .sort_values("profit", ascending=False)
        .head(10)
    )

    fig_sub = px.bar(
        sub_profit,
        x="sub_category",
        y="profit",
        text="profit",
        title="Top 10 Sub-Categories by Profit"
    )
    fig_sub.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
    fig_sub.update_layout(
        xaxis_title="Sub-Category",
        yaxis_title="Profit",
        xaxis_tickangle=-35
    )
    col2.plotly_chart(fig_sub, use_container_width=True)
else:
    col2.info("Sub-category data not available.")

st.divider()

# --------------------------------------------------
# DISCOUNT IMPACT
# --------------------------------------------------
st.header("Discount Impact on Profitability")

discount_df = discount_base_df.dropna(subset=["sales", "profit", "discount", "category"]).copy()
discount_df = discount_df[discount_df["sales"] > 0]

if selected_discount_categories:
    discount_df = discount_df[
        discount_df["category"].isin(selected_discount_categories)
    ]
else:
    discount_df = discount_df.iloc[0:0]

if not discount_df.empty:
    fig_discount = px.scatter(
        discount_df,
        x="discount",
        y="profit",
        color="category",
        hover_data=["sales", "profit", "discount"],
        title="Discount vs Profit"
    )

    fig_discount.update_traces(
        marker=dict(
            size=9,
            opacity=0.65,
            line=dict(width=1, color="black")
        )
    )

    fig_discount.update_layout(
        xaxis_title="Discount",
        yaxis_title="Profit",
        legend_title="Category",
        height=550,
        plot_bgcolor="white"
    )

    fig_discount.update_xaxes(
        showgrid=True,
        gridcolor="lightgray",
        dtick=0.1
    )

    fig_discount.update_yaxes(
        showgrid=True,
        gridcolor="lightgray"
    )

    st.plotly_chart(fig_discount, use_container_width=True)
else:
    st.info("No valid data available for the selected discount chart categories.")

st.divider()

# --------------------------------------------------
# SHIPPING ANALYSIS
# --------------------------------------------------
st.header("Shipping Analysis")

col1, col2 = st.columns(2)

if "ship_mode" in filtered_df.columns:
    ship_mode_df = filtered_df["ship_mode"].value_counts().reset_index()
    ship_mode_df.columns = ["ship_mode", "count"]

    fig_ship = px.bar(
        ship_mode_df,
        x="ship_mode",
        y="count",
        text="count",
        title="Shipping Mode Usage"
    )
    fig_ship.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
    fig_ship.update_layout(
        xaxis_title="Ship Mode",
        yaxis_title="Number of Orders"
    )
    col1.plotly_chart(fig_ship, use_container_width=True)
else:
    col1.info("Ship mode data not available.")

if "order_priority" in filtered_df.columns:
    priority_df = filtered_df["order_priority"].value_counts().reset_index()
    priority_df.columns = ["order_priority", "count"]

    fig_priority = px.bar(
        priority_df,
        x="order_priority",
        y="count",
        text="count",
        title="Order Priority Distribution"
    )
    fig_priority.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
    fig_priority.update_layout(
        xaxis_title="Order Priority",
        yaxis_title="Number of Orders"
    )
    col2.plotly_chart(fig_priority, use_container_width=True)
else:
    col2.info("Order priority data not available.")

st.divider()

# --------------------------------------------------
# CUSTOMER SEGMENT REVENUE
# --------------------------------------------------
st.header("Customer Segment Revenue")

if "segment" in filtered_df.columns and "sales" in filtered_df.columns:
    segment_sales = (
        filtered_df.groupby("segment", as_index=False)["sales"]
        .sum()
        .sort_values("sales", ascending=False)
    )

    fig_segment = px.bar(
        segment_sales,
        x="segment",
        y="sales",
        text="sales",
        title="Revenue by Customer Segment"
    )
    fig_segment.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
    fig_segment.update_layout(
        xaxis_title="Segment",
        yaxis_title="Revenue"
    )

    st.plotly_chart(fig_segment, use_container_width=True)
else:
    st.info("Segment revenue data not available.")

st.divider()

# --------------------------------------------------
# DATA PREVIEW
# --------------------------------------------------
with st.expander("Show filtered data preview"):
    st.dataframe(filtered_df, use_container_width=True)