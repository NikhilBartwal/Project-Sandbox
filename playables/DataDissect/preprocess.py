import pandas as pd
import streamlit as st

from playables.DataDissect.utils import display_dataset_info

def pre_process_data(df):
    try:
        df = pd.read_csv('newdata.csv')
    except:
        pass
    display_dataset_info(df)
    options_available, options_selectbox = st.beta_columns(2)
    with options_available:
        st.subheader('Options Available:')
    with options_selectbox:
        options = ['Fix Missing Values', 'Convert DataType', 'Handle Categorical Data']
        todo = st.selectbox(' ', options)

    if todo == options[0]:
        df.head().to_csv('newdata.csv')
        st.write('done dona done done')
    elif todo == options[1]:
        st.write('convert datatype')
    elif todo == options[2]:
        st.write('handle categorical')
