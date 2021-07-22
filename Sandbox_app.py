import os
import pandas as pd
import streamlit as st
st.set_page_config(layout="wide")

from playables.DataDissect.data_dissect import load_data_dissect

def display_homepage():
    st.write('Welcome to Project Sandbox!')
    #st.image('logos/sandbox.png')

def load_app():
    options = ['Data Dissect', 'Homepage']
    option = st.sidebar.selectbox('Please select one of the following:', options)
    if option==options[1]:
        display_homepage()
    elif option==options[0]:
        load_data_dissect()

if __name__ == '__main__':
    load_app()
