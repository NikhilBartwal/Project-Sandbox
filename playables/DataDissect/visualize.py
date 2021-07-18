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
    _, subheader, _ = st.beta_columns([1,1,2])
    with subheader:
        st.subheader('Data Correlation Heatmap')

    heatmap_col, type_col = st.beta_columns([3,2])

    with heatmap_col:
        fig, ax = plt.subplots()
        sns.heatmap(df.corr(), ax=ax)
        st.write(fig)

    with type_col:
        dataset_general_info(df)

    analysis_types = ['Dataset Correlation Heatmap', 'Univariate analysis', 'Bivariate analysis']
    analysis_type = st.sidebar.radio('Select type of visualization to perform:', analysis_types)

    if analysis_type == analysis_types[1]:
        univariate_analysis(df)
    elif analysis_type == analysis_types[2]:
        bivariate_analysis(df)

def univariate_analysis(df):
    pass

def bivariate_analysis(df):
    pass
