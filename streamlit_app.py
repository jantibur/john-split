import streamlit as st
import pandas as pd
import numpy as np

vin_df = pd.DataFrame([{"60": 0, "100": 0, "200": 0, "350": 0, "1L": 0}], dtype=int)
soy_df = pd.DataFrame([{"60": 0, "100": 0, "200": 0, "350": 0, "1L": 0}], dtype=int)
ufc_df = pd.DataFrame([{"25": 0, "100": 0, "325": 0, "550": 0, "1L": 0}], dtype=int)

price_list = {
    "VIN 60": 3.5, "VIN 100": 5.5, "VIN 200": 7.6, "VIN 350": 17.75, "VIN 1L": 41.25,
    "SOY 60": 4, "SOY 100": 6.25, "SOY 200": 10, "SOY 350": 18.75, "SOY 1L": 51,
    "UFC 25": 3.5, "UFC 100": 10.25, "UFC 325": 26, "UFC 550": 42.5, "UFC 1L": 66.75
}

with st.container(border=True):
    n_split = st.number_input(min_value=1, max_value=50, label="Number of Splits", step=1, icon="🧾")

with st.container(border=True):
    st.header("🎍 VINEGAR")
    vin_df_i = st.data_editor(vin_df, column_config={
        "60": st.column_config.NumberColumn("60", min_value=0),
        "100": st.column_config.NumberColumn("100", min_value=0),
        "200": st.column_config.NumberColumn("200", min_value=0),
        "350": st.column_config.NumberColumn("350", min_value=0),
        "1L": st.column_config.NumberColumn("1L", min_value=0),
    }, hide_index=True, key="vin_df")

with st.container(border=True):
    st.header("🫘 SOY")
    soy_df_i = st.data_editor(soy_df, column_config={
        "60": st.column_config.NumberColumn("60", min_value=0),
        "100": st.column_config.NumberColumn("100", min_value=0),
        "200": st.column_config.NumberColumn("200", min_value=0),
        "350": st.column_config.NumberColumn("350", min_value=0),
        "1L": st.column_config.NumberColumn("1L", min_value=0),
    }, hide_index=True, key="soy_df")

with st.container(border=True):
    st.header("🍅 UFC")
    ufc_df_i = st.data_editor(ufc_df, column_config={
        "25": st.column_config.NumberColumn("25", min_value=0),
        "100": st.column_config.NumberColumn("100", min_value=0),
        "325": st.column_config.NumberColumn("325", min_value=0),
        "550": st.column_config.NumberColumn("550", min_value=0),
        "1L": st.column_config.NumberColumn("1L", min_value=0),
    }, hide_index=True, key="ufc_df")

def df_to_dict(df, prod):
    if prod not in ("VIN", "SOY", "UFC"):
        raise ValueError("Invalid product...")
    
    df = df.fillna(0).astype(int)

    df_dict = {}

    for size in df.columns:
        amount = int(df[size].iloc[0])
        if amount != 0:
            df_dict[f"{prod} {size}"] = int(amount)

    return df_dict

def split_num(num, n_split):
    c = np.zeros(n_split)
    
    i = 0
    while(sum(c) < num):
        c[i] += 1
        if i == n_split - 1:
            i = 0
        else:
            i += 1
    
    return c.tolist()


def split_dict(prod_dict, n_split):
    spl_dict = {}
    for key, item in prod_dict.items():
        spl_dict[key] = split_num(item, n_split)
    return spl_dict

def const_invoice(spl_dict, n_split):
    invoices = []

    for i in range(n_split):
        c_invoice = []
        for key, amounts in spl_dict.items(): 
            amount = int(amounts[i]) if i < len(amounts) else 0   
            if amount > 0:
                price = price_list.get(key, 0)
                c_invoice.append({"Product": key, "Amount": amount, "Unit Price": price, "Price": amount * price})
        if c_invoice:
            invoices.append(c_invoice)

    return invoices


split_btn = st.button(width="stretch", label="Split", icon="🧾")

if split_btn:
    vin_df_dict = df_to_dict(vin_df_i, "VIN")
    soy_df_dict = df_to_dict(soy_df_i, "SOY")
    ufc_df_dict = df_to_dict(ufc_df_i, "UFC")
    
    vin_spl_dict = split_dict(vin_df_dict, n_split)
    soy_spl_dict = split_dict(soy_df_dict, n_split)
    ufc_spl_dict = split_dict(ufc_df_dict, n_split)
    spl_dict = vin_spl_dict | soy_spl_dict | ufc_spl_dict
    
    invoices = const_invoice(spl_dict, n_split)

    if len(invoices) == n_split:
        for i, invoice in enumerate(invoices): 
            with st.container(border=True):
                c_inv_p = [item["Price"] for item in invoice]
                st.header(f"Invoice {i+1}") 
                st.dataframe(invoice)
                st.markdown(f"Total price: **{sum(c_inv_p)}**")            
    else:
        st.header("Please input required data first...")
