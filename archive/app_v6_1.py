import streamlit as st
import pandas as pd
import plotly.express as px
import ollama

if "messages" not in st.session_state:
    st.session_state.messages = []
# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="Sales Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)

# =====================================
# LOAD DATA
# =====================================

df = pd.read_csv("data/Sales Data 2.csv")
df = df.drop("Unnamed: 0", axis=1)

# =====================================
# GLOBAL METRICS (DO NOT CHANGE)
# =====================================

global_best_city = (
    df.groupby("City")["Sales"]
    .sum()
    .idxmax()
)

global_most_sold_product = (
    df.groupby("Product")["Quantity Ordered"]
    .sum()
    .idxmax()
)

global_best_month = (
    df.groupby("Month")["Sales"]
    .sum()
    .idxmax()
)

# =====================================
# SIDEBAR FILTERS
# =====================================

st.sidebar.title("🔍 Filters")

city_list = ["All"] + sorted(df["City"].unique().tolist())

selected_city = st.sidebar.selectbox(
    "Select City",
    city_list
)

month_list = ["All"] + sorted(df["Month"].unique().tolist())

selected_month = st.sidebar.selectbox(
    "Select Month",
    month_list
)

filtered_df = df.copy()

if selected_city != "All":
    filtered_df = filtered_df[
        filtered_df["City"] == selected_city
    ]

if selected_month != "All":
    filtered_df = filtered_df[
        filtered_df["Month"] == selected_month
    ]

# =====================================
# TITLE
# =====================================

st.title("📊 Sales Intelligence Dashboard")

st.markdown(
    "Analyze revenue, products, cities and customer buying behavior."
)

# =====================================
# GLOBAL BUSINESS CHAMPIONS
# =====================================

st.subheader("🏅 Global Business Champions")

g1, g2, g3 = st.columns([2, 3, 1])

with g1:
    st.metric(
        "🌆 Best City",
        global_best_city
    )

with g2:
    st.metric(
        "📦 Most Sold Product",
        global_most_sold_product
    )

with g3:
    st.metric(
        "📅 Best Month",
        str(global_best_month)
    )

st.divider()

# =====================================
# FILTERED KPI CALCULATIONS
# =====================================

total_revenue = filtered_df["Sales"].sum()

total_orders = filtered_df["Order ID"].nunique()

top_product = (
    filtered_df.groupby("Product")["Sales"]
    .sum()
    .idxmax()
)

peak_hour = (
    filtered_df.groupby("Hour")["Sales"]
    .sum()
    .idxmax()
)

avg_order_value = total_revenue / total_orders

# =====================================
# CURRENT FILTER ANALYSIS
# =====================================

st.subheader("📈 Current Filter Analysis")

c1, c2, c3, c4, c5 = st.columns([1.5, 1, 2, 1, 1])

with c1:
    st.metric(
        "💰 Revenue",
        f"${total_revenue:,.0f}"
    )

with c2:
    st.metric(
        "📦 Orders",
        f"{total_orders:,}"
    )

with c3:
    st.metric(
        "🏆 Highest Revenue Product",
        top_product
    )

with c4:
    st.metric(
        "⏰ Peak Hour",
        f"{peak_hour}:00"
    )

with c5:
    st.metric(
        "💵 Avg Order Value",
        f"${avg_order_value:.0f}"
    )

st.divider()

# =====================================
# MONTHLY REVENUE TREND
# =====================================

monthly_sales = (
    filtered_df.groupby("Month")["Sales"]
    .sum()
    .reset_index()
)

fig_month = px.line(
    monthly_sales,
    x="Month",
    y="Sales",
    markers=True,
    title="Monthly Revenue Trend"
)

st.plotly_chart(
    fig_month,
    use_container_width=True
)

# =====================================
# PRODUCTS + CITY SECTION
# =====================================

left, right = st.columns(2)

