import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

def create_customer_bycity_df(df):
    customer_bycity_df = df.groupby(by="customer_city").customer_id.nunique().reset_index()
    return customer_bycity_df

def create_customer_bystate_df(df):
    customer_bystate_df = df.groupby(by="customer_state").customer_id.nunique().reset_index()
    return customer_bystate_df

def create_order_bycity_df(df):
    order_bycity_df = df.groupby(by="customer_city").order_id.nunique().reset_index()
    return order_bycity_df

def create_order_bystate_df(df):
    order_bystate_df = df.groupby(by="customer_state").order_id.nunique().reset_index()
    return order_bystate_df

def create_order_payments_df(df):
    order_payments_df = df.groupby(by="payment_type").order_id.nunique().reset_index()
    return order_payments_df

def create_rfm_df(df):
    rfm_df = df.groupby(by="customer_state", as_index=False).agg({
    "order_purchase_timestamp": "max", #mengambil tanggal order terakhir
    "order_id": "nunique",
    "payment_value": "sum"
})
    
    rfm_df.columns = ["customer_state", "order_purchase_timestamp", "frequency", "monetary"]

    rfm_df["order_purchase_timestamp"] = rfm_df["order_purchase_timestamp"].dt.date
    recent_date = df["order_purchase_timestamp"].dt.date.max()
    rfm_df["recency"] = rfm_df["order_purchase_timestamp"].apply(lambda x: (recent_date - x).days)
    rfm_df.drop("order_purchase_timestamp", axis=1, inplace=True)
    
    return rfm_df
 
# Load cleaned data
all_df = pd.read_csv("https://raw.githubusercontent.com/JibrilAhmad/Proyek-Analisis-Data/main/Dashboard/all_data.csv")

datetime_columns = ["order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date","order_delivered_customer_date","order_estimated_delivery_date"]
all_df.sort_values(by="order_purchase_timestamp", inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

# Filter Data
min_date = all_df["order_purchase_timestamp"].min()
max_date = all_df["order_purchase_timestamp"].max()

with st.sidebar:    
    # Menambahkan logo
    st.image("https://raw.githubusercontent.com/JibrilAhmad/Proyek-Analisis-Data/main/Dashboard/e-com_logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["order_purchase_timestamp"] >= str(start_date)) & 
                (all_df["order_purchase_timestamp"] <= str(end_date))]

customer_bycity_df = create_customer_bycity_df(main_df)
customer_bystate_df = create_customer_bystate_df(main_df)
order_bycity_df = create_order_bycity_df(main_df)
order_bystate_df = create_order_bystate_df(main_df)
order_payments_df = create_order_payments_df(main_df)
rfm_df = create_rfm_df(main_df)
highest_city_customer_counts = customer_bycity_df.sort_values(by="customer_id", ascending=False).head(5)
highest_state_customer_counts = customer_bystate_df.sort_values(by="customer_id", ascending=False).head(5)
highest_city_order_counts = order_bycity_df.sort_values(by="order_id", ascending=False).head(5)
highest_state_order_counts = order_bystate_df.sort_values(by="order_id", ascending=False).head(5)
rank_payments = order_payments_df.sort_values(by="order_id", ascending=False).head(4)

st.header('E-Commerce Public Dashboard :sparkles:')
st.subheader('Customer Distribution by City')

fig, ax = plt.subplots(figsize=(30, 15))
    
colors = ["#FFFF00", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(
    x="customer_id", 
    y="customer_city",
    data=highest_city_customer_counts,
    palette=colors,
    ax=ax
)
ax.set_title("Number of Customers in the Top 5 Cities", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=30)
ax.tick_params(axis='x', labelsize=30)
st.pyplot(fig)

st.subheader('Customer Distribution by State')

fig, ax = plt.subplots(figsize=(30, 15))
   
colors = ["#FFFF00", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(
    x="customer_id", 
    y="customer_state",
    data=highest_state_customer_counts,
    palette=colors,
    ax=ax
)
ax.set_title("Number of Customers in the Top 5 States", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=30)
ax.tick_params(axis='x', labelsize=30)
st.pyplot(fig)

st.subheader('Orders Distribution')

col1, col2 = st.columns(2)
 
with col1:
    # By City
    fig, ax = plt.subplots(figsize=(20,10))
    colors2 = ["#FFFF00", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

    sns.barplot(
        x='customer_city', 
        y='order_id', 
        data=highest_city_order_counts,
        palette=colors2,
        ax=ax
    )

    ax.set_title("Most Order City", loc="center", fontsize=30)
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    ax.tick_params(axis='y', labelsize=25)
    ax.tick_params(axis='x', labelsize=20)
    st.pyplot(fig)
 
with col2:
    #By State
    fig, ax = plt.subplots(figsize=(20,10))
    colors2 = ["#FFFF00", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

    sns.barplot(
        x='customer_state', 
        y='order_id', 
        data=highest_state_order_counts,
        palette=colors2,
        ax=ax
    )
    ax.set_title("Most Order State", loc="center", fontsize=30)
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    ax.tick_params(axis='y', labelsize=25)
    ax.tick_params(axis='x', labelsize=20)
    st.pyplot(fig)

st.subheader('Payment Type Mostly Used')

fig, ax = plt.subplots(figsize=(30, 15))
   
colors = ["#FFFF00", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(
    x="payment_type", 
    y="order_id",
    data=rank_payments,
    palette=colors,
    ax=ax
)
ax.set_title("Payment Type Ranks", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=30)
ax.tick_params(axis='x', labelsize=30)
st.pyplot(fig)

st.subheader("Best State on RFM Analysis")
 
col1, col2, col3 = st.columns(3)
 
with col1:
    avg_recency = round(rfm_df.recency.mean(), 1)
    st.metric("Average Recency (days)", value=avg_recency)
 
with col2:
    avg_frequency = round(rfm_df.frequency.mean(), 2)
    st.metric("Average Frequency", value=avg_frequency)
 
with col3:
    avg_frequency = format_currency(rfm_df.monetary.mean(), "ARS", locale='es_AR') 
    st.metric("Average Monetary", value=avg_frequency)
 
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(35, 15))
colors = ["#FFFF00", "#FFFF00", "#FFFF00", "#FFFF00", "#FFFF00"]
 
sns.barplot(y="recency", x="customer_state", data=rfm_df.sort_values(by="recency", ascending=True).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("customer_state", fontsize=30)
ax[0].set_title("By Recency (days)", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=30)
ax[0].tick_params(axis='x', labelsize=15)
 
sns.barplot(y="frequency", x="customer_state", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("customer_state", fontsize=30)
ax[1].set_title("By Frequency", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=30)
ax[1].tick_params(axis='x', labelsize=15)
 
sns.barplot(y="monetary", x="customer_state", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel("customer_state", fontsize=30)
ax[2].set_title("By Monetary", loc="center", fontsize=50)
ax[2].tick_params(axis='y', labelsize=30)
ax[2].tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)
 
st.caption('Copyright (c) Ahmad Jibril with Dicoding 2023')