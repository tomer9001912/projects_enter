#import the essentials
import time
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import datetime 
# the data exploration
df = pd.read_csv(r'C:\Users\User\Downloads\file.csv', encoding='windows-1255') #reading the csv
# TYPES OF cols = ISSUANCEDATE, BONDS, SERIES, ACTUALTERMTOMATURITY, ORIGINALTERMTOMATURITY, 
# REDEMTIONDATE, COUPON, OFFEREDQUANTITY, PURCHASEDQUANTITY, ADDITIONALPURCHASED, AVERAGEPRICE, 
# CUTOFFPRICE, TOTALFUNDING, DEMANDEDAMOUNT, COVERRATIO, GROSSAVGYIELD, GROSSCUTOFFYIELD
# most early-late date to pay the last payment of the bond
most_early_year = df.sort_values('BONDS').groupby('REDEMTIONDATE').head(-1)
most_late_year = df.sort_values('BONDS').groupby('REDEMTIONDATE').head(1)
grouped_by_bonds = df.groupby('BONDS')['SERIES'].count()
#data for bar chart 
grouped_by_quantity_offered = df.groupby('BONDS')['OFFEREDQUANTITY'].sum()
grouped_by_quantity_purchased = df.groupby('BONDS')['PURCHASEDQUANTITY'].sum()
grouped = df.groupby('BONDS')[['OFFEREDQUANTITY', 'PURCHASEDQUANTITY']].shift()
#data for demand chart
df['YEAR'] = pd.to_datetime(df['ISSUANCEDATE'])
df_grouped_by_year = df.groupby(df['YEAR'].dt.year)[['ISSUANCEDATE', 'DEMANDEDAMOUNT']].count()
unique_val_of_bonds = df['BONDS'].unique()
#data for corrlation
grouped_by_cover_price_vars = df.groupby('BONDS')[['ACTUALTERMTOMATURITY','COUPON','ADDITIONALPURCHASED', 'GROSSAVGYIELD','COVERRATIO','CUTOFFPRICE', 'TOTALFUNDING']].shift()
#data for cost of each purchase
sort_by_purchase = df.sort_values('BONDS')[['BONDS','PURCHASEDQUANTITY','AVERAGEPRICE']]
quantity_price_multiply = sort_by_purchase['PURCHASEDQUANTITY'] * sort_by_purchase['AVERAGEPRICE']
quantity_price_sum_by_group = quantity_price_multiply.groupby(sort_by_purchase['BONDS']).sum()
quantity_price_mean_by_group = quantity_price_multiply.groupby(sort_by_purchase['BONDS']).mean()
quantity_price_min_by_group = quantity_price_multiply.groupby(sort_by_purchase['BONDS']).min()
quantity_price_max_by_group = quantity_price_multiply.groupby(sort_by_purchase['BONDS']).max()

# the straemlit website

st.title("Review of government bonds in the Israeli market")
st.write(df.head())
bonds_col_1, bonds_col_2 = st.columns(2)
with bonds_col_1:
    st.write('The most early end of payment date of each bond' ,most_early_year.min())
with bonds_col_2:
    st.write('The most late end of payment date of each bond is' ,most_late_year.max())
st.write('count of bonds for each one',grouped_by_bonds)
col_1_quantity_price, col_2_quantity_price = st.columns(2)
with col_1_quantity_price:
    st.write('sum by each bond')
    st.write(quantity_price_sum_by_group)
with col_2_quantity_price:
    st.write('mean of each bond')
    st.write(quantity_price_mean_by_group)
col_3_quantity_price, col_4_quantity_price =st.columns(2)
with col_3_quantity_price:
    st.write('minimum single bond price')
    st.write(quantity_price_min_by_group)
with col_4_quantity_price:
    st.write('maximum single bond price')
    st.write(quantity_price_max_by_group)
st.subheader('grouped both offered and purchased by chronological index and quantity (value)')
st.bar_chart(data=grouped)
offered ,purchased = st.columns(2)
with offered:
    st.write('bonds quantity that offered')
    st.bar_chart(grouped_by_quantity_offered)
with purchased:
    st.write('bonds quantity that purchased')
    st.bar_chart(grouped_by_quantity_purchased)

# bar chart of year DEMANDEDAMOUNT
st.subheader('Demand amount from 2021 to 2025')
st.bar_chart(df_grouped_by_year['DEMANDEDAMOUNT'])

#corrlation by Seaborn
st.subheader("Correlation Matrix Heatmap")
data_frame = pd.DataFrame(grouped_by_cover_price_vars)
st.subheader("Original Data:")
st.dataframe(data_frame)
correlation_matrix = data_frame.corr()
st.subheader("Correlation Matrix:")
st.dataframe(correlation_matrix)
st.subheader("Correlation Heatmap:")
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.4, ax=ax)
plt.title("Variables of funding by precentage")
st.pyplot(fig)

with st.expander("information & clarification"):
    st.subheader('the article is includes data from data.gov.il')
    st.subheader('the data is updated to Nov 3rd 2025')
st.subheader('you reached to the end of this page, you deserve a cat photo')
mr_snekardoodles = 'https://images.pexels.com/photos/45201/kitty-cat-kitten-pet-45201.jpeg'
st.image(mr_snekardoodles)