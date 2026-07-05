import streamlit as st
import pandas as pd
import plotly.express as px 
import numpy as np

# Page Configuration
st.set_page_config(
    page_title="Bank Marketing Dashboard",
    page_icon="🏦",
    layout="wide"
)

# Dashboard Title
st.title("🏦 Bank Marketing Analysis Dashboard")
st.markdown("Analyze customer subscription patterns and marketing campaign performance.")

# Load Dataset
df = pd.read_csv("bank-full.csv", sep=";")

# Rename target column
df.rename(columns={"y": "subscription"}, inplace=True)


# ==========================================
# Sidebar Filters
# ==========================================

st.sidebar.header("🔍 Filters")

job = st.sidebar.multiselect(
    "Select Job",
    options=sorted(df["job"].unique()),
    default=sorted(df["job"].unique())
)

marital = st.sidebar.multiselect(
    "Select Marital Status",
    options=sorted(df["marital"].unique()),
    default=sorted(df["marital"].unique())
)

education = st.sidebar.multiselect(
    "Select Education",
    options=sorted(df["education"].unique()),
    default=sorted(df["education"].unique())
)

housing = st.sidebar.multiselect(
    "Housing Loan",
    options=sorted(df["housing"].unique()),
    default=sorted(df["housing"].unique())
)

loan = st.sidebar.multiselect(
    "Personal Loan",
    options=sorted(df["loan"].unique()),
    default=sorted(df["loan"].unique())
)

# ==========================================
# Apply Filters
# ==========================================

filtered_df = df[
    (df["job"].isin(job)) &
    (df["marital"].isin(marital)) &
    (df["education"].isin(education)) &
    (df["housing"].isin(housing)) &
    (df["loan"].isin(loan))
]


# ==========================================
# KPI Cards
# ==========================================

total_customers = filtered_df.shape[0]

subscribed_customers = filtered_df[
    filtered_df["subscription"] == "yes"
].shape[0]

subscription_rate = (
    subscribed_customers / total_customers * 100
    if total_customers > 0 else 0
)

average_age = filtered_df["age"].mean()

average_balance = filtered_df["balance"].mean()

average_duration = filtered_df["duration"].mean()


# ==========================================
# Funnel Metrics
# ==========================================
drop_off = total_customers - subscribed_customers

