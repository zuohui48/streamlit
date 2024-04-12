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


text_search = st.text_input("Search company", placeholder="Enter Company Name")
    
# @st.experimental_memo(ttl=60)
def get_companyStats_data():
  db = client.indeed #establish connection to the 'sample_guide' db
  items = db.companyStats.find() 
  return pd.DataFrame(list(items))

data = get_companyStats_data()


data['companyName'] = data['companyName'].fillna(data['companyShorthand']) # if companyname na, use companyshorthand
company_df = data[data["companyName"].str.contains(text_search, case=False)]

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
  

if text_search:
  if len(company_df) == 0:
    st.write("Company not found")
  else:
    for i in range(len(company_df)):
      with st.container(border=True):
        company_name = (company_df.iloc[i]["companyName"])
        company_review_url = (company_df.iloc[i]["companyReviewUrl"])
        company_url = (company_df.iloc[i]["companyUrl"])

        st.write(f"Find out more about {company_name} [here]({company_url})")
        st.write(f"Read reviews about {company_name} [here]({company_review_url})")
        st.write("\n")
        rating_test = company_df.iloc[i]["companyOverallRating"]
        if np.isnan(rating_test):
          print(f"{company_name} does not have enough ratings")
          st.write(f"{company_name} does not have enough ratings")

        if not np.isnan(rating_test):
          overall = (company_df.iloc[i]["companyOverallRating"])
          culture = (company_df.iloc[i]["companyCultureRating"])
          jobsecurity = company_df.iloc[i]["companyJobsecurityadvancementRating"]
          management = company_df.iloc[i]["companyManagementRating"]
          salary_benefits = company_df.iloc[i]["companySalaryBenefitsRating"]
          wlb = company_df.iloc[i]["companyWorkLifeBalanceRating"]

          rating_types = [overall, culture, jobsecurity, management, salary_benefits, wlb]
          rating_strings = ["Overall Rating", "Culture Rating", "Job Security Rating", "Management Rating", "Salary Benefits Rating", "Work Life Balance Rating"]

            
          # Determine the maximum length of the rating strings
          max_length = max(len(s) for s in rating_strings)

          # Display the ratings
          for j in range(len(rating_types)):
              if j == 1:
                st.write("\n")
                st.write("Ratings by Category")
              # Align the rating strings using string formatting
              formatted_rating_string = f"{rating_strings[j]:<{max_length + 5}}"
              if not np.isnan(rating_types[j]):
                st.write(f"{formatted_rating_string} : {display_rating(rating_types[j])} {rating_types[j]}")

      
          star_test = company_df.iloc[i]["companyTotal1Star"]
          if not np.isnan(star_test):
            st.write("\n")

            # Define categories and values
            categories = ['1 star', '2 star', '3 star', '4 star', '5 star']
            values = [
                int(company_df.iloc[i]["companyTotal1Star"]),
                int(company_df.iloc[i]["companyTotal2Star"]),
                int(company_df.iloc[i]["companyTotal3Star"]),
                int(company_df.iloc[i]["companyTotal4Star"]),
                int(company_df.iloc[i]["companyTotal5Star"])
            ]
            
            # Create a bar chart using Matplotlib
            fig, ax = plt.subplots(figsize=(8, 6))

            # Plot bars with adjusted width and color
            bars = ax.bar(categories, values, color='skyblue', width=0.6)

            # Add data labels on top of bars
            for bar, value in zip(bars, values):
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), str(value), ha='center', color='black')

            # Add gridlines
            ax.grid(axis='y', linestyle='--', alpha=0.7)

            # Set labels and title
            ax.set_xlabel('Reviews')
            ax.set_ylabel('Counts')
            ax.set_title(f'Review Counts for {company_name}')

            # Display the plot using Streamlit
            st.pyplot(fig)
        
        if not np.isnan(rating_test):
            st.markdown("""---""")
            st.write("\n")
            average_overall_rating = data["companyOverallRating"].mean()
            difference = overall - average_overall_rating
            if difference > 0:
              st.write(f"{company_name} has overall rating higher than average by {round(difference,2)} stars")
            else:
              st.write(f"{company_name} has overall rating lower than average by {round(abs(difference),2)} stars")
              
          # Plot histogram
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.hist(data["companyOverallRating"], bins=20, color='skyblue', edgecolor='black')
            ax.set_title('Distribution of Overall Ratings Across Companies')
            ax.set_xlabel('Overall Rating')
            ax.set_ylabel('Frequency')
            ax.grid(True)

            # Add vertical lines with labels
            ax.axvline(x=average_overall_rating, color='black', linestyle='--')  # Vertical line at x=3.5
            ax.text(average_overall_rating, 40, 'Average Overall Rating', color='black')  # Label for the vertical line at x=3.5

            ax.axvline(x=overall, color='red', linestyle='--')  # Vertical line at x=4.5
            ax.text(overall, 30, f"{company_name} Overall Rating", color='red')  # Label for the vertical line at x=4.5

            # Display the plot in Streamlit
            st.pyplot(fig)
