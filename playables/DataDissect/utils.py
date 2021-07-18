import io
import numpy as np
import os
import pandas as pd
import streamlit as st

import pandas_profiling
from streamlit_pandas_profiling import st_profile_report

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

def dataset_general_info(df):
    st.subheader('Dataset General Info:')

    buf = io.StringIO()
    df.info(buf=buf)
    info_df, headers, footers = parse_pandas_info(buf.getvalue())

    for info in headers:
        st.write("**_" + info + "_**")
    st.write(info_df)
    for info in footers:
        st.write("**_" + info + "_**")

@st.cache
def get_dataset_profile_report(df):
    return df.profile_report()

def display_dataset_info(df, without_summary=False, subheader=None):
    if subheader:
        st.subheader(subheader)
    else:
        st.subheader('Uploaded Dataset Sample:')
    st.write(df.head())
    #Since the df.info() prints directly to the console, so we are using an
    # IO buffer to store the output as a string which can further be converted into a Pandas DataFrame

    profile = get_dataset_profile_report(df)
    st_profile_report(profile)

def load_df(startup=False, initial_data=None, curr_df=None):
    if startup:
        try:
            #Try reading the OG dataset from the uploaded file
            df = pd.read_csv(initial_data)
            #If successful, store the dataset for later
            df.to_csv('original.csv', index=False)
        except:
            try:
                #If the uploaded file is no longer present, use the cached dataset
                df = pd.read_csv('original.csv')
            except:
                #Warning generated in case of any server issue
                st.write('Dataset not found!')
        return df

    else:
        try:
            #Try to load the latest version of the dataset is tt exists
            curr_df = pd.read_pickle('new_df.pkl')
            #st.warning('Currently running on cache! Please use the `Clear Cache` button to use the original dataset')
        except:
            pass
    return curr_df

def save_df(df):
    df.to_pickle('new_df.pkl')
    st.experimental_rerun()

def clear_cache(warning=True):
    try:
        os.remove('new_df.pkl')
        st.experimental_rerun()
    except:
        if warning:
            st.warning('No current cache found!')
        else:
            pass

def calc_column_mode(df_col):
    #Return the value with the highest count amongst all
    return df_col.value_counts().index[0]

def get_func_to_fill(method):
    method = method.lower()
    if method in 'mean':
        return np.mean
    elif method == 'median':
        return np.nanmedian
    elif method == 'mode':
        return calc_column_mode

def get_feature_info(df):
    missing_info = df.isnull().sum()
    num_features = list(df.select_dtypes(include='number').columns.values)
    cat_features = list(df.select_dtypes(include='object').columns.values)
    bool_features = list(df.select_dtypes(include='bool').columns.values)

    feature_type = {'num': num_features, 'cat': cat_features, 'bool': bool_features}
    return missing_info, feature_type

def display_data_dissect_info():
    st.title('Welcome to Data Dissect!')
    st.subheader('Summarize, Understand, Pre-process and Visualize your dataset the way you want, without writing a single line of code!')
