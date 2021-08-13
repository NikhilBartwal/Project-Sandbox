import io
import numpy as np
import os
import pandas as pd
import streamlit as st

import pandas_profiling
from streamlit_pandas_profiling import st_profile_report

def parse_pandas_info(info):
    "Convert raw pandas info strings to organized DataFrame"
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
    "Convert the raw dataset info in an organized Pandas Df format"
    st.subheader('Dataset Features Info:')

    buf = io.StringIO()
    df.info(buf=buf)
    info_df, headers, footers = parse_pandas_info(buf.getvalue())

    st.write(info_df)
    for info in footers:
        st.write("**_" + info + "_**")


def display_dataset_info(df, without_summary=False, profiling=False, subheader=None):
    """
    Displays the dataset info on the Landing Page after user uploads a datset

    Args:
    df (Pandas DataFrame)    : The uploaded dataset by the user
    without_summary (Boolean): Flag whether to display summary or not
    profiling (Boolean)      : Flag whether we need to generate the pandas profiling report
    subheader (Boolean)      : Flag whether to display subheaders with summary or not

    Returns:
    Displays the dataset sample as well as either the summary or the profiling
    report depending upon the arguments passed
    """
    if subheader:
        st.subheader(subheader)
    else:
        st.subheader('Uploaded Dataset Sample:')
    st.write(df.head())
    #Since the df.info() prints directly to the console, so we are using an
    # IO buffer to store the output as a string which can further be converted into a Pandas DataFrame
    if profiling:
        profile = df.profile_report()
        st_profile_report(profile)

def load_df(startup=False, initial_data=None, curr_df=None):
    """
    Loads the original/updated dataset on each streamlit run

    Args:
    startup (Boolean)          : Flag whether this is the first streamlit run
    initial_data (Bytes Data)  : Initial uploaded dataset, to be used with startup=True
    curr_df (Pandas DataFrame) : The current working df for successive runs

    Returns:
    (Pandas DataFrame)         : The new/updated df per the current streamlit run
    """
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

def download_link(object_to_download, download_filename, download_link_text):
    """
    Generates a link to download the given object_to_download.

    object_to_download (str, pd.DataFrame):  The object to be downloaded.
    download_filename (str): filename and extension of file. e.g. mydata.csv, some_txt_output.txt
    download_link_text (str): Text to display for download link.

    Examples:
    download_link(YOUR_DF, 'YOUR_DF.csv', 'Click here to download data!')
    download_link(YOUR_STRING, 'YOUR_STRING.txt', 'Click here to download your text!')

    """
    if isinstance(object_to_download,pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)

    # some strings <-> bytes conversions necessary here
    b64 = base64.b64encode(object_to_download.encode()).decode()

    return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'

def download_df(df):
    tmp_download_link = download_link(df, 'YOUR_INPUT.txt', 'Click here to download your text!')
    st.markdown(tmp_download_link, unsafe_allow_html=True)

def clear_cache(warning=True):
    """Clear the cache when the dataset is removed/replaced"""
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
    """Function to get the chosen numpy method from its name"""
    method = method.lower()
    if method in 'mean':
        return np.mean
    elif method == 'median':
        return np.nanmedian
    elif method == 'mode':
        return calc_column_mode

def get_feature_info(df):
    """
    Returns the missing info dataframe as well as the data type for all features

    Args:
    df (Pandas DataFrame): The current DataFrame

    Returns:
    missing_info (Pandas DataFrame): Info of each feature and the no. of NULL values in it
    feature_type (dict)            : Dictionary of numerical, categorical and boolean features
    """
    missing_info = df.isnull().sum()
    num_features = list(df.select_dtypes(include='number').columns.values)
    cat_features = list(df.select_dtypes(include='object').columns.values)
    bool_features = list(df.select_dtypes(include='bool').columns.values)

    feature_type = {'num': num_features, 'cat': cat_features, 'bool': bool_features}
    return missing_info, feature_type

def display_data_dissect_info():
    """Renders the DataDissect Landing page and its components"""
    _, title_col, _ = st.columns([1,2,1])
    with title_col:
        st.title('Welcome to Data Dissect!')

    st.subheader('Summarize, Understand, Pre-process and Visualize your dataset, without writing a single line of code!')

    _, image_col, _ = st.columns([1,4.5,1])
    with image_col:
        st.image('logos/datadissect.png', use_column_width='auto')
