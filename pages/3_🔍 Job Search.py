import streamlit as st
from pymongo import MongoClient
import pandas as pd
import certifi
import matplotlib.pyplot as plt
import numpy as np


ca = certifi.where()

password = st.secrets.db_pswd
username = st.secrets.db_username
cluster_name = st.secrets.cluster_name

uri = f"mongodb+srv://{username}:{password}@{cluster_name}.xtz5a2z.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

def init_connection():
  return MongoClient(uri,tlsCAFile=ca)

client = init_connection()


text_search = st.text_input("Search job", value="")

def get_companyStats_data():
  db = client.indeed #establish connection to the 'sample_guide' db
  items = db.jobDescriptions.find() 
  return pd.DataFrame(list(items))

data = get_companyStats_data()


job_df = data[data["jobTitle"].str.contains(text_search, case=False)]


if text_search:
  if len(job_df) == 0:
    st.write("Job not found")
  else:
    job_df.sort_values(by = "dateCreated", inplace = True)
    for row in range(len(job_df)):
      date_posted = str(job_df.iloc[row]["dateCreated"]).split(" ")[0]
      company_name = job_df.iloc[row]["companyName"] 
      job_title = job_df.iloc[row]["jobTitle"] 
      jd = job_df.iloc[row]["jobDescription"] 
      apply_url = job_df.iloc[row]["applyNowUrl"] 
      with st.expander(f"{job_title} @ {company_name}"):
        st.write(f"Date posted : {date_posted}")
        st.write(company_name)
        st.write(job_title)
        st.write(jd)
        st.write(f"Apply [here]({apply_url})")
