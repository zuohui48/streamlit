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
        Page("pages/Company List.py"),
        Page("pages/Overall Rating Statistics.py"),
        Page("pages/Culture Rating Statistics.py"),
        Page("pages/Management Rating Statistics.py"),
        Page("pages/Security & Advancement Statistics.py"),
        Page("pages/Salary Benefits Statistics.py"),
        Page("pages/Work Life Balance Statistics.py"),
        Page("pages/Company Search.py"),
        Section("Job Industry", icon="💼"),
        Page("pages/Job Title Statistics.py"),
        Page("pages/Tech Stack Statistics.py"),
        Page("pages/Job Search.py", icon = "🔍", in_section = False)
    ]
)

st.title("Welcome to JobMiner Insider")
st.header('About this app')
st.markdown('**What can this application do?**')
st.info('1. This application provides job seekers statistics on data/software related jobs according to recent industry trends. \n'
          '2. This application provides job seekers statistics on relevant companies for them to better assess their job opportunities. \n'
          '3. This application provides job seekers with summarised descriptions and recommended similar jobs based on selected jobs')
st.markdown('**How to use the app?**')
st.info('To engage with the app,\n'
             '1. Proceed to the company tab to view statistics of various metrics across companies and search for desired companies to see how they compare against others. \n'
             '2. Proceed to the job industry tab to view statistics of data related jobs in terms of titles and tech stacks. \n'
             '3. Proceed to the job search tab to find summarised descriptions and top recommended similar jobs.')


