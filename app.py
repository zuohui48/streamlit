import streamlit as st
from pymongo import MongoClient

def main():
    st.title('My Streamlit App')
    st.write('Welcome to my Streamlit app!')

    # @st.experimental_singleton(suppress_st_warning=True)
    def init_connection():
        return MongoClient("mongodb+srv://st.secrets.db_username:st.secrets.db_pswd@st.secrets.cluster_name.n4ycr4f.mongodb.net/?retryWrites=true&w=majority")

    client = init_connection()
    
    # @st.experimental_memo(ttl=60)
    def get_companyStats_data():
        db = client.indeed #establish connection to the 'sample_guide' db
        items = db.companyStats.find() 
        items = list(items)        
        return items
    
    data = get_companyStats_data()

    for item in data:
        st.write(item)

if __name__ == '__main__':
    main()