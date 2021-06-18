import io
import os
import pandas as pd
import streamlit as st

from playables.DataDissect.utils import *
from playables.DataDissect.preprocess import pre_process_data
from matplotlib import pyplot as plt

def visualize_data():
    pass
    
def load_data_dissect():
    welcome_container = st.beta_container()
    file = st.file_uploader('Upload a csv dataset here (Max Size Limit: 150MBs)', type=['csv'])
    #Start the analysis only when the user has uploaded a dataset
    if file:
        df = pd.read_csv(file)
        data_options = ['Display Original Dataset',
                        'Pre-process data',
                        'Visualizations']

        st.sidebar.subheader('Choose what to do with the dataset!')
        option = st.sidebar.selectbox('Please select one:', data_options)

        if option == data_options[0]:
            display_dataset_info(df)
        elif option == data_options[1]:
            pre_process_data(df)
        elif option == data_options[2]:
            visualize_data(df)
    else:
        with welcome_container:
            display_data_dissect_info()
