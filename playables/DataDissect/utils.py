import io
import numpy as np
import os
import pandas as pd
import streamlit as st

def parse_pandas_info(info):
    splits = info.split('\n')
    #Since the first and end parts consist of extra info about the dataset,
    # we store them separately and process the remaining data into a Pandas DataFrame
    basic_info = splits[1:3]
    end_info = splits[-3:-1]
    col = []
    count = []
    dtype = []
    for row in splits[5:-3]:
        values = row.split()
        col.append(" ".join(values[1:-3]))
        count.append(" ".join(values[-3:-1]))
        dtype.append(values[-1])
    info_df = pd.DataFrame({'Columns': col, 'Non-Null Count': count, 'Dtype': dtype})
    return info_df, basic_info, end_info

def display_dataset_info(df, without_summary=False, subheader=None):
    if subheader:
        st.subheader(subheader)
    else:
        st.subheader('Uploaded Dataset Sample:')
    st.write(df.head())
    #Since the df.info() prints directly to the console, so we are using an
    # IO buffer to store the output as a string which can further be converted into a Pandas DataFrame
    if without_summary:
        return
    else:
        st.subheader('Dataset General Info:')

        buf = io.StringIO()
        df.info(buf=buf)
        info_df, headers, footers = parse_pandas_info(buf.getvalue())

        for info in headers:
            st.write("**_" + info + "_**")
        st.write(info_df)
        for info in footers:
            st.write("**_" + info + "_**")

def load_df(startup=False, initial_data=None, curr_df=None):
    if startup:
        df = pd.read_csv(initial_data)
        return df
    else:
        try:
            curr_df = pd.read_csv('new_df.csv')
            st.warning('Currently running on cache! Please use the `Clear Cache` button to use the original dataset')
        except:
            pass
    return curr_df

def save_df(df):
    df.to_csv('new_df.csv', index=False)

def clear_cache():
    try:
        os.remove('new_df.csv')
        st.experimental_rerun()
    except:
        st.warning('No current cache found!')

def get_func_to_fill(method):
    method = method.lower()
    if method in 'mean':
        return np.mean
    elif method == 'median':
        return np.nanmedian

def update_custom_values(new_df, columns_to_fill, feature_fill_methods, feature_static_values):
    df_dtypes = dict(new_df.dtypes)
    for column in columns_to_fill:
        #Fill all the mean/median ones individually
        if column in feature_fill_methods.keys():
            func = get_func_to_fill(feature_fill_methods[column])
            st.write('Filling', column, 'with', func(new_df[column]))
            new_df[column].fillna(func(new_df[column]), inplace=True, downcast='infer')
    #Fill all the static values in one go
    new_df.fillna(feature_static_values, inplace=True, downcast='infer')
    return new_df

def display_data_dissect_info():
    st.title('Welcome to Data Dissect!')
    st.subheader('Pre-process your dataset without any code and visualize any/all relationships you want to!')
