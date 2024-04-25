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
    return MongoClient(uri, tlsCAFile=ca)


client = init_connection()


text_search = st.text_input("Search job", value="")


def get_companyStats_data():
    db = client.indeed  # establish connection to the 'sample_guide' db
    items = db.jobDescriptions.find()
    return pd.DataFrame(list(items))


def get_summarised_descriptions():
    db = client.indeed
    items = db.summarisedDescriptions.find()
    return pd.DataFrame(list(items))


def get_top_similiar_jobs():
    db = client.indeed
    items = db.topSimilarJobs.find()
    return pd.DataFrame(list(items))


data = get_companyStats_data()
data["str_id"] = data["_id"].astype(str)
summarised_descriptions = get_summarised_descriptions()
summarised_descriptions["str_id"] = summarised_descriptions["_id"].astype(str)

common_rows = pd.merge(data,summarised_descriptions, on=['str_id', 'str_id'], how='inner')
common_primary_keys = common_rows['str_id']
data = data[data['str_id'].isin(common_primary_keys)]


top_similar_jobs = get_top_similiar_jobs()

top_similar_jobs["jobID"] = top_similar_jobs["jobID"].astype(str)

s = top_similar_jobs["jobID"]

top_similar_jobs = top_similar_jobs[top_similar_jobs['jobID'].isin(common_primary_keys)]




job_df = data[data["jobTitle"].str.contains(text_search, case=False)]

if text_search:
    if len(job_df) == 0:
        st.write("Job not found")
    else:
        displayed_jobs = set()
        job_df["str_id"] = job_df["_id"].astype(str)
        for row in range(len(job_df)):
            date_posted = str(job_df.iloc[row]["dateCreated"]).split(" ")[0]
            company_name = job_df.iloc[row]["companyName"]
            job_title = job_df.iloc[row]["jobTitle"]
            display_string = f"{job_title} @ {company_name}"
            if display_string in displayed_jobs:
                continue
            else:
                displayed_jobs.add(display_string)
            jd = job_df.iloc[row]["jobDescription"]
            apply_url = job_df.iloc[row]["applyNowUrl"]
            job_id = job_df.iloc[row]["str_id"]
            

            summarised_description = summarised_descriptions[summarised_descriptions["str_id"] == job_id].iloc[0]["summarisedJobDescription"]
            similar_jobs = top_similar_jobs[top_similar_jobs["jobID"] == job_id].iloc[0]["nearest_jobs"]
            #st.write(top_similar_jobs[top_similar_jobs["jobID"] == job_id].iloc[0])
            with st.expander(display_string):
                st.write(f"Date posted : {date_posted}")
                st.write(company_name)
                st.write(job_title)
                st.write(jd)
                st.write(f"Apply [here]({apply_url})")
                st.markdown("""---""")
                st.write("\n")
                st.write("Summarised Descriptions")
                st.write(summarised_description)
                st.markdown("""---""")
                st.write("\n")
                st.write("Top similar jobs")
                count = 1

                for similar_job_id in similar_jobs:
                  similar_job = data.loc[data["str_id"] == similar_job_id]
                  similar_job_title = similar_job.iloc[0]["jobTitle"]
                  similar_job_company = similar_job.iloc[0]["companyName"]
                  similar_jd = similar_job.iloc[0]["jobDescription"] 
                  similar_summarised_description = summarised_descriptions[summarised_descriptions["str_id"] == similar_job_id].iloc[0]["summarisedJobDescription"]
                  similar_apply_url = job_df.iloc[row]["applyNowUrl"]
                  st.write(f"{count}. {similar_job_title} @ {similar_job_company}")
                  st.write(f"Apply [here]({similar_apply_url})")
                  count += 1

