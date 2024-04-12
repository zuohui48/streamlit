import streamlit as st
from st_pages import Page, Section, show_pages, add_page_title

# Either this or add_indentation() MUST be called on each page in your
# app to add indendation in the sidebar
add_page_title()

# Specify what pages should be shown in the sidebar, and what their titles and icons
# should be
show_pages(
    [
        Page("app.py", "Home", "🏠"),
        Section("Company", icon = "🏢"),
        Page("pages/Overall Rating Statistics.py"),
        Page("pages/Culture Rating Statistics.py"),
        Page("pages/Management Rating Statistics.py"),
        Page("pages/Security & Advancement Statistics.py"),
        Page("pages/Salary Benefits Statistics.py"),
        Page("pages/Work Life Balance Statistics.py"),
        Page("pages/Company Search.py"),
        
        # Pages after a section will be indented
        Section("Job Industry", icon="💼"),
        Page("pages/Job Title Statistics.py"),
        Page("pages/Tech Stack Statistics.py"),
        # Unless you explicitly say in_section=False
        Page("pages/Job Search.py", icon = "🔍", in_section = False)
    ]
)

st.title("WOW WELCOME TO DATA JOBS TIME TO FIND MASSIVE MEGA GOOT STRADEJ")
st.header('About this app')
st.markdown('**What can this application do?**')
st.info('1. This application provides job seekers statistics on data/software related jobs according to recent industry trends. \n'
          '2. This application provides job seekers statistics on relevant companies for them to better assess their job opportunities. \n'
          '3. This application provides job seekers with recommended similar jobs based on selected jobs')
st.markdown('**How to use the app?**')
st.info('To engage with the app,\n'
             '1. Proceed to the company statistics page to view statistics of desired company \n'
             '2. Proceed to the job statistics page to view statistics of data related jobs \n'
             '3. Select the job u want to apply and we will recommend you some similar GOOD jobs')


