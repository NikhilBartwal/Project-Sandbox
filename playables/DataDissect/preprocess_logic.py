import pandas as pd
import streamlit as st

from playables.DataDissect.utils import save_df, get_func_to_fill

def fix_missing_values_with(df, method, num_features=None, cat_features=None, bool_features=None):
    #This is the function that actually fills the NULL values with the specified method
    # and saves an updated dataset state
    new_df = df.copy()
    columns_to_fill = num_features + cat_features + bool_features

    if method == 'do nothing':
        return
    elif method == 'drop':
        st.write('This change is ir-reversible, so please confirm your choice!')
        confirm_update = st.button('Drop NULL rows')

        if confirm_update:
            st.write('testing')
            new_df.dropna(inplace=True)
            save_df(new_df)
    elif method in ['mean', 'median']:
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
                        feature_choice = st.radio('', custom_options_num, key=feature_name+'_missing_choice')
                    elif feature_name in cat_features or bool_features:
                        feature_choice = st.radio('', custom_options_cat, key=feature_name+'_missing_choice')
                    #Takes the value for static input, defaults to mean if option selected but value not entered
                    value = st.text_input('Enter value (for static input):', key=feature_name+'_static_input')

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

def display_cat_preview(df, encoding_choices, feature_choice, feature_values, use_defaults):
    final_label_encoding = {}
    final_onehot_encoding = []

    with st.form('Categorical Encoding Preview'):
        for feature_name, feature_encoding in feature_choice.items():
            feature_col, encoding_col = st.beta_columns(2)
            feature_col.write(f'Feature Name: **{feature_name}**')

            if feature_encoding == encoding_choices[1]:
                default_status = 'Default' if use_defaults[feature_name]==True else 'Custom'
                encoding_col.write(f'Encoding Choice: ** *{feature_encoding} ({default_status})* **')

                if default_status == 'Default':
                    final_label_encoding[feature_name] = 'default'
                else:
                    final_label_encoding[feature_name] = get_custom_encodings(feature_values[feature_name].index)
            else:
                encoding_col.write(f'{feature_encoding}')
                if feature_encoding == encoding_choices[2]:
                    final_onehot_encoding.append(feature_name)
            st.write('-----')

        update = st.form_submit_button('Update Dataset')
    back = st.button('Back', key='myback')

    if update:
        apply_cat_encodings(df, final_label_encoding, final_onehot_encoding)
    if back:
        st.experimental_rerun()

def get_custom_encodings(feature_values):
    st.write('Please enter custom encoding values (in integer format):')
    custom_encoding_values = {}

    for value in feature_values:
        value_name_col, custom_value_col, _ = st.beta_columns(3)

        value_name_col.write(f'Original value: **{value}**')

        with custom_value_col:
            custom_value = st.text_input('Encoded value:', key=value+'custom_encoding')

        custom_encoding_values[value] = custom_value

    return custom_encoding_values

def apply_cat_encodings(df, final_label_encoding, final_onehot_encoding):
    st.write(final_label_encoding)
    st.write(final_onehot_encoding)

def get_cat_feature_values(df, feature_name):
    return df[feature_name].value_counts()

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

def compatibility_convert(str_column, change_from, change_to):
        #Str can be converted to int/float only if all the str values are actually numerical
        try:
            str_column = str_column.astype(float)
        except:
            st.write(f'{str_column} is not compatible to be converted from {change_from} to {change_to}')
            return str_column

        if change_to == 'int':
            str_column = str_column.astype(int)

        return str_column

def convert_datatype_with(df, feature_selections, feature_types, all_features):
    for feature_name in all_features:
        change_from = feature_types[feature_name]
        change_to = feature_selections[feature_name]

        if change_from != 'str':
            #st.write(f'{change_from} -> {change_to} compatible')
            func = get_func_convert(change_to)
            if func is not None:
                df[feature_name] = df[feature_name].astype(func)
        else:
            df[feature_name] = compatibility_convert(df[feature_name], change_from, change_to)

    save_df(df)
