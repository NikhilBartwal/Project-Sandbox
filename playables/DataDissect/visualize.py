import io
import os
import pandas as pd
import seaborn as sns
import streamlit as st

from matplotlib import pyplot as plt
from playables.DataDissect.utils import load_df, save_df
from playables.DataDissect.utils import dataset_general_info

def visualize_data(df):
    df = load_df(curr_df=df)

    analysis_types = ['Dataset Correlation Heatmap', 'Visualize Dataset Features']
    analysis_type = st.sidebar.radio('Select option to perform:', analysis_types)

    if analysis_type == analysis_types[0]:
        display_correlation(df)
    elif analysis_type == analysis_types[1]:
        display_visualization(df)

def display_correlation(df):
    _, subheader, _ = st.columns([1,1,2])
    with subheader:
        st.subheader('Data Correlation Heatmap')

    heatmap_col, type_col = st.columns([3,2])

    with heatmap_col:
        fig, ax = plt.subplots()
        sns.heatmap(df.corr(), ax=ax)
        st.write(fig)

    with type_col:
        dataset_general_info(df)

def display_visualization(df):
    st.title('Feature Inter-relationships Visualization')
    hue = st.sidebar.selectbox('Select variable for hue:', [None] + list(df.columns))
    kind = st.sidebar.radio('Select kind of plot:', ['Scatter', 'KDE', 'Hist', 'Reg'])
    diag_kind = st.sidebar.radio('Select kind of plot for diagonal:', ['Auto', 'Hist', 'KDE', None])

    if diag_kind is not None:
        fig = sns.pairplot(df, size=2.5, hue=hue, kind=kind.lower(), diag_kind=diag_kind.lower())
    else:
        fig = sns.pairplot(df, size=2.5, hue=hue, kind=kind.lower())
    st.pyplot(fig)
