import pandas as pd
import streamlit as st

from playables.DataDissect.utils import display_dataset_info

def fix_missing_values(df):
    container = st.beta_container()
    with container:
        missing_col, fix_options_col = st.beta_columns(2)

    with missing_col:
        missing_info = df.isnull().sum()
        st.write(f'There are a total of {missing_info.sum()} missing values in the dataset')
        st.write(missing_info)

    if df.shape[0] > 5:
        with fix_options_col:
            fix_options = ['Do Nothing', 'Mean', 'Median', 'Mode', 'Different method for each feature']
            fix_option = st.radio('How to fill the dataset NULL values?', fix_options)

        if fix_option == fix_options[1]:
            st.write('Use mean to fill up all the null values in the dataset?')
            confirm = st.button('update')
            if confirm:
                newdf = df.head()
                newdf.to_csv('newdata.csv')
                with container:
                    st.write('Dataset has been updated!')

def convert_datatype(df):
    pass

def handle_categorical(df):
    pass

def pre_process_data(df):
    try:
        df = pd.read_csv('newdata.csv')
    except:
        pass
    display_dataset_info(df, without_summary=True, subheader='Current Dataset:')
    options_available, option_description = st.beta_columns([1,2])
    with options_available:
        options = ['', 'Fix Missing Values', 'Convert DataType', 'Handle Categorical Data']
        todo = st.radio('Options Available:', options)

    if todo == options[1]:
        with option_description:
            st.write("\n\n\n\n")
            st.write('Null/Missing values can be harmful to the modelling.\
                      Use Mean, Median or Mode to fill up the missing values!')
        fix_missing_values(df)
    elif todo == options[2]:
        with option_description:
            st.write("\n\n\n\n")
            st.write('Sometimes, we might have to convert the datatype of certain\
            variables to use them.')
            convert_datatype(df)
    elif todo == options[3]:
        with option_description:
            st.write("\n\n\n\n")
            st.write('Convert categorical data into its numeric counterpart')
            handle_categorical(df)
