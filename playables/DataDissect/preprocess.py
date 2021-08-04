import pandas as pd
import streamlit as st

from playables.DataDissect.utils import display_dataset_info, get_func_to_fill
from playables.DataDissect.utils import load_df, save_df, clear_cache, get_feature_info
from playables.DataDissect.preprocess_logic import update_custom_values, fix_missing_values_with, display_cat_preview
from playables.DataDissect.preprocess_logic import convert_datatype_with, get_feature_types, get_cat_feature_values

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

def convert_datatype(df, missing_info, feature_type):

    if missing_info.sum() != 0:
        st.write('The dataset seems to contain missing/Null values. Please fill the missing values before proceeding further :)')
        return

    num_features, cat_features, bool_features = feature_type.values()
    all_features = num_features + cat_features + bool_features
    dtypes = df.dtypes
    st.write(pd.DataFrame(df.dtypes, columns=['DataType']))

    conversion_options = {
        'int': ['No Change', 'float', 'str'],
        'float': ['No Change', 'int', 'str'],
        'str': ['No Change', 'int', 'float'],
        'bool': ['No Change', 'int', 'str']
    }
    feature_selections = {}
    feature_types = get_feature_types(dtypes, all_features)

    with st.form('Datatype Conversion Form'):
        for feature_name in all_features:
            feature_container, type_container, convert_box = st.beta_columns(3)
            type = feature_types[feature_name]
            with feature_container:
                st.write(f'Feature Name: **{feature_name}**')
                st.write('\n')
                st.write('\n')
            with type_container:
                st.write(f'Current Datatype: ** *{type}* **')
                st.write('\n')
                st.write('\n')
            with convert_box:
                type_select = st.selectbox('Select new datatype:', conversion_options[type], key=feature_name)
                feature_selections[feature_name] = type_select
        st.write('This step is ir-reversible. Please check the selections and click Update')
        update = st.form_submit_button('Update Dataset')
        if update:
            convert_datatype_with(df, feature_selections, feature_types, all_features)

def handle_categorical(df, feature_type):
    _, cat_features, _ = feature_type.values()

    if len(cat_features) == 0:
        st.write('All categorical data seems to have been handled well ;)')
        return

    #Convert the categorical features to one-hot/label encoded form as selected by user
    st.write('Please select the desired option for the categorical features present in the dataset.')
    st.write('You can uncheck the **USE DEFAULTS** checkbox to enter custom labels for label encoding on the next page')

    encoding_choices = ['No Change', 'Label Encoding', 'One-Hot Encoding']
    feature_choice = {}
    feature_values = {}
    use_defaults = {}

    placeholder = st.empty()
    first_screen = False

    if 'preview_status' not in st.session_state:
        first_screen = True
    else:
        if st.session_state['preview_status'] == False:
            first_screen = True

    if first_screen:
        with placeholder.form('Handling Categorical'):
            for feature_name in cat_features:
                feature_choice_col, feature_values_col = st.beta_columns(2)

                with feature_choice_col:
                    st.write(f'Feature Name: **{feature_name}**')
                    feature_choice[feature_name] = st.radio('Select your choice', encoding_choices, key=feature_name)
                    use_defaults[feature_name] = st.checkbox(
                        'Use default values for encoding \n \
                        (Uncheck this to provide custom encodings on the next page)',
                        key=feature_name+'default_encoding')

                with feature_values_col:
                    st.write('Value distribution of feature:')
                    feature_values[feature_name] = get_cat_feature_values(df, feature_name)
                    st.write(feature_values[feature_name])

            st.warning('On clicking the Preview button, you might receive a \'Bad Message\' warning.\
                It is a bug in the current release of Streamlit and will be fixed in the future update.\
                Simply click Done and continue with your work :)')

            preview_button = st.form_submit_button('Preview')
    else:
        preview_button = True

    if preview_button:
        st.session_state['preview_status'] = True
        placeholder.empty()
        display_cat_preview(df, encoding_choices, feature_choice, feature_values, use_defaults)

def pre_process_data(df):
    df = load_df(curr_df=df)
    display_dataset_info(df, without_summary=True, profiling=False, subheader='Current Dataset:')
    options_available, option_description = st.beta_columns([1,2])
    missing_info, feature_type = get_feature_info(df)

    with options_available:
        options = ['', 'Fix Missing Values', 'Convert DataType', 'Handle Categorical Data']
        todo = st.radio('Options Available:', options)

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
        convert_datatype(df, missing_info, feature_type)
    elif todo == options[3]:
        with option_description:
            st.write("\n\n\n\n")
            st.write('Convert categorical data into its numeric counterpart')
        handle_categorical(df, feature_type)
