import io
import numpy as np
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

def display_dataset_info(df, without_summary=False):
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

def display_data_dissect_info():
    st.title('Welcome to Data Dissect!')
    st.subheader('Pre-process your dataset without any code and visualize any/all relationships you want to!')
