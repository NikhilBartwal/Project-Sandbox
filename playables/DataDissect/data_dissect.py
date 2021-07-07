import io
import os
import pandas as pd
import streamlit as st

from playables.DataDissect.utils import *
from playables.DataDissect.preprocess import pre_process_data
from playables.DataDissect.utils import load_df, save_df
from matplotlib import pyplot as plt

def visualize_data(df):
    pass

def load_data_dissect():
    welcome_container = st.beta_container()
    file = st.file_uploader('Upload a csv dataset here (Max Size Limit: 150MBs)', type=['csv'])
    #Start the analysis only when the user has uploaded a dataset
    if file:
        df = load_df(startup=True, initial_data=file)
        data_options = ['Display Original Dataset',
                        'Pre-process data',
                        'Visualizations']

        st.sidebar.subheader('Choose what to do with the dataset!')
        option = st.sidebar.selectbox('Please select one:', data_options, key='menu_select')

        if option == data_options[0]:
            display_dataset_info(df)
        elif option == data_options[1]:
            pre_process_data(df)
        elif option == data_options[2]:
            visualize_data(df)

        #A little hack to discard the menu option from the previous run
        if 'menu_select' in st.session_state:
            del st.session_state['menu_select']
    else:
        clear_cache(warning=False)
        with welcome_container:
            display_data_dissect_info()
