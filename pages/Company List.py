import streamlit as st
from pymongo import MongoClient
import pandas as pd
import certifi
import matplotlib.pyplot as plt
import numpy as np
from st_pages import Page, Section, show_pages, add_page_title

add_page_title()

ca = certifi.where()

password = st.secrets.db_pswd
username = st.secrets.db_username
cluster_name = st.secrets.cluster_name

uri = f"mongodb+srv://{username}:{password}@{cluster_name}.xtz5a2z.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

def init_connection():
  return MongoClient(uri,tlsCAFile=ca)

client = init_connection()

def get_companyStats_data():
  db = client.indeed #establish connection to the 'sample_guide' db
  items = db.companyStats.find() 
  return pd.DataFrame(list(items))

data = get_companyStats_data()

columns = [string for string in data.columns if "rating" in string.lower() or "star" in string.lower() or "counts" in string.lower()]
sort_column = st.selectbox('Select column to sort by:', columns)

order = st.selectbox("", ["ascending", "descending"])

if order == "ascending":
  df_sorted = data.sort_values(by=sort_column, ascending=True)
else:
  df_sorted = data.sort_values(by=sort_column, ascending=False)

show = ["companyName"] + columns
st.dataframe(df_sorted[show])
