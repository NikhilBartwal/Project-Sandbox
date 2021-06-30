import pandas as pd
import streamlit as st

from playables.DataDissect.utils import display_dataset_info, get_func_to_fill
from playables.DataDissect.utils import update_custom_values, load_df, save_df, clear_cache

def fix_missing_values_with(df, method, num_features=None, cat_features=None):
    #This is the function that actually fills the NULL values with the specified method
    # and saves an updated dataset state
    new_df = df.copy()
    columns_to_fill = num_features + cat_features

    if method == 'drop':
        st.write('This change is ir-reversible, so please confirm your choice!')
        confirm_update = st.button('Drop NULL rows')

        if confirm_update:
            new_df.dropna(inplace=True)

        save_df(new_df)

    if method != 'custom':
        # Usin the same template for mean, median over entire dataframe
        st.write(f'Use {method} to fill up all the null values in the dataset?')
        confirm_update = st.button('Update')
        func = get_func_to_fill(method)
        if confirm_update:
            #Use mean/median only for the numerical features
            for column in num_features:
                new_df[column].fillna(func(new_df[column]), inplace=True)
            save_df(new_df)
    else:
        #Display each column with options to be selected individually
        st.write('Please select how to fill the columns with NULL values:')
        custom_options_num = ['Mean', 'Median', 'Drop', 'Static Value']
        custom_options_cat = ['Mode', 'Drop', 'Static Value']
        #To hold the selected ioption whether mean or median
        feature_fill_methods = {}
        # To hold the static value in case user enters own value
        feature_fill_values = {}
        #To drop the rows with NULL values altogether
        feature_drop_values = []
        #Enclose all the columns and their options in a form, so they can be processed together
        with st.form('Feature Choice Selection'):
            #Dynamic number of containers to hold each column and its options
            feature_containers = st.beta_columns(len(columns_to_fill))
            for feature_ind, feature_name in enumerate(columns_to_fill):
                with feature_containers[feature_ind]:
                    #Display column name and options in each container
                    st.write(feature_name)
                    if feature_name in num_features:
                        feature_choice = st.radio('', custom_options_num, key=feature_name)
                    elif feature_name in cat_features or bool_features:
                        feature_choice = st.radio('', custom_options_cat, key=feature_name)
                    #Takes the value for static input, defaults to mean if option selected but value not entered
                    value = st.text_input('Enter value (for static input):', key=feature_name)

                    #In case static value is selected but no value is entered
                    if feature_choice == 'Static Value' and value == '':
                        if feature_name in num_features:
                            feature_choice = custom_options_num[0] #Use mean
                        elif feature_name in cat_features or bool_features:
                            feature_choice = custom_options_cat[0] #Use mode

                    #Hold the selected/entered choice in the respective dict
                    if feature_choice in ['Mean', 'Median', 'Mode']:
                        feature_fill_methods[feature_name] = feature_choice
                    elif feature_choice == 'Drop':
                        feature_drop_values.append(feature_name)
                    else:
                        feature_fill_values[feature_name] = value

            st.write('If the **Static Value** option is selected, but no value is entered, \
                it will be filled with mean for numerical features and mode for categorical features by default')
            st.write('Please check the selected options a last time (This step is non-reversible)')

            update = st.form_submit_button('Update Dataset')
            if update:
                new_df = update_custom_values(
                    new_df,
                    columns_to_fill,
                    feature_fill_methods,
                    feature_fill_values,
                    feature_drop_values
                    )
                save_df(new_df)


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

        fix_missing_values_with(df, fix_option.lower(), num_features, cat_features)
    else:
        st.write('There are no missing values in the dataset!')

def convert_datatype(df, feature_type):
    num_features, cat_features, bool_features = feature_type.values()
    all_features = num_features + cat_features + bool_features

    with st.form('Datatype Conversion Form'):


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
