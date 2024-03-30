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


text_search = st.text_input("Search company", value="")
    
# @st.experimental_memo(ttl=60)
def get_companyStats_data():
  db = client.indeed #establish connection to the 'sample_guide' db
  items = db.companyStats.find() 
  return pd.DataFrame(list(items))

data = get_companyStats_data()


company_df = data[data["companyName"].str.contains(text_search, case=False)]


if text_search:
  if len(company_df) == 0:
    st.write("Company not found")
  else:
    company_name = (company_df.iloc[0]["companyName"])
    company_review_url = (company_df.iloc[0]["companyReviewUrl"])
    company_url = (company_df.iloc[0]["companyUrl"])

    st.write(f"Find out more about {company_name} at  {company_url}")
    st.write(f"Read reviews about {company_name} at  {company_review_url}")
    st.write("\n")
    rating_test = company_df.iloc[0]["companyOverallRating"]

    if not np.isnan(rating_test):
      overall = (company_df.iloc[0]["companyOverallRating"])
      culture = (company_df.iloc[0]["companyCultureRating"])
      jobsecurity = company_df.iloc[0]["companyJobsecurityadvancementRating"]
      management = company_df.iloc[0]["companyManagementRating"]
      salary_benefits = company_df.iloc[0]["companySalaryBenefitsRating"]
      wlb = company_df.iloc[0]["companyWorkLifeBalanceRating"]

      rating_types = [overall, culture, jobsecurity, management, salary_benefits, wlb]
      rating_strings = ["Overall Rating", "Culture Rating", "Job Security Rating", "Management Rating", "Salary Benefits Rating", "Work Life Balance Rating"]

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
        
      # Determine the maximum length of the rating strings
      max_length = max(len(s) for s in rating_strings)

      # Display the ratings
      for i in range(len(rating_types)):
          if i == 1:
             st.write("\n")
             st.write("Ratings by Category")
          # Align the rating strings using string formatting
          formatted_rating_string = f"{rating_strings[i]:<{max_length + 5}}"
          st.write(f"{formatted_rating_string} : {display_rating(rating_types[i])} {rating_types[i]}")

    
    star_test = company_df.iloc[0]["companyTotal1Star"]
    if not np.isnan(star_test):
      st.write("\n")

      categories = ['1 star', '2 star', '3 star', '4 star', '5 star']
      values = [int(company_df["companyTotal1Star"]), int(company_df["companyTotal2Star"]), int(company_df["companyTotal3Star"]), int(company_df["companyTotal4Star"]), int(company_df["companyTotal5Star"])]
      
      # # Create a bar chart using Matplotlib
      fig, ax = plt.subplots()
      bars = ax.bar(categories, values)


      ax.bar(categories, values)
      ax.set_xlabel('Reviews')
      ax.set_ylabel('Counts')
      
    
      ax.set_title(f'Review Counts for {company_name}')

      # # Display the plot using Streamlit
      st.pyplot(fig)