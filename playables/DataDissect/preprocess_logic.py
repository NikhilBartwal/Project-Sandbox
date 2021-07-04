import pandas as pd
import streamlit as st

from playables.DataDissect.utils import save_df, get_func_to_fill

def fix_missing_values_with(df, method, num_features=None, cat_features=None, bool_features=None):
    #This is the function that actually fills the NULL values with the specified method
    # and saves an updated dataset state
    new_df = df.copy()
    columns_to_fill = num_features + cat_features + bool_features

    if method == 'drop':
        st.write('This change is ir-reversible, so please confirm your choice!')
        confirm_update = st.button('Drop NULL rows')

        if confirm_update:
            new_df.dropna(inplace=True)

        save_df(new_df)
    elif method != 'custom':
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

def update_custom_values(
    new_df,
    columns_to_fill,
    feature_fill_methods,
    feature_static_values,
    feature_drop_values
):
    for column in columns_to_fill:
        #Fill all the mean/median/drop ones individually
        if column in feature_fill_methods.keys():
            func = get_func_to_fill(feature_fill_methods[column])
            new_df[column].fillna(func(new_df[column]), inplace=True, downcast='infer')
        elif column in feature_drop_values:
            #Drop the rows that have the specified column NULL
            new_df = new_df[new_df[column].notnull()]
    #Fill all the static values in one go
    new_df.fillna(feature_static_values, inplace=True, downcast='infer')
    return new_df

def get_func_convert(feature_type):
    feature_type = feature_type.lower()

    if feature_type == 'no change':
        return
    elif feature_type == 'int':
        return int
    elif feature_type == 'float':
        return float
    elif feature_type == 'str':
        return str

def get_feature_types(orig_dtypes, all_features):
    #Return dict of features and their simplified datatype
    orig_dtypes = dict(orig_dtypes)
    simple_dtypes = {}
    for feature_name in all_features:
        feature_dtype = orig_dtypes[feature_name].name
        if 'int' in feature_dtype:
            simple_dtype = 'int'
        elif 'float' in feature_dtype:
            simple_dtype = 'float'
        elif 'bool' in feature_dtype:
            simple_dtype = 'bool'
        elif 'object' in feature_dtype:
            simple_dtype = 'str'

        simple_dtypes[feature_name] = simple_dtype
    return simple_dtypes

def check_compatibility(col_values, change_from, change_to):
    if change_from != 'str':
        return True
    else:
        #Str can be converted to int/float only if all the str values are actually numerical
        for value in col_values:
            if not value.isnumeric():
                return False
        return True

def convert_datatype_with(df, feature_selections, feature_types, all_features):
    for feature_name in all_features:
        change_from = feature_types[feature_name]
        change_to = feature_selections[feature_name]

        if check_compatibility(df[feature_name].value_counts().index, change_from, change_to):
            #st.write(f'{change_from} -> {change_to} compatible')
            func = get_func_convert(change_to)
            if func is not None:
                #st.write(f'Convering {feature_name} to {change_to}')
                df[feature_name] = df[feature_name].astype(func)
                #st.write(df.dtypes)
                #st.write('change done')
    save_df(df)
