import streamlit as st
from pymongo import MongoClient
import pandas as pd

password = st.secrets.db_pswd
username = st.secrets.db_username
cluster_name = st.secrets.cluster_name

uri = f"mongodb+srv://{username}:{password}@{cluster_name}.xtz5a2z.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

def init_connection():
  return MongoClient(uri)

client = init_connection()

st.title("WOW DATA JOBS")
with st.expander('About this app'):
  st.markdown('**What can this app do?**')
  st.info('This app shows job seekers on some good statistics on data/software related jobs.')
  st.markdown('**How to use the app?**')
  st.info('To engage with the app,\n'
             '1. Select which company u want to see then u will see some good stats \n'
             '2. Select the job u want to apply and we will show u some GOOD jobs')

text_search = st.text_input("Search company", value="")
    
# @st.experimental_memo(ttl=60)
def get_companyStats_data():
  db = client.indeed #establish connection to the 'sample_guide' db
  items = db.companyStats.find() 
  return pd.DataFrame(list(items))

data = get_companyStats_data()

m1 = data["companyName"].str.contains(text_search)

if text_search:
  st.write(m1)