product_sales = (
    filtered_df.groupby("Product")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig_products = px.bar(
    product_sales,
    x="Sales",
    y="Product",
    orientation="h",
    title="Top 10 Products by Revenue"
)

left.plotly_chart(
    fig_products,
    use_container_width=True
)

if selected_city == "All":

    city_sales = (
        filtered_df.groupby("City")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig_city = px.bar(
        city_sales,
        x="Sales",
        y="City",
        orientation="h",
        title="Top Cities by Revenue"
    )

    right.plotly_chart(
        fig_city,
        use_container_width=True
    )

else:

    city_revenue = filtered_df["Sales"].sum()

    city_orders = filtered_df["Order ID"].nunique()

    city_top_product = (
        filtered_df.groupby("Product")["Sales"]
        .sum()
        .idxmax()
    )

    right.subheader("📍 Selected City Insights")

    right.success(
        f"💰 Revenue: ${city_revenue:,.0f}"
    )

    right.info(
        f"📦 Orders: {city_orders:,}"
    )

    right.warning(
        f"🏆 Best Product: {city_top_product}"
    )

# =====================================
# HOURLY SALES
# =====================================

hourly_sales = (
    filtered_df.groupby("Hour")["Sales"]
    .sum()
    .reset_index()
)

fig_hour = px.line(
    hourly_sales,
    x="Hour",
    y="Sales",
    markers=True,
    title="Sales by Hour"
)

st.plotly_chart(
    fig_hour,
    use_container_width=True
)

# =====================================
# BUSINESS INSIGHTS
# =====================================

st.subheader("📌 Key Business Insights")

i1, i2 = st.columns(2)

with i1:

    st.info(
        f"🏆 Highest Revenue Product: {top_product}"
    )

    st.info(
        f"📦 Most Sold Product: {global_most_sold_product}"
    )

with i2:

    st.info(
        f"📅 Best Month Overall: {global_best_month}"
    )

    st.info(
        f"⏰ Peak Sales Hour: {peak_hour}:00"
    )
# =====================================
# QUICK INSIGHTS
# =====================================

st.divider()

st.subheader("📌 Quick Insights")

city_label = selected_city if selected_city != "All" else "All Cities"

insight_text = f"""
### Business Summary

✅ {city_label} generated **${total_revenue:,.0f}** in revenue.

✅ Total orders placed: **{total_orders:,}**

✅ Highest revenue product: **{top_product}**

✅ Peak sales occur around **{peak_hour}:00**

✅ Average order value is **${avg_order_value:.0f}**

✅ Overall business champion city remains {global_best_city}

✅ Overall most sold product remains **{global_most_sold_product}**
"""

st.markdown(insight_text)

# =====================================
# AI SALES ASSISTANT V6.1
# =====================================

st.divider()

st.subheader("🤖 AI Sales Assistant")

st.caption(
    "Ask questions about the currently selected sales data."
)

# --------------------------
# DISPLAY CHAT HISTORY
# --------------------------

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --------------------------
# USER INPUT
# --------------------------

user_question = st.chat_input(
    "Ask a business question..."
)

if user_question:

    # --------------------------
    # SHOW USER MESSAGE
    # --------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_question
        }
    )

    with st.chat_message("user"):
        st.markdown(user_question)

    # --------------------------
    # TOP 5 CITIES
    # --------------------------

    top_cities = (
        filtered_df.groupby("City")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )

    city_text = ""

    for city, revenue in top_cities.items():

        city_text += (
            f"{city}: ${revenue:,.0f}\n"
        )

    # --------------------------
    # TOP 5 PRODUCTS
    # --------------------------

    top_products = (
        filtered_df.groupby("Product")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )

    product_text = ""

    for product, revenue in top_products.items():

        product_text += (
            f"{product}: ${revenue:,.0f}\n"
        )

    # --------------------------
    # CONTEXT
    # --------------------------

    context = f"""
Sales Dashboard Summary

Revenue:
${total_revenue:,.0f}

Orders:
{total_orders:,}

Highest Revenue Product:
{top_product}

Most Sold Product:
{global_most_sold_product}

Peak Sales Hour:
{peak_hour}:00

Best Month:
{global_best_month}

Selected City:
{selected_city}

Selected Month:
{selected_month}

Top 5 Cities By Revenue:
{city_text}

Top 5 Products By Revenue:
{product_text}
"""

    prompt = f"""
You are an experienced sales analyst.

IMPORTANT RULES:

- Use only the provided data.
- Do not assume company names.
- Do not invent facts.
- If information is unavailable, clearly say so.
- Give concise and useful business insights.
- Use bullet points whenever appropriate.

DATA:

{context}

QUESTION:

{user_question}
"""

    with st.chat_message("assistant"):

        with st.spinner(
            "Analyzing sales data..."
        ):

            try:

                response = ollama.chat(
                    model="llama3",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

                answer = (
                    response["message"]["content"]
                )

                st.markdown(answer)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

            except Exception as e:

                error_message = (
                    f"Error: {e}"
                )

                st.error(error_message)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message
                    }
                )