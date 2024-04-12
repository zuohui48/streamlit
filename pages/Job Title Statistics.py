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

st.title("Trending data jobs in the industry")

ca = certifi.where()

password = st.secrets.db_pswd
username = st.secrets.db_username
cluster_name = st.secrets.cluster_name

uri = f"mongodb+srv://{username}:{password}@{cluster_name}.xtz5a2z.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

def init_connection():
  return MongoClient(uri,tlsCAFile=ca)

client = init_connection()

def get_jobs_data():
  db = client.indeed #establish connection to the 'sample_guide' db
  items = db.jobDescriptions.find() 
  return pd.DataFrame(list(items))

data = get_jobs_data()
data["jobTitle"] = data["jobTitle"].str.lower()

data_analyst_counts = len(data[data["jobTitle"].str.contains("data analyst")])
data_engineer_counts = len(data[data["jobTitle"].str.contains("data engineer")])
swe_counts = len(data[data["jobTitle"].str.contains("software engineer")])
data_scientist_counts = len(data[data["jobTitle"].str.contains("data scientist")])
business_analyst_counts = len(data[data["jobTitle"].str.contains("business analyst")])


# Labels and counts
labels = ['Data Analyst', 'Data Engineer', 'Software Engineer', 'Data Scientist', 'Business Analyst']
sizes = [data_analyst_counts, data_engineer_counts, swe_counts, data_scientist_counts, business_analyst_counts]

# Filter out categories with zero counts
filtered_labels = []
filtered_sizes = []
for label, size in zip(labels, sizes):
    if size != 0:
        filtered_labels.append(label)
        filtered_sizes.append(size)

# Plotting the pie chart
fig, ax = plt.subplots(figsize=(8, 6))  # Set a larger figure size for better visualization

# Define colors
colors = plt.cm.Paired.colors

# Explode slices (optional)
explode = (0.1, 0, 0, 0, 0)  # Explode the first slice by 0.1

# Plot the pie chart with enhanced aesthetics
wedges, texts, autotexts = ax.pie(filtered_sizes, labels=filtered_labels, autopct='%1.1f%%', startangle=140,
                                   colors=colors, textprops=dict(color="white"))

# Equal aspect ratio ensures that pie is drawn as a circle
ax.axis('equal')

# Add a legend
ax.legend(wedges, filtered_labels, loc="best")

# Set title
ax.set_title('Distribution of Job Titles', pad=20)

# Display the plot in Streamlit
st.pyplot(fig)