drop_off_rate = (
    drop_off / total_customers * 100
    if total_customers > 0 else 0
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("👥 Total Customers", f"{total_customers:,}")

col2.metric("✅ Subscribers", f"{subscribed_customers:,}")

col3.metric("📈 Subscription Rate", f"{subscription_rate:.2f}%")

col4.metric("🎂 Average Age", f"{average_age:.1f}")

col5, col6, col7, col8 = st.columns(4)

col5.metric("💰 Average Balance", f"{average_balance:.0f}")

col6.metric("⏱ Average Duration", f"{average_duration:.0f} sec")

col7.metric("📈 Conversion Rate",f"{subscription_rate:.2f}%")

col8.metric("📉 Drop-off Rate",f"{drop_off_rate:.2f}%")

# ==========================================
# Marketing Funnel
# ==========================================
st.subheader("🎯 Marketing Funnel")
funnel_df = pd.DataFrame({
    "Stage": [
        "Customers Contacted",
        "Customers Subscribed"
    ],
    "Count": [
        total_customers,
        subscribed_customers
    ]
})
fig = px.funnel(
    funnel_df,
    x="Count",
    y="Stage"
)

st.plotly_chart(fig, use_container_width=True)


# ==========================================
# Subscription Distribution
# ==========================================

st.subheader("🥧 Subscription Distribution")

subscription_counts = (
    filtered_df["subscription"]
    .value_counts()
    .reset_index()
)

subscription_counts.columns = ["Subscription", "Count"]

fig = px.pie(
    subscription_counts,
    names="Subscription",
    values="Count",
    hole=0.4,                     # Makes it a donut chart
)

fig.update_traces(
    textinfo="percent+label"
)

st.plotly_chart(fig, use_container_width=True)


# ==========================================
# Age Distribution (Bar Chart)
# ==========================================

st.subheader("📊 Age Distribution")

# Create age bins of 5 years
min_age = (filtered_df["age"].min() // 5) * 5
max_age = ((filtered_df["age"].max() // 5) + 1) * 5

bins = np.arange(min_age, max_age + 5, 5)

filtered_df["Age Group"] = pd.cut(
    filtered_df["age"],
    bins=bins,
    right=False
)

age_distribution = (
    filtered_df["Age Group"]
    .value_counts()
    .sort_index()
    .reset_index()
)

age_distribution.columns = ["Age Group", "Customers"]

# Convert interval labels into strings
age_distribution["Age Group"] = age_distribution["Age Group"].astype(str)

fig = px.bar(
    age_distribution,
    x="Age Group",
    y="Customers",
    text="Customers",
    title="Customer Distribution by Age Group (5-Year Interval)"
)

fig.update_traces(textposition="outside")

fig.update_layout(
    xaxis_title="Age Group",
    yaxis_title="Number of Customers",
    xaxis=dict(type="category")
)

st.plotly_chart(fig, use_container_width=True)

# ==========================================
# Education & Marital Status Distribution
# ==========================================

col1, col2 = st.columns(2)

# ------------------------------------------
# Education Distribution
# ------------------------------------------
with col1:

    st.subheader("🎓 Education Distribution")

    education_counts = (
        filtered_df["education"]
        .value_counts()
        .reset_index()
    )

    education_counts.columns = ["Education", "Customers"]

    fig = px.pie(
        education_counts,
        names="Education",
        values="Customers",
        hole=0.4
    )

    fig.update_traces(textinfo="percent+label")

    st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------
# Marital Status Distribution
# ------------------------------------------
with col2:

    st.subheader("💍 Marital Status Distribution")

    marital_counts = (
        filtered_df["marital"]
        .value_counts()
        .reset_index()
    )

    marital_counts.columns = ["Marital Status", "Customers"]

    fig = px.pie(
        marital_counts,
        names="Marital Status",
        values="Customers",
        hole=0.4
    )

    fig.update_traces(textinfo="percent+label")

    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# Campaign Analysis
# ==========================================

st.header("📞 Campaign Analysis")

# ==========================================
# Month-wise Campaign Analysis
# ==========================================
st.subheader("📅 Month-wise Customer Contacts")
month_order = [
    "jan", "feb", "mar", "apr", "may", "jun",
    "jul", "aug", "sep", "oct", "nov", "dec"
]
month_data = (
    filtered_df["month"]
    .value_counts()
    .reindex(month_order, fill_value=0)
    .reset_index()
)
month_data.columns = ["Month", "Customers"]
fig = px.bar(
    month_data,
    x="Month",
    y="Customers",
    text="Customers"
)
fig.update_traces(textposition="outside")
st.plotly_chart(fig, use_container_width=True)


# ==========================================
# Call Duration Distribution
# ==========================================

st.subheader("⏱ Call Duration Distribution")

fig = px.histogram(
    filtered_df,
    x="duration",
    nbins=30
)

fig.update_layout(
    xaxis_title="Call Duration (Seconds)",
    yaxis_title="Number of Customers"
)

st.plotly_chart(fig, use_container_width=True)

# ==========================================
# Account Balance Distribution
# ==========================================

st.subheader("💰 Account Balance Distribution")

fig = px.histogram(
    filtered_df,
    x="balance",
    nbins=30
)

fig.update_layout(
    xaxis_title="Account Balance",
    yaxis_title="Number of Customers"
)

st.plotly_chart(fig, use_container_width=True)

# ==========================================
# Campaign Contacts Distribution
# ==========================================

st.subheader("📞 Campaign Contacts Distribution")

campaign_data = (
    filtered_df["campaign"]
    .value_counts()
    .sort_index()
    .reset_index()
)

campaign_data.columns = ["Number of Contacts", "Customers"]

fig = px.bar(
    campaign_data,
    x="Number of Contacts",
    y="Customers",
    text="Customers",
    title="Number of Contacts per Customer"
)

fig.update_traces(textposition="outside")

fig.update_layout(
    xaxis_title="Campaign Contacts",
    yaxis_title="Number of Customers"
)

st.plotly_chart(fig, use_container_width=True)

# ==========================================
# Contact Type Analysis
# ==========================================

st.subheader("☎ Contact Type")

contact_data = (
    filtered_df["contact"]
    .value_counts()
    .reset_index()
)

contact_data.columns = ["Contact Type", "Customers"]

fig = px.pie(
    contact_data,
    names="Contact Type",
    values="Customers",
    hole=0.4
)

fig.update_traces(textinfo="percent+label")

st.plotly_chart(fig, use_container_width=True)

# ==========================================
# Previous Campaign Outcome
# ==========================================

st.subheader("📈 Previous Marketing Campaign Outcome")

poutcome_data = (
    filtered_df["poutcome"]
    .value_counts()
    .reset_index()
)

poutcome_data.columns = ["Outcome", "Customers"]

fig = px.bar(
    poutcome_data,
    x="Outcome",
    y="Customers",
    color="Outcome",
    text="Customers"
)

fig.update_traces(textposition="outside")

fig.update_layout(
    xaxis_title="Previous Campaign Outcome",
    yaxis_title="Number of Customers"
)

st.plotly_chart(fig, use_container_width=True)


# ==========================================
# Conversion Analysis
# ==========================================

st.header("📊 Conversion Analysis")
print('\n')
print('/n')
#  ==========================================
# Subscription Rate by Job
# ==========================================

st.subheader(" Subscription Rate by Job")

job_rate = (
    filtered_df
    .groupby("job")["subscription"]
    .apply(lambda x: (x == "yes").mean() * 100)
    .reset_index(name="Subscription Rate")
    .sort_values("Subscription Rate", ascending=False)
)

fig = px.bar(
    job_rate,
    x="job",
    y="Subscription Rate",
    text="Subscription Rate"
)

fig.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside"
)

st.plotly_chart(fig, use_container_width=True)

# Subscription rate by Education 

st.subheader("🎓 Subscription Rate by Education")

education_rate = (
    filtered_df
    .groupby("education")["subscription"]
    .apply(lambda x: (x == "yes").mean() * 100)
    .reset_index(name="Subscription Rate")
    .sort_values("Subscription Rate", ascending=False)
)

fig = px.bar(
    education_rate,
    x="education",
    y="Subscription Rate",
    text="Subscription Rate",
    color="Subscription Rate"
)

fig.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside"
)

fig.update_layout(
    xaxis_title="Education",
    yaxis_title="Subscription Rate (%)"
)

st.plotly_chart(fig, use_container_width=True)

# Subscription rate by marital status

st.subheader("💍 Subscription Rate by Marital Status")
marital_rate = (
    filtered_df
    .groupby("marital")["subscription"]
    .apply(lambda x: (x == "yes").mean() * 100)
    .reset_index(name="Subscription Rate")
)
fig = px.bar(
    marital_rate,
    x="marital",
    y="Subscription Rate",
    text="Subscription Rate",
    color="Subscription Rate"
)
fig.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside"
)
fig.update_layout(
    xaxis_title="Marital Status",
    yaxis_title="Subscription Rate (%)"
)
st.plotly_chart(fig, use_container_width=True)

# ==========================================
# Housing Loan vs Subscription
# ==========================================
st.subheader("🏠 Housing Loan vs Subscription")
housing_subscription = (
    filtered_df
    .groupby(["housing", "subscription"])
    .size()
    .reset_index(name="Customers")
)
fig = px.bar(
    housing_subscription,
    x="housing",
    y="Customers",
    color="subscription",
    barmode="group",
    text="Customers"
)
fig.update_traces(textposition="outside")
fig.update_layout(
    xaxis_title="Housing Loan",
    yaxis_title="Number of Customers"
)
st.plotly_chart(fig, use_container_width=True)

# ==========================================
# Personal Loan vs Subscription
# ==========================================
st.subheader("💳 Personal Loan vs Subscription")
loan_subscription = (
    filtered_df
    .groupby(["loan", "subscription"])
    .size()
    .reset_index(name="Customers")
)
fig = px.bar(
    loan_subscription,
    x="loan",
    y="Customers",
    color="subscription",
    barmode="group",
    text="Customers"
)
fig.update_traces(textposition="outside")
fig.update_layout(
    xaxis_title="Personal Loan",
    yaxis_title="Number of Customers"
)
st.plotly_chart(fig, use_container_width=True)