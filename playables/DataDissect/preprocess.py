import pandas as pd
import streamlit as st

from playables.DataDissect.utils import display_dataset_info, get_func_to_fill

def fix_missing_values_with(df, method, columns_to_fill):
    #This is the function that actually fills the NULL values with the specified method
    # and saves an updated dataset state
    new_df = df.copy()
    columns_to_fill = columns_to_fill.index.to_list()

    if method != 'custom':
        # Usin the same template for mean, median over entire dataframe
        st.write(f'Use {method} to fill up all the null values in the dataset?')
        confirm_update = st.button('Update')
        func = get_func_to_fill(method)
        if confirm_update:
            for column in columns_to_fill:
                new_df[column].fillna(func(new_df[column]), inplace=True)
    else:
        #Display each column with missing data to be filled 
        st.write('Please select how to fill the columns with NULL values:')
        custom_options = ['Mean', 'Median', 'Static Value']
        column_methods = {}
        column_static_values = {}
        with st.form('trial'):
            column_containers = st.beta_columns(len(columns_to_fill))
            for container_ind, column in enumerate(column_containers):
                with column:
                    st.write(columns_to_fill[container_ind])
                    column_choice = st.radio('', custom_options, key=columns_to_fill[container_ind])
                    if column_choice in (custom_options[0], custom_options[1]):
                        column_methods[columns_to_fill[container_ind]] = column_choice
                    else:
                        if column_choice == custom_options[2]:
                            value = st.text_input('Enter value:', key=columns_to_fill[container_ind])
                        column_static_values[columns_to_fill[container_ind]] = value

            trial = st.form_submit_button('Try')
            if trial:
                st.write(column_methods)
                st.write(column_static_values)

    #st.experimental_rerun()

def fix_missing_values(df):
    container = st.beta_container()
    with container:
        missing_col, fix_options_col = st.beta_columns(2)

    with missing_col:
        missing_info = df.isnull().sum()
        st.write(f'There are a total of {missing_info.sum()} missing values in the dataset\
                These are the columns that will be updated:')
        st.write(missing_info)

    if missing_info.sum() != 0:
        with fix_options_col:
            fix_options = ['Do Nothing',
                            'Mean',
                            'Median',
                            'Different method for each feature'
                            ]
            fix_option = st.radio('How to fill the dataset NULL values?', fix_options)

        if fix_option == fix_options[1]:
            fix_missing_values_with(df, 'mean', missing_info)
        elif fix_option == fix_options[2]:
            fix_missing_values_with(df, 'median', missing_info)
        elif fix_option == fix_options[3]:
            fix_missing_values_with(df, 'custom', missing_info)

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
