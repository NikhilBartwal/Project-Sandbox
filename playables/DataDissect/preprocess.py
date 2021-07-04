import pandas as pd
import streamlit as st

from playables.DataDissect.utils import display_dataset_info, get_func_to_fill
from playables.DataDissect.utils import load_df, save_df, clear_cache, get_feature_info
from playables.DataDissect.preprocess_logic import update_custom_values, fix_missing_values_with
from playables.DataDissect.preprocess_logic import convert_datatype_with, get_feature_types

def fix_missing_values(df, missing_info, feature_type):
    container = st.beta_container()
    with container:
        missing_col, fix_options_col = st.beta_columns(2)

    num_features, cat_features, bool_features = feature_type.values()

    if missing_info.sum() != 0:
        with missing_col:
            st.write(f'There are a total of {missing_info.sum()} missing values in the dataset\
                    These are the columns that will be updated:')
            st.write(missing_info)
        with fix_options_col:
            fix_options = ['Do Nothing',
                            'Mean',
                            'Median',
                            'Drop',
                            'Custom'
                            ]
            fix_option = st.radio('How to fill the dataset NULL values?', fix_options)

        fix_missing_values_with(df, fix_option.lower(), num_features, cat_features, bool_features)
    else:
        st.write('There are no missing values in the dataset!')

def convert_datatype(df, feature_type):
    num_features, cat_features, bool_features = feature_type.values()
    all_features = num_features + cat_features + bool_features
    dtypes = df.dtypes
    st.write(dtypes)

    conversion_options = {
        'int': ['No Change', 'float', 'str'],
        'float': ['No Change', 'int', 'str'],
        'str': ['No Change', 'int', 'float'],
        'bool': ['No Change', 'int', 'str']
    }
    feature_selections = {}
    feature_types = get_feature_types(dtypes, all_features)

    with st.form('Datatype Conversion Form'):
        feature_container, type_container, convert_box = st.beta_columns(3)
        for feature_name in all_features:
            type = feature_types[feature_name]
            with feature_container:
                st.write(f'**{feature_name}**')
            with type_container:
                st.write(f'Current Datatype: *{type}*')
            with convert_box:
                type_select = st.selectbox('', conversion_options[type], key=feature_name)
                feature_selections[feature_name] = type_select
        st.write('This step is ir-reversible. Please check the selections and click Update')
        update = st.form_submit_button('Update Dataset')
        if update:
            convert_datatype_with(df, feature_selections, feature_types, all_features)
            save_df(new_df)

def handle_categorical(df):
    pass

def pre_process_data(df):
    df = load_df(curr_df=df)
    display_dataset_info(df, without_summary=True, subheader='Current Dataset:')
    options_available, option_description = st.beta_columns([1,2])
    clear_button = st.button('Clear Cache')
    missing_info, feature_type = get_feature_info(df)

    with options_available:
        options = ['', 'Fix Missing Values', 'Convert DataType', 'Handle Categorical Data']
        todo = st.radio('Options Available:', options)

    if clear_button:
        clear_cache()

    if todo == options[1]:
        with option_description:
            st.write("\n\n\n\n")
            st.write('Null/Missing values can be harmful to the modelling.\
                      Use Mean, Median or Mode to fill up the missing values!')
        fix_missing_values(df, missing_info, feature_type)
    elif todo == options[2]:
        with option_description:
            st.write("\n\n\n\n")
            st.write('Sometimes, we might have to convert the datatype of certain\
            variables to use them.')
        convert_datatype(df, feature_type)
    elif todo == options[3]:
        with option_description:
            st.write("\n\n\n\n")
            st.write('Convert categorical data into its numeric counterpart')
        handle_categorical(df)
