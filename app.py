import streamlit as st

st.title("WOW DATA JOBS")
with st.expander('About this app'):
  st.markdown('**What can this app do?**')
  st.info('This app shows job seekers on some good statistics on data/software related jobs.')
  st.markdown('**How to use the app?**')
  st.info('To engage with the app,\n'
             '1. Select which company u want to see then u will see some good stats \n'
             '2. Select the job u want to apply and we will show u some GOOD jobs')

text_search = st.text_input("Search Company", value="")