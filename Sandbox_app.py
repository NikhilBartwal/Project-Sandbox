import os
import pandas as pd
import streamlit as st
st.set_page_config(layout="wide")

from playables.DataDissect.data_dissect import load_data_dissect

def display_homepage():
    st.write('Welcome to Project Sandbox!')

def load_app():
    options = ['Homepage', 'Data Dissect']
    option = st.sidebar.selectbox('Please select one of the following:', options)
    if option==options[0]:
        display_homepage()
    elif option==options[1]:
        load_data_dissect()

if __name__ == '__main__':
    load_app()
