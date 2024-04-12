import streamlit as st
from pymongo import MongoClient
import pandas as pd
import certifi
import matplotlib.pyplot as plt
import numpy as np
from st_pages import Page, Section, show_pages, add_page_title

# Either this or add_indentation() MUST be called on each page in your
# app to add indendation in the sidebar
add_page_title()

ca = certifi.where()

password = st.secrets.db_pswd
username = st.secrets.db_username
cluster_name = st.secrets.cluster_name

uri = f"mongodb+srv://{username}:{password}@{cluster_name}.xtz5a2z.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

def init_connection():
  return MongoClient(uri,tlsCAFile=ca)

client = init_connection()
    
# @st.experimental_memo(ttl=60)
def get_hardSkills_data():
  db = client.indeed #establish connection to the 'sample_guide' db
  items = db.hardSkills.find() 
  return pd.DataFrame(list(items))

data = get_hardSkills_data()

data_science = data[data["mainJob"] == "data science"]
skills = []

for i in data_science["hardSkills"]:
  st.write(f"i {i}")
  for j in i.split(","):
    lst = j.split(" ")
    st.write(lst)
