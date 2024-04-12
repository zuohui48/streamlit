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
def get_companyStats_data():
  db = client.indeed #establish connection to the 'sample_guide' db
  items = db.companyStats.find() 
  return pd.DataFrame(list(items))

data = get_companyStats_data()

def display_rating(rating):
  full_star = '★'
  half_star = '½'
  empty_star = '☆'
  full_stars = int(rating)
  remainder = rating - full_stars
  if remainder >= 0.75:
    return full_star * full_stars + '★' + empty_star * (5 - full_stars - 1)
  elif remainder >= 0.25:
     return full_star * full_stars + half_star + empty_star * (5 - full_stars - 1)
  else:
     return full_star * full_stars + empty_star * (5 - full_stars)




average_salarybenefits_rating = data["companySalaryBenefitsRating"].mean()
min_salarybenefits_rating = data["companySalaryBenefitsRating"].min()
max_salarybenefits_rating = data["companySalaryBenefitsRating"].max()






st.write(f"Average Salary Benefits ratings : {display_rating(average_salarybenefits_rating)} {round(average_salarybenefits_rating,2)}")
st.write(f"Minimum Salary Benefits ratings : {display_rating(min_salarybenefits_rating)} {round(min_salarybenefits_rating,2)}")
st.write(f"Maximum Salary Benefits ratings : {display_rating(max_salarybenefits_rating)} {round(max_salarybenefits_rating,2)}")

# Plot histogram
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(data["companySalaryBenefitsRating"], bins=20, color='skyblue', edgecolor='black')
ax.set_title('Distribution of Salary Benefits Ratings Across Companies')
ax.set_xlabel('Security and Salary Benefits Rating')
ax.set_ylabel('Frequency')
ax.grid(True)

# Display the plot in Streamlit
st.pyplot(fig)