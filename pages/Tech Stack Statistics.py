import streamlit as st
from pymongo import MongoClient
import pandas as pd
import certifi
import matplotlib.pyplot as plt
import numpy as np
from st_pages import Page, Section, show_pages, add_page_title
from collections import Counter

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


job_skills = {}
for mainjob in data["mainJob"].unique():
  filtered = data[data["mainJob"] == mainjob]
  for i in filtered["hardSkills"]:
    k = i.split(",")
    for j in k:
      l = j.split(" ")
      if len(l) <= 2:
        skill = "".join(l).lower()
        if skill != "none":
          if mainjob not in job_skills:
            job_skills[mainjob] = [skill]
          else:
            curr_list = job_skills[mainjob]
            curr_list.append(skill)
            job_skills[mainjob] = curr_list

for mainjob, skills_list in job_skills.items():
    st.write(mainjob.title())
    top_skills = list(Counter(skills_list).most_common(5))
    skills, count = zip(*top_skills)
    
    fig, ax = plt.subplots()
    
    # Generate random colors for each bar
    colors = plt.cm.tab20(np.arange(len(skills)))
    
    # Plotting the bar chart with different colors
    bars = ax.bar(skills, count, color=colors)
    
    # Attach numeric labels above each bar
    for bar, value in zip(bars, count):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(), value, ha='center', va='bottom')
    
    ax.set_title(f"Most Common Tech Stack for {mainjob.title()}")

    # Display the bar chart
    st.pyplot(fig)



