import io
import os
import pandas as pd
import streamlit as st

from playables.DataDissect.utils import *
from playables.DataDissect.preprocess import pre_process_data
from playables.DataDissect.visualize import visualize_data
from playables.DataDissect.utils import load_df, save_df
from matplotlib import pyplot as plt

def load_data_dissect():
    """
    Renders and displays the DataDissect Homepage along with all the available features.

    Current avilable options:
        a. Display Dataset Profile Report
        b. Pre-process dataset
        c. Visualize Dataset
    """
    welcome_container = st.container()
    file = st.file_uploader('Upload a csv dataset here (Max Size Limit: 100MBs)', type=['csv'])
    #Start the analysis only when the user has uploaded a dataset
    if file:
        df = load_df(startup=True, initial_data=file)
        data_options = ['Display Dataset Summary',
                        'Pre-process data',
                        'Visualize Dataset']

        #Create buttons and select box for the sidebar to get user choices
        st.sidebar.subheader('Choose what to do with the dataset!')
        option = st.sidebar.selectbox('Please select one:', data_options, key='menu_select')
        download_button = st.sidebar.button('Download Updated Dataset')

        if download_button:
            download_df(df)

        if option == data_options[0]:
            #Display profile report explicitly, defaults to only dataset sample
            display_dataset_info(df, profiling=True)
        elif option == data_options[1]:
            pre_process_data(df)
        elif option == data_options[2]:
            visualize_data(df)

        #A little hack to discard the menu option from the previous run
        if 'menu_select' in st.session_state:
            del st.session_state['menu_select']
    else:
        #When the user removes/replaces the current dataset, delete the cache and reload the page
        clear_cache(warning=False)
        with welcome_container:
            display_data_dissect_info()